TASK-000 — Criar monorepo base
Objetivo

Criar a estrutura raiz do projeto com /frontend, /backend, /docs, .gitignore e README.md.

Critérios de aceite
A raiz deve conter /frontend, /backend e /docs.
.gitignore deve ignorar:
.env
.venv
__pycache__/
.pytest_cache/
node_modules/
arquivos SQLite locais *.db, *.sqlite, *.sqlite3
logs
O arquivo README.md da raiz deve conter:
nome do projeto;
objetivo;
stack;
estrutura de pastas;
status atual.
TASK-001 — Criar documentação base
Objetivo

Criar os documentos operacionais do projeto em /docs.

Arquivos obrigatórios
docs/vision.md
docs/requirements.md
docs/spec.md
docs/architecture.md
docs/backlog.md
docs/decisions.md
docs/tests.md
docs/deployment.md
docs/changelog.md
Conteúdo mínimo
docs/vision.md

Deve conter:

problema;
objetivo;
público-alvo;
proposta de valor;
escopo inicial;
fora de escopo.
docs/requirements.md

Deve conter:

requisitos funcionais RF01 a RF22;
requisitos não funcionais RNF01 a RNF14;
regras de negócio RN01 a RN12.
docs/spec.md

Deve conter:

telas previstas;
entradas;
saídas;
fluxos;
exceções;
critérios gerais de aceite.
docs/architecture.md

Deve conter:

stack;
arquitetura geral;
estrutura de pastas;
modelo de dados;
endpoints previstos;
riscos técnicos.
docs/backlog.md

Deve conter:

épicos;
tasks;
prioridade;
status.
docs/decisions.md

Registrar:

DEC-001: MVP sem login.
DEC-002: escopo genérico para operação contábil.
DEC-003: frontend SaaS moderno.
DEC-004: backend FastAPI.
DEC-005: SQLite.
DEC-006: Railway.
DEC-007: GitHub.
DEC-008: OpenAI GPT-4o.
DEC-009: prompt especialista versionado.
DEC-010: React Flow.
docs/tests.md

Deve conter checklist mínimo:

health check;
criação de processo;
validação de processo sem nome;
criação de etapa;
validação de etapa sem nome;
persistência SQLite;
validação de schema.
docs/deployment.md

Deve conter:

Railway;
variáveis de ambiente;
volume persistente;
caminho do SQLite;
comandos futuros.
docs/changelog.md

Iniciar com:

versão 0.1.0;
criação da base do projeto.
TASK-010 — Configurar FastAPI
Objetivo

Criar backend FastAPI funcional com rota /health.

Arquivos impactados
backend/app/main.py
backend/app/core/config.py
backend/requirements.txt
backend/.env.example
backend/README.md
Dependências em requirements.txt

Usar versões compatíveis estáveis, sem fixar versões se não for necessário:

fastapi
uvicorn[standard]
sqlalchemy
pydantic
pydantic-settings
python-dotenv
pytest
httpx
Configuração esperada

Criar backend/app/core/config.py com classe de settings baseada em pydantic-settings.

Variáveis esperadas:

APP_NAME=QDT Processos Contabeis API
APP_ENV=development
DATABASE_URL=sqlite:///./data/qdt_processos.db
CORS_ORIGINS=http://localhost:5173
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o

Mesmo que OpenAI não seja implementada neste pacote, deixar variáveis previstas no .env.example.

Endpoint obrigatório
GET /health

Resposta:

{
  "status": "ok",
  "service": "qdt-backend"
}
Critérios de aceite
Rodar o backend com uvicorn app.main:app --reload.
Acessar http://localhost:8000/health.
Retornar JSON com status: ok.
Não haver erro de importação.
TASK-011 — Configurar SQLite com SQLAlchemy
Objetivo

Criar camada de banco com SQLite e SQLAlchemy.

