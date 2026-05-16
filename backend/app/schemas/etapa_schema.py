from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class EtapaBase(BaseModel):
    nome: str
    descricao: Optional[str] = None
    responsavel: Optional[str] = None
    entrada: Optional[str] = None
    saida: Optional[str] = None
    sistema_utilizado: Optional[str] = None
    tempo_estimado: Optional[str] = None
    tipo_etapa: Optional[str] = None
    risco: Optional[str] = None
    gargalo: Optional[str] = None
    oportunidade_automacao: Optional[str] = None
    posicao_x: Optional[float] = None
    posicao_y: Optional[float] = None

class EtapaCreate(EtapaBase):
    pass

class EtapaResponse(EtapaBase):
    id: int
    processo_id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
