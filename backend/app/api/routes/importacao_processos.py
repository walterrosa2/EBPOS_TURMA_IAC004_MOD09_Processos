from fastapi import APIRouter, Depends, UploadFile, File, HTTPException, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.importacao_processo_schema import ProcessImportResponseSchema
from app.services.process_import_service import ProcessImportService
from loguru import logger

router = APIRouter(prefix="/api/processos", tags=["processos"])

@router.post(
    "/importar", 
    response_model=ProcessImportResponseSchema, 
    status_code=status.HTTP_201_CREATED,
    summary="Importa um processo a partir de um documento operacional DOCX"
)
async def importar_processo(
    file: UploadFile = File(...), 
    db: Session = Depends(get_db)
):
    """
    Recebe um arquivo .docx contendo um mapeamento de processo operacional,
    higieniza dados confidenciais, interpreta a estrutura por IA e cadastra
    o processo, etapas e conexões automaticamente na base de dados de forma transacional.
    """
    # 1. Validar se o arquivo foi enviado
    if not file or not file.filename:
        logger.warning("Tentativa de importação sem arquivo.")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Nenhum arquivo foi enviado."
        )

    filename = file.filename
    logger.info(f"Recebida requisição de importação de arquivo: {filename}")

    # 2. Validar extensão do arquivo (apenas .docx)
    if not filename.lower().endswith(".docx"):
        logger.warning(f"Extensão de arquivo inválida: {filename}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Extensão de arquivo não permitida. Apenas documentos no formato .docx são suportados nesta versão."
        )

    try:
        # 3. Ler os bytes do arquivo de upload
        file_bytes = await file.read()
        
        # 4. Validar arquivo vazio
        if len(file_bytes) == 0:
            logger.warning(f"O arquivo {filename} está completamente vazio.")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="O arquivo enviado está vazio e não contém nenhum texto ou dados operacionais."
            )

        # 5. Validar tamanho máximo (10MB)
        max_size = 10 * 1024 * 1024  # 10 Megabytes
        if len(file_bytes) > max_size:
            logger.warning(f"O arquivo {filename} excede o limite máximo de tamanho: {len(file_bytes)} bytes.")
            raise HTTPException(
                status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                detail="O arquivo enviado excede o limite máximo permitido de 10 megabytes (MB)."
            )

        # 6. Chamar o serviço orquestrador de importação
        result = ProcessImportService.import_process_from_docx(db, file_bytes, filename)
        return result

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Erro inesperado durante importação de processos: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Ocorreu um erro interno inesperado durante o processamento da importação."
        )
