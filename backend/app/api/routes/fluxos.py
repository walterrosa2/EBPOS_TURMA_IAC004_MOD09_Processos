from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.fluxo_schema import FluxoResponse
from app.services import fluxo_service

router = APIRouter(prefix="/api/processos/{processo_id}/fluxo", tags=["fluxo"])

@router.get("", response_model=FluxoResponse)
def obter_fluxo(processo_id: int, db: Session = Depends(get_db)):
    return fluxo_service.obter_fluxo(db, processo_id)

@router.put("", response_model=FluxoResponse)
def salvar_fluxo(processo_id: int, payload: dict, db: Session = Depends(get_db)):
    return fluxo_service.salvar_fluxo(db, processo_id, payload)
