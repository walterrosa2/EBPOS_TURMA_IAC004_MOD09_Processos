PRD v1.0 — QDT Processos Contábeis
1. Visão do Produto

O QDT Processos Contábeis será uma plataforma web para gestores de operações contábeis mapearem, catalogarem, visualizarem e analisarem processos internos. O sistema deverá permitir o cadastro estruturado de processos e etapas, a visualização do fluxo em formato visual interativo e a análise por IA com recomendações de melhoria, automação e uso de inteligência artificial.

O produto deve atuar como uma camada de inteligência operacional sobre os processos da empresa, ajudando o gestor a transformar conhecimento tácito em documentação, visão gerencial e backlog de automação.

2. Problema

Gestores de operações contábeis frequentemente têm dificuldade para entender, documentar e melhorar os processos internos porque:

os processos estão dispersos em pessoas, planilhas, conversas e hábitos operacionais;
há baixo nível de padronização;
muitas etapas dependem de conhecimento tácito;
gargalos, riscos e retrabalhos nem sempre estão visíveis;
oportunidades de automação são percebidas de forma informal;
a IA só gera boas recomendações quando recebe contexto estruturado.
3. Objetivo do MVP

Criar uma versão funcional da plataforma que permita:

cadastrar processos de qualquer área da operação contábil;
cadastrar etapas detalhadas;
conectar etapas visualmente;
salvar o fluxo no SQLite;
analisar o processo com OpenAI GPT-4o;
exibir diagnóstico, gargalos, riscos, melhorias e automações;
gerar diretrizes de automação acionáveis;
publicar a aplicação na Railway com GitHub como repositório.
4. Decisões Técnicas Fixadas
Código	Decisão	Descrição
DEC-001	Sem login no MVP	O MVP não terá autenticação. Uso em ambiente controlado.
DEC-002	Escopo genérico	O sistema deve servir para qualquer área da operação contábil.
DEC-003	Visual SaaS moderno	Interface em React com layout dashboard.
DEC-004	Backend Python/FastAPI	API responsável por regras, banco e IA.
DEC-005	Banco SQLite	Persistência inicial em SQLite.
DEC-006	Deploy Railway	Frontend e backend serão hospedados na Railway.
DEC-007	GitHub	Repositório único em modelo monorepo.
DEC-008	LLM OpenAI GPT-4o	Análise de processos via modelo gpt-4o.
DEC-009	Prompt especialista versionado	System prompt salvo em arquivo próprio no backend.
DEC-010	React Flow	Editor visual de processos usando React Flow.

A documentação oficial da OpenAI lista o GPT-4o como modelo disponível na API, com suporte a entrada de texto e imagem, saída em texto e Structured Outputs; também lista os endpoints compatíveis, incluindo Responses e Chat Completions.

A Railway permite serviços implantados a partir de repositórios GitHub, com build/deploy automático quando há push na branch conectada; para dados persistentes, como SQLite em produção, o serviço deve usar volume persistente, não armazenamento efêmero.

5. Stack do MVP
Frontend
React
Vite
React Router
React Flow
CSS moderno/customizado
Axios ou Fetch
Backend
Python
FastAPI
SQLAlchemy
Pydantic
SQLite
OpenAI SDK
Uvicorn
Deploy
GitHub monorepo
Railway com dois serviços:
- frontend
- backend

Volume persistente no backend:
- mount path recomendado: /app/data
- SQLite: sqlite:////app/data/qdt_processos.db

A Railway informa que aplicações React podem ser implantadas diretamente a partir de GitHub, CLI ou Dockerfile, e recomenda configurar URL pública e variáveis de ambiente para o serviço.

6. Público-Alvo
Usuário principal

Gestor de operação contábil

Necessita mapear processos, entender fluxos, identificar riscos, padronizar execução e priorizar automações.

