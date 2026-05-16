from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class Etapa(Base):
    __tablename__ = "etapas"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    nome = Column(String, nullable=False)
    descricao = Column(String, nullable=True)
    responsavel = Column(String, nullable=True)
    entrada = Column(String, nullable=True)
    saida = Column(String, nullable=True)
    sistema_utilizado = Column(String, nullable=True)
    tempo_estimado = Column(String, nullable=True)
    tipo_etapa = Column(String, nullable=True)
    risco = Column(String, nullable=True)
    gargalo = Column(String, nullable=True)
    oportunidade_automacao = Column(String, nullable=True)
    posicao_x = Column(Float, nullable=True)
    posicao_y = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
