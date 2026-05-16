from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class AnaliseIA(Base):
    __tablename__ = "analises_ia"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    resumo_executivo = Column(String, nullable=True)
    diagnostico_operacional = Column(String, nullable=True)
    nivel_maturidade = Column(String, nullable=True)
    json_resultado = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
