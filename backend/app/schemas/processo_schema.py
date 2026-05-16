from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ProcessoBase(BaseModel):
    nome: str
    area: str
    descricao: Optional[str] = None
    objetivo: Optional[str] = None
    responsavel: Optional[str] = None
    periodicidade: Optional[str] = None
    criticidade: Optional[str] = None
    status: Optional[str] = None
    sistemas_utilizados: Optional[str] = None
    documentos_utilizados: Optional[str] = None
    observacoes: Optional[str] = None

class ProcessoCreate(ProcessoBase):
    pass

class ProcessoResponse(ProcessoBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
