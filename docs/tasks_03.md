Regras obrigatórias
Não implementar React Flow neste pacote.
Não implementar IA neste pacote.
Não implementar login.
Não implementar upload de documentos.
Não implementar exportação PDF.
Não hardcodar URL da API.
Usar VITE_API_URL.
Centralizar chamadas HTTP em /frontend/src/services.
Não chamar fetch diretamente dentro de múltiplos componentes sem abstração.
Criar componentes reutilizáveis.
Criar estados de loading, erro e vazio.
Tratar erro de API de forma amigável.
Manter visual moderno estilo dashboard SaaS.
Usar CSS organizado, com variáveis globais de cor, espaçamento, borda e sombra.
Atualizar /docs/backlog.md, /docs/changelog.md e /docs/tests.md.
Não criar dependências desnecessárias.
A aplicação deve rodar localmente com npm run dev.
Estrutura esperada após este pacote
frontend/
  index.html
  package.json
  vite.config.js
  .env.example

  src/
    main.jsx
    App.jsx

    components/
      common/
        Button.jsx
        Card.jsx
        EmptyState.jsx
        ErrorState.jsx
        LoadingState.jsx
        Badge.jsx
        ConfirmDialog.jsx

      layout/
        DashboardLayout.jsx
        Sidebar.jsx
        Header.jsx

      dashboard/
        MetricCard.jsx
        RecentProcesses.jsx

      processos/
        ProcessoTable.jsx
        ProcessoFilters.jsx
        ProcessoForm.jsx
        ProcessoStatusBadge.jsx
        ProcessoCriticidadeBadge.jsx

    pages/
      Dashboard.jsx
      Processos.jsx
      ProcessoNovo.jsx
      ProcessoEditar.jsx
      ProcessoDetalhe.jsx
      NotFound.jsx

    services/
      api.js
      processosApi.js

    utils/
      constants.js
      formatters.js

    styles/
      global.css
Variáveis de ambiente

Criar:

frontend/.env.example

Conteúdo:

VITE_API_URL=http://localhost:8000

Regras:

O frontend deve ler a URL da API via import.meta.env.VITE_API_URL.
Não commitar .env.
.env deve estar no .gitignore.
TASK-040 — Criar frontend React + Vite
Objetivo

Inicializar a aplicação frontend em React com Vite e configurar a base de navegação.

Arquivos impactados
frontend/package.json
frontend/vite.config.js
frontend/index.html
frontend/src/main.jsx
frontend/src/App.jsx
frontend/src/pages/NotFound.jsx
frontend/.env.example
docs/backlog.md
docs/changelog.md
Rotas obrigatórias
/                     -> Dashboard
/processos            -> Catálogo de processos
/processos/novo       -> Novo processo
/processos/:id        -> Detalhe do processo
/processos/:id/editar -> Editar processo
*                     -> NotFound
Regras
Usar React Router.
Usar layout base em todas as páginas principais.
A rota * deve mostrar página amigável de rota não encontrada.
Não implementar autenticação.
Critérios de aceite
Dado que o frontend está rodando,
quando acessar http://localhost:5173,
então a página Dashboard deve carregar.

Dado que o usuário acessa /processos,
quando a rota carregar,
então a página de catálogo deve aparecer.

Dado que o usuário acessa rota inexistente,
quando a rota carregar,
então deve aparecer página NotFound amigável.
Comandos esperados
cd frontend
npm install
npm run dev
TASK-041 — Criar layout SaaS
Objetivo

Criar layout visual moderno com sidebar, header e área principal.

Arquivos impactados
frontend/src/components/layout/DashboardLayout.jsx
frontend/src/components/layout/Sidebar.jsx
frontend/src/components/layout/Header.jsx
frontend/src/styles/global.css
frontend/src/App.jsx
Diretriz visual

A interface deve seguir padrão dashboard SaaS moderno, com:

sidebar lateral fixa
header superior
área de conteúdo com espaçamento amplo
cards com bordas arredondadas
sombras leves
paleta limpa
badges para status
tabelas limpas
botões claros
responsividade básica
Navegação da Sidebar

