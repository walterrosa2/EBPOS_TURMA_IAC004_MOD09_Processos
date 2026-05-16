from typing import List, Optional
from sqlalchemy.orm import Session
from app.models.conexao import Conexao
from app.schemas.fluxo_schema import ConexaoCreate

def list_conexoes_by_processo(db: Session, processo_id: int) -> List[Conexao]:
    return db.query(Conexao).filter(Conexao.processo_id == processo_id).all()

def create_conexao(db: Session, processo_id: int, data: dict) -> Conexao:
    db_obj = Conexao(**data, processo_id=processo_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_conexoes_by_etapa(db: Session, etapa_id: int) -> None:
    db.query(Conexao).filter(
        (Conexao.etapa_origem_id == etapa_id) | (Conexao.etapa_destino_id == etapa_id)
    ).delete()
    db.commit()

def delete_conexoes_by_processo(db: Session, processo_id: int) -> None:
    db.query(Conexao).filter(Conexao.processo_id == processo_id).delete()
    db.commit()
