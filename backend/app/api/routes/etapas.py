from typing import List
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.etapa_schema import EtapaCreate, EtapaResponse
from app.services import etapa_service

router = APIRouter(tags=["etapas"])

@router.get("/api/processos/{processo_id}/etapas", response_model=List[EtapaResponse])
def listar_etapas(processo_id: int, db: Session = Depends(get_db)):
    return etapa_service.listar_etapas(db, processo_id)

@router.post("/api/processos/{processo_id}/etapas", response_model=EtapaResponse, status_code=status.HTTP_201_CREATED)
def criar_etapa(processo_id: int, payload: EtapaCreate, db: Session = Depends(get_db)):
    return etapa_service.criar_etapa(db, processo_id, payload)

@router.put("/api/etapas/{etapa_id}", response_model=EtapaResponse)
def atualizar_etapa(etapa_id: int, payload: EtapaCreate, db: Session = Depends(get_db)):
    return etapa_service.atualizar_etapa(db, etapa_id, payload)

@router.delete("/api/etapas/{etapa_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_etapa(etapa_id: int, db: Session = Depends(get_db)):
    etapa_service.excluir_etapa(db, etapa_id)