Itens:

Dashboard -> /
Processos -> /processos
Fluxos -> item desabilitado ou futuro
IA Insights -> item desabilitado ou futuro
Automações -> item desabilitado ou futuro

Como React Flow e IA ainda não serão implementados, os itens futuros podem aparecer com badge “Em breve” ou ficar ocultos. Preferência: mostrar como “Em breve” para indicar roadmap.

Header

Deve exibir:

Título da página atual
Subtítulo contextual opcional
CSS

Criar variáveis em global.css:

:root {
  --color-bg: #f6f7fb;
  --color-surface: #ffffff;
  --color-border: #e5e7eb;
  --color-text: #111827;
  --color-muted: #6b7280;
  --color-primary: #2563eb;
  --color-primary-dark: #1d4ed8;
  --radius-md: 12px;
  --radius-lg: 18px;
  --shadow-sm: 0 1px 2px rgba(15, 23, 42, 0.08);
  --shadow-md: 0 8px 24px rgba(15, 23, 42, 0.08);
}

Não é obrigatório usar exatamente essas cores, mas manter visual moderno, limpo e consistente.

Critérios de aceite
Dado que o usuário acessa qualquer página principal,
quando a página carregar,
então sidebar, header e área principal devem aparecer.

Dado que o usuário clica em Processos,
quando clicar no item da sidebar,
então deve navegar para /processos.

Dado que a tela é redimensionada,
quando a largura diminuir,
então o layout não deve quebrar visualmente.
TASK-042 — Criar client de API
Objetivo

Centralizar chamadas HTTP do frontend para o backend.

Arquivos impactados
frontend/src/services/api.js
frontend/src/services/processosApi.js
frontend/src/components/common/ErrorState.jsx
frontend/src/components/common/LoadingState.jsx
Serviço base

Criar api.js com:

API_BASE_URL a partir de VITE_API_URL
função request(path, options)
tratamento de erro HTTP
parse seguro de JSON
mensagem amigável em caso de falha de conexão
Processos API

Criar processosApi.js com funções:

listarProcessos(filters)
obterProcesso(id)
criarProcesso(payload)
atualizarProcesso(id, payload)
excluirProcesso(id)
Regras
Não duplicar URL base.
Não hardcodar localhost:8000 dentro dos componentes.
Tratar erro de API offline.
Retornar erro com mensagem amigável.
Critérios de aceite
Dado que VITE_API_URL está configurado,
quando chamar listarProcessos,
então a requisição deve ir para a API correta.

Dado que a API está fora do ar,
quando a tela tentar buscar processos,
então deve exibir mensagem de erro amigável.

Dado que a API retorna erro 404 ou 400,
quando o serviço receber a resposta,
então deve propagar mensagem controlada para a interface.
TASK-050 — Dashboard inicial
Objetivo

Criar dashboard executivo inicial com indicadores derivados dos processos existentes.

Arquivos impactados
frontend/src/pages/Dashboard.jsx
frontend/src/components/dashboard/MetricCard.jsx
frontend/src/components/dashboard/RecentProcesses.jsx
frontend/src/components/common/Card.jsx
frontend/src/services/processosApi.js
Indicadores iniciais

Como ainda não há API específica de métricas, calcular no frontend a partir de listarProcessos():

total de processos
processos críticos
processos em rascunho
processos analisados
processos por área
últimos processos cadastrados ou atualizados
Regras
Usar dados reais da API.
Mostrar loading enquanto busca.
Mostrar erro se API falhar.
Mostrar estado vazio se não houver processos.
Não inventar métricas que ainda não existem no backend, como gargalos e automações, salvo exibir como “Em breve”.
Critérios de aceite
Dado que existem processos cadastrados,
quando abrir o dashboard,
então o total de processos deve aparecer.

Dado que existem processos com criticidade Alta,
quando abrir o dashboard,
então o card de processos críticos deve refletir a quantidade.

