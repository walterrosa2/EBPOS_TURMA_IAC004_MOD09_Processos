Regras obrigatórias
Usar React Flow para o canvas.
Não implementar IA neste pacote.
Não implementar login.
Não implementar upload de documentos.
Não hardcodar URL da API.
Usar VITE_API_URL via service centralizado.
Criar services específicos para etapas e fluxo.
Não chamar fetch diretamente dentro do editor.
Salvar posições X/Y das etapas.
Salvar conexões entre etapas.
Não permitir criar etapa sem nome.
Tratar erro de API com mensagem amigável.
Manter visual SaaS moderno.
Criar painel lateral para edição de etapa.
Atualizar docs/backlog.md, docs/changelog.md e docs/tests.md.
Não criar dependências desnecessárias além de React Flow.
A aplicação deve continuar rodando com npm run dev.
Não quebrar telas existentes dos Pacotes 03.
Instalação obrigatória

Instalar React Flow no frontend:

cd frontend
npm install reactflow

Importar CSS base do React Flow em local adequado, preferencialmente no componente do editor ou em main.jsx:

import 'reactflow/dist/style.css';
Estrutura esperada após este pacote
frontend/
  src/
    pages/
      FluxoEditor.jsx

    components/
      fluxo/
        FlowEditor.jsx
        EtapaNode.jsx
        EtapaPanel.jsx
        FlowToolbar.jsx
        FlowEmptyState.jsx

    services/
      etapasApi.js
      fluxoApi.js

    utils/
      flowMappers.js

    styles/
      global.css

Também atualizar rotas em:

frontend/src/App.jsx
frontend/src/pages/ProcessoDetalhe.jsx
frontend/src/components/layout/Sidebar.jsx
TASK-060 — Instalar e configurar React Flow
Objetivo

Criar a base do editor visual de fluxo usando React Flow.

Arquivos impactados
frontend/package.json
frontend/src/App.jsx
frontend/src/pages/FluxoEditor.jsx
frontend/src/components/fluxo/FlowEditor.jsx
frontend/src/components/fluxo/EtapaNode.jsx
frontend/src/components/fluxo/FlowToolbar.jsx
frontend/src/components/fluxo/FlowEmptyState.jsx
frontend/src/styles/global.css
docs/backlog.md
docs/changelog.md
Rota obrigatória

Adicionar rota:

/processos/:id/fluxo

Essa rota deve renderizar FluxoEditor.jsx.

Comportamento esperado
1. Usuário acessa detalhe do processo.
2. Clica em "Abrir fluxo visual".
3. Sistema navega para /processos/:id/fluxo.
4. Tela carrega dados do processo.
5. Tela carrega fluxo via API.
6. Canvas é exibido.
Componentes React Flow esperados

O editor deve conter:

ReactFlow
Background
Controls
MiniMap, se ficar visualmente adequado
Critérios de aceite
Dado que o usuário está na tela de detalhe do processo,
quando clicar em "Abrir fluxo visual",
então deve navegar para /processos/:id/fluxo.

Dado que o processo existe,
quando abrir /processos/:id/fluxo,
então o canvas do React Flow deve aparecer.

Dado que o processo não possui etapas,
quando abrir o editor,
então deve aparecer estado vazio orientando criar a primeira etapa.

Dado que a API está fora do ar,
quando abrir o editor,
então deve aparecer mensagem de erro amigável.
TASK-061 — Criar services de etapas e fluxo
Objetivo

Centralizar chamadas HTTP para etapas e fluxo.

Arquivos impactados
frontend/src/services/etapasApi.js
frontend/src/services/fluxoApi.js
frontend/src/services/api.js
Funções obrigatórias em etapasApi.js
listarEtapas(processoId)
criarEtapa(processoId, payload)
atualizarEtapa(etapaId, payload)
excluirEtapa(etapaId)
Funções obrigatórias em fluxoApi.js
obterFluxo(processoId)
salvarFluxo(processoId, payload)
Regras
Usar o client base api.js.
Não duplicar VITE_API_URL.
Propagar erros com mensagens amigáveis.
Não colocar regra visual dentro dos services.
Critérios de aceite
Dado que VITE_API_URL está configurado,
quando chamar obterFluxo,
então a requisição deve ir para /api/processos/{id}/fluxo.

