from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app.database.session import get_db
from app.schemas.analise_schema import AnaliseIAResponse, AnaliseIAListItem
from app.services import analise_service

router = APIRouter(prefix="/api", tags=["analises"])

@router.post("/processos/{processo_id}/analises", response_model=AnaliseIAResponse)
def create_analise_ia(processo_id: int, db: Session = Depends(get_db)):
    return analise_service.request_analise(db, processo_id)

@router.get("/processos/{processo_id}/analises", response_model=List[AnaliseIAListItem])
def list_analises_ia(processo_id: int, db: Session = Depends(get_db)):
    return analise_service.list_analises(db, processo_id)

@router.get("/analises/{analise_id}", response_model=AnaliseIAResponse)
def get_analise_ia(analise_id: int, db: Session = Depends(get_db)):
    return analise_service.get_analise(db, analise_id)
