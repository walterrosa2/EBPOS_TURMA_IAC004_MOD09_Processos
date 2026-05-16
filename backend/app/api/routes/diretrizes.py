from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.diretriz_schema import DiretrizAutomacaoResponse, DiretrizAutomacaoUpdate
from app.services import diretriz_service

router = APIRouter(prefix="/api", tags=["diretrizes"])

@router.get("/processos/{processo_id}/diretrizes", response_model=List[DiretrizAutomacaoResponse])
def list_diretrizes(processo_id: int, db: Session = Depends(get_db)):
    return diretriz_service.list_diretrizes(db, processo_id)

@router.put("/diretrizes/{diretriz_id}", response_model=DiretrizAutomacaoResponse)
def update_diretriz(diretriz_id: int, data: DiretrizAutomacaoUpdate, db: Session = Depends(get_db)):
    return diretriz_service.update_diretriz(db, diretriz_id, data)
