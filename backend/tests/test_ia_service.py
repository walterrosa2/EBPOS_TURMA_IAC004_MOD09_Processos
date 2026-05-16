import pytest
import json
from unittest.mock import patch, MagicMock
from fastapi import HTTPException
from app.services import ia_service
from app.core.config import settings

def test_missing_openai_key_returns_controlled_error():
    with patch("app.services.ia_service.settings") as mock_settings:
        mock_settings.openai_api_key = None
        with pytest.raises(HTTPException) as exc:
            ia_service.generate_process_analysis({})
        assert exc.value.status_code == 500
        assert "OPENAI_API_KEY" in exc.value.detail

@patch("app.services.ia_service.OpenAI")
def test_valid_json_response_is_parsed_and_validated(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    valid_json = json.dumps({
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
    })
    mock_response.choices[0].message.content = valid_json
    mock_client.chat.completions.create.return_value = mock_response

    result = ia_service.generate_process_analysis({})
    assert result.resumo_executivo == "Teste"

@patch("app.services.ia_service.OpenAI")
def test_invalid_json_response_raises_controlled_error(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    mock_response.choices[0].message.content = "not json"
    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(HTTPException) as exc:
        ia_service.generate_process_analysis({})
    assert exc.value.status_code == 502

@patch("app.services.ia_service.OpenAI")
def test_schema_invalid_response_raises_controlled_error(mock_openai):
    mock_client = MagicMock()
    mock_openai.return_value = mock_client
    
    mock_response = MagicMock()
    invalid_schema_json = json.dumps({
        "resumo_executivo": "Teste"
        # Missing other fields
    })
    mock_response.choices[0].message.content = invalid_schema_json
    mock_client.chat.completions.create.return_value = mock_response

    with pytest.raises(HTTPException) as exc:
        ia_service.generate_process_analysis({})
    assert exc.value.status_code == 502
