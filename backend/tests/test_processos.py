import pytest


def test_create_processo_success(client):
    response = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    assert response.status_code == 201
    assert response.json()["nome"] == "Proc A"


def test_create_processo_without_nome_returns_422(client):
    response = client.post("/api/processos", json={"area": "Fiscal"})
    assert response.status_code == 422


def test_create_processo_without_area_returns_422(client):
    response = client.post("/api/processos", json={"nome": "Proc A"})
    assert response.status_code == 422


def test_list_processos(client):
    client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    client.post("/api/processos", json={"nome": "Proc B", "area": "RH"})
    response = client.get("/api/processos")
    assert response.status_code == 200
    assert len(response.json()) >= 2


def test_get_processo_by_id(client):
    res = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    pid = res.json()["id"]
    response = client.get(f"/api/processos/{pid}")
    assert response.status_code == 200
    assert response.json()["id"] == pid


def test_get_processo_not_found_returns_404(client):
    response = client.get("/api/processos/999")
    assert response.status_code == 404


def test_update_processo(client):
    res = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    pid = res.json()["id"]
    response = client.put(f"/api/processos/{pid}", json={"nome": "Proc A updated", "area": "Fiscal"})
    assert response.status_code == 200
    assert response.json()["nome"] == "Proc A updated"


def test_delete_processo(client):
    res = client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    pid = res.json()["id"]
    response = client.delete(f"/api/processos/{pid}")
    assert response.status_code == 204

    res_get = client.get(f"/api/processos/{pid}")
    assert res_get.status_code == 404


def test_filter_processos_by_area(client):
    client.post("/api/processos", json={"nome": "Proc A", "area": "Fiscal"})
    client.post("/api/processos", json={"nome": "Proc B", "area": "RH"})
    response = client.get("/api/processos?area=Fiscal")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    for d in data:
        assert d["area"] == "Fiscal"
