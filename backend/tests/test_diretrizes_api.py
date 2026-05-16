import pytest

from app.models.processo import Processo
from app.models.diretriz import DiretrizAutomacao


def test_list_diretrizes_by_processo(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    diretriz = DiretrizAutomacao(processo_id=processo.id, titulo="Diretriz 1", status="Sugerida")
    db_session.add(diretriz)
    db_session.commit()

    response = client.get(f"/api/processos/{processo.id}/diretrizes")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_diretriz_status_success(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    diretriz = DiretrizAutomacao(processo_id=processo.id, titulo="Diretriz 1", status="Sugerida")
    db_session.add(diretriz)
    db_session.commit()
    db_session.refresh(diretriz)

    response = client.put(f"/api/diretrizes/{diretriz.id}", json={"status": "Priorizada"})
    assert response.status_code == 200
    assert response.json()["status"] == "Priorizada"


def test_update_diretriz_invalid_status_returns_error(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    diretriz = DiretrizAutomacao(processo_id=processo.id, titulo="Diretriz 1", status="Sugerida")
    db_session.add(diretriz)
    db_session.commit()
    db_session.refresh(diretriz)

    response = client.put(f"/api/diretrizes/{diretriz.id}", json={"status": "Inexistente"})
    assert response.status_code == 422


def test_update_diretriz_not_found_returns_404(client):
    response = client.put("/api/diretrizes/999", json={"status": "Priorizada"})
    assert response.status_code == 404
