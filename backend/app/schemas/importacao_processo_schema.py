from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class TipoEtapaEnum(str, Enum):
    MANUAL = "Manual"
    AUTOMATICA = "Automática"
    DECISAO = "Decisão"
    VALIDACAO = "Validação"
    INTEGRACAO = "Integração"
    DOCUMENTO = "Documento"
    OUTRO = "Outro"

class TipoConexaoEnum(str, Enum):
    PADRAO = "padrao"
    SUCESSO = "sucesso"
    FALHA = "falha"
    CONDICIONAL = "condicional"

class ConfiancaEnum(str, Enum):
    ALTA = "Alta"
    MEDIA = "Média"
    BAIXA = "Baixa"

class AlertaSensivelTipoEnum(str, Enum):
    CREDENCIAL = "credencial"
    DADO_PESSOAL = "dado_pessoal"
    CERTIFICADO = "certificado"
    OUTRO = "outro"

class AcaoAplicadaEnum(str, Enum):
    MASCARADO = "mascarado"
    REMOVIDO = "removido"
    IGNORADO = "ignorado"

class ImportedProcessSchema(BaseModel):
    nome: str = Field(..., description="Nome do processo mapeado no documento")
    area: str = Field("Fiscal", description="Área do processo (padrão: Fiscal)")
    descricao: Optional[str] = Field(None, description="Resumo do funcionamento geral do processo")
    objetivo: Optional[str] = Field(None, description="Objetivo principal do processo")
    responsavel: Optional[str] = Field(None, description="Responsável geral pela operação")
    periodicidade: Optional[str] = Field(None, description="Frequência de execução (ex: Mensal)")
    criticidade: Optional[str] = Field(None, description="Grau de criticidade (ex: Alta)")
    status: Optional[str] = Field("Ativo", description="Status inicial do processo")
    sistemas_utilizados: Optional[str] = Field(None, description="Sistemas identificados (ex: Protheus, PVA)")
    documentos_utilizados: Optional[str] = Field(None, description="Documentos/planilhas utilizados")
    observacoes: Optional[str] = Field(None, description="Observações ou notas de importação")

class ImportedStepSchema(BaseModel):
    ordem: int = Field(..., description="Ordem sequencial da etapa")
    nome: str = Field(..., description="Título curto e claro da etapa")
    descricao: str = Field(..., description="Descrição detalhada das ações executadas nesta etapa")
    responsavel: Optional[str] = Field(None, description="Quem executa a etapa")
    entrada: Optional[str] = Field(None, description="Arquivos, dados ou planilhas de entrada")
    saida: Optional[str] = Field(None, description="Resultados, relatórios ou arquivos gerados")
    sistema_utilizado: Optional[str] = Field(None, description="Software ou plataforma usada no passo")
    tempo_estimado: Optional[str] = Field(None, description="Tempo médio para conclusão da etapa")
    tipo_etapa: TipoEtapaEnum = Field(TipoEtapaEnum.OUTRO, description="Tipo lógico de atividade")
    risco: Optional[str] = Field(None, description="Riscos identificados nesta etapa")
    gargalo: Optional[str] = Field(None, description="Gargalos operacionais previstos")
    oportunidade_automacao: Optional[str] = Field(None, description="Possibilidade de automação detectada")
    confianca_extracao: ConfiancaEnum = Field(ConfiancaEnum.MEDIA, description="Nível de confiança da IA na extração")
    evidencia_documental: Optional[str] = Field(None, description="Trecho ou referência de imagem do documento")

class ImportedConnectionSchema(BaseModel):
    ordem_origem: int = Field(..., description="Ordem da etapa de origem")
    ordem_destino: int = Field(..., description="Ordem da etapa de destino")
    tipo_conexao: TipoConexaoEnum = Field(TipoConexaoEnum.PADRAO, description="Tipo de transição lógica")
    condicao: Optional[str] = Field(None, description="Texto explicativo para caminhos condicionais")

class ImportGapSchema(BaseModel):
    campo_ou_tema: str = Field(..., description="Qual informação ficou incompleta ou ambígua")
    descricao: str = Field(..., description="Motivo do alerta de lacuna (ex: imagem não interpretada)")
    pergunta_recomendada: str = Field(..., description="Pergunta sugerida ao usuário para complementar a informação")

class SensitiveAlertSchema(BaseModel):
    tipo: AlertaSensivelTipoEnum = Field(..., description="Tipo de dado sensível detectado")
    descricao: str = Field(..., description="Breve descrição da higienização")
    acao_aplicada: AcaoAplicadaEnum = Field(..., description="Ação tomada (removido, mascarado)")

class ResumoImportacaoSchema(BaseModel):
    quantidade_etapas: int = Field(..., description="Quantidade de etapas extraídas")
    quantidade_conexoes: int = Field(..., description="Quantidade de conexões criadas")
    quantidade_lacunas: int = Field(..., description="Quantidade de lacunas registradas")
    confianca_geral: ConfiancaEnum = Field(ConfiancaEnum.MEDIA, description="Nível geral de confiança")

class ProcessImportAIResultSchema(BaseModel):
    processo: ImportedProcessSchema
    etapas: List[ImportedStepSchema]
    conexoes: List[ImportedConnectionSchema]
    lacunas_mapeamento: List[ImportGapSchema]
    alertas_sensiveis: List[SensitiveAlertSchema]
    resumo_importacao: ResumoImportacaoSchema

class ProcessImportResponseSchema(BaseModel):
    processo_id: int = Field(..., description="Identificador do processo criado no banco")
    mensagem: str = Field(..., description="Mensagem de retorno descritiva")
    nome_processo: str = Field(..., description="Nome do processo criado")
    etapas_criadas: int = Field(..., description="Total de etapas gravadas")
    conexoes_criadas: int = Field(..., description="Total de conexões gravadas")
    lacunas_identificadas: List[str] = Field([], description="Breve resumo textual das lacunas identificadas")
    alertas_sensiveis: List[SensitiveAlertSchema] = Field([], description="Alertas de higienização de credenciais")