Usuários futuros
coordenadores de área;
analistas líderes;
equipe de melhoria contínua;
consultores de processos;
equipe de automação interna.
7. Escopo Funcional do MVP
7.1 Dentro do escopo
Módulo	Descrição
Dashboard	Visão executiva dos processos cadastrados.
Catálogo de Processos	Lista, filtro, criação, edição e exclusão de processos.
Detalhe do Processo	Visão centralizada do processo.
Editor Visual	Canvas para criar, mover e conectar etapas.
Etapas	Cadastro estruturado das atividades do processo.
Análise IA	Envio do processo estruturado para GPT-4o.
Resultado IA	Exibição do diagnóstico operacional.
Diretrizes de Automação	Lista acionável de oportunidades sugeridas.
Persistência	SQLite com volume persistente na Railway.
Deploy	Aplicação publicada via Railway.
7.2 Fora do escopo
Item	Motivo
Login	Reduzir complexidade do MVP.
Multiusuário	Fase futura.
Controle de permissões	Depende de autenticação.
Upload de documentos	Fase futura.
Leitura automática de PDFs	Fase futura.
Integração com sistemas contábeis	Exige análise específica por sistema.
Execução real de automações	O MVP apenas recomenda automações.
Exportação PDF	Fase futura.
RPA	Fase futura.
8. Requisitos Funcionais
ID	Requisito
RF01	O sistema deve permitir cadastrar processos.
RF02	O sistema deve permitir editar processos.
RF03	O sistema deve permitir excluir processos.
RF04	O sistema deve listar processos cadastrados.
RF05	O sistema deve permitir filtrar processos por área, criticidade e status.
RF06	O sistema deve permitir cadastrar etapas vinculadas a um processo.
RF07	O sistema deve permitir editar etapas.
RF08	O sistema deve permitir excluir etapas.
RF09	O sistema deve permitir conectar etapas no editor visual.
RF10	O sistema deve salvar posição X/Y das etapas no canvas.
RF11	O sistema deve reabrir o fluxo salvo mantendo etapas e conexões.
RF12	O sistema deve permitir enviar um processo para análise com IA.
RF13	O sistema deve usar OpenAI GPT-4o para análise do processo.
RF14	O sistema deve validar a resposta da IA como JSON antes de salvar.
RF15	O sistema deve salvar o resultado da análise no SQLite.
RF16	O sistema deve exibir resumo executivo e diagnóstico operacional.
RF17	O sistema deve exibir gargalos e riscos encontrados.
RF18	O sistema deve exibir sugestões de melhoria.
RF19	O sistema deve exibir sugestões de automação.
RF20	O sistema deve gerar diretrizes de automação a partir da análise.
RF21	O sistema deve permitir alterar status das diretrizes.
RF22	O sistema deve exibir indicadores no dashboard.
9. Requisitos Não Funcionais
ID	Requisito
RNF01	A interface deve seguir estilo moderno/dashboard SaaS.
RNF02	O backend deve expor API REST em FastAPI.
RNF03	O frontend deve consumir a API via variável VITE_API_URL.
RNF04	O backend deve usar DATABASE_URL para configurar SQLite.
RNF05	A chave OpenAI deve ficar apenas em variável de ambiente.
RNF06	Nenhuma credencial deve ser versionada no GitHub.
RNF07	O sistema deve registrar erros sem expor dados sensíveis.
RNF08	O backend deve tratar falhas da OpenAI de forma controlada.
RNF09	O backend deve validar payloads com Pydantic.
RNF10	O SQLite deve ser armazenado em volume persistente na Railway.
RNF11	O sistema deve ter endpoints de health check.
RNF12	O backend deve configurar CORS para o domínio do frontend.
RNF13	O projeto deve ter README com execução local e deploy.
RNF14	O código deve ser organizado por responsabilidades.

As regras de segurança do projeto devem impedir exposição de senhas, tokens, chaves de API, credenciais e dados sensíveis em código-fonte ou logs.

10. Regras de Negócio
ID	Regra
RN01	Um processo deve ter nome e área obrigatórios.
RN02	Uma etapa deve ter nome obrigatório.
RN03	Toda etapa deve pertencer a um processo existente.
RN04	Toda conexão deve ligar duas etapas do mesmo processo.
RN05	Um processo precisa ter ao menos uma etapa para ser analisado pela IA.
RN06	A análise IA deve ser vinculada ao processo analisado.
RN07	Uma nova análise não deve excluir análises anteriores.
RN08	Diretrizes de automação devem nascer a partir da análise IA.
RN09	Sugestões da IA não executam ações automaticamente.
RN10	O sistema não deve ter regras rígidas específicas de uma única área contábil.
RN11	O sistema deve indicar lacunas quando o processo estiver pouco detalhado.
RN12	A IA não deve inventar prazos legais, sistemas ou obrigações fiscais.
11. Modelo de Dados
11.1 Processo
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
11.2 Etapa
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
11.3 Conexão
id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
etapa_origem_id INTEGER NOT NULL
etapa_destino_id INTEGER NOT NULL
tipo_conexao TEXT
condicao TEXT
created_at DATETIME
11.4 Análise IA
id INTEGER PRIMARY KEY
processo_id INTEGER NOT NULL
resumo_executivo TEXT
diagnostico_operacional TEXT
nivel_maturidade TEXT
json_resultado TEXT NOT NULL
created_at DATETIME
11.5 Diretriz de Automação
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
12. API REST Prevista
12.1 Health
Método	Endpoint	Objetivo
GET	/health	Verificar se a API está online.

