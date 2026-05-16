from sqlalchemy.orm import Session
from app.models.diretriz import DiretrizAutomacao
from typing import List

def create_diretriz(db: Session, data: dict):
    db_diretriz = DiretrizAutomacao(**data)
    db.add(db_diretriz)
    db.commit()
    db.refresh(db_diretriz)
    return db_diretriz

def bulk_create_diretrizes(db: Session, diretrizes: List[dict]):
    db_diretrizes = [DiretrizAutomacao(**d) for d in diretrizes]
    db.bulk_save_objects(db_diretrizes)
    db.commit()
    # bulk_save_objects doesn't populate IDs back automatically, but for our case it's fine
    return db_diretrizes

def list_diretrizes_by_processo(db: Session, processo_id: int):
    return db.query(DiretrizAutomacao).filter(DiretrizAutomacao.processo_id == processo_id).order_by(DiretrizAutomacao.created_at.desc()).all()

def get_diretriz_by_id(db: Session, diretriz_id: int):
    return db.query(DiretrizAutomacao).filter(DiretrizAutomacao.id == diretriz_id).first()

def update_diretriz(db: Session, db_diretriz: DiretrizAutomacao, data: dict):
    for key, value in data.items():
        setattr(db_diretriz, key, value)
    db.commit()
    db.refresh(db_diretriz)
    return db_diretriz
