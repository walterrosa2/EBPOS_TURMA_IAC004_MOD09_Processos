import os
import json
from loguru import logger
from fastapi import HTTPException
from openai import OpenAI, OpenAIError
from app.core.config import settings
from app.schemas.importacao_processo_schema import ProcessImportAIResultSchema
from pydantic import ValidationError
from datetime import datetime

class ProcessImportIAService:
    @staticmethod
    def _load_prompt(filename: str) -> str:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        prompts_dir = os.path.join(current_dir, "..", "prompts")
        filepath = os.path.join(prompts_dir, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    @classmethod
    def call_import_ia(cls, doc_text: str, doc_metadata: dict) -> ProcessImportAIResultSchema:
        """
        Envia o texto sanitizado e metadados do documento para a API da OpenAI (gpt-4o)
        e retorna o cadastro do processo estruturado e validado por Pydantic.
        """
        if not settings.openai_api_key:
            logger.error("Chave de API do OpenAI não configurada no backend.")
            raise HTTPException(status_code=500, detail="Serviço de IA não configurado. Verifique a OPENAI_API_KEY no .env.")

        # 1. Auditoria da requisição (python_audit_core.md)
        logger.bind(audit=True).info({
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "actor": "agent_importer",
            "action": "llm_import_request",
            "target": doc_metadata.get("filename", "unknown"),
            "outcome": "processing",
            "extra_data": {
                "chars_count": doc_metadata.get("num_characters", 0),
                "images_count": doc_metadata.get("num_images", 0)
            }
        })

        # 2. Carregar e preencher prompts
        try:
            system_prompt = cls._load_prompt("system_process_importer.md")
            user_template = cls._load_prompt("user_process_import_template.md")
        except Exception as e:
            logger.error(f"Erro ao carregar arquivos de prompt da IA: {e}")
            raise HTTPException(status_code=500, detail="Erro interno ao carregar arquivos de configuração do motor de IA.")

        user_prompt = user_template.replace("{{FILENAME}}", str(doc_metadata.get("filename", "")))
        user_prompt = user_prompt.replace("{{SIZE_BYTES}}", str(doc_metadata.get("size_bytes", 0)))
        user_prompt = user_prompt.replace("{{NUM_PARAGRAPHS}}", str(doc_metadata.get("num_paragraphs", 0)))
        user_prompt = user_prompt.replace("{{NUM_IMAGES}}", str(doc_metadata.get("num_images", 0)))
        user_prompt = user_prompt.replace("{{NUM_CHARACTERS}}", str(doc_metadata.get("num_characters", 0)))
        user_prompt = user_prompt.replace("{{DOCUMENT_TEXT}}", doc_text)

        # Instanciar cliente
        client = OpenAI(
            api_key=settings.openai_api_key,
            timeout=settings.openai_timeout_seconds
        )

        # 3. Execução com Retries e Timeout (llm_state_management.md)
        max_retries = 2
        for attempt in range(1, max_retries + 1):
            logger.info(f"Enviando chamada para a OpenAI. Tentativa {attempt}/{max_retries}.")
            try:
                response = client.chat.completions.create(
                    model=settings.openai_model,  # gpt-4o
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt},
                    ],
                    response_format={"type": "json_object"},
                    temperature=0.1  # Baixa temperatura para maior determinismo e adesão ao JSON
                )

                content = response.choices[0].message.content
                if not content:
                    logger.warning("Resposta da OpenAI retornou conteúdo vazio.")
                    raise ValueError("Conteúdo da resposta é nulo.")

                # Realizar o parse
                parsed_data = json.loads(content)
                
                # Validar usando o Schema do Pydantic
                validated_schema = ProcessImportAIResultSchema.model_validate(parsed_data)
                
                # Sucesso
                logger.bind(audit=True).info({
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "actor": "agent_importer",
                    "action": "llm_import_response",
                    "target": doc_metadata.get("filename", "unknown"),
                    "outcome": "success",
                    "extra_data": {
                        "steps_extracted": len(validated_schema.etapas),
                        "connections_extracted": len(validated_schema.conexoes),
                        "gaps_found": len(validated_schema.lacunas_mapeamento)
                    }
                })
                
                return validated_schema

            except (json.JSONDecodeError, ValidationError) as e:
                logger.error(f"Erro de decodificação/validação do JSON da IA (Tentativa {attempt}): {e}")
                if attempt == max_retries:
                    logger.bind(audit=True).info({
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "actor": "agent_importer",
                        "action": "llm_import_response",
                        "target": doc_metadata.get("filename", "unknown"),
                        "outcome": "error",
                        "extra_data": {"error_type": "json_validation", "detail": str(e)}
                    })
                    raise HTTPException(
                        status_code=502,
                        detail="A inteligência artificial retornou uma resposta fora do formato de dados aceito. Nenhuma alteração foi feita no banco."
                    )
            except OpenAIError as e:
                logger.error(f"Erro na chamada da API da OpenAI (Tentativa {attempt}): {e}")
                if attempt == max_retries:
                    logger.bind(audit=True).info({
                        "timestamp": datetime.utcnow().isoformat() + "Z",
                        "actor": "agent_importer",
                        "action": "llm_import_response",
                        "target": doc_metadata.get("filename", "unknown"),
                        "outcome": "error",
                        "extra_data": {"error_type": "openai_api_error", "detail": str(e)}
                    })
                    raise HTTPException(
                        status_code=502,
                        detail="Falha ao se comunicar com o motor de Inteligência Artificial externo. Tente novamente."
                    )
            except Exception as e:
                logger.error(f"Erro inesperado na chamada do modelo (Tentativa {attempt}): {e}")
                if attempt == max_retries:
                    raise HTTPException(
                        status_code=500,
                        detail="Ocorreu um erro interno durante o processamento da IA."
                    )