Dado que criarEtapa recebe payload válido,
quando chamar a função,
então deve enviar POST para /api/processos/{id}/etapas.

Dado que a API retorna erro,
quando o service receber a resposta,
então deve devolver erro controlado para o componente.
TASK-062 — Mapear dados da API para React Flow
Objetivo

Criar funções de transformação entre o formato da API e o formato do React Flow.

Arquivo impactado
frontend/src/utils/flowMappers.js
Funções obrigatórias
mapEtapasToNodes(etapas)
mapConexoesToEdges(conexoes)
mapNodesToEtapasPayload(nodes)
mapEdgesToConexoesPayload(edges)
Entrada da API

Etapa:

{
  "id": 1,
  "processo_id": 1,
  "nome": "Receber documentos",
  "descricao": "Receber documentos do cliente",
  "responsavel": "Analista",
  "entrada": "Documentos do cliente",
  "saida": "Documentos recebidos",
  "sistema_utilizado": "Portal",
  "tempo_estimado": "2 horas",
  "tipo_etapa": "Entrada de informação",
  "risco": "Atraso no envio",
  "gargalo": "Documentos incompletos",
  "oportunidade_automacao": "Checklist automático",
  "posicao_x": 120,
  "posicao_y": 80
}

Node esperado:

{
  "id": "1",
  "type": "etapaNode",
  "position": {
    "x": 120,
    "y": 80
  },
  "data": {
    "etapa": {}
  }
}

Conexão da API:

{
  "id": 1,
  "processo_id": 1,
  "etapa_origem_id": 1,
  "etapa_destino_id": 2,
  "tipo_conexao": "sequencial",
  "condicao": null
}

Edge esperado:

{
  "id": "1-2",
  "source": "1",
  "target": "2",
  "type": "smoothstep",
  "label": "sequencial"
}
Regras
IDs do React Flow devem ser string.
IDs enviados para backend devem ser número.
Se posicao_x ou posicao_y estiverem vazios, definir posição padrão.
Não perder dados originais da etapa no data.etapa.
Critérios de aceite
Dado que a API retorna etapas,
quando mapear para nodes,
então cada etapa deve virar um node válido do React Flow.

Dado que a API retorna conexões,
quando mapear para edges,
então cada conexão deve virar uma edge válida.

Dado que nodes são movidos,
quando mapear para payload,
então o payload deve conter id, posicao_x e posicao_y.

Dado que edges existem,
quando mapear para payload,
então o payload deve conter etapa_origem_id e etapa_destino_id.
TASK-063 — Criar node customizado de etapa
Objetivo

Criar componente visual para representar uma etapa no fluxo.

Arquivo impactado
frontend/src/components/fluxo/EtapaNode.jsx
Conteúdo visual do node

O node deve exibir:

Nome da etapa
Tipo da etapa, se informado
Responsável, se informado
Badge de gargalo, se houver gargalo
Badge de risco, se houver risco
Ações

Ao clicar no node:

Abrir painel lateral de edição da etapa.
Diretriz visual

O node deve parecer um card pequeno e moderno, com:

borda arredondada
sombra leve
título claro
metadados compactos
badges pequenos
handles de entrada e saída
React Flow Handles

Adicionar:

Handle target no topo ou lado esquerdo
Handle source embaixo ou lado direito
Critérios de aceite
Dado que uma etapa existe,
quando o fluxo carregar,
então a etapa deve aparecer como node customizado.

Dado que a etapa possui gargalo,
quando o node for exibido,
então deve mostrar indicação visual de gargalo.

Dado que o usuário clica no node,
quando clicar,
então o painel lateral deve abrir com dados da etapa.
TASK-064 — Criar painel lateral de etapa
Objetivo

Criar painel lateral para criar e editar dados de uma etapa.

Arquivo impactado
frontend/src/components/fluxo/EtapaPanel.jsx
Campos do painel
nome
descricao
responsavel
entrada
saida
sistema_utilizado
tempo_estimado
tipo_etapa
risco
gargalo
oportunidade_automacao
Tipos de etapa

Usar opções:

Entrada de informação
Conferência
Processamento
Aprovação
Envio
Controle
Arquivamento
Decisão
Comunicação
Outro
Comportamentos

O painel deve permitir:

