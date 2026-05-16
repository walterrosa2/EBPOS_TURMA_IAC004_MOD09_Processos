import pytest


def create_process_with_etapas(client):
    res = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    pid = res.json()["id"]
    res1 = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 1"})
    res2 = client.post(f"/api/processos/{pid}/etapas", json={"nome": "Etapa 2"})
    return pid, res1.json()["id"], res2.json()["id"]


def test_get_fluxo_success(client):
    pid, e1, e2 = create_process_with_etapas(client)
    response = client.get(f"/api/processos/{pid}/fluxo")
    assert response.status_code == 200
    data = response.json()
    assert len(data["etapas"]) == 2
    assert len(data["conexoes"]) == 0


def test_get_fluxo_invalid_processo_returns_404(client):
    response = client.get("/api/processos/999/fluxo")
    assert response.status_code == 404


def test_save_fluxo_positions_success(client):
    pid, e1, e2 = create_process_with_etapas(client)
    payload = {
        "etapas": [{"id": e1, "posicao_x": 100, "posicao_y": 200}],
        "conexoes": []
    }
    res = client.put(f"/api/processos/{pid}/fluxo", json=payload)
    assert res.status_code == 200

    res_get = client.get(f"/api/processos/{pid}/fluxo")
    etapa1 = next(e for e in res_get.json()["etapas"] if e["id"] == e1)
    assert etapa1["posicao_x"] == 100
    assert etapa1["posicao_y"] == 200


def test_save_fluxo_connection_success(client):
    pid, e1, e2 = create_process_with_etapas(client)
    payload = {
        "etapas": [],
        "conexoes": [{"etapa_origem_id": e1, "etapa_destino_id": e2, "tipo_conexao": "sequencial"}]
    }
    res = client.put(f"/api/processos/{pid}/fluxo", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert len(data["conexoes"]) == 1
    assert data["conexoes"][0]["etapa_origem_id"] == e1


def test_save_fluxo_with_etapa_from_other_processo_returns_400(client):
    pid, e1, e2 = create_process_with_etapas(client)

    res_other = client.post("/api/processos", json={"nome": "Proc B", "area": "RH"})
    pid_other = res_other.json()["id"]
    res3 = client.post(f"/api/processos/{pid_other}/etapas", json={"nome": "Etapa 3"})
    e3 = res3.json()["id"]

    payload = {
        "etapas": [],
        "conexoes": [{"etapa_origem_id": e1, "etapa_destino_id": e3, "tipo_conexao": "sequencial"}]
    }
    res = client.put(f"/api/processos/{pid}/fluxo", json=payload)
    assert res.status_code == 400


def test_save_fluxo_then_get_returns_persisted_data(client):
    pid, e1, e2 = create_process_with_etapas(client)
    payload = {
        "etapas": [{"id": e1, "posicao_x": 100, "posicao_y": 200}],
        "conexoes": [{"etapa_origem_id": e1, "etapa_destino_id": e2, "tipo_conexao": "sequencial"}]
    }
    client.put(f"/api/processos/{pid}/fluxo", json=payload)

    response = client.get(f"/api/processos/{pid}/fluxo")
    data = response.json()
    assert len(data["conexoes"]) == 1
    etapa1 = next(e for e in data["etapas"] if e["id"] == e1)
    assert etapa1["posicao_x"] == 100
