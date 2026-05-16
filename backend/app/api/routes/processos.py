from typing import List, Optional
from fastapi import APIRouter, Depends, Query, status
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.schemas.processo_schema import ProcessoCreate, ProcessoResponse
from app.services import processo_service

router = APIRouter(prefix="/api/processos", tags=["processos"])

@router.get("", response_model=List[ProcessoResponse])
def listar_processos(
    area: Optional[str] = Query(None),
    criticidade: Optional[str] = Query(None),
    status_param: Optional[str] = Query(None, alias="status"),
    q: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    filters = {
        "area": area,
        "criticidade": criticidade,
        "status": status_param,
        "q": q
    }
    return processo_service.listar_processos(db, filters)

@router.post("", response_model=ProcessoResponse, status_code=status.HTTP_201_CREATED)
def criar_processo(payload: ProcessoCreate, db: Session = Depends(get_db)):
    return processo_service.criar_processo(db, payload)

@router.get("/{processo_id}", response_model=ProcessoResponse)
def obter_processo(processo_id: int, db: Session = Depends(get_db)):
    return processo_service.obter_processo(db, processo_id)

@router.put("/{processo_id}", response_model=ProcessoResponse)
def atualizar_processo(processo_id: int, payload: ProcessoCreate, db: Session = Depends(get_db)):
    return processo_service.atualizar_processo(db, processo_id, payload)

@router.delete("/{processo_id}", status_code=status.HTTP_204_NO_CONTENT)
def excluir_processo(processo_id: int, db: Session = Depends(get_db)):
    processo_service.excluir_processo(db, processo_id)