Criar nova etapa
Editar etapa existente
Salvar
Cancelar
Excluir etapa existente
Validações frontend
nome é obrigatório
nome não pode ser string vazia
Regras
O painel deve receber mode: create ou edit.
Em modo create, ao salvar, chamar criarEtapa.
Em modo edit, ao salvar, chamar atualizarEtapa.
Em modo edit, exibir botão excluir.
Após salvar, recarregar ou atualizar nodes no estado local.
Após excluir, remover node e conexões relacionadas do estado local.
Exibir loading ao salvar.
Exibir erro amigável se falhar.
Critérios de aceite
Dado que o usuário clica em "Nova etapa",
quando o painel abrir,
então deve aparecer formulário vazio.

Dado que o usuário tenta salvar sem nome,
quando clicar em salvar,
então deve aparecer validação.

Dado que o usuário preenche nome válido,
quando salvar,
então a etapa deve ser criada e aparecer no canvas.

Dado que o usuário clica em uma etapa existente,
quando o painel abrir,
então os dados da etapa devem estar preenchidos.

Dado que o usuário altera uma etapa,
quando salvar,
então o node deve refletir os novos dados.

Dado que o usuário exclui uma etapa,
quando confirmar,
então a etapa deve desaparecer do canvas.
TASK-065 — Conectar etapas no canvas
Objetivo

Permitir criar conexões entre etapas usando React Flow.

Arquivo impactado
frontend/src/components/fluxo/FlowEditor.jsx
Comportamento
Usuário arrasta conexão de um node origem para um node destino.
Sistema adiciona edge no estado local.
Usuário clica em salvar fluxo.
Sistema envia conexões para backend.
Backend valida e persiste.
Regras
Não permitir conexão sem source ou target.
Evitar duplicidade exata da mesma conexão source-target.
Permitir múltiplas conexões se forem entre nodes diferentes.
Label padrão da conexão: sequencial.
Tipo visual da edge: smoothstep.
Permitir remover conexão selecionada, preferencialmente com tecla Delete/Backspace ou botão de remoção.
Critérios de aceite
Dado que existem duas etapas,
quando o usuário conectar a origem ao destino,
então uma edge deve aparecer no canvas.

Dado que a conexão já existe,
quando o usuário tentar conectar novamente as mesmas etapas,
então a conexão duplicada não deve ser criada.

Dado que o usuário remove uma conexão,
quando salvar fluxo,
então a conexão removida não deve reaparecer após recarregar.

Dado que o usuário salva o fluxo,
quando recarregar a página,
então as conexões salvas devem reaparecer.
TASK-066 — Persistir layout visual
Objetivo

Salvar posições X/Y das etapas e conexões do fluxo.

Arquivos impactados
frontend/src/components/fluxo/FlowEditor.jsx
frontend/src/services/fluxoApi.js
frontend/src/utils/flowMappers.js
Botões obrigatórios na toolbar
Nova etapa
Salvar fluxo
Recarregar
Voltar para detalhe
Payload esperado para salvar fluxo
{
  "etapas": [
    {
      "id": 1,
      "posicao_x": 120,
      "posicao_y": 80
    }
  ],
  "conexoes": [
    {
      "etapa_origem_id": 1,
      "etapa_destino_id": 2,
      "tipo_conexao": "sequencial",
      "condicao": null
    }
  ]
}
Regras
Ao mover node, atualizar estado local.
Ao clicar em salvar, enviar posições e conexões.
Após salvar, exibir mensagem de sucesso.
Ao recarregar tela, buscar fluxo do backend.
Não salvar fluxo automaticamente neste pacote; usar botão manual “Salvar fluxo”.
Critérios de aceite
Dado que o usuário move uma etapa,
quando clicar em salvar fluxo,
então a posição X/Y deve ser enviada ao backend.

Dado que o fluxo foi salvo,
quando recarregar a tela,
então os nodes devem aparecer nas posições salvas.

Dado que o usuário conecta etapas e salva,
quando recarregar a tela,
então as conexões devem aparecer.

Dado que ocorre erro ao salvar,
quando a API falhar,
então o usuário deve ver mensagem amigável e o canvas não deve quebrar.
TASK-067 — Integrar editor ao detalhe do processo
Objetivo

Atualizar a tela de detalhe para permitir abrir o editor visual.

