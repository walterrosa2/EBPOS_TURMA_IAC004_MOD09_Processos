import os
import json
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from app.core.config import settings
from app.schemas.analise_schema import AnaliseIAResultadoSchema
from pydantic import ValidationError

def load_prompt(filename: str) -> str:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    prompts_dir = os.path.join(current_dir, "..", "prompts")
    filepath = os.path.join(prompts_dir, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        return f.read()

def generate_process_analysis(processo_payload: dict) -> AnaliseIAResultadoSchema:
    if not settings.openai_api_key:
        raise HTTPException(status_code=500, detail="Serviço de IA não configurado. Verifique OPENAI_API_KEY.")

    system_prompt = load_prompt("system_process_mapper.md")
    user_prompt_template = load_prompt("user_process_analysis_template.md")

    processo_json_str = json.dumps(processo_payload, ensure_ascii=False, indent=2)
    user_prompt = user_prompt_template.replace("{{PROCESSO_JSON}}", processo_json_str)

    client = OpenAI(
        api_key=settings.openai_api_key,
        timeout=settings.openai_timeout_seconds
    )

    try:
        response = client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            response_format={"type": "json_object"}
        )

        content = response.choices[0].message.content
        if not content:
            raise HTTPException(status_code=502, detail="A IA retornou uma resposta em formato inválido. Nenhuma análise foi salva.")
            
        parsed_data = json.loads(content)
        validated_schema = AnaliseIAResultadoSchema.model_validate(parsed_data)
        return validated_schema

    except (json.JSONDecodeError, ValidationError) as e:
        print(f"Erro de Validação da IA: {e}")
        raise HTTPException(status_code=502, detail="A IA retornou uma resposta em formato inválido. Nenhuma análise foi salva.")
    except OpenAIError as e:
        print(f"Erro na API da OpenAI: {e}")
        raise HTTPException(status_code=502, detail="Erro ao se comunicar com a inteligência artificial.")