Resposta esperada:

{
  "status": "ok",
  "service": "qdt-backend"
}
12.2 Processos
Método	Endpoint	Objetivo
GET	/api/processos	Listar processos.
POST	/api/processos	Criar processo.
GET	/api/processos/{id}	Detalhar processo.
PUT	/api/processos/{id}	Atualizar processo.
DELETE	/api/processos/{id}	Excluir processo.
12.3 Etapas
Método	Endpoint	Objetivo
GET	/api/processos/{processo_id}/etapas	Listar etapas do processo.
POST	/api/processos/{processo_id}/etapas	Criar etapa.
PUT	/api/etapas/{id}	Atualizar etapa.
DELETE	/api/etapas/{id}	Excluir etapa.
12.4 Fluxos
Método	Endpoint	Objetivo
GET	/api/processos/{processo_id}/fluxo	Obter etapas e conexões.
PUT	/api/processos/{processo_id}/fluxo	Salvar layout, etapas e conexões.
12.5 Análise IA
Método	Endpoint	Objetivo
POST	/api/processos/{processo_id}/analises	Gerar análise IA.
GET	/api/processos/{processo_id}/analises	Listar análises do processo.
GET	/api/analises/{id}	Obter análise específica.
12.6 Diretrizes
Método	Endpoint	Objetivo
GET	/api/processos/{processo_id}/diretrizes	Listar diretrizes.
PUT	/api/diretrizes/{id}	Atualizar status da diretriz.
13. Especificação da IA
13.1 Arquivos obrigatórios
backend/app/prompts/system_process_mapper.md
backend/app/prompts/user_process_analysis_template.md
backend/app/services/ia_service.py
backend/app/schemas/analise_schema.py
13.2 Modelo
OPENAI_MODEL=gpt-4o
13.3 Entrada da IA

O backend deve montar um JSON estruturado contendo:

processo
etapas
conexoes
riscos informados
gargalos informados
sistemas utilizados
documentos utilizados
observacoes
13.4 Saída obrigatória

A IA deve retornar JSON válido com:

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
13.5 Regras do agente de IA

A IA deve:

analisar apenas informações fornecidas;
não inventar sistemas, prazos legais, obrigações fiscais ou responsáveis;
apontar lacunas de mapeamento;
diferenciar melhoria de fluxo, automação simples, integração, IA, RPA, controle e governança;
classificar impacto, esforço e prioridade;
alertar sobre dados sensíveis quando aplicável;
devolver somente JSON válido;
gerar recomendações acionáveis, não genéricas.
14. UX/UI — Diretriz Visual
14.1 Estilo

A interface deve seguir padrão dashboard SaaS moderno, com:

sidebar lateral
header superior
cards executivos
badges de status
tabelas limpas
cards de automação
canvas visual
painéis laterais
componentes responsivos
14.2 Telas
Tela	Objetivo
Dashboard	Indicadores executivos.
Processos	Catálogo e filtros.
Novo Processo	Cadastro.
Detalhe do Processo	Visão centralizada.
Editor Visual	Mapeamento de fluxo.
Análise IA	Resultado interpretado.
Automações	Diretrizes acionáveis.
15. Critérios Gerais de Aceite do MVP

O MVP estará aceito quando:

for possível criar processo com nome e área;
for possível listar, editar e excluir processos;
for possível criar etapas vinculadas ao processo;
for possível conectar etapas visualmente;
as posições do canvas forem persistidas;
ao recarregar a página, o fluxo visual for reconstruído;
um processo com etapas puder ser analisado por GPT-4o;
a resposta da IA for validada como JSON;
a análise for salva no SQLite;
gargalos, riscos, melhorias e automações forem exibidos;
diretrizes de automação forem geradas;
o status das diretrizes puder ser alterado;
frontend e backend estiverem publicados na Railway;
o SQLite estiver salvo em volume persistente;
a chave OpenAI estiver apenas em variável de ambiente;
o README explicar execução local, variáveis e deploy.
Plano de Tasks v1.0 — Desenvolvimento Agentic

As tasks abaixo foram organizadas para permitir execução incremental, validação rápida e baixo retrabalho. O planejamento segue a priorização recomendada: base estrutural, fluxo principal, persistência, validações, interface, integrações, testes, deploy e melhorias.

