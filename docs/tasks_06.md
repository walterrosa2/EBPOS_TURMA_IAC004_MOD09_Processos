Stack deste pacote

Frontend:

React
Vite
React Router
CSS customizado
Fetch API via services existentes

Backend consumido:

POST /api/processos/{processo_id}/analises
GET  /api/processos/{processo_id}/analises
GET  /api/analises/{analise_id}

GET  /api/processos/{processo_id}/diretrizes
PUT  /api/diretrizes/{diretriz_id}
Regras obrigatórias
Não hardcodar URL da API.
Usar VITE_API_URL via service centralizado.
Não chamar fetch diretamente nas páginas.
Criar analisesApi.js e diretrizesApi.js.
Criar componentes reutilizáveis para exibir análise.
Criar estados de loading, erro, vazio e sucesso.
Não implementar IA diretamente no frontend.
O frontend deve apenas chamar o backend.
Não expor OPENAI_API_KEY no frontend.
Não exibir stack trace técnico para usuário final.
Exibir mensagens claras para falha de IA.
Manter visual moderno estilo dashboard SaaS.
Preservar telas existentes.
Atualizar documentação em /docs.
Não criar dependências desnecessárias.
Não alterar endpoints do backend sem necessidade.
Ações futuras devem ficar visíveis apenas se funcionais ou marcadas como “Em breve”.
Componentes devem ser organizados por responsabilidade.

As instruções para agentes de desenvolvimento devem ser específicas, verificáveis, com arquivos impactados, critérios de aceite e testes esperados.

Estrutura esperada após este pacote
frontend/
  src/
    pages/
      Analises.jsx
      AnaliseDetalhe.jsx
      Automacoes.jsx

    components/
      ia/
        AnaliseHeader.jsx
        AnaliseSummaryCard.jsx
        MaturidadeCard.jsx
        GargalosList.jsx
        RiscosList.jsx
        MelhoriasList.jsx
        AutomacoesList.jsx
        OportunidadesIAList.jsx
        LacunasList.jsx
        IndicadoresList.jsx
        PerguntasList.jsx
        AlertasList.jsx
        AnaliseEmptyState.jsx
        AnaliseLoadingState.jsx

      automacoes/
        AutomacaoBoard.jsx
        AutomacaoTable.jsx
        AutomacaoFilters.jsx
        AutomacaoStatusSelect.jsx
        PrioridadeBadge.jsx
        ImpactoBadge.jsx
        EsforcoBadge.jsx
        TipoAutomacaoBadge.jsx

    services/
      analisesApi.js
      diretrizesApi.js

    utils/
      analysisFormatters.js

Também atualizar:

frontend/src/App.jsx
frontend/src/pages/ProcessoDetalhe.jsx
frontend/src/pages/Dashboard.jsx
frontend/src/components/layout/Sidebar.jsx
frontend/src/styles/global.css
docs/backlog.md
docs/changelog.md
docs/tests.md
TASK-090 — Criar services de análises e diretrizes
Objetivo

Centralizar chamadas HTTP relacionadas à IA e automações.

Arquivos impactados
frontend/src/services/analisesApi.js
frontend/src/services/diretrizesApi.js
frontend/src/services/api.js
Funções obrigatórias em analisesApi.js
gerarAnalise(processoId)
listarAnalises(processoId)
obterAnalise(analiseId)
Funções obrigatórias em diretrizesApi.js
listarDiretrizes(processoId)
atualizarDiretriz(diretrizId, payload)
Regras
Usar o client base api.js.
Não duplicar VITE_API_URL.
Tratar erro de API offline.
Propagar mensagem amigável.
Não incluir nenhuma chave OpenAI no frontend.
Critérios de aceite
Dado que VITE_API_URL está configurado,
quando chamar gerarAnalise,
então a requisição deve ir para POST /api/processos/{id}/analises.

Dado que listarAnalises é chamado,
quando o backend responder,
então deve retornar a lista de análises do processo.

Dado que atualizarDiretriz é chamado com status válido,
quando o backend responder,
então deve retornar a diretriz atualizada.

