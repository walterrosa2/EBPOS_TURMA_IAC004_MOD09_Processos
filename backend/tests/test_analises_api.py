import pytest
from unittest.mock import patch

from app.models.processo import Processo
from app.models.etapa import Etapa
from app.models.analise import AnaliseIA
from app.schemas.analise_schema import AnaliseIAResultadoSchema


def test_create_analise_success_with_mocked_ia(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    etapa = Etapa(processo_id=processo.id, nome="Etapa 1")
    db_session.add(etapa)
    db_session.commit()

    mock_resultado = AnaliseIAResultadoSchema(
        resumo_executivo="Resumo",
        diagnostico_operacional="Diagnostico",
        nivel_maturidade={"nivel": "Padronizado", "justificativa": "ok"},
        pontos_fortes=[], gargalos=[], riscos=[], sugestoes_melhoria=[], sugestoes_automacao=[],
        oportunidades_ia=[], lacunas_mapeamento=[], indicadores_recomendados=[], diretrizes_automacao=[],
        perguntas_para_aprofundamento=[], alertas=[]
    )

    with patch("app.services.analise_service.generate_process_analysis", return_value=mock_resultado):
        response = client.post(f"/api/processos/{processo.id}/analises")
        assert response.status_code == 200
        assert response.json()["resumo_executivo"] == "Resumo"


def test_create_analise_without_etapas_returns_400(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    response = client.post(f"/api/processos/{processo.id}/analises")
    assert response.status_code == 400


def test_create_analise_invalid_processo_returns_404(client):
    response = client.post("/api/processos/999/analises")
    assert response.status_code == 404


def test_list_analises_by_processo(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    analise = AnaliseIA(processo_id=processo.id, json_resultado="{}")
    db_session.add(analise)
    db_session.commit()

    response = client.get(f"/api/processos/{processo.id}/analises")
    assert response.status_code == 200
    assert len(response.json()) == 1


def test_get_analise_by_id(client, db_session):
    processo = Processo(nome="Processo 1", area="Area")
    db_session.add(processo)
    db_session.commit()
    db_session.refresh(processo)

    analise = AnaliseIA(processo_id=processo.id, json_resultado="{}")
    db_session.add(analise)
    db_session.commit()
    db_session.refresh(analise)

    response = client.get(f"/api/analises/{analise.id}")
    assert response.status_code == 200
    assert response.json()["id"] == analise.id