Regras Transversais para todos os Agentes
Não salvar segredos no código.
Não commitar .env.
Não alterar escopo sem atualizar /docs.
Toda rota deve ter tratamento de erro.
Todo payload de entrada deve ter schema Pydantic.
Toda resposta da IA deve ser validada antes de salvar.
Todo componente visual deve ser reutilizável quando possível.
Toda task deve atualizar o README ou documentação quando mudar execução.
Toda entrega deve ter teste manual mínimo.
Não criar dependências desnecessárias.

Instruções para agentes de código devem ser específicas, verificáveis, com arquivos impactados, restrições, critérios de aceite e testes esperados.

Épico 0 — Preparação do Repositório
TASK-000 — Criar monorepo base
Objetivo

Criar a estrutura inicial do projeto com frontend, backend e docs.

Arquivos/Diretórios
qdt-processos-ctb/
  frontend/
  backend/
  docs/
  README.md
  .gitignore
Regras
O repositório deve ser único.
Frontend e backend devem ficar separados.
/docs deve conter os artefatos do projeto.
.env deve estar no .gitignore.
Critérios de aceite
Dado que o repositório foi criado, quando abrir a raiz do projeto, então devem existir /frontend, /backend e /docs.
Dado que existe .gitignore, quando verificar o arquivo, então .env, node_modules, __pycache__, .venv e arquivos SQLite locais devem estar ignorados.
Testes
Verificar estrutura de pastas.
Verificar git status sem arquivos sensíveis.
TASK-001 — Criar documentação base do projeto
Objetivo

Criar os documentos operacionais do SDD.

Arquivos
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
visão do produto;
decisões técnicas;
requisitos;
arquitetura;
backlog;
riscos;
instruções de deploy.
Critérios de aceite
Dado que a pasta /docs existe, quando abrir os documentos, então cada arquivo deve conter pelo menos título, objetivo e status.
Dado que uma decisão técnica foi tomada, quando abrir docs/decisions.md, então ela deve estar registrada.
Épico 1 — Backend Base
TASK-010 — Configurar FastAPI
Objetivo

Criar a API base.

Arquivos
backend/app/main.py
backend/app/core/config.py
backend/requirements.txt
backend/README.md
Regras
Criar rota GET /health.
Configurar CORS via variável CORS_ORIGINS.
Configuração deve vir de variáveis de ambiente.
Não hardcodar secrets.
Critérios de aceite
Dado que o backend está rodando, quando acessar /health, então deve retornar status ok.
Dado que CORS_ORIGINS está configurado, quando o frontend chamar a API, então a requisição deve ser permitida.
Testes
curl http://localhost:8000/health
TASK-011 — Configurar SQLite com SQLAlchemy
Objetivo

Criar camada de banco com SQLite.

Arquivos
backend/app/database/session.py
backend/app/database/base.py
backend/app/core/config.py
backend/app/models/
Regras
Usar DATABASE_URL.
Local: sqlite:///./data/qdt_processos.db.
Railway: sqlite:////app/data/qdt_processos.db.
Criar diretório data em runtime se não existir.
Não criar banco durante build da Railway.
Critérios de aceite
Dado que a API inicia, quando o SQLite não existir, então o sistema deve criar o arquivo no caminho configurado.
Dado que DATABASE_URL aponta para /app/data, quando em Railway, então o banco deve usar o volume persistente.
Testes
Iniciar backend local.
Criar registro de teste.
Reiniciar backend.
Confirmar persistência.
TASK-012 — Criar modelos SQLAlchemy
Objetivo

Criar entidades do banco.

Arquivos
backend/app/models/processo.py
backend/app/models/etapa.py
backend/app/models/conexao.py
backend/app/models/analise.py
backend/app/models/diretriz.py
Entidades
Processo
Etapa
Conexao
AnaliseIA
DiretrizAutomacao
Critérios de aceite
Dado que a API inicia, quando as tabelas não existem, então devem ser criadas.
Dado que o modelo Etapa existe, quando verificar seus campos, então deve conter processo_id, nome, posicao_x e posicao_y.
Dado que o modelo AnaliseIA existe, quando verificar seus campos, então deve conter json_resultado.
TASK-013 — Criar schemas Pydantic
Objetivo

Validar entrada e saída da API.