Dado que a API falha,
quando qualquer service receber erro,
então deve propagar mensagem controlada para a interface.
TASK-091 — Ativar ações de IA no detalhe do processo
Objetivo

Atualizar a tela de detalhe do processo para permitir análise IA e acesso às telas relacionadas.

Arquivo impactado
frontend/src/pages/ProcessoDetalhe.jsx
Ações obrigatórias

Adicionar ou ativar botões:

Analisar com IA
Ver análises
Ver automações
Comportamento
Botão “Analisar com IA”

Ao clicar:

1. Exibir estado de loading no botão.
2. Chamar gerarAnalise(processoId).
3. Se sucesso, navegar para /processos/:id/analises/:analiseId.
4. Se erro, exibir mensagem amigável.
Botão “Ver análises”

Navegar para:

/processos/:id/analises
Botão “Ver automações”

Navegar para:

/processos/:id/automacoes
Tratamento de erros esperado

Se o backend retornar processo sem etapas:

"O processo precisa ter pelo menos uma etapa cadastrada antes da análise IA."

Se OpenAI não estiver configurada:

"O serviço de IA ainda não está configurado. Verifique a configuração do backend."

Se falha genérica:

"Não foi possível gerar a análise agora. Tente novamente em instantes."
Critérios de aceite
Dado que o processo existe,
quando abrir o detalhe,
então os botões Analisar com IA, Ver análises e Ver automações devem aparecer.

Dado que o usuário clica em Analisar com IA,
quando a análise estiver sendo gerada,
então o botão deve mostrar loading e evitar duplo clique.

Dado que a análise é gerada com sucesso,
quando o backend retornar,
então o usuário deve ser levado para o detalhe da análise.

Dado que o processo não possui etapas,
quando tentar analisar,
então deve aparecer erro amigável.
TASK-092 — Criar rotas de análise e automações
Objetivo

Adicionar rotas frontend para listar análises, visualizar análise específica e listar diretrizes.

Arquivo impactado
frontend/src/App.jsx
Rotas obrigatórias
/processos/:id/analises
/processos/:id/analises/:analiseId
/processos/:id/automacoes
Páginas
Analises.jsx
AnaliseDetalhe.jsx
Automacoes.jsx
Critérios de aceite
Dado que o usuário acessa /processos/:id/analises,
quando a rota carregar,
então deve exibir lista de análises do processo.

Dado que o usuário acessa /processos/:id/analises/:analiseId,
quando a rota carregar,
então deve exibir a análise específica.

Dado que o usuário acessa /processos/:id/automacoes,
quando a rota carregar,
então deve exibir as diretrizes de automação do processo.
TASK-093 — Criar página de listagem de análises
Objetivo

Exibir análises anteriores de um processo.

Arquivo impactado
frontend/src/pages/Analises.jsx
Componentes sugeridos
Card
Badge
LoadingState
ErrorState
EmptyState
Button
Conteúdo da lista

Cada análise deve exibir:

ID da análise
Data de criação
Resumo executivo curto
Nível de maturidade
Botão "Abrir análise"
Regras
Buscar processo para exibir título.
Buscar análises pelo processo.
Ordenar visualmente por data mais recente primeiro, caso backend não ordene.
Estado vazio deve orientar o usuário a gerar a primeira análise.
Botão “Gerar nova análise” deve chamar o mesmo fluxo de geração.
Critérios de aceite
Dado que existem análises salvas,
quando abrir a página de análises,
então elas devem aparecer em cards ou lista.

Dado que não existem análises,
quando abrir a página,
então deve aparecer estado vazio.

Dado que clicar em Abrir análise,
quando houver análise,
então deve navegar para /processos/:id/analises/:analiseId.

Dado que clicar em Gerar nova análise,
quando sucesso,
então deve navegar para a análise recém-criada.
TASK-094 — Criar página de detalhe da análise IA
Objetivo

Renderizar visualmente o JSON estruturado da análise IA.

