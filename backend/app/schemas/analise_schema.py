from pydantic import BaseModel, BeforeValidator
from typing import Optional, List, Literal, Annotated
from datetime import datetime

# --- Normalização de escalas qualitativas vindas da IA ---
# A LLM frequentemente varia gênero/acento/caixa (ex.: "Alta" no lugar de "Alto",
# "media" sem acento). Normalizamos para a forma canônica ANTES da validação,
# preservando a tipagem rígida do schema.

# Cada chave (sem acento, minúscula) mapeia para (forma masculina, forma feminina).
_ESCALA_BASE = {
    "baixo": ("Baixo", "Baixa"),
    "baixa": ("Baixo", "Baixa"),
    "medio": ("Médio", "Média"),
    "media": ("Médio", "Média"),
    "alto": ("Alto", "Alta"),
    "alta": ("Alto", "Alta"),
}

_ACENTOS = str.maketrans("áàâãéèêíïóôõöúüç", "aaaaeeeiioooouuc")

def _normalizar_escala(valor, feminino: bool):
    if not isinstance(valor, str):
        return valor
    chave = valor.strip().lower().translate(_ACENTOS)
    if chave in _ESCALA_BASE:
        return _ESCALA_BASE[chave][1 if feminino else 0]
    return valor

EscalaMasculina = Annotated[
    Literal["Baixo", "Médio", "Alto"],
    BeforeValidator(lambda v: _normalizar_escala(v, feminino=False)),
]
EscalaFeminina = Annotated[
    Literal["Baixa", "Média", "Alta"],
    BeforeValidator(lambda v: _normalizar_escala(v, feminino=True)),
]


class NivelMaturidadeSchema(BaseModel):
    nivel: Literal["Inicial", "Repetível", "Padronizado", "Gerenciado", "Otimizado"]
    justificativa: str

class GargaloSchema(BaseModel):
    titulo: str
    descricao: str
    etapa_relacionada: Optional[str] = None
    impacto: EscalaMasculina

class RiscoSchema(BaseModel):
    titulo: str
    descricao: str
    tipo: Literal["operacional", "prazo", "qualidade", "compliance", "dados", "dependencia_pessoa", "sistema", "comunicacao"]
    etapa_relacionada: Optional[str] = None
    severidade: EscalaMasculina
    mitigacao_sugerida: str

class SugestaoMelhoriaSchema(BaseModel):
    titulo: str
    descricao: str
    tipo: Literal["melhoria_fluxo", "controle", "documentacao", "treinamento", "indicador", "governanca"]
    impacto: EscalaMasculina
    esforco: EscalaMasculina
    prioridade: EscalaFeminina
    etapa_relacionada: Optional[str] = None
    beneficio_esperado: str

class SugestaoAutomacaoSchema(BaseModel):
    titulo: str
    descricao: str
    tipo: Literal["automacao_simples", "integracao", "ia", "rpa"]
    impacto: EscalaMasculina
    esforco: EscalaMasculina
    prioridade: EscalaFeminina
    etapa_relacionada: Optional[str] = None
    pre_requisitos: List[str]
    beneficio_esperado: str
    risco_implementacao: str

class OportunidadeIASchema(BaseModel):
    titulo: str
    descricao: str
    entrada_necessaria: str
    saida_esperada: str
    validacao_humana_necessaria: bool
    impacto: EscalaMasculina
    esforco: EscalaMasculina

class LacunaMapeamentoSchema(BaseModel):
    campo_ou_tema: str
    descricao: str
    pergunta_recomendada: str

class IndicadorRecomendadoSchema(BaseModel):
    nome: str
    objetivo: str
    formula_ou_forma_medicao: str
    frequencia: str

class DiretrizAutomacaoIASchema(BaseModel):
    titulo: str
    descricao: str
    tipo: Literal["automacao_simples", "integracao", "ia", "rpa", "workflow"]
    prioridade: EscalaFeminina
    primeiro_passo: str
    dependencias: List[str]
    criterio_sucesso: str

class AnaliseIAResultadoSchema(BaseModel):
    resumo_executivo: str
    diagnostico_operacional: str
    nivel_maturidade: NivelMaturidadeSchema
    pontos_fortes: List[str]
    gargalos: List[GargaloSchema]
    riscos: List[RiscoSchema]
    sugestoes_melhoria: List[SugestaoMelhoriaSchema]
    sugestoes_automacao: List[SugestaoAutomacaoSchema]
    oportunidades_ia: List[OportunidadeIASchema]
    lacunas_mapeamento: List[LacunaMapeamentoSchema]
    indicadores_recomendados: List[IndicadorRecomendadoSchema]
    diretrizes_automacao: List[DiretrizAutomacaoIASchema]
    perguntas_para_aprofundamento: List[str]
    alertas: List[str]

# API Schemas

class AnaliseIABase(BaseModel):
    resumo_executivo: Optional[str] = None
    diagnostico_operacional: Optional[str] = None
    nivel_maturidade: Optional[str] = None
    json_resultado: str

class AnaliseIACreate(AnaliseIABase):
    processo_id: int

class AnaliseIAResponse(AnaliseIABase):
    id: int
    processo_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class AnaliseIAListItem(BaseModel):
    id: int
    processo_id: int
    resumo_executivo: Optional[str] = None
    nivel_maturidade: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True
