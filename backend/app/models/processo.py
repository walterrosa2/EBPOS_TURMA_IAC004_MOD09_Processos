from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database.base import Base

class Processo(Base):
    __tablename__ = "processos"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String, nullable=False)
    area = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    objetivo = Column(String, nullable=True)
    responsavel = Column(String, nullable=True)
    periodicidade = Column(String, nullable=True)
    criticidade = Column(String, nullable=True)
    status = Column(String, nullable=True)
    sistemas_utilizados = Column(String, nullable=True)
    documentos_utilizados = Column(String, nullable=True)
    observacoes = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