Arquivo impactado
frontend/src/pages/AnaliseDetalhe.jsx
Componentes obrigatórios
frontend/src/components/ia/AnaliseHeader.jsx
frontend/src/components/ia/AnaliseSummaryCard.jsx
frontend/src/components/ia/MaturidadeCard.jsx
frontend/src/components/ia/GargalosList.jsx
frontend/src/components/ia/RiscosList.jsx
frontend/src/components/ia/MelhoriasList.jsx
frontend/src/components/ia/AutomacoesList.jsx
frontend/src/components/ia/OportunidadesIAList.jsx
frontend/src/components/ia/LacunasList.jsx
frontend/src/components/ia/IndicadoresList.jsx
frontend/src/components/ia/PerguntasList.jsx
frontend/src/components/ia/AlertasList.jsx
Dados esperados

A análise possui:

id
processo_id
resumo_executivo
diagnostico_operacional
nivel_maturidade
json_resultado
created_at

json_resultado pode chegar como objeto ou string JSON, dependendo da implementação do backend. O frontend deve tratar os dois casos com segurança:

Se json_resultado for objeto, usar diretamente.
Se json_resultado for string, fazer parse seguro.
Se parse falhar, exibir erro "Não foi possível interpretar o resultado da análise."
Blocos visuais obrigatórios
Cabeçalho

Exibir:

Nome do processo
Data da análise
Nível de maturidade
Botão voltar
Botão ver automações
Resumo

Exibir:

resumo_executivo
diagnostico_operacional
Maturidade

Exibir:

nível
justificativa
Listas estruturadas

Exibir se existirem:

pontos_fortes
gargalos
riscos
sugestoes_melhoria
sugestoes_automacao
oportunidades_ia
lacunas_mapeamento
indicadores_recomendados
perguntas_para_aprofundamento
alertas
Diretriz visual
Usar cards separados por tema.
Usar badges para impacto, esforço, prioridade e severidade.
Alertas devem ter destaque visual.
Lacunas devem ser apresentadas como pontos de melhoria no mapeamento.
Perguntas devem ser exibidas como checklist para o gestor.
Critérios de aceite
Dado que existe análise salva,
quando abrir o detalhe,
então resumo executivo e diagnóstico devem aparecer.

Dado que a análise possui gargalos,
quando renderizar,
então cada gargalo deve mostrar título, descrição, etapa relacionada e impacto.

Dado que a análise possui riscos,
quando renderizar,
então cada risco deve mostrar tipo, severidade e mitigação.

Dado que a análise possui sugestões de automação,
quando renderizar,
então cada sugestão deve mostrar impacto, esforço, prioridade e pré-requisitos.

Dado que json_resultado está inválido,
quando abrir a análise,
então o frontend deve exibir erro amigável sem quebrar a aplicação.
TASK-095 — Criar componentes visuais da análise
Objetivo

Criar componentes reutilizáveis para cada seção da análise.

Arquivos impactados
frontend/src/components/ia/AnaliseSummaryCard.jsx
frontend/src/components/ia/MaturidadeCard.jsx
frontend/src/components/ia/GargalosList.jsx
frontend/src/components/ia/RiscosList.jsx
frontend/src/components/ia/MelhoriasList.jsx
frontend/src/components/ia/AutomacoesList.jsx
frontend/src/components/ia/OportunidadesIAList.jsx
frontend/src/components/ia/LacunasList.jsx
frontend/src/components/ia/IndicadoresList.jsx
frontend/src/components/ia/PerguntasList.jsx
frontend/src/components/ia/AlertasList.jsx
frontend/src/utils/analysisFormatters.js
Regras
Cada componente recebe dados por props.
Cada componente deve lidar com lista vazia.
Não fazer chamada de API dentro desses componentes.
Badges devem ser reutilizados quando possível.
Não duplicar lógica de formatação.
analysisFormatters.js

Criar helpers para:

parseAnaliseResultado(json_resultado)
getImpactoVariant(impacto)
getPrioridadeVariant(prioridade)
getSeveridadeVariant(severidade)
formatDateTime(date)
safeList(value)
Critérios de aceite
Dado que uma lista está vazia,
quando o componente renderizar,
então ele não deve quebrar.

Dado que impacto é Alto,
quando exibir badge,
então deve usar destaque visual maior.

Dado que prioridade é Alta,
quando exibir badge,
então deve ser claramente visível.

