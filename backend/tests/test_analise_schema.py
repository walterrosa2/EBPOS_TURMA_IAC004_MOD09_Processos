import pytest
from pydantic import ValidationError
from app.schemas.analise_schema import AnaliseIAResultadoSchema

def test_valid_analise_resultado_schema():
    data = {
        "resumo_executivo": "Teste",
        "diagnostico_operacional": "Teste",
        "nivel_maturidade": {"nivel": "Padronizado", "justificativa": "Teste"},
        "pontos_fortes": [],
        "gargalos": [],
        "riscos": [],
        "sugestoes_melhoria": [],
        "sugestoes_automacao": [],
        "oportunidades_ia": [],
        "lacunas_mapeamento": [],
        "indicadores_recomendados": [],
        "diretrizes_automacao": [],
        "perguntas_para_aprofundamento": [],
        "alertas": []
    }
    schema = AnaliseIAResultadoSchema(**data)
    assert schema.resumo_executivo == "Teste"

def test_invalid_prioridade_fails():
    data = {
        "resumo_executivo": "Teste",
        "diagnostico_operacional": "Teste",
        "nivel_maturidade": {"nivel": "Padronizado", "justificativa": "Teste"},
        "pontos_fortes": [],
        "gargalos": [],
        "riscos": [],
        "sugestoes_melhoria": [],
        "sugestoes_automacao": [
            {
                "titulo": "teste",
                "descricao": "teste",
                "tipo": "ia",
                "impacto": "Alto",
                "esforco": "Alto",
                "prioridade": "Urgente", # Invalid
                "etapa_relacionada": None,
                "pre_requisitos": [],
                "beneficio_esperado": "teste",
                "risco_implementacao": "teste"
            }
        ],
        "oportunidades_ia": [],
        "lacunas_mapeamento": [],
        "indicadores_recomendados": [],
        "diretrizes_automacao": [],
        "perguntas_para_aprofundamento": [],
        "alertas": []
    }
    with pytest.raises(ValidationError):
        AnaliseIAResultadoSchema(**data)

def test_missing_required_field_fails():
    data = {
        "resumo_executivo": "Teste",
        # missing diagnostico_operacional
    }
    with pytest.raises(ValidationError):
        AnaliseIAResultadoSchema(**data)

def test_empty_lists_are_valid():
    data = {
        "resumo_executivo": "Teste",
        "diagnostico_operacional": "Teste",
        "nivel_maturidade": {"nivel": "Padronizado", "justificativa": "Teste"},
        "pontos_fortes": [],
        "gargalos": [],
        "riscos": [],
        "sugestoes_melhoria": [],
        "sugestoes_automacao": [],
        "oportunidades_ia": [],
        "lacunas_mapeamento": [],
        "indicadores_recomendados": [],
        "diretrizes_automacao": [],
        "perguntas_para_aprofundamento": [],
        "alertas": []
    }
    schema = AnaliseIAResultadoSchema(**data)
    assert len(schema.pontos_fortes) == 0
