from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.repositories import diretriz_repository
from app.models.processo import Processo
from app.schemas.diretriz_schema import DiretrizAutomacaoUpdate

def list_diretrizes(db: Session, processo_id: int):
    processo = db.query(Processo).filter(Processo.id == processo_id).first()
    if not processo:
        raise HTTPException(status_code=404, detail="Processo não encontrado.")
    return diretriz_repository.list_diretrizes_by_processo(db, processo_id)

def update_diretriz(db: Session, diretriz_id: int, diretriz_update: DiretrizAutomacaoUpdate):
    diretriz = diretriz_repository.get_diretriz_by_id(db, diretriz_id)
    if not diretriz:
        raise HTTPException(status_code=404, detail="Diretriz não encontrada.")
    
    return diretriz_repository.update_diretriz(db, diretriz, diretriz_update.model_dump())