Dado que json_resultado está como string válida,
quando parsear,
então deve retornar objeto.
TASK-096 — Criar tela de diretrizes de automação
Objetivo

Exibir as diretrizes de automação geradas pela análise IA e permitir atualização de status.

Arquivo impactado
frontend/src/pages/Automacoes.jsx
Componentes obrigatórios
frontend/src/components/automacoes/AutomacaoBoard.jsx
frontend/src/components/automacoes/AutomacaoTable.jsx
frontend/src/components/automacoes/AutomacaoFilters.jsx
frontend/src/components/automacoes/AutomacaoStatusSelect.jsx
frontend/src/components/automacoes/PrioridadeBadge.jsx
frontend/src/components/automacoes/TipoAutomacaoBadge.jsx
Campos exibidos
Título
Tipo
Descrição
Prioridade
Impacto, se existir
Esforço, se existir
Primeiro passo, se existir
Dependências
Critério de sucesso
Status
Data de criação
Filtros
prioridade
tipo
status
texto livre
Status permitidos
Sugerida
Em avaliação
Priorizada
Em implementação
Concluída
Descartada
Regras
Buscar diretrizes pelo processo.
Exibir estado vazio quando não houver diretrizes.
Atualizar status chamando PUT /api/diretrizes/{id}.
Após atualizar, refletir novo status na tela.
Se atualização falhar, reverter visualmente ou recarregar dados.
Não permitir status fora dos permitidos.
Critérios de aceite
Dado que existem diretrizes,
quando abrir /processos/:id/automacoes,
então elas devem aparecer.

Dado que não existem diretrizes,
quando abrir a tela,
então deve aparecer estado vazio orientando gerar análise IA.

Dado que o usuário altera status para Priorizada,
quando salvar,
então o novo status deve persistir.

Dado que o backend retorna erro ao atualizar status,
quando falhar,
então deve aparecer erro amigável.

Dado que o usuário filtra por prioridade Alta,
quando aplicar filtro,
então apenas diretrizes de prioridade Alta devem aparecer.
TASK-097 — Atualizar Dashboard com indicadores de IA e automação
Objetivo

Melhorar o dashboard inicial com indicadores derivados dos dados já disponíveis.

Arquivo impactado
frontend/src/pages/Dashboard.jsx
frontend/src/components/dashboard/MetricCard.jsx
frontend/src/services/analisesApi.js
frontend/src/services/diretrizesApi.js
Atenção

O backend ainda não possui endpoint agregado de métricas. Portanto, o dashboard pode calcular parcialmente a partir dos processos e, se viável sem complexidade excessiva, buscar análises/diretrizes por processo.

Indicadores permitidos
Total de processos
Processos críticos
Processos em rascunho
Processos analisados
Processos sem análise
Total de diretrizes de automação
Diretrizes priorizadas
Regra de complexidade

Se buscar análises/diretrizes para todos os processos gerar muitas chamadas ou complexidade excessiva, manter apenas:

Total de processos
Processos críticos
Processos por status
Processos por área
Cards "IA Insights" e "Automações" como próximos indicadores

Registrar em docs/backlog.md a necessidade futura de endpoint /api/dashboard/metrics.

Critérios de aceite
Dado que existem processos,
quando abrir dashboard,
então indicadores básicos devem aparecer.

Dado que existem processos analisados,
quando os dados estiverem disponíveis,
então dashboard deve refletir análises.

Dado que não for implementado endpoint agregado,
quando atualizar documentação,
então deve registrar melhoria futura para métricas consolidadas.
TASK-098 — Estados de loading, erro, vazio e sucesso
Objetivo

Garantir UX consistente nas telas de análise e automação.

Arquivos impactados
frontend/src/pages/Analises.jsx
frontend/src/pages/AnaliseDetalhe.jsx
frontend/src/pages/Automacoes.jsx
frontend/src/components/common/LoadingState.jsx
frontend/src/components/common/ErrorState.jsx
frontend/src/components/common/EmptyState.jsx
frontend/src/styles/global.css
Estados obrigatórios
Analises.jsx
loading ao buscar análises
erro se API falhar
vazio se não houver análise
sucesso com lista
loading ao gerar nova análise
AnaliseDetalhe.jsx
loading ao buscar análise
erro se análise não existir
erro se JSON estiver inválido
sucesso com análise renderizada
Automacoes.jsx
loading ao buscar diretrizes
erro se API falhar
vazio se não houver diretrizes
sucesso com lista/tabela
loading ao atualizar status
erro ao atualizar status
Critérios de aceite
Dado que a API demora,
quando abrir qualquer tela do pacote,
então deve aparecer loading.