Arquivos
backend/app/schemas/processo_schema.py
backend/app/schemas/etapa_schema.py
backend/app/schemas/fluxo_schema.py
backend/app/schemas/analise_schema.py
backend/app/schemas/diretriz_schema.py
Regras
Nome e área são obrigatórios em Processo.
Nome é obrigatório em Etapa.
Conexão exige origem e destino.
Análise IA deve validar estrutura JSON esperada.
Critérios de aceite
Dado que um processo é enviado sem nome, quando a API receber o payload, então deve retornar erro 422.
Dado que uma etapa é enviada sem nome, quando a API receber o payload, então deve retornar erro 422.
Épico 2 — API de Processos, Etapas e Fluxos
TASK-020 — CRUD de processos
Objetivo

Implementar endpoints de processo.

Arquivos
backend/app/api/routes/processos.py
backend/app/services/processo_service.py
backend/app/repositories/processo_repository.py
Endpoints
GET    /api/processos
POST   /api/processos
GET    /api/processos/{id}
PUT    /api/processos/{id}
DELETE /api/processos/{id}
Critérios de aceite
Criar processo com nome e área.
Listar processos.
Buscar processo por ID.
Atualizar processo.
Excluir processo.
Retornar 404 para processo inexistente.
Testes
POST válido.
POST inválido.
GET lista.
GET id inexistente.
PUT válido.
DELETE válido.
TASK-021 — CRUD de etapas
Objetivo

Implementar endpoints de etapas.

Arquivos
backend/app/api/routes/etapas.py
backend/app/services/etapa_service.py
backend/app/repositories/etapa_repository.py
Endpoints
GET    /api/processos/{processo_id}/etapas
POST   /api/processos/{processo_id}/etapas
PUT    /api/etapas/{id}
DELETE /api/etapas/{id}
Regras
Etapa só pode ser criada para processo existente.
Etapa deve ter nome.
Excluir etapa deve remover conexões relacionadas.
Critérios de aceite
Dado que o processo existe, quando criar etapa válida, então a etapa deve ser salva.
Dado que o processo não existe, quando tentar criar etapa, então deve retornar 404.
Dado que uma etapa é excluída, quando buscar fluxo, então conexões órfãs não devem existir.
TASK-022 — API de fluxo visual
Objetivo

Persistir e recuperar o fluxo completo.

Arquivos
backend/app/api/routes/fluxos.py
backend/app/services/fluxo_service.py
backend/app/schemas/fluxo_schema.py
Endpoints
GET /api/processos/{processo_id}/fluxo
PUT /api/processos/{processo_id}/fluxo
Payload esperado
{
  "etapas": [],
  "conexoes": []
}
Regras
Toda conexão deve ligar etapas do mesmo processo.
Posições X/Y devem ser salvas.
O endpoint PUT deve atualizar layout e conexões.
Critérios de aceite
Dado que o usuário move etapas no canvas, quando salvar fluxo, então X/Y devem ser persistidos.
Dado que o usuário conecta duas etapas, quando salvar fluxo, então a conexão deve ser persistida.
Dado que o usuário recarrega a tela, quando buscar fluxo, então etapas e conexões devem retornar corretamente.
Épico 3 — Serviço de IA
TASK-030 — Criar system prompt especialista
Objetivo

Criar prompt profundo para análise de processos contábeis.

Arquivo
backend/app/prompts/system_process_mapper.md
Conteúdo obrigatório
papel da IA;
contexto de operação contábil;
critérios de análise;
regras anti-alucinação;
regras de segurança;
formato JSON obrigatório;
classificação de impacto, esforço e prioridade;
tipos de automação;
critérios de maturidade do processo.
Critérios de aceite
Dado que o arquivo existe, quando abrir o prompt, então ele deve instruir a IA a retornar somente JSON.
Dado que o prompt existe, quando revisar regras, então deve proibir invenção de sistemas, prazos legais e obrigações fiscais.
Dado que há dados sensíveis, quando a IA analisar, então deve gerar alerta de privacidade.
TASK-031 — Criar schema de resposta da IA
Objetivo

Validar o JSON retornado pelo GPT-4o.

Arquivo
backend/app/schemas/analise_schema.py
Campos obrigatórios
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
Critérios de aceite
Dado que a IA retorna JSON válido, quando validar schema, então a validação deve passar.
Dado que a IA retorna texto fora do JSON, quando validar schema, então a validação deve falhar sem salvar no banco.
TASK-032 — Implementar ia_service.py
Objetivo

Integrar backend com OpenAI GPT-4o.

