from sqlalchemy.orm import Session
from app.models.analise import AnaliseIA
from app.schemas.analise_schema import AnaliseIACreate

def create_analise(db: Session, data: AnaliseIACreate):
    db_analise = AnaliseIA(
        processo_id=data.processo_id,
        resumo_executivo=data.resumo_executivo,
        diagnostico_operacional=data.diagnostico_operacional,
        nivel_maturidade=data.nivel_maturidade,
        json_resultado=data.json_resultado
    )
    db.add(db_analise)
    db.commit()
    db.refresh(db_analise)
    return db_analise

def list_analises_by_processo(db: Session, processo_id: int):
    return db.query(AnaliseIA).filter(AnaliseIA.processo_id == processo_id).order_by(AnaliseIA.created_at.desc()).all()

def get_analise_by_id(db: Session, analise_id: int):
    return db.query(AnaliseIA).filter(AnaliseIA.id == analise_id).first()