Dado que a API falha,
quando abrir qualquer tela do pacote,
então deve aparecer erro amigável.

Dado que não há dados,
quando abrir análises ou automações,
então deve aparecer estado vazio orientativo.

Dado que uma ação é concluída,
quando salvar ou gerar análise,
então deve haver feedback visual.
TASK-099 — Atualizar documentação
Objetivo

Atualizar documentação operacional do projeto.

Arquivos impactados
docs/backlog.md
docs/changelog.md
docs/tests.md
docs/spec.md
docs/architecture.md
docs/backlog.md

Marcar como concluídas ou em andamento:

TASK-090 — Criar services de análises e diretrizes
TASK-091 — Ativar ações de IA no detalhe do processo
TASK-092 — Criar rotas de análise e automações
TASK-093 — Criar página de listagem de análises
TASK-094 — Criar página de detalhe da análise IA
TASK-095 — Criar componentes visuais da análise
TASK-096 — Criar tela de diretrizes de automação
TASK-097 — Atualizar Dashboard com indicadores de IA e automação
TASK-098 — Estados de loading, erro, vazio e sucesso
docs/changelog.md

Adicionar:

## 0.6.0

- Criados services frontend para análises IA.
- Criados services frontend para diretrizes de automação.
- Ativado botão "Analisar com IA" no detalhe do processo.
- Criada tela de listagem de análises do processo.
- Criada tela de detalhe da análise IA.
- Criados componentes visuais para resumo, maturidade, gargalos, riscos, melhorias, automações, oportunidades IA, lacunas, indicadores, perguntas e alertas.
- Criada tela de diretrizes de automação.
- Implementada atualização de status das diretrizes.
- Adicionados filtros de automações.
- Melhorados estados de loading, erro, vazio e sucesso.
docs/tests.md

Adicionar checklist:

- Botão Analisar com IA validado.
- Loading de geração de análise validado.
- Processo sem etapas exibe erro amigável.
- Listagem de análises validada.
- Detalhe da análise validado.
- Parse de json_resultado validado.
- Gargalos renderizados.
- Riscos renderizados.
- Sugestões de melhoria renderizadas.
- Sugestões de automação renderizadas.
- Lacunas e perguntas renderizadas.
- Alertas renderizados.
- Tela de automações validada.
- Atualização de status de diretriz validada.
- Filtros de automações validados.
Testes manuais obrigatórios

Registrar e executar:

1. Criar processo.
2. Criar pelo menos uma etapa no editor visual.
3. Voltar ao detalhe do processo.
4. Clicar em Analisar com IA.
5. Confirmar loading no botão.
6. Confirmar navegação para detalhe da análise.
7. Validar resumo executivo.
8. Validar diagnóstico operacional.
9. Validar nível de maturidade.
10. Validar gargalos.
11. Validar riscos.
12. Validar sugestões de melhoria.
13. Validar sugestões de automação.
14. Validar oportunidades IA.
15. Validar lacunas de mapeamento.
16. Validar perguntas de aprofundamento.
17. Validar alertas.
18. Abrir tela de automações.
19. Alterar status de uma diretriz.
20. Recarregar tela e confirmar status persistido.
21. Filtrar automações por prioridade.
22. Filtrar automações por tipo.
23. Filtrar automações por status.
24. Simular backend fora do ar.
25. Confirmar erro amigável.
26. Tentar analisar processo sem etapas.
27. Confirmar erro amigável.
Comandos esperados
Rodar backend
cd backend
uvicorn app.main:app --reload
Rodar frontend
cd frontend
npm install
npm run dev
Acessar frontend
http://localhost:5173
Fluxo de validação recomendado
1. Criar processo.
2. Abrir fluxo visual.
3. Criar etapas.
4. Salvar fluxo.
5. Voltar para detalhe.
6. Gerar análise IA.
7. Ver análise.
8. Ver automações.
9. Atualizar status.
Definition of Done do Pacote 06