Dado que não existem processos,
quando abrir o dashboard,
então deve aparecer estado vazio orientando a criar o primeiro processo.

Dado que a API está fora,
quando abrir o dashboard,
então deve aparecer mensagem de erro amigável.
TASK-051 — Catálogo de processos
Objetivo

Criar tela de listagem, busca e filtros de processos.

Arquivos impactados
frontend/src/pages/Processos.jsx
frontend/src/components/processos/ProcessoTable.jsx
frontend/src/components/processos/ProcessoFilters.jsx
frontend/src/components/processos/ProcessoStatusBadge.jsx
frontend/src/components/processos/ProcessoCriticidadeBadge.jsx
frontend/src/components/common/Button.jsx
frontend/src/components/common/EmptyState.jsx
frontend/src/components/common/ErrorState.jsx
frontend/src/components/common/LoadingState.jsx
frontend/src/services/processosApi.js
frontend/src/utils/constants.js
frontend/src/utils/formatters.js
Campos exibidos na tabela
Nome
Área
Responsável
Periodicidade
Criticidade
Status
Atualizado em
Ações
Filtros
q
area
criticidade
status
Ações
Ver detalhe
Editar
Excluir
Criar novo processo
Constantes

Criar em utils/constants.js:

AREAS_CONTABEIS
CRITICIDADES
STATUS_PROCESSO
PERIODICIDADES

Valores:

Áreas:
Fiscal
Contábil
Folha de Pagamento
Departamento Pessoal
Societário
Legalização
Financeiro
BPO Financeiro
Atendimento ao Cliente
Controladoria
Consultivo
Administrativo
Outros

Criticidade:
Baixa
Média
Alta

Status:
Rascunho
Mapeado
Em análise
Analisado
Em melhoria

Periodicidade:
Diário
Semanal
Quinzenal
Mensal
Trimestral
Anual
Sob demanda
Regras
Filtros devem usar query params da API.
Botão “Novo processo” deve navegar para /processos/novo.
Excluir processo deve pedir confirmação.
Após excluir, a lista deve ser atualizada.
A tabela deve mostrar estado vazio quando não houver registros.
Critérios de aceite
Dado que existem processos cadastrados,
quando abrir /processos,
então eles devem aparecer na tabela.

Dado que filtro por área Fiscal,
quando aplicar o filtro,
então a API deve receber area=Fiscal e retornar apenas processos dessa área.

Dado que pesquiso por texto,
quando preencher o campo de busca,
então a API deve receber q com o texto informado.

Dado que clico em Novo processo,
quando clicar,
então devo navegar para /processos/novo.

Dado que clico em Excluir,
quando confirmar,
então o processo deve ser removido e a lista atualizada.
TASK-052 — Formulário de processo
Objetivo

Criar formulário reutilizável para criação e edição de processos.

Arquivos impactados
frontend/src/components/processos/ProcessoForm.jsx
frontend/src/pages/ProcessoNovo.jsx
frontend/src/pages/ProcessoEditar.jsx
frontend/src/services/processosApi.js
frontend/src/utils/constants.js
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
Campos obrigatórios
nome
area
Comportamento em criação

Rota:

/processos/novo

Ao salvar com sucesso:

navegar para /processos/:id
Comportamento em edição

Rota:

/processos/:id/editar

Ao salvar com sucesso:

navegar para /processos/:id
Validações frontend
nome não pode estar vazio
area não pode estar vazia

Mesmo com validação frontend, manter backend como fonte final de validação.

Regras
Formulário deve ser reutilizável para criar e editar.
Em edição, carregar dados existentes antes de exibir.
Mostrar loading ao carregar processo.
Mostrar loading ao salvar.
Exibir erro amigável se falhar.
Botão cancelar deve voltar para a página anterior ou catálogo.
Critérios de aceite
Dado que nome está vazio,
quando tentar salvar,
então deve exibir mensagem de validação no formulário.

Dado que área está vazia,
quando tentar salvar,
então deve exibir mensagem de validação no formulário.