Arquivo
backend/app/services/ia_service.py
Regras
Ler OPENAI_API_KEY do ambiente.
Ler OPENAI_MODEL, default gpt-4o.
Carregar system prompt do arquivo.
Enviar processo estruturado como entrada.
Solicitar resposta estruturada.
Validar JSON antes de retornar ao service.
Tratar timeout e erro da API.
Critérios de aceite
Dado que OPENAI_API_KEY está ausente, quando chamar análise, então deve retornar erro controlado.
Dado que o processo tem etapas, quando chamar análise, então deve enviar payload estruturado à OpenAI.
Dado que a OpenAI retorna JSON válido, quando receber resposta, então deve validar e devolver ao chamador.
TASK-033 — Endpoint de análise IA
Objetivo

Criar geração e persistência da análise.

Arquivos
backend/app/api/routes/analises.py
backend/app/services/analise_service.py
backend/app/repositories/analise_repository.py
backend/app/repositories/diretriz_repository.py
Endpoint
POST /api/processos/{processo_id}/analises
Regras
Bloquear análise se processo não tiver etapas.
Salvar análise no banco.
Gerar diretrizes a partir de diretrizes_automacao.
Não apagar análises anteriores.
Critérios de aceite
Dado que o processo não tem etapas, quando solicitar análise, então retornar erro 400.
Dado que a análise foi concluída, quando buscar análises do processo, então a nova análise deve aparecer.
Dado que a IA gerou diretrizes, quando abrir diretrizes, então elas devem estar persistidas.
Épico 4 — Frontend Base
TASK-040 — Criar frontend React + Vite
Objetivo

Inicializar aplicação frontend.

Arquivos
frontend/package.json
frontend/src/main.jsx
frontend/src/App.jsx
frontend/src/styles/global.css
Regras
Usar React + Vite.
Configurar React Router.
Criar estrutura de páginas.
Usar VITE_API_URL.
Critérios de aceite
Dado que o frontend está rodando, quando acessar o navegador, então deve abrir a aplicação.
Dado que VITE_API_URL está configurado, quando chamar /health, então deve receber resposta da API.
TASK-041 — Criar layout SaaS
Objetivo

Criar estrutura visual base.

Arquivos
frontend/src/components/layout/Sidebar.jsx
frontend/src/components/layout/Header.jsx
frontend/src/components/layout/DashboardLayout.jsx
frontend/src/styles/global.css
Regras
Sidebar fixa.
Header com título da página.
Área principal responsiva.
Visual moderno com cards, sombras leves, bordas e espaçamento consistente.
Critérios de aceite
Dado que o usuário acessa qualquer página, quando a página carregar, então sidebar e header devem estar visíveis.
Dado que a tela é redimensionada, quando a largura mudar, então o layout não deve quebrar.
TASK-042 — Criar client de API
Objetivo

Centralizar chamadas HTTP.

Arquivos
frontend/src/services/api.js
frontend/src/services/processosApi.js
frontend/src/services/etapasApi.js
frontend/src/services/analisesApi.js
frontend/src/services/diretrizesApi.js
Regras
Usar VITE_API_URL.
Tratar erro HTTP.
Não duplicar base URL.
Retornar mensagens controladas para a interface.
Critérios de aceite
Dado que a API está fora, quando chamar endpoint, então frontend deve exibir erro amigável.
Dado que a API responde, quando chamar processos, então deve retornar dados para a tela.
Épico 5 — Telas de Processo
TASK-050 — Dashboard
Objetivo

Criar dashboard executivo.

Arquivos
frontend/src/pages/Dashboard.jsx
frontend/src/components/dashboard/MetricCard.jsx
frontend/src/components/dashboard/RecentProcesses.jsx
Indicadores
total de processos
processos críticos
processos sem análise IA
oportunidades de automação
gargalos identificados
processos por área
Critérios de aceite
Dado que existem processos, quando abrir dashboard, então total deve aparecer.
Dado que existem processos críticos, quando abrir dashboard, então card de criticidade deve refletir quantidade.
Dado que não há dados, quando abrir dashboard, então estado vazio deve ser exibido.
TASK-051 — Catálogo de processos
Objetivo

Criar tela de listagem e filtros.

Arquivos
frontend/src/pages/Processos.jsx
frontend/src/components/processos/ProcessoTable.jsx
frontend/src/components/processos/ProcessoFilters.jsx
Filtros
área
criticidade
status
texto livre
Critérios de aceite
Dado que existem processos, quando abrir catálogo, então eles devem aparecer.
Dado que filtrar por área, quando aplicar filtro, então lista deve mostrar apenas processos da área.
Dado que clicar em processo, quando selecionar item, então deve navegar para detalhe.
TASK-052 — Formulário de processo
Objetivo