Arquivo impactado
frontend/src/pages/ProcessoDetalhe.jsx
Comportamento

O botão que antes estava desabilitado ou “Em breve” deve ser ativado:

Abrir fluxo visual

Ao clicar:

navigate(`/processos/${id}/fluxo`)
Critérios de aceite
Dado que o usuário está no detalhe do processo,
quando clicar em Abrir fluxo visual,
então deve navegar para o editor do processo.

Dado que o usuário está no editor,
quando clicar em Voltar para detalhe,
então deve retornar para /processos/:id.
TASK-068 — Estados visuais e UX do editor
Objetivo

Garantir experiência adequada no editor.

Arquivos impactados
frontend/src/pages/FluxoEditor.jsx
frontend/src/components/fluxo/FlowEditor.jsx
frontend/src/components/fluxo/FlowEmptyState.jsx
frontend/src/components/common/LoadingState.jsx
frontend/src/components/common/ErrorState.jsx
frontend/src/styles/global.css
Estados obrigatórios
loading ao carregar fluxo
erro se API falhar
vazio se processo não possui etapas
sucesso após salvar
erro ao salvar
erro ao criar etapa
erro ao editar etapa
erro ao excluir etapa
UX mínima
Canvas deve ocupar boa parte da tela.
Toolbar deve ficar visível no topo.
Painel lateral deve ficar à direita.
Botões devem ter texto claro.
Mensagens de erro devem ser compreensíveis.
Critérios de aceite
Dado que a API demora,
quando abrir editor,
então deve aparecer loading.

Dado que o processo não possui etapas,
quando abrir editor,
então deve aparecer estado vazio com botão para criar primeira etapa.

Dado que a API falha,
quando buscar fluxo,
então deve aparecer erro amigável.

Dado que o fluxo salva com sucesso,
quando finalizar,
então deve aparecer confirmação visual.
Dados de etapa — campos e nomes esperados

Usar exatamente estes nomes ao enviar para o backend:

nome
descricao
responsavel
entrada
saida
sistema_utilizado
tempo_estimado
tipo_etapa
risco
gargalo
oportunidade_automacao
posicao_x
posicao_y

Não usar nomes alternativos como:

system
owner
input
output
risk
bottleneck
Integração esperada com API do Pacote 02

Consumir:

GET    /api/processos/{processo_id}/fluxo
PUT    /api/processos/{processo_id}/fluxo
GET    /api/processos/{processo_id}/etapas
POST   /api/processos/{processo_id}/etapas
PUT    /api/etapas/{etapa_id}
DELETE /api/etapas/{etapa_id}
GET    /api/processos/{processo_id}

Não consumir ainda:

POST   /api/processos/{processo_id}/analises
GET    /api/processos/{processo_id}/analises
GET    /api/processos/{processo_id}/diretrizes
Testes manuais obrigatórios

Registrar em docs/tests.md:

1. Abrir detalhe de um processo.
2. Clicar em Abrir fluxo visual.
3. Verificar se o editor carrega.
4. Criar primeira etapa.
5. Tentar criar etapa sem nome.
6. Editar etapa existente.
7. Mover etapa no canvas.
8. Criar segunda etapa.
9. Conectar primeira etapa à segunda.
10. Salvar fluxo.
11. Recarregar página.
12. Confirmar que posições foram preservadas.
13. Confirmar que conexão foi preservada.
14. Excluir etapa.
15. Confirmar que etapa sumiu do canvas.
16. Confirmar que conexões relacionadas sumiram.
17. Simular API fora do ar e verificar erro amigável.
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
Fluxo de teste recomendado
1. Criar processo pelo frontend.
2. Abrir detalhe do processo.
3. Abrir fluxo visual.
4. Criar etapas.
5. Conectar etapas.
6. Salvar fluxo.
7. Recarregar.
8. Validar persistência.
Atualização obrigatória da documentação
docs/backlog.md

Marcar como concluídas ou em andamento:

TASK-060 — Instalar e configurar React Flow
TASK-061 — Criar services de etapas e fluxo
TASK-062 — Mapear dados da API para React Flow
TASK-063 — Criar node customizado de etapa
TASK-064 — Criar painel lateral de etapa
TASK-065 — Conectar etapas no canvas
TASK-066 — Persistir layout visual
TASK-067 — Integrar editor ao detalhe do processo
TASK-068 — Estados visuais e UX do editor
docs/changelog.md

