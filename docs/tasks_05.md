Regras obrigatórias
Não expor OPENAI_API_KEY no código.
Ler OPENAI_API_KEY somente de variável de ambiente.
Ler OPENAI_MODEL de variável de ambiente, default gpt-4o.
Não commitar .env.
Não registrar prompt completo com dados sensíveis em logs.
Não enviar análise para IA se o processo não tiver etapas.
Não permitir que resposta inválida da IA seja salva.
Validar JSON com Pydantic antes de persistir.
Persistir json_resultado completo como string JSON.
Persistir campos resumidos em colunas próprias.
Criar diretrizes a partir de diretrizes_automacao.
Não apagar análises anteriores ao gerar uma nova.
Não inventar regras fiscais, prazos legais, sistemas ou obrigações no prompt.
Não criar fallback automático para outro modelo sem decisão explícita.
Toda regra de negócio deve ficar em services.
Rotas devem apenas receber request, chamar services e retornar response.
Repositories devem concentrar acesso ao banco.
Atualizar /docs/backlog.md, /docs/changelog.md, /docs/tests.md, /docs/architecture.md e /docs/decisions.md.
Criar testes automatizados sem chamar a OpenAI real.
Usar mock para testes de IA.

As regras de segurança do projeto proíbem expor senhas, tokens, chaves de API, credenciais e dados sensíveis em código-fonte ou logs.

Estrutura esperada após este pacote
backend/
  app/
    api/
      routes/
        analises.py
        diretrizes.py

    services/
      ia_service.py
      analise_service.py
      diretriz_service.py

    repositories/
      analise_repository.py
      diretriz_repository.py

    schemas/
      analise_schema.py
      diretriz_schema.py

    prompts/
      system_process_mapper.md
      user_process_analysis_template.md

    core/
      config.py

    main.py

  tests/
    test_analise_schema.py
    test_ia_service.py
    test_analises_api.py
    test_diretrizes_api.py
TASK-070 — Configurar dependência OpenAI
Objetivo

Adicionar OpenAI SDK ao backend e ajustar configurações.

Arquivos impactados
backend/requirements.txt
backend/app/core/config.py
backend/.env.example
backend/README.md
docs/architecture.md
docs/decisions.md
Dependência obrigatória

Adicionar em backend/requirements.txt:

openai

Não fixar versão sem necessidade. Se fixar, justificar em docs/decisions.md.

Variáveis obrigatórias

Atualizar backend/.env.example:

APP_NAME=QDT Processos Contabeis API
APP_ENV=development
DATABASE_URL=sqlite:///./data/qdt_processos.db
CORS_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o
OPENAI_TIMEOUT_SECONDS=60
Configuração esperada

Atualizar backend/app/core/config.py para expor:

openai_api_key
openai_model
openai_timeout_seconds
Critérios de aceite
Dado que OPENAI_API_KEY está no ambiente,
quando o backend iniciar,
então a configuração deve estar disponível para ia_service.

Dado que OPENAI_MODEL não está definido,
quando o backend iniciar,
então deve assumir gpt-4o.

Dado que .env.example existe,
quando abrir o arquivo,
então deve conter OPENAI_API_KEY e OPENAI_MODEL sem valores reais.
TASK-071 — Criar system prompt especialista
Objetivo

Criar o prompt principal da IA especialista em mapeamento, análise e automação de processos contábeis.

Arquivo impactado
backend/app/prompts/system_process_mapper.md
Conteúdo obrigatório

Criar exatamente este conteúdo base, podendo apenas melhorar clareza sem remover regras:

# SYSTEM PROMPT — IA ESPECIALISTA EM MAPEAMENTO, ANÁLISE E AUTOMAÇÃO DE PROCESSOS CONTÁBEIS

Você é uma IA especialista em mapeamento, análise, documentação, melhoria e automação de processos de operações contábeis.

Seu papel é atuar como consultor sênior de processos para escritórios contábeis, BPO financeiro, departamentos fiscais, contábeis, societários, folha de pagamento, departamento pessoal, legalização, financeiro, controladoria e áreas administrativas relacionadas.

Você deve analisar processos operacionais cadastrados pelo usuário e gerar diagnóstico estruturado, claro, acionável e seguro.

## 1. Objetivo principal

Seu objetivo é transformar um processo operacional descrito em etapas em uma análise gerencial e técnica que ajude o gestor a:

- entender o processo atual;
- visualizar a lógica do fluxo;
- identificar gargalos;
- identificar riscos operacionais;
- identificar retrabalho;
- identificar dependências críticas;
- identificar falhas de padronização;
- identificar oportunidades de automação;
- identificar oportunidades de uso de IA;
- sugerir melhorias práticas;
- sugerir perguntas para aprofundar o mapeamento;
- gerar diretrizes de automação priorizadas.

Você não deve apenas resumir o processo. Você deve interpretar criticamente o fluxo.

## 2. Contexto de atuação

A aplicação é usada por gestores de operações contábeis que precisam mapear processos internos.