Arquivos impactados
backend/app/database/session.py
backend/app/database/base.py
backend/app/main.py
backend/app/core/config.py
Regras técnicas
Usar DATABASE_URL.
Criar engine SQLAlchemy.
Criar SessionLocal.
Criar Base = declarative_base().
Criar função de dependência get_db().
Criar função init_db().
Garantir criação do diretório data/ quando o banco for SQLite local.
Não usar Alembic neste pacote.
Não criar banco em pasta temporária.
Para Railway, o caminho previsto será sqlite:////app/data/qdt_processos.db.
Critérios de aceite
Ao iniciar backend, se data/ não existir, deve ser criado.
Ao iniciar backend, se tabelas não existirem, devem ser criadas.
O backend deve continuar respondendo /health.
TASK-012 — Criar modelos SQLAlchemy
Objetivo

Criar modelos de dados do MVP.

Arquivos impactados
backend/app/models/processo.py
backend/app/models/etapa.py
backend/app/models/conexao.py
backend/app/models/analise.py
backend/app/models/diretriz.py
backend/app/models/__init__.py
backend/app/database/base.py
Modelo: Processo

Tabela: processos

Campos:

id INTEGER PRIMARY KEY
nome TEXT NOT NULL
area TEXT NOT NULL
descricao TEXT
objetivo TEXT
responsavel TEXT
periodicidade TEXT
criticidade TEXT
status TEXT
sistemas_utilizados TEXT
documentos_utilizados TEXT
observacoes TEXT
created_at DATETIME
updated_at DATETIME

Relacionamentos:

um processo possui muitas etapas;
um processo possui muitas conexões;
um processo possui muitas análises;
um processo possui muitas diretrizes.
Modelo: Etapa

Tabela: etapas

Campos:

id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
nome TEXT NOT NULL
descricao TEXT
responsavel TEXT
entrada TEXT
saida TEXT
sistema_utilizado TEXT
tempo_estimado TEXT
tipo_etapa TEXT
risco TEXT
gargalo TEXT
oportunidade_automacao TEXT
posicao_x REAL
posicao_y REAL
created_at DATETIME
updated_at DATETIME

Relacionamentos:

etapa pertence a um processo;
etapa pode ser origem ou destino de conexões.
Modelo: Conexao

Tabela: conexoes

Campos:

id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
etapa_origem_id INTEGER NOT NULL
etapa_destino_id INTEGER NOT NULL
tipo_conexao TEXT
condicao TEXT
created_at DATETIME

Regras:

etapa_origem_id e etapa_destino_id devem apontar para etapas existentes.
Conexões devem estar ligadas a um processo.
Modelo: AnaliseIA

Tabela: analises_ia

Campos:

id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
resumo_executivo TEXT
diagnostico_operacional TEXT
nivel_maturidade TEXT
json_resultado TEXT NOT NULL
created_at DATETIME
Modelo: DiretrizAutomacao

Tabela: diretrizes_automacao

Campos:

id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
analise_id INTEGER
titulo TEXT NOT NULL
tipo TEXT
descricao TEXT
impacto TEXT
esforco TEXT
prioridade TEXT
status TEXT
pre_requisitos TEXT
created_at DATETIME
updated_at DATETIME
Regras gerais
Usar datetime.utcnow ou equivalente para timestamps.
Usar cascade adequado para excluir etapas, conexões, análises e diretrizes ao excluir processo.
Evitar lógica de negócio dentro dos models.
Importar todos os models em models/__init__.py para criação das tabelas.
Critérios de aceite
Ao iniciar a API, as tabelas devem ser criadas no SQLite.
O arquivo .db deve aparecer em backend/data/qdt_processos.db no ambiente local.
Não deve haver erro de relacionamento SQLAlchemy.
TASK-013 — Criar schemas Pydantic
Objetivo

Criar schemas de validação para API.

Arquivos impactados
backend/app/schemas/processo_schema.py
backend/app/schemas/etapa_schema.py
backend/app/schemas/fluxo_schema.py
backend/app/schemas/analise_schema.py
backend/app/schemas/diretriz_schema.py
Schemas de Processo

Criar:

ProcessoBase
ProcessoCreate
ProcessoUpdate
ProcessoResponse

Regras:

nome obrigatório em create.
area obrigatório em create.
update deve permitir parcial.
Schemas de Etapa

Criar:

EtapaBase
EtapaCreate
EtapaUpdate
EtapaResponse

