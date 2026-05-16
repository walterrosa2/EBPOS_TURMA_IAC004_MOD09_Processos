from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.etapa import Etapa
from app.schemas.etapa_schema import EtapaCreate

def list_etapas_by_processo(db: Session, processo_id: int) -> List[Etapa]:
    return db.query(Etapa).filter(Etapa.processo_id == processo_id).all()

def get_etapa_by_id(db: Session, etapa_id: int) -> Optional[Etapa]:
    return db.query(Etapa).filter(Etapa.id == etapa_id).first()

def create_etapa(db: Session, processo_id: int, data: EtapaCreate) -> Etapa:
    db_obj = Etapa(**data.model_dump(), processo_id=processo_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def update_etapa(db: Session, etapa: Etapa, data: dict) -> Etapa:
    for key, value in data.items():
        setattr(etapa, key, value)
    db.commit()
    db.refresh(etapa)
    return etapa

def delete_etapa(db: Session, etapa: Etapa) -> None:
    db.delete(etapa)
    db.commit()

def update_etapa_position(db: Session, etapa: Etapa, posicao_x: Optional[float], posicao_y: Optional[float]) -> Etapa:
    etapa.posicao_x = posicao_x
    etapa.posicao_y = posicao_y
    db.commit()
    db.refresh(etapa)
    return etapa

def list_etapas_by_ids(db: Session, ids: List[int]) -> List[Etapa]:
    return db.query(Etapa).filter(Etapa.id.in_(ids)).all()