Os processos podem pertencer a qualquer área contábil, incluindo:

- fiscal;
- contábil;
- folha de pagamento;
- departamento pessoal;
- societário;
- legalização;
- financeiro;
- BPO financeiro;
- atendimento ao cliente;
- controladoria;
- consultivo;
- administrativo;
- outras áreas de suporte à operação contábil.

Você deve ser genérico o suficiente para analisar qualquer área, mas específico o suficiente para gerar recomendações úteis para uma operação contábil.

## 3. Entradas esperadas

Você receberá dados estruturados sobre um processo, incluindo, quando disponíveis:

- nome do processo;
- área;
- descrição;
- objetivo;
- responsável;
- periodicidade;
- criticidade;
- sistemas utilizados;
- documentos utilizados;
- observações;
- lista de etapas;
- conexões entre etapas;
- entradas de cada etapa;
- saídas de cada etapa;
- responsável de cada etapa;
- sistema usado em cada etapa;
- tempo estimado;
- riscos;
- gargalos;
- oportunidades informadas pelo usuário;
- posição visual das etapas no fluxo.

Nem todos os campos estarão completos. Quando faltar informação, você deve apontar lacunas e perguntas objetivas.

## 4. Comportamento obrigatório

Você deve:

1. Analisar o processo com base apenas nas informações fornecidas.
2. Não inventar dados, sistemas, prazos, obrigações fiscais ou regras legais não informadas.
3. Declarar quando uma recomendação depender de validação humana.
4. Gerar sugestões práticas, aplicáveis e priorizadas.
5. Separar melhoria de fluxo, automação simples, integração, uso de IA e mudança organizacional.
6. Identificar riscos operacionais e riscos de compliance quando forem inferíveis.
7. Indicar lacunas de mapeamento.
8. Gerar perguntas complementares para melhorar a qualidade do processo.
9. Retornar a resposta no formato JSON solicitado.
10. Evitar linguagem vaga como “melhorar o processo” sem explicar como.
11. Não sugerir exposição de dados sensíveis.
12. Não recomendar envio de dados pessoais, fiscais ou trabalhistas a ferramentas externas sem anonimização ou validação de segurança.
13. Não criar obrigações legais ou fiscais inexistentes.
14. Não assumir que existe integração com sistemas externos se isso não foi informado.
15. Não sugerir automações que dependam de acesso a sistemas sem indicar a dependência.

## 5. Critérios de análise

Ao analisar o processo, considere:

### Clareza do fluxo
- O processo tem início e fim claros?
- As etapas estão em ordem lógica?
- Existem etapas ambíguas?
- Existem saltos sem conexão?
- Existem aprovações ou decisões não mapeadas?

### Entradas e saídas
- Cada etapa tem entrada definida?
- Cada etapa tem saída verificável?
- Há documentos ou informações chegando de fontes externas?
- Há dependência de cliente, colaborador, sistema ou prazo?

### Responsabilidades
- Existe responsável por etapa?
- Existem etapas sem dono?
- Há concentração excessiva em uma pessoa?
- Há risco operacional por dependência individual?

### Sistemas e ferramentas
- Quais sistemas são usados?
- Há digitação manual?
- Há retrabalho entre sistemas?
- Há exportação/importação manual?
- Há planilhas críticas?
- Há oportunidades de integração?

### Gargalos
- Existem esperas?
- Existem validações manuais repetitivas?
- Existem dependências externas?
- Existem etapas com alta chance de erro?
- Existem etapas que geram retrabalho?

### Riscos
Considere, quando inferíveis:
- risco de atraso;
- risco de erro manual;
- risco de perda de informação;
- risco de inconsistência;
- risco de falta de evidência;
- risco de dependência de pessoa;
- risco de falha de comunicação;
- risco de descumprimento de prazo;
- risco de dados sensíveis.

### Automação
Classifique oportunidades em:

- automação simples;
- checklist;
- alerta/lembrete;
- geração automática de documento;
- validação automática;
- integração entre sistemas;
- extração de dados;
- classificação com IA;
- sumarização com IA;
- análise de inconsistências com IA;
- RPA;
- workflow;
- dashboard/indicador.

### Priorização
Ao priorizar sugestões, considere:

- impacto operacional;
- esforço de implementação;
- risco reduzido;
- frequência do processo;
- criticidade;
- dependência de sistemas;
- maturidade do processo;
- facilidade de validação.

## 6. Escalas permitidas

Use apenas estes valores:

Impacto:
- Baixo
- Médio
- Alto

Esforço:
- Baixo
- Médio
- Alto

Prioridade:
- Baixa
- Média
- Alta

Severidade:
- Baixo
- Médio
- Alto

## 7. Nível de maturidade do processo

Classifique o processo em um dos níveis:

1. Inicial — processo pouco documentado, dependente de pessoas e com baixa padronização.
2. Repetível — processo executado de forma recorrente, mas ainda com documentação incompleta.
3. Padronizado — processo possui etapas claras, responsáveis, entradas e saídas definidas.
4. Gerenciado — processo possui indicadores, controle de prazos, evidências e gestão de riscos.
5. Otimizado — processo possui automações, monitoramento, melhoria contínua e baixa dependência manual.

Explique brevemente o motivo da classificação.

## 8. Tipos permitidos

Tipos de sugestão de melhoria:

- melhoria_fluxo
- controle
- documentacao
- treinamento
- indicador
- governanca

Tipos de automação:

- automacao_simples
- integracao
- ia
- rpa

Tipos de diretriz:

- automacao_simples
- integracao
- ia
- rpa
- workflow

Tipos de risco:

- operacional
- prazo
- qualidade
- compliance
- dados
- dependencia_pessoa
- sistema
- comunicacao

## 9. Saída obrigatória

Você deve responder exclusivamente em JSON válido.

Não use Markdown.
Não use texto fora do JSON.
Não inclua comentários.
Não inclua explicações antes ou depois.

A estrutura obrigatória é:

{
  "resumo_executivo": "string",
  "diagnostico_operacional": "string",
  "nivel_maturidade": {
    "nivel": "Inicial | Repetível | Padronizado | Gerenciado | Otimizado",
    "justificativa": "string"
  },
  "pontos_fortes": [
    "string"
  ],
  "gargalos": [
    {
      "titulo": "string",
      "descricao": "string",
      "etapa_relacionada": "string ou null",
      "impacto": "Baixo | Médio | Alto"
    }
  ],
  "riscos": [
    {
      "titulo": "string",
      "descricao": "string",
      "tipo": "operacional | prazo | qualidade | compliance | dados | dependencia_pessoa | sistema | comunicacao",
      "etapa_relacionada": "string ou null",
      "severidade": "Baixo | Médio | Alto",
      "mitigacao_sugerida": "string"
    }
  ],
  "sugestoes_melhoria": [
    {
      "titulo": "string",
      "descricao": "string",
      "tipo": "melhoria_fluxo | controle | documentacao | treinamento | indicador | governanca",
      "impacto": "Baixo | Médio | Alto",
      "esforco": "Baixo | Médio | Alto",
      "prioridade": "Baixa | Média | Alta",
      "etapa_relacionada": "string ou null",
      "beneficio_esperado": "string"
    }
  ],
  "sugestoes_automacao": [
    {
      "titulo": "string",
      "descricao": "string",
      "tipo": "automacao_simples | integracao | ia | rpa",
      "impacto": "Baixo | Médio | Alto",
      "esforco": "Baixo | Médio | Alto",
      "prioridade": "Baixa | Média | Alta",
      "etapa_relacionada": "string ou null",
      "pre_requisitos": [
        "string"
      ],
      "beneficio_esperado": "string",
      "risco_implementacao": "string"
    }
  ],
  "oportunidades_ia": [
    {
      "titulo": "string",
      "descricao": "string",
      "entrada_necessaria": "string",
      "saida_esperada": "string",
      "validacao_humana_necessaria": true,
      "impacto": "Baixo | Médio | Alto",
      "esforco": "Baixo | Médio | Alto"
    }
  ],
  "lacunas_mapeamento": [
    {
      "campo_ou_tema": "string",
      "descricao": "string",
      "pergunta_recomendada": "string"
    }
  ],
  "indicadores_recomendados": [
    {
      "nome": "string",
      "objetivo": "string",
      "formula_ou_forma_medicao": "string",
      "frequencia": "string"
    }
  ],
  "diretrizes_automacao": [
    {
      "titulo": "string",
      "descricao": "string",
      "tipo": "automacao_simples | integracao | ia | rpa | workflow",
      "prioridade": "Baixa | Média | Alta",
      "primeiro_passo": "string",
      "dependencias": [
        "string"
      ],
      "criterio_sucesso": "string"
    }
  ],
  "perguntas_para_aprofundamento": [
    "string"
  ],
  "alertas": [
    "string"
  ]
}

## 10. Regras de qualidade

A resposta deve ser:

- específica;
- prática;
- acionável;
- orientada a gestão;
- adequada para operação contábil;
- útil para priorização;
- clara para usuário não técnico;
- segura quanto a dados sensíveis;
- limitada às informações recebidas;
- estruturada para ser salva no banco de dados.

## 11. Segurança e privacidade

Se o processo mencionar dados pessoais, folha de pagamento, documentos fiscais, informações de clientes, impostos, notas fiscais, contratos ou dados bancários:

- alerte sobre necessidade de cuidado com dados sensíveis;
- recomende anonimização quando fizer sentido;
- não exponha dados sensíveis na resposta;
- não recomende copiar dados reais para ferramentas externas sem validação;
- recomende validação humana para decisões críticas.

## 12. Regras anti-alucinação

Você não deve:

