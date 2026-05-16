import pytest


def create_process(client):
    res = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    return res.json()["id"]


def test_create_etapa_success(client):
    pid = create_process(client)
    response = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    assert response.status_code == 201
    assert response.json()["nome"] == "Etapa 1"
    assert response.json()["processo_id"] == pid


def test_create_etapa_without_nome_returns_422(client):
    pid = create_process(client)
    response = client.post(f"/api/processos/{pid}/etapas", json={"descricao": "Etapa desc"})
    assert response.status_code == 422


def test_create_etapa_for_invalid_processo_returns_404(client):
    response = client.post("/api/processos/999/etapas", json={"nome": "Etapa 1"})
    assert response.status_code == 404


def test_list_etapas_by_processo(client):
    pid = create_process(client)
    client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 2"})

    response = client.get(f"/api/processos/{pid}/etapas")
    assert response.status_code == 200
    assert len(response.json()) == 2


def test_update_etapa(client):
    pid = create_process(client)
    res = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    eid = res.json()["id"]

    response = client.put(f"/api/etapas/{eid}", json={"nome": "Etapa 1 updated"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Etapa 1 updated"


def test_delete_etapa(client):
    pid = create_process(client)
    res = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    eid = res.json()["id"]

    response = client.delete(f"/api/etapas/{eid}")
    assert response.status_code == 204

    res_list = client.get(f"/api/processos/{pid}/etapas")
    assert len(res_list.json()) == 0


def test_delete_etapa_removes_related_conexoes(client):
    pid = create_process(client)
    res1 = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    eid1 = res1.json()["id"]
    res2 = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 2"})
    eid2 = res2.json()["id"]

    client.put(f"/api/processos/{pid}/fluxo", json={
        "etapas": [{"id": eid1}, {"id": eid2}],
        "conexoes": [{"etapa_origem_id": eid1, "etapa_destino_id": eid2, "tipo_conexao": "sequencial"}]
    })

    client.delete(f"/api/etapas/{eid1}")

    res_fluxo = client.get(f"/api/processos/{pid}/fluxo")
    assert res_fluxo.status_code == 200
    data = res_fluxo.json()
    assert len(data["conexoes"]) == 0