Regras:

nome obrigatório em create.
update deve permitir parcial.
Schemas de Conexao e Fluxo

Criar:

ConexaoBase
ConexaoCreate
ConexaoResponse
FluxoResponse
FluxoUpdate

FluxoResponse deve conter:

{
  "processo_id": 1,
  "etapas": [],
  "conexoes": []
}

FluxoUpdate deve aceitar:

{
  "etapas": [],
  "conexoes": []
}
Schemas de Análise IA

Criar schemas suficientes para validar a resposta futura da IA.

Criar:

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

AnaliseIAResultadoSchema deve validar os campos:

resumo_executivo
diagnostico_operacional
nivel_maturidade
pontos_fortes
gargalos
riscos
sugestoes_melhoria
sugestoes_automacao
oportunidades_ia
lacunas_mapeamento
indicadores_recomendados
diretrizes_automacao
perguntas_para_aprofundamento
alertas
Schemas de Diretriz

Criar:

DiretrizBase
DiretrizCreate
DiretrizUpdate
DiretrizResponse
Critérios de aceite
Processo sem nome deve falhar na validação.
Processo sem area deve falhar na validação.
Etapa sem nome deve falhar na validação.
JSON válido da IA deve passar em AnaliseIAResultadoSchema.
JSON inválido da IA deve falhar.
Testes obrigatórios neste pacote

Criar pelo menos:

backend/tests/test_health.py

O teste deve verificar:

GET /health retorna 200
GET /health retorna status ok
GET /health retorna service qdt-backend

Se possível, criar também:

backend/tests/test_schemas.py

Com validação de:

Processo válido;
Processo sem nome;
Processo sem área;
Etapa válida;
Etapa sem nome;
Análise IA mínima válida.
Comandos esperados
Criar ambiente virtual
cd backend
python -m venv .venv
Ativar ambiente virtual no Windows
.venv\Scripts\activate
Ativar ambiente virtual no Mac/Linux
source .venv/bin/activate
Instalar dependências
pip install -r requirements.txt
Rodar backend
uvicorn app.main:app --reload
Testar health
curl http://localhost:8000/health
Rodar testes
pytest
Definition of Done do Pacote 01

A entrega só estará concluída quando:

[ ] Estrutura monorepo criada.
[ ] `/frontend`, `/backend` e `/docs` existem.
[ ] `.gitignore` protege `.env`, `.venv`, cache, node_modules e SQLite local.
[ ] Documentos base em `/docs` criados.
[ ] FastAPI sobe localmente.
[ ] `/health` retorna status ok.
[ ] SQLite é configurado por `DATABASE_URL`.
[ ] Diretório `backend/data` é criado corretamente.
[ ] Models SQLAlchemy estão definidos.
[ ] Tabelas são criadas no SQLite.
[ ] Schemas Pydantic estão definidos.
[ ] Validações obrigatórias funcionam.
[ ] Teste de health passa.
[ ] README raiz e README backend explicam execução local.
[ ] Nenhum segredo foi versionado.
Restrições

Não implemente neste pacote:

frontend React
CRUD de processos
CRUD de etapas
API de fluxo
OpenAI
ia_service.py
system prompt
React Flow
deploy Railway
login
upload de arquivos
exportação PDF

Esses itens serão implementados nos próximos pacotes.

Resultado esperado

Ao final, o projeto deve estar pronto para avançar para o Pacote 02, que implementará:

CRUD de processos
CRUD de etapas
API de fluxo visual
repositories
services
rotas REST
testes de API

---

# Checklist de Revisão para você usar após o Antigravity executar

Depois que o Antigravity terminar, valide estes pontos:

```text
1. A pasta raiz tem frontend, backend e docs?
2. O backend roda com uvicorn app.main:app --reload?
3. O endpoint /health retorna status ok?
4. O arquivo backend/data/qdt_processos.db é criado?
5. As tabelas são criadas no SQLite?
6. Existe .env.example?
7. O .gitignore bloqueia .env e arquivos .db?
8. Os models estão separados em arquivos próprios?
9. Os schemas estão separados em arquivos próprios?
10. pytest executa pelo menos o teste de health?