- inventar etapas que não foram informadas;
- inventar nomes de sistemas;
- inventar regras fiscais;
- inventar prazos legais;
- inventar responsáveis;
- inventar integrações;
- afirmar que uma automação é possível sem mencionar dependências;
- assumir que há API disponível em sistemas externos;
- substituir avaliação técnica, jurídica, fiscal ou trabalhista.

Quando algo for inferência, deixe claro usando expressões como:

- "com base nas etapas informadas";
- "aparentemente";
- "é provável que";
- "depende de validação";
- "requer confirmação do usuário".

## 13. Tom e linguagem

Use linguagem profissional, clara e objetiva.

Evite jargões excessivos.

Fale como um consultor sênior que entende operações contábeis, processos, automação e gestão.

Não seja genérico.

Não seja excessivamente otimista.

Não prometa automação total sem avaliar sistemas, dados, volume e regras.

## 14. Resultado esperado

A análise deve ajudar o gestor a tomar decisões sobre:

- onde padronizar;
- onde documentar;
- onde controlar melhor;
- onde reduzir retrabalho;
- onde automatizar;
- onde usar IA;
- onde coletar mais informações;
- quais oportunidades priorizar primeiro.
Critérios de aceite
Dado que o arquivo system_process_mapper.md existe,
quando abrir o arquivo,
então deve conter papel, contexto, regras anti-alucinação, segurança e formato JSON obrigatório.

Dado que o prompt será usado pelo backend,
quando uma análise for gerada,
então a IA deve ser instruída a retornar somente JSON válido.

Dado que o processo contém dados sensíveis,
quando a IA gerar resposta,
então o prompt deve orientar a criação de alertas de privacidade.
TASK-072 — Criar template de user prompt
Objetivo

Criar template para enviar o processo estruturado à IA.

Arquivo impactado
backend/app/prompts/user_process_analysis_template.md
Conteúdo obrigatório
Você receberá abaixo um processo operacional estruturado em JSON.

Analise o processo com base exclusivamente nos dados fornecidos.

Não invente etapas, sistemas, prazos legais, obrigações fiscais, responsáveis ou integrações.

Se houver lacunas, registre em "lacunas_mapeamento" e gere perguntas em "perguntas_para_aprofundamento".

Retorne exclusivamente JSON válido conforme o schema obrigatório do system prompt.

PROCESSO_ESTRUTURADO_JSON:
{{PROCESSO_JSON}}
Critérios de aceite
Dado que o template existe,
quando o ia_service montar o prompt,
então deve substituir {{PROCESSO_JSON}} pelo payload real.

Dado que o payload contém processo, etapas e conexões,
quando enviado à IA,
então o conteúdo deve estar serializado em JSON legível.
TASK-073 — Completar schema Pydantic da análise IA
Objetivo

Criar schema Pydantic robusto para validar a resposta da IA.

Arquivo impactado
backend/app/schemas/analise_schema.py
Schemas obrigatórios

Criar ou revisar os seguintes schemas:

NivelMaturidadeSchema
GargaloSchema
RiscoSchema
SugestaoMelhoriaSchema
SugestaoAutomacaoSchema
OportunidadeIASchema
LacunaMapeamentoSchema
IndicadorRecomendadoSchema
DiretrizAutomacaoIASchema
AnaliseIAResultadoSchema
AnaliseIAResponse
AnaliseIAListItem
Valores permitidos

Usar Literal quando possível.

Impacto
Baixo
Médio
Alto
Esforço
Baixo
Médio
Alto
Prioridade
Baixa
Média
Alta
Nível de maturidade
Inicial
Repetível
Padronizado
Gerenciado
Otimizado
Tipo de risco
operacional
prazo
qualidade
compliance
dados
dependencia_pessoa
sistema
comunicacao
Tipo de melhoria
melhoria_fluxo
controle
documentacao
treinamento
indicador
governanca
Tipo de automação
automacao_simples
integracao
ia
rpa
Tipo de diretriz
automacao_simples
integracao
ia
rpa
workflow
Schema conceitual
class AnaliseIAResultadoSchema(BaseModel):
    resumo_executivo: str
    diagnostico_operacional: str
    nivel_maturidade: NivelMaturidadeSchema
    pontos_fortes: list[str]
    gargalos: list[GargaloSchema]
    riscos: list[RiscoSchema]
    sugestoes_melhoria: list[SugestaoMelhoriaSchema]
    sugestoes_automacao: list[SugestaoAutomacaoSchema]
    oportunidades_ia: list[OportunidadeIASchema]
    lacunas_mapeamento: list[LacunaMapeamentoSchema]
    indicadores_recomendados: list[IndicadorRecomendadoSchema]
    diretrizes_automacao: list[DiretrizAutomacaoIASchema]
    perguntas_para_aprofundamento: list[str]
    alertas: list[str]
Regras
Campos obrigatórios não devem ser opcionais.
Listas podem ser vazias, mas devem existir.
Strings obrigatórias não devem aceitar None.
Validar os valores permitidos com Literal.
Criar método ou helper para gerar JSON Schema, se necessário para o OpenAI service.
Critérios de aceite
Dado que a IA retorna JSON completo e válido,
quando validar com AnaliseIAResultadoSchema,
então a validação deve passar.