Criar cadastro e edição.

Arquivos
frontend/src/components/processos/ProcessoForm.jsx
frontend/src/pages/ProcessoNovo.jsx
frontend/src/pages/ProcessoEditar.jsx
Campos
nome
area
descricao
objetivo
responsavel
periodicidade
criticidade
status
sistemas_utilizados
documentos_utilizados
observacoes
Critérios de aceite
Dado que nome está vazio, quando salvar, então deve exibir validação.
Dado que área está vazia, quando salvar, então deve exibir validação.
Dado que dados obrigatórios estão preenchidos, quando salvar, então processo deve ser criado.
TASK-053 — Detalhe do processo
Objetivo

Centralizar navegação do processo.

Arquivo
frontend/src/pages/ProcessoDetalhe.jsx
Componentes
resumo
metadados
quantidade de etapas
status da última análise
botão editar
botão abrir fluxo
botão analisar IA
botão ver automações
Critérios de aceite
Dado que o processo existe, quando abrir detalhe, então dados principais devem aparecer.
Dado que o processo não existe, quando abrir URL inválida, então deve exibir erro controlado.
Épico 6 — Editor Visual
TASK-060 — Instalar e configurar React Flow
Objetivo

Preparar canvas visual.

Arquivos
frontend/src/pages/FluxoEditor.jsx
frontend/src/components/fluxo/FlowEditor.jsx
frontend/src/components/fluxo/EtapaNode.jsx
frontend/src/components/fluxo/EtapaPanel.jsx
Critérios de aceite
Dado que abrir fluxo de processo sem etapas, quando carregar tela, então canvas vazio deve aparecer.
Dado que existem etapas, quando carregar tela, então nodes devem aparecer.
TASK-061 — Criar/editar etapas pelo canvas
Objetivo

Permitir criação e edição de etapas.

Regras
Botão “Nova etapa”.
Painel lateral para edição.
Nome obrigatório.
Salvar no backend.
Critérios de aceite
Dado que o usuário cria etapa, quando salvar, então node deve aparecer no canvas.
Dado que o usuário edita etapa, quando salvar, então node deve refletir novo nome.
TASK-062 — Conectar etapas
Objetivo

Permitir ligações visuais.

Regras
Usuário deve conectar node origem a node destino.
Conexão deve ser salva via API de fluxo.
Conexões inválidas devem ser bloqueadas pelo backend.
Critérios de aceite
Dado que duas etapas existem, quando conectar e salvar, então conexão deve persistir.
Dado que recarregar página, quando abrir fluxo, então conexão deve reaparecer.
TASK-063 — Persistir layout X/Y
Objetivo

Salvar posição visual das etapas.

Critérios de aceite
Dado que o usuário move uma etapa, quando salvar fluxo, então X/Y devem ser enviados ao backend.
Dado que recarrega a tela, quando abrir fluxo, então etapa deve aparecer na posição salva.
Épico 7 — Resultado IA e Automações
TASK-070 — Tela de análise IA
Objetivo

Permitir solicitar análise e visualizar resultado.

Arquivos
frontend/src/pages/AnaliseIA.jsx
frontend/src/components/ia/AnalisePanel.jsx
frontend/src/components/ia/GargalosList.jsx
frontend/src/components/ia/RiscosList.jsx
frontend/src/components/ia/AutomacaoSuggestions.jsx
Critérios de aceite
Dado que processo tem etapas, quando clicar em analisar, então botão deve entrar em loading.
Dado que análise retorna com sucesso, quando finalizar, então resultado deve aparecer.
Dado que erro ocorre, quando falhar, então mensagem amigável deve aparecer.
TASK-071 — Renderizar resposta estruturada da IA
Objetivo

Exibir JSON da IA em componentes visuais.

Componentes
Resumo executivo
Diagnóstico operacional
Nível de maturidade
Pontos fortes
Gargalos
Riscos
Sugestões de melhoria
Sugestões de automação
Lacunas
Indicadores
Alertas
Critérios de aceite
Dado que existe análise salva, quando abrir tela, então resumo e diagnóstico devem aparecer.
Dado que há gargalos, quando renderizar, então cada gargalo deve mostrar impacto.
Dado que há alertas, quando renderizar, então devem aparecer em destaque.
TASK-072 — Tela de diretrizes de automação
Objetivo

Exibir oportunidades acionáveis.

