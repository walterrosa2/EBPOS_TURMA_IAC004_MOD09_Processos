from typing import List
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import processo_repository
from app.schemas.processo_schema import ProcessoCreate, ProcessoResponse
from app.models.processo import Processo

def listar_processos(db: Session, filters: dict) -> List[Processo]:
    return processo_repository.list_processos(db, filters)

def obter_processo(db: Session, processo_id: int) -> Processo:
    processo = processo_repository.get_processo_by_id(db, processo_id)
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return processo

def criar_processo(db: Session, payload: ProcessoCreate) -> Processo:
    return processo_repository.create_processo(db, payload)

def atualizar_processo(db: Session, processo_id: int, payload: ProcessoCreate) -> Processo:
    processo = obter_processo(db, processo_id)
    return processo_repository.update_processo(db, processo, payload.model_dump(exclude_unset=True))

def excluir_processo(db: Session, processo_id: int) -> None:
    processo = obter_processo(db, processo_id)
    processo_repository.delete_processo(db, processo)