Dado que nome e área estão preenchidos,
quando salvar novo processo,
então a API deve criar o processo e o usuário deve ser redirecionado para o detalhe.

Dado que estou editando processo existente,
quando alterar campos e salvar,
então a API deve atualizar o processo e voltar para o detalhe.

Dado que o backend retorna erro,
quando salvar,
então o formulário deve mostrar mensagem amigável.
TASK-053 — Detalhe do processo
Objetivo

Criar tela de detalhe do processo com metadados e ações futuras.

Arquivo impactado
frontend/src/pages/ProcessoDetalhe.jsx
frontend/src/components/common/Card.jsx
frontend/src/components/common/Badge.jsx
frontend/src/services/processosApi.js
Componentes da tela
Nome do processo
Área
Descrição
Objetivo
Responsável
Periodicidade
Criticidade
Status
Sistemas utilizados
Documentos utilizados
Observações
Data de criação
Data de atualização
Botão editar
Botão voltar para catálogo
Botão abrir fluxo visual — desabilitado ou “Em breve”
Botão analisar com IA — desabilitado ou “Em breve”
Botão ver automações — desabilitado ou “Em breve”
Regras
Carregar dados pela API.
Se o processo não existir, exibir erro amigável.
Ações futuras devem ficar visíveis como roadmap, mas desabilitadas.
Não implementar fluxo visual neste pacote.
Critérios de aceite
Dado que o processo existe,
quando abrir /processos/:id,
então os dados principais devem aparecer.

Dado que o processo não existe,
quando abrir /processos/999999,
então deve aparecer mensagem de erro amigável.

Dado que clico em Editar,
quando clicar,
então devo navegar para /processos/:id/editar.

Dado que clico em Voltar,
quando clicar,
então devo navegar para /processos.
Componentes comuns obrigatórios

Criar componentes simples e reutilizáveis:

Button.jsx

Props sugeridas:

children
type
variant
onClick
disabled
loading
Card.jsx

Props sugeridas:

children
className
Badge.jsx

Props sugeridas:

children
variant
LoadingState.jsx

Usado para telas carregando.

ErrorState.jsx

Usado para erro de API.

EmptyState.jsx

Usado para listas vazias.

ConfirmDialog.jsx

Pode ser simples usando window.confirm encapsulado ou componente visual básico.
Preferência: nesta fase pode usar confirmação simples para reduzir complexidade.

Integração esperada com API do Pacote 02

O frontend deve consumir os endpoints:

GET    /api/processos
POST   /api/processos
GET    /api/processos/{processo_id}
PUT    /api/processos/{processo_id}
DELETE /api/processos/{processo_id}

Não consumir ainda:

/api/processos/{processo_id}/etapas
/api/processos/{processo_id}/fluxo
/api/processos/{processo_id}/analises

Esses serão usados em pacotes futuros.

Estados de interface obrigatórios

Toda tela que busca dados deve considerar:

loading
erro
vazio
sucesso
Exemplo de comportamento
Dashboard:
- loading enquanto carrega processos;
- erro se API falhar;
- vazio se não há processos;
- cards se houver dados.

Catálogo:
- loading enquanto carrega lista;
- erro se API falhar;
- vazio se não há processos;
- tabela se houver dados.

Detalhe:
- loading enquanto carrega processo;
- erro se processo não existir;
- conteúdo se sucesso.
Testes manuais obrigatórios

Registrar em docs/tests.md:

1. Abrir frontend local.
2. Verificar se Dashboard carrega.
3. Verificar se sidebar navega para Processos.
4. Criar processo válido.
5. Tentar criar processo sem nome.
6. Tentar criar processo sem área.
7. Listar processos.
8. Filtrar por área.
9. Editar processo.
10. Abrir detalhe do processo.
11. Excluir processo.
12. Simular backend fora do ar e verificar erro amigável.
Comandos esperados
Instalar dependências
cd frontend
npm install
Rodar frontend
npm run dev
Rodar backend em outro terminal
cd backend
uvicorn app.main:app --reload
Testar localmente

Frontend:

http://localhost:5173