A entrega só estará concluída quando:

[ ] analisesApi.js criado.
[ ] diretrizesApi.js criado.
[ ] Botão Analisar com IA ativado no detalhe.
[ ] Botão Ver análises ativado.
[ ] Botão Ver automações ativado.
[ ] Rota /processos/:id/analises criada.
[ ] Rota /processos/:id/analises/:analiseId criada.
[ ] Rota /processos/:id/automacoes criada.
[ ] Página de listagem de análises funciona.
[ ] Página de detalhe da análise funciona.
[ ] json_resultado é parseado com segurança.
[ ] Resumo executivo é exibido.
[ ] Diagnóstico operacional é exibido.
[ ] Maturidade é exibida.
[ ] Gargalos são exibidos.
[ ] Riscos são exibidos.
[ ] Melhorias são exibidas.
[ ] Automações são exibidas.
[ ] Oportunidades IA são exibidas.
[ ] Lacunas são exibidas.
[ ] Indicadores são exibidos.
[ ] Perguntas são exibidas.
[ ] Alertas são exibidos.
[ ] Tela de automações funciona.
[ ] Filtros de automação funcionam.
[ ] Status da diretriz pode ser atualizado.
[ ] Estados de loading existem.
[ ] Estados de erro existem.
[ ] Estados vazios existem.
[ ] Erros de API são amigáveis.
[ ] Nenhum segredo foi exposto no frontend.
[ ] Nenhuma chamada HTTP foi espalhada fora dos services.
[ ] Documentação foi atualizada.
[ ] Telas anteriores continuam funcionando.
Restrições

Não implemente neste pacote:

Login
Deploy Railway
Upload de documentos
Exportação PDF
RPA
Integração com sistemas contábeis externos
Edição do system prompt
Novo endpoint de dashboard, salvo se explicitamente necessário
Resultado esperado

Ao final deste pacote, o MVP terá o fluxo principal completo:

Cadastrar processo
→ mapear etapas visualmente
→ salvar fluxo
→ gerar análise IA
→ visualizar diagnóstico
→ consultar diretrizes de automação
→ atualizar status das oportunidades

O próximo pacote será:

Pacote 07 — Validação Final, Testes, Hardening e Deploy Railway

Ele deverá implementar:

Revisão técnica geral
Correção de inconsistências
Checklist de segurança
Validação de variáveis de ambiente
Preparação Railway
Volume persistente para SQLite
Deploy backend
Deploy frontend
Teste de persistência após redeploy
README final
Plano de homologação do MVP

---

# Checklist de Revisão após o Antigravity executar

Use este checklist antes de avançar:

```text
1. O frontend continua rodando?
2. O backend continua rodando?
3. O botão Analisar com IA aparece no detalhe?
4. O botão evita duplo clique durante loading?
5. Processo sem etapas mostra erro amigável?
6. Processo com etapas gera análise?
7. Após gerar análise, navega para o detalhe da análise?
8. A lista de análises carrega?
9. A análise específica carrega?
10. json_resultado como objeto funciona?
11. json_resultado como string funciona?
12. json_resultado inválido mostra erro amigável?
13. Maturidade aparece corretamente?
14. Gargalos aparecem?
15. Riscos aparecem?
16. Melhorias aparecem?
17. Sugestões de automação aparecem?
18. Oportunidades IA aparecem?
19. Lacunas aparecem?
20. Perguntas aparecem?
21. Alertas aparecem?
22. Tela de automações abre?
23. Diretrizes aparecem?
24. Filtro por prioridade funciona?
25. Filtro por tipo funciona?
26. Filtro por status funciona?
27. Atualização de status persiste?
28. Erro ao atualizar status é tratado?
29. Nenhum segredo foi colocado no frontend?
30. Nenhuma chamada HTTP foi feita fora dos services?
31. docs/backlog.md foi atualizado?
32. docs/changelog.md foi atualizado?
33. docs/tests.md foi atualizado?