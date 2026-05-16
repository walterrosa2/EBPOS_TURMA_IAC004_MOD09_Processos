from pydantic import BaseModel
from typing import Optional, Literal
from datetime import datetime

class DiretrizAutomacaoBase(BaseModel):
    titulo: str
    tipo: Optional[str] = None
    descricao: Optional[str] = None
    impacto: Optional[str] = None
    esforco: Optional[str] = None
    prioridade: Optional[str] = None
    status: Optional[Literal["Sugerida", "Em avaliação", "Priorizada", "Em implementação", "Concluída", "Descartada"]] = None
    pre_requisitos: Optional[str] = None

class DiretrizAutomacaoCreate(DiretrizAutomacaoBase):
    pass

class DiretrizAutomacaoUpdate(BaseModel):
    status: Literal["Sugerida", "Em avaliação", "Priorizada", "Em implementação", "Concluída", "Descartada"]

class DiretrizAutomacaoResponse(DiretrizAutomacaoBase):
    id: int
    processo_id: int
    analise_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
