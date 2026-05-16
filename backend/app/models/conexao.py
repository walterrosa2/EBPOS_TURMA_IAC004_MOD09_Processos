from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.database.base import Base

class Conexao(Base):
    __tablename__ = "conexoes"

    id = Column(Integer, primary_key=True, index=True)
    processo_id = Column(Integer, ForeignKey("processos.id"), nullable=False)
    etapa_origem_id = Column(Integer, ForeignKey("etapas.id"), nullable=False)
    etapa_destino_id = Column(Integer, ForeignKey("etapas.id"), nullable=False)
    tipo_conexao = Column(String, nullable=True)
    condicao = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