Adicionar:

## 0.4.0

- Implementado editor visual de fluxo com React Flow.
- Criada rota /processos/:id/fluxo.
- Criados services de etapas e fluxo.
- Criado mapeamento entre API e React Flow.
- Criado node customizado de etapa.
- Criado painel lateral para criação e edição de etapas.
- Implementada conexão visual entre etapas.
- Implementada persistência de posições X/Y.
- Implementada persistência de conexões.
- Ativado botão Abrir fluxo visual na tela de detalhe do processo.
- Adicionados estados de loading, erro, vazio e sucesso no editor.
docs/tests.md

Adicionar checklist:

- Editor visual validado.
- Criação de etapa pelo canvas validada.
- Edição de etapa pelo painel lateral validada.
- Exclusão de etapa validada.
- Conexão entre etapas validada.
- Persistência de posição X/Y validada.
- Persistência de conexões validada.
- Estado vazio do editor validado.
- Erro de API no editor validado.
Definition of Done do Pacote 04

A entrega só estará concluída quando:

[ ] React Flow instalado.
[ ] Rota /processos/:id/fluxo criada.
[ ] Botão Abrir fluxo visual ativado no detalhe.
[ ] Editor carrega fluxo da API.
[ ] Etapas aparecem como nodes.
[ ] Node customizado de etapa implementado.
[ ] Painel lateral de etapa implementado.
[ ] Criar etapa funciona.
[ ] Editar etapa funciona.
[ ] Excluir etapa funciona.
[ ] Conectar etapas funciona.
[ ] Remover conexão funciona.
[ ] Salvar fluxo envia posições X/Y.
[ ] Salvar fluxo envia conexões.
[ ] Recarregar tela reconstrói fluxo salvo.
[ ] Estados de loading, erro e vazio existem.
[ ] Erros de API são amigáveis.
[ ] URL da API não está hardcoded.
[ ] Chamada HTTP está centralizada em services.
[ ] Documentação foi atualizada.
[ ] Nenhuma chave ou segredo foi versionado.
[ ] Telas anteriores continuam funcionando.
Restrições

Não implemente neste pacote:

OpenAI
ia_service.py
system_process_mapper.md
Análise IA
Resultado IA
Diretrizes de automação
Railway deploy
Login
Upload de arquivos
Exportação PDF
Dashboard avançado de gargalos
Resultado esperado

Ao final deste pacote, o usuário deve conseguir mapear visualmente um processo contábil genérico, criar etapas, conectar atividades e persistir o fluxo para posterior análise com IA.

O próximo pacote será:

Pacote 05 — Serviço de IA com OpenAI GPT-4o + System Prompt Especialista

Ele deverá implementar:

system_process_mapper.md
user_process_analysis_template.md
ia_service.py
schema completo de resposta da IA
endpoint POST /api/processos/:id/analises
persistência da análise
geração de diretrizes de automação
tratamento de erro da OpenAI

---

# Checklist de Revisão após o Antigravity executar

Use este checklist antes de avançar:

```text
1. O frontend continua rodando em http://localhost:5173?
2. O backend continua rodando em http://localhost:8000?
3. O detalhe do processo tem botão Abrir fluxo visual?
4. A rota /processos/:id/fluxo abre corretamente?
5. O editor carrega sem erro?
6. Processo sem etapas mostra estado vazio?
7. Nova etapa é criada pelo painel?
8. Etapa sem nome é bloqueada?
9. Etapa existente pode ser editada?
10. Etapa existente pode ser excluída?
11. Duas etapas podem ser conectadas?
12. Conexão duplicada é evitada?
13. Conexão pode ser removida?
14. Mover etapa altera posição no canvas?
15. Salvar fluxo persiste posições?
16. Salvar fluxo persiste conexões?
17. Recarregar página mantém posições?
18. Recarregar página mantém conexões?
19. API fora do ar mostra erro amigável?
20. Nenhum fetch direto foi espalhado nos componentes?
21. fluxoApi.js e etapasApi.js centralizam as chamadas?
22. docs/backlog.md foi atualizado?
23. docs/changelog.md foi atualizado?
24. docs/tests.md foi atualizado?