Backend:

http://localhost:8000/health
Atualização obrigatória da documentação
docs/backlog.md

Marcar como concluídas ou em andamento:

TASK-040 — Criar frontend React + Vite
TASK-041 — Criar layout SaaS
TASK-042 — Criar client de API
TASK-050 — Dashboard inicial
TASK-051 — Catálogo de processos
TASK-052 — Formulário de processo
TASK-053 — Detalhe do processo
docs/changelog.md

Adicionar:

## 0.3.0

- Criado frontend React com Vite.
- Configurado React Router.
- Criado layout dashboard SaaS.
- Criado client de API com VITE_API_URL.
- Criado dashboard inicial.
- Criado catálogo de processos.
- Criado formulário de criação e edição de processos.
- Criada tela de detalhe do processo.
- Adicionados estados de loading, erro e vazio.
docs/tests.md

Adicionar checklist do frontend:

- Dashboard validado.
- Catálogo de processos validado.
- Criação de processo validada.
- Edição de processo validada.
- Exclusão de processo validada.
- Detalhe do processo validado.
- Erro de API validado.
Definition of Done do Pacote 03

A entrega só estará concluída quando:

[ ] Frontend React + Vite criado.
[ ] React Router configurado.
[ ] VITE_API_URL configurado.
[ ] Layout com sidebar e header implementado.
[ ] Dashboard inicial carrega dados reais da API.
[ ] Catálogo lista processos reais da API.
[ ] Filtros de processos funcionam.
[ ] Formulário cria processo.
[ ] Formulário edita processo.
[ ] Exclusão de processo funciona com confirmação.
[ ] Detalhe do processo exibe dados reais.
[ ] Estados de loading existem.
[ ] Estados de erro existem.
[ ] Estados vazios existem.
[ ] CSS está organizado.
[ ] Nenhuma URL de API está hardcoded em componente.
[ ] Nenhum segredo foi versionado.
[ ] Documentação foi atualizada.
[ ] Backend e frontend rodam localmente em conjunto.
Restrições

Não implemente neste pacote:

React Flow
Editor visual
Cadastro de etapas via frontend
Conexões entre etapas
OpenAI
ia_service.py
system_process_mapper.md
Análise IA
Diretrizes de automação
Railway deploy
Login
Upload de arquivos
Exportação PDF
Resultado esperado

Ao final deste pacote, o usuário deve conseguir operar o cadastro básico de processos pela interface web, com visual moderno e integração real com o backend.

O próximo pacote será:

Pacote 04 — Editor Visual de Fluxo com React Flow

Ele deverá implementar:

Tela /processos/:id/fluxo
React Flow
Criação de etapas pelo canvas
Edição de etapas em painel lateral
Conexão entre etapas
Persistência de layout X/Y
Integração com API de fluxo

---

# Checklist de Revisão após o Antigravity executar

Use este checklist antes de avançar:

```text
1. O backend está rodando em http://localhost:8000?
2. O frontend está rodando em http://localhost:5173?
3. VITE_API_URL aponta para o backend?
4. A sidebar aparece em todas as páginas?
5. O Dashboard carrega sem erro?
6. O Dashboard exibe estado vazio se não houver processos?
7. O Catálogo lista processos reais da API?
8. O filtro por área funciona?
9. O filtro por criticidade funciona?
10. O filtro por status funciona?
11. A busca por texto funciona?
12. O botão Novo processo abre /processos/novo?
13. Processo sem nome é bloqueado no frontend?
14. Processo sem área é bloqueado no frontend?
15. Processo válido é criado?
16. Após criar, redireciona para detalhe?
17. A edição carrega os dados existentes?
18. A edição salva alterações?
19. A exclusão pede confirmação?
20. A exclusão remove o processo da lista?
21. Processo inexistente mostra erro amigável?
22. API fora do ar mostra erro amigável?
23. Não há URL hardcoded em componentes?
24. docs/backlog.md foi atualizado?
25. docs/changelog.md foi atualizado?
26. docs/tests.md foi atualizado?