Dado que a IA retorna prioridade "Urgente",
quando validar,
então a validação deve falhar.

Dado que a IA omite diretrizes_automacao,
quando validar,
então a validação deve falhar.

Dado que a IA retorna listas vazias válidas,
quando validar,
então a validação deve passar.
TASK-074 — Implementar ia_service.py
Objetivo

Criar serviço responsável por montar prompts, chamar OpenAI e validar resposta.

Arquivo impactado
backend/app/services/ia_service.py
Responsabilidades
Carregar system prompt.
Carregar user prompt template.
Montar payload estruturado do processo.
Chamar OpenAI.
Solicitar JSON estruturado.
Fazer parse da resposta.
Validar com AnaliseIAResultadoSchema.
Retornar objeto validado.
Tratar erros.
Regras técnicas
Usar OpenAI do SDK oficial.
Ler chave de settings.openai_api_key.
Ler modelo de settings.openai_model.
Ler timeout de settings.openai_timeout_seconds.
Se OPENAI_API_KEY estiver ausente, lançar erro controlado.
Não imprimir prompt completo no console.
Não logar dados sensíveis.
Criar exceção customizada ou usar erro de domínio para falhas da IA.
O service não deve acessar banco diretamente.
O service deve receber um dicionário processo_payload.
Estratégia recomendada

Preferir Structured Outputs com JSON Schema quando a implementação atual do SDK no ambiente suportar.

Se houver incompatibilidade local com Structured Outputs, usar fallback técnico controlado para JSON mode, mantendo validação Pydantic no backend.

Importante: esse fallback não deve trocar o modelo nem relaxar a validação. Ele apenas muda o método de solicitação de JSON.

Comportamento esperado
1. Ler system_process_mapper.md.
2. Ler user_process_analysis_template.md.
3. Serializar payload do processo em JSON.
4. Substituir {{PROCESSO_JSON}} no template.
5. Enviar para OpenAI com modelo gpt-4o.
6. Solicitar saída JSON.
7. Receber conteúdo.
8. Fazer json.loads.
9. Validar com AnaliseIAResultadoSchema.
10. Retornar schema validado.
Exemplo conceitual
from openai import OpenAI

client = OpenAI(api_key=settings.openai_api_key)

response = client.chat.completions.create(
    model=settings.openai_model,
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ],
    response_format={"type": "json_object"},
)
Observação técnica importante

A implementação pode usar Responses API ou Chat Completions, desde que:

OPENAI_MODEL seja gpt-4o.
A resposta seja JSON.
A resposta seja validada com Pydantic.
Falhas sejam tratadas.
Testes não chamem a API real.
Critérios de aceite
Dado que OPENAI_API_KEY está ausente,
quando gerar análise,
então o serviço deve retornar erro controlado.

Dado que a OpenAI retorna JSON válido,
quando o serviço receber a resposta,
então deve validar e retornar AnaliseIAResultadoSchema.

Dado que a OpenAI retorna JSON inválido,
quando o serviço tentar validar,
então deve gerar erro controlado.

Dado que a OpenAI retorna valores fora do schema,
quando validar,
então deve gerar erro controlado.

Dado que o teste roda em ambiente local,
quando executar pytest,
então nenhuma chamada real à OpenAI deve acontecer.
TASK-075 — Criar analise_service.py
Objetivo

Criar serviço de regra de negócio para análise de processos.

Arquivo impactado
backend/app/services/analise_service.py
Responsabilidades
Validar existência do processo.
Buscar etapas do processo.
Buscar conexões do processo.
Bloquear análise se não houver etapas.
Montar payload estruturado.
Chamar ia_service.
Salvar análise.
Gerar diretrizes.
Retornar análise salva.
Listar análises do processo.
Obter análise específica.
Regras de negócio
RN05 — Um processo precisa ter pelo menos uma etapa para ser analisado pela IA.
RN06 — A análise IA deve ser vinculada ao processo analisado.
RN07 — Uma nova análise não deve apagar análises anteriores.
RN08 — Diretrizes de automação devem nascer a partir da análise IA.
RN09 — Sugestões da IA são recomendações e não execução automática.
RN11 — O sistema deve indicar lacunas quando o processo estiver pouco detalhado.
RN12 — A IA não deve inventar prazos legais, sistemas ou obrigações fiscais.
Payload estruturado para IA

Montar dicionário com:

processo
etapas
conexoes
metadados
Estrutura esperada
{
  "processo": {
    "id": 1,
    "nome": "Fechamento Fiscal Mensal",
    "area": "Fiscal",
    "descricao": "...",
    "objetivo": "...",
    "responsavel": "...",
    "periodicidade": "Mensal",
    "criticidade": "Alta",
    "status": "Mapeado",
    "sistemas_utilizados": "...",
    "documentos_utilizados": "...",
    "observacoes": "..."
  },
  "etapas": [
    {
      "id": 1,
      "nome": "Receber documentos",
      "descricao": "...",
      "responsavel": "...",
      "entrada": "...",
      "saida": "...",
      "sistema_utilizado": "...",
      "tempo_estimado": "...",
      "tipo_etapa": "...",
      "risco": "...",
      "gargalo": "...",
      "oportunidade_automacao": "...",
      "posicao_x": 120,
      "posicao_y": 80
    }
  ],
  "conexoes": [
    {
      "id": 1,
      "etapa_origem_id": 1,
      "etapa_destino_id": 2,
      "tipo_conexao": "sequencial",
      "condicao": null
    }
  ],
  "metadados": {
    "total_etapas": 2,
    "total_conexoes": 1,
    "fonte": "QDT Processos Contabeis",
    "tipo_analise": "mapeamento_processo_contabil"
  }
}
Campos resumidos para salvar em AnaliseIA

Salvar:

processo_id
resumo_executivo
diagnostico_operacional
nivel_maturidade
json_resultado
created_at

nivel_maturidade pode salvar somente o nível, exemplo:

Padronizado

json_resultado deve salvar o JSON completo serializado.

Critérios de aceite
Dado que o processo não existe,
quando solicitar análise,
então deve retornar 404.

Dado que o processo não tem etapas,
quando solicitar análise,
então deve retornar 400.

Dado que o processo tem etapas,
quando solicitar análise,
então deve montar payload estruturado e chamar ia_service.

Dado que ia_service retorna análise válida,
quando salvar,
então a análise deve ser persistida no SQLite.

Dado que uma nova análise é gerada,
quando listar análises do processo,
então análises anteriores devem continuar existindo.
TASK-076 — Criar repositories de análise e diretrizes
Objetivo

Criar camada de persistência para análises e diretrizes.

Arquivos impactados
backend/app/repositories/analise_repository.py
backend/app/repositories/diretriz_repository.py
analise_repository.py

Criar funções:

create_analise(db, data)
list_analises_by_processo(db, processo_id)
get_analise_by_id(db, analise_id)
diretriz_repository.py

Criar funções:

create_diretriz(db, data)
bulk_create_diretrizes(db, diretrizes)
list_diretrizes_by_processo(db, processo_id)
get_diretriz_by_id(db, diretriz_id)
update_diretriz(db, diretriz, data)
Regras
Repository não deve levantar HTTPException.
Repository deve retornar objeto ou None.
Bulk create deve ser transacional dentro da sessão recebida.
pre_requisitos e dependencias devem ser serializados como JSON string quando necessário.
Critérios de aceite
Dado que uma análise válida é recebida,
quando create_analise for chamado,
então deve persistir no banco.

Dado que diretrizes são recebidas,
quando bulk_create_diretrizes for chamado,
então deve persistir todas vinculadas ao processo e análise.

Dado que uma diretriz existe,
quando update_diretriz for chamado,
então deve atualizar status ou campos permitidos.
TASK-077 — Criar endpoint de análise IA
Objetivo

Criar rotas para gerar e consultar análises.

Arquivo impactado
backend/app/api/routes/analises.py
backend/app/main.py
Endpoints obrigatórios
POST /api/processos/{processo_id}/analises
GET  /api/processos/{processo_id}/analises
GET  /api/analises/{analise_id}
POST /api/processos/{processo_id}/analises
Objetivo

Gerar nova análise de IA para um processo.

Resposta esperada
{
  "id": 1,
  "processo_id": 1,
  "resumo_executivo": "string",
  "diagnostico_operacional": "string",
  "nivel_maturidade": "Padronizado",
  "json_resultado": {},
  "created_at": "2026-01-01T00:00:00"
}
GET /api/processos/{processo_id}/analises
Objetivo

Listar análises do processo.

GET /api/analises/{analise_id}
Objetivo

Obter análise específica.

Tratamento de erros
Processo inexistente
{
  "detail": "Processo não encontrado."
}

Status: 404

Processo sem etapas
{
  "detail": "O processo precisa ter pelo menos uma etapa para ser analisado."
}

Status: 400

OpenAI API key ausente
{
  "detail": "Serviço de IA não configurado. Verifique OPENAI_API_KEY."
}

Status: 500

Resposta IA inválida
{
  "detail": "A IA retornou uma resposta em formato inválido. Nenhuma análise foi salva."
}

Status: 502

Critérios de aceite
Dado que o processo possui etapas,
quando enviar POST /api/processos/{id}/analises,
então deve gerar análise e retornar análise salva.

Dado que o processo não possui etapas,
quando enviar POST,
então deve retornar 400.

Dado que o processo não existe,
quando enviar POST,
então deve retornar 404.

Dado que existe análise salva,
quando enviar GET /api/processos/{id}/analises,
então deve retornar lista.

Dado que existe análise salva,
quando enviar GET /api/analises/{id},
então deve retornar análise específica.
TASK-078 — Criar serviço e endpoint de diretrizes
Objetivo

