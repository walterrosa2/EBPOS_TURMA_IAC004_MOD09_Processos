from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.models.processo import Processo
from app.schemas.processo_schema import ProcessoCreate

def list_processos(db: Session, filters: dict) -> List[Processo]:
    query = db.query(Processo)
    if "area" in filters and filters["area"]:
        query = query.filter(Processo.area == filters["area"])
    if "criticidade" in filters and filters["criticidade"]:
        query = query.filter(Processo.criticidade == filters["criticidade"])
    if "status" in filters and filters["status"]:
        query = query.filter(Processo.status == filters["status"])
    if "q" in filters and filters["q"]:
        search_term = f"%{filters['q']}%"
        query = query.filter(or_(Processo.nome.ilike(search_term), Processo.descricao.ilike(search_term)))
    
    return query.all()

def get_processo_by_id(db: Session, processo_id: int) -> Optional[Processo]:
    return db.query(Processo).filter(Processo.id == processo_id).first()

def create_processo(db: Session, data: ProcessoCreate) -> Processo:
    db_obj = Processo(**data.model_dump())
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_processo(db: Session, processo: Processo, data: dict) -> Processo:
    for key, value in data.items():
        setattr(processo, key, value)
    db.commit()
    db.refresh(processo)
    return processo

def delete_processo(db: Session, processo: Processo) -> None:
    db.delete(processo)
    db.commit()
