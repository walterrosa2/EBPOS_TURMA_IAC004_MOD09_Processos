from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from .etapa_schema import EtapaResponse

class ConexaoBase(BaseModel):
    etapa_origem_id: int
    etapa_destino_id: int
    tipo_conexao: Optional[str] = None
    condicao: Optional[str] = None

class ConexaoCreate(ConexaoBase):
    pass

class ConexaoResponse(ConexaoBase):
    id: int
    processo_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class FluxoResponse(BaseModel):
    etapas: List[EtapaResponse]
    conexoes: List[ConexaoResponse]
