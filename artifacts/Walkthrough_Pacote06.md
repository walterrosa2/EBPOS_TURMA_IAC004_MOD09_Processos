# Walkthrough - Pacote 06 (Frontend IA)

## O que foi feito
A interface do gestor para visualizar os diagnósticos da Inteligência Artificial e administrar as Diretrizes de Automação foi inteiramente desenvolvida no padrão "Production-Minded", focando na componentização do React.

### Arquitetura de Comunicação:
- **`frontend/src/services/analisesApi.js`**: Implementados os métodos `gerarAnalise(id)`, `listarAnalises(id)` e `obterAnalise(analiseId)`.
- **`frontend/src/services/diretrizesApi.js`**: Implementados `listarDiretrizes(id)` e `atualizarDiretriz(diretrizId, payload)`.

### Utils de Visualização:
- **`frontend/src/utils/analysisFormatters.js`**: Centraliza o parser de JSON das análises (visto que a IA envia uma string em `json_resultado`), converte prioridades/impacto/severidade para variants de estilo do sistema (primary, warning, success, danger).

### Fluxo de Componentes (IA):
A página de detalhes da Análise tornou-se um grande dashboard segmentado com subcomponentes de responsabilidade única. Isso previne o arquivo monolítico e permite testabilidade futura:
- `MaturidadeCard.jsx`: Renderiza a nota e justificativa da maturidade do processo.
- `AnaliseSummaryCard.jsx`: O Resumo Executivo e Diagnóstico.
- `RiscosList.jsx`, `GargalosList.jsx`, `MelhoriasList.jsx`, `AutomacoesList.jsx`: Transformam as matrizes e arrays de JSON retornados pela IA em quadros com badges.
- `OportunidadesIAList.jsx`, `LacunasList.jsx`, `IndicadoresList.jsx`, `PerguntasList.jsx`, `AlertasList.jsx`: Destacam outras saídas avançadas do GPT-4o.

### Fluxo de Componentes (Automação):
- `AutomacaoBoard.jsx`: O componente orquestrador do acompanhamento das automações sugeridas.
- `AutomacaoFilters.jsx`: Filtros por texto, prioridade e status.
- `AutomacaoTable.jsx`: Tabela estilo Data-Grid listando as sugestões.
- `AutomacaoStatusSelect.jsx`: Dropdown controlável que chama a API `atualizarDiretriz` via callback onStatusChange, permitindo ao gestor gerir a execução da automação.

### Roteamento e Interação:
- Atualizado o **`ProcessoDetalhe.jsx`** para liberar os botões `Analisar com IA` (com spinner/loading block e try-catch focado nas regras de negócio da IA: erro de etapas vazias e erro de API key).
- Inseridas rotas no **`App.jsx`**.
- Atualizado **`global.css`** com os badges baseados nas diretrizes do Tailwind/Bootstrap para visuais premium.

## Como Validar
1. Acesse o Frontend (normalmente porta `5173`).
2. Acesse um Processo existente que contenha etapas (crie um processo e desenhe etapas caso não haja).
3. No detalhe do Processo, clique em **Analisar com IA** (certifique-se de que a variável `OPENAI_API_KEY` esteja válida no `.env` do backend).
4. O frontend bloqueará o botão. Assim que concluído, será redirecionado para `AnaliseDetalhe`.
5. Valide que todos os cards contêm as informações mapeadas.
6. Retorne ao detalhe do processo e clique em **Ver Automações**.
7. Teste os filtros na página de automações e mude o status de uma automação para `Priorizada`. Recarregue a página e observe que o status foi persistido (comunicação PUT ocorreu perfeitamente).

## Próximos Passos (Possíveis Otimizações)
- Atualizar a página `Dashboard.jsx` para puxar e consolidar as métricas gerais de processos e automações.
- Preparar scripts de Deploy e CI/CD.
