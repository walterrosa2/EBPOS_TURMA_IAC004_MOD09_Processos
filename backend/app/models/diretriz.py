from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class DiretrizAutomacao(Base):
    __tablename__ = "diretrizes_automacao"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    analise_id = Column(Integer, ForeignKey("analises_ia.id"), nullable=True)
    titulo = Column(String, nullable=False)
    tipo = Column(String, nullable=True)
    descricao = Column(String, nullable=True)
    impacto = Column(String, nullable=True)
    esforco = Column(String, nullable=True)
    prioridade = Column(String, nullable=True)
    status = Column(String, nullable=True)
    pre_requisitos = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