Arquivos
frontend/src/pages/Automacoes.jsx
frontend/src/components/automacoes/AutomacaoBoard.jsx
frontend/src/components/automacoes/PrioridadeBadge.jsx
Critérios de aceite
Dado que existem diretrizes, quando abrir tela, então lista deve aparecer.
Dado que alterar status, quando salvar, então status deve persistir.
Dado que filtrar por prioridade, quando aplicar filtro, então lista deve ser filtrada.
Épico 8 — Deploy Railway
TASK-080 — Preparar backend para Railway
Objetivo

Configurar backend para deploy.

Arquivos
backend/requirements.txt
backend/Procfile ou comando de start Railway
backend/README.md
Variáveis
APP_ENV=production
DATABASE_URL=sqlite:////app/data/qdt_processos.db
OPENAI_API_KEY=
OPENAI_MODEL=gpt-4o
CORS_ORIGINS=
Critérios de aceite
Backend inicia na Railway.
/health responde publicamente.
Volume /app/data está configurado.
SQLite persiste após redeploy.
TASK-081 — Preparar frontend para Railway
Objetivo

Configurar frontend para deploy.

Variáveis
VITE_API_URL=https://url-do-backend
Critérios de aceite
Frontend publica na Railway.
Frontend chama backend corretamente.
Rotas React funcionam após refresh.
TASK-082 — Teste de persistência Railway
Objetivo

Validar SQLite com volume.

Procedimento
1. Criar processo em produção.
2. Confirmar que aparece no catálogo.
3. Fazer novo deploy.
4. Acessar catálogo.
5. Confirmar que processo continua salvo.
Critério de aceite
Dado que houve redeploy, quando acessar a aplicação, então dados anteriores devem continuar disponíveis.
Épico 9 — Testes e Qualidade
TASK-090 — Testes mínimos de backend
Objetivo

Criar testes de API.

Arquivos
backend/tests/test_health.py
backend/tests/test_processos.py
backend/tests/test_etapas.py
backend/tests/test_fluxo.py
backend/tests/test_analise_schema.py
Cenários
health responde
processo válido é criado
processo sem nome falha
etapa válida é criada
etapa sem nome falha
fluxo salva conexão
schema IA valida JSON correto
schema IA rejeita JSON inválido
TASK-091 — Checklist de validação manual frontend
Objetivo

Criar checklist de homologação.

Arquivo
docs/tests.md
Cenários
criar processo
editar processo
criar etapa
mover etapa
conectar etapas
recarregar fluxo
analisar com IA
visualizar análise
alterar status da automação
testar erro de API
TASK-092 — Revisão técnica final
Objetivo

Verificar aderência ao PRD.

Checklist
requisitos funcionais implementados
rotas funcionando
dados persistindo
IA retornando JSON válido
frontend responsivo
segredos fora do código
README atualizado
deploy funcionando
Matriz de Rastreabilidade
Requisito	Tasks principais
RF01–RF05 Processos	TASK-020, TASK-050, TASK-051, TASK-052, TASK-053
RF06–RF08 Etapas	TASK-021, TASK-061
RF09–RF11 Fluxo visual	TASK-022, TASK-060, TASK-062, TASK-063
RF12–RF15 Análise IA	TASK-030, TASK-031, TASK-032, TASK-033, TASK-070
RF16–RF19 Resultado IA	TASK-071
RF20–RF21 Diretrizes	TASK-072
RF22 Dashboard	TASK-050
RNF05–RNF07 Segurança	TASK-010, TASK-032, TASK-080
RNF10 SQLite persistente	TASK-011, TASK-080, TASK-082
Deploy Railway	TASK-080, TASK-081, TASK-082
Documentação	TASK-001, TASK-091
Definition of Done do MVP

O MVP só deve ser considerado pronto quando:

[ ] Repositório GitHub criado.
[ ] Frontend e backend separados.
[ ] Backend FastAPI rodando.
[ ] SQLite funcionando localmente.
[ ] SQLite persistindo na Railway.
[ ] CRUD de processos funcionando.
[ ] CRUD de etapas funcionando.
[ ] Editor visual salvando etapas, conexões e posições.
[ ] OpenAI GPT-4o integrada por variável de ambiente.
[ ] System prompt especialista criado.
[ ] Resposta da IA validada como JSON.
[ ] Análise salva no banco.
[ ] Diretrizes de automação geradas.
[ ] Dashboard exibindo indicadores.
[ ] Frontend publicado na Railway.
[ ] Backend publicado na Railway.
[ ] README atualizado.
[ ] Testes mínimos executados.
[ ] Nenhuma chave ou segredo no GitHub.