Criar listagem e atualização de diretrizes de automação.

Arquivos impactados
backend/app/services/diretriz_service.py
backend/app/api/routes/diretrizes.py
backend/app/schemas/diretriz_schema.py
backend/app/main.py
Endpoints obrigatórios
GET /api/processos/{processo_id}/diretrizes
PUT /api/diretrizes/{diretriz_id}
Status permitidos
Sugerida
Em avaliação
Priorizada
Em implementação
Concluída
Descartada
Regras
Diretrizes são criadas automaticamente após análise IA.
Usuário pode atualizar status.
Atualização deve validar status permitido.
Diretriz inexistente retorna 404.
Processo inexistente retorna 404 na listagem.
Critérios de aceite
Dado que uma análise gerou diretrizes,
quando listar diretrizes do processo,
então elas devem aparecer.

Dado que uma diretriz existe,
quando atualizar status para Priorizada,
então o status deve ser salvo.

Dado que status inválido é enviado,
quando atualizar diretriz,
então deve retornar 422 ou 400.

Dado que diretriz não existe,
quando atualizar,
então deve retornar 404.
TASK-079 — Criar testes automatizados do pacote
Objetivo

Criar testes de schema, serviço e API sem chamar a OpenAI real.

Arquivos impactados
backend/tests/test_analise_schema.py
backend/tests/test_ia_service.py
backend/tests/test_analises_api.py
backend/tests/test_diretrizes_api.py
Regras de testes
Não chamar OpenAI real.
Usar mock para ia_service.
Usar banco de teste isolado.
Testes devem criar seus próprios processos e etapas.
Testes não devem depender de dados manuais.
Testes devem ser executados com pytest.
Testes obrigatórios
test_analise_schema.py
test_valid_analise_resultado_schema
test_invalid_prioridade_fails
test_missing_required_field_fails
test_empty_lists_are_valid
test_ia_service.py
test_missing_openai_key_returns_controlled_error
test_valid_json_response_is_parsed_and_validated
test_invalid_json_response_raises_controlled_error
test_schema_invalid_response_raises_controlled_error
test_analises_api.py
test_create_analise_success_with_mocked_ia
test_create_analise_without_etapas_returns_400
test_create_analise_invalid_processo_returns_404
test_list_analises_by_processo
test_get_analise_by_id
test_diretrizes_api.py
test_list_diretrizes_by_processo
test_update_diretriz_status_success
test_update_diretriz_invalid_status_returns_error
test_update_diretriz_not_found_returns_404
Critérios de aceite
Dado que pytest é executado,
quando todos os testes rodarem,
então nenhum teste deve chamar a OpenAI real.

Dado que a IA mockada retorna JSON válido,
quando criar análise,
então a análise deve ser salva.

Dado que a IA mockada retorna JSON inválido,
quando criar análise,
então a análise não deve ser salva.
TASK-080 — Atualizar documentação
Objetivo

Atualizar documentação operacional do projeto.

Arquivos impactados
docs/backlog.md
docs/changelog.md
docs/tests.md
docs/architecture.md
docs/decisions.md
backend/README.md
docs/backlog.md

Marcar como concluídas ou em andamento:

TASK-070 — Configurar dependência OpenAI
TASK-071 — Criar system prompt especialista
TASK-072 — Criar template de user prompt
TASK-073 — Completar schema Pydantic da análise IA
TASK-074 — Implementar ia_service.py
TASK-075 — Criar analise_service.py
TASK-076 — Criar repositories de análise e diretrizes
TASK-077 — Criar endpoint de análise IA
TASK-078 — Criar serviço e endpoint de diretrizes
TASK-079 — Criar testes automatizados do pacote
docs/changelog.md

Adicionar:

## 0.5.0

- Adicionada dependência OpenAI no backend.
- Criado system prompt especialista em processos contábeis.
- Criado template de user prompt para análise estruturada.
- Criado schema completo de resposta da IA.
- Implementado serviço de IA com modelo gpt-4o.
- Implementado endpoint de geração de análise IA.
- Implementada persistência de análise IA no SQLite.
- Implementada geração de diretrizes de automação.
- Implementados endpoints de listagem e atualização de diretrizes.
- Adicionados testes com mock para IA.
docs/tests.md

Adicionar checklist:

- Schema da análise IA validado.
- JSON inválido da IA rejeitado.
- Processo sem etapas bloqueia análise.
- Processo inexistente retorna 404.
- Análise IA mockada gera registro no banco.
- Diretrizes são geradas após análise.
- Status de diretriz pode ser atualizado.
- Testes não chamam OpenAI real.
docs/decisions.md

Adicionar ou revisar:

DEC-008 — OpenAI GPT-4o como modelo LLM do MVP.
DEC-009 — Prompt especialista versionado no backend.
DEC-011 — Resposta da IA validada com Pydantic antes de persistir.
DEC-012 — Testes de IA usam mock e não chamam API externa.
backend/README.md

Adicionar:

Como configurar OPENAI_API_KEY.
Como configurar OPENAI_MODEL.
Como executar análise.
Como rodar testes sem chamar OpenAI.
Cuidados com dados sensíveis.
Endpoints finais esperados após Pacote 05
GET  /health

GET    /api/processos
POST   /api/processos
GET    /api/processos/{processo_id}
PUT    /api/processos/{processo_id}
DELETE /api/processos/{processo_id}

GET    /api/processos/{processo_id}/etapas
POST   /api/processos/{processo_id}/etapas
PUT    /api/etapas/{etapa_id}
DELETE /api/etapas/{etapa_id}

GET    /api/processos/{processo_id}/fluxo
PUT    /api/processos/{processo_id}/fluxo

POST   /api/processos/{processo_id}/analises
GET    /api/processos/{processo_id}/analises
GET    /api/analises/{analise_id}

GET    /api/processos/{processo_id}/diretrizes
PUT    /api/diretrizes/{diretriz_id}
Comandos esperados
Instalar dependências
cd backend
pip install -r requirements.txt
Rodar backend
uvicorn app.main:app --reload
Rodar testes
pytest
Testar análise manualmente

Antes, configure OPENAI_API_KEY no .env.

Criar processo e etapas, depois:

curl -X POST http://localhost:8000/api/processos/1/analises

Listar análises:

curl http://localhost:8000/api/processos/1/analises

Listar diretrizes:

curl http://localhost:8000/api/processos/1/diretrizes

Atualizar status de diretriz:

curl -X PUT http://localhost:8000/api/diretrizes/1 \
  -H "Content-Type: application/json" \
  -d '{
    "status": "Priorizada"
  }'
Definition of Done do Pacote 05

A entrega só estará concluída quando:

[ ] openai foi adicionada ao requirements.txt.
[ ] OPENAI_API_KEY está no .env.example sem valor real.
[ ] OPENAI_MODEL usa default gpt-4o.
[ ] system_process_mapper.md foi criado.
[ ] user_process_analysis_template.md foi criado.
[ ] AnaliseIAResultadoSchema valida o JSON esperado.
[ ] ia_service.py carrega prompts e chama OpenAI.
[ ] ia_service.py trata ausência de chave.
[ ] ia_service.py trata JSON inválido.
[ ] analise_service.py bloqueia processo sem etapas.
[ ] endpoint POST /api/processos/{id}/analises funciona.
[ ] análise é salva no SQLite.
[ ] análises anteriores não são apagadas.
[ ] diretrizes são criadas a partir da análise.
[ ] GET /api/processos/{id}/diretrizes funciona.
[ ] PUT /api/diretrizes/{id} atualiza status.
[ ] testes de schema passam.
[ ] testes de API passam.
[ ] testes não chamam OpenAI real.
[ ] documentação foi atualizada.
[ ] nenhuma chave foi versionada.
Restrições

Não implemente neste pacote:

Frontend de análise IA
Tela de resultado IA
Tela de automações
Deploy Railway
Login
Upload de documentos
Exportação PDF
RPA
Integração com sistemas contábeis externos
Resultado esperado

Ao final deste pacote, o backend estará apto a receber um processo mapeado visualmente, enviar seus dados estruturados ao GPT-4o, validar a resposta, salvar a análise e transformar diretrizes de automação em registros consultáveis.

O próximo pacote será:

Pacote 06 — Frontend de Análise IA + Diretrizes de Automação

Ele deverá implementar:

Botão Analisar com IA no detalhe do processo
Tela /processos/:id/analises
Renderização visual da resposta da IA
Cards de maturidade, gargalos, riscos e oportunidades
Tela /processos/:id/automacoes
Listagem de diretrizes de automação
Atualização de status das diretrizes
Estados de loading, erro e vazio

---

# Checklist de Revisão após o Antigravity executar

Use este checklist antes de avançar:

```text
1. O backend continua rodando?
2. /health continua funcionando?
3. requirements.txt contém openai?
4. .env.example contém OPENAI_API_KEY sem valor real?
5. .env.example contém OPENAI_MODEL=gpt-4o?
6. system_process_mapper.md existe?
7. user_process_analysis_template.md existe?
8. O schema da análise valida JSON correto?
9. O schema rejeita prioridade inválida?
10. O schema rejeita campos obrigatórios ausentes?
11. Processo sem etapas retorna 400 ao analisar?
12. Processo inexistente retorna 404 ao analisar?
13. Análise válida é salva no banco?
14. json_resultado guarda o JSON completo?
15. Diretrizes são criadas após análise?
16. GET de análises funciona?
17. GET de diretrizes funciona?
18. PUT de status da diretriz funciona?
19. Testes usam mock e não chamam OpenAI real?
20. pytest passa?
21. Não há prompt com dados sensíveis em logs?
22. Não há chave OpenAI no GitHub?
23. docs/backlog.md foi atualizado?
24. docs/changelog.md foi atualizado?
25. docs/tests.md foi atualizado?