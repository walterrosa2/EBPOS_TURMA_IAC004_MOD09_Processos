# Walkthrough - Pacote 04

## O que foi feito
Foi implementado com sucesso o **Editor Visual de Fluxo** para mapeamento de etapas em processos contábeis, utilizando a biblioteca `React Flow`. Este módulo compõe o Pacote 04 e foi acoplado diretamente à arquitetura React + Vite elaborada no Pacote 03, extraindo e enviando os dados das APIs REST (FastAPI) definidas no Pacote 02.

### Principais Entregas
1. **Instalação e Configuração (`reactflow`):**
    - Dependência adicionada com sucesso.
    - O CSS base (`reactflow/dist/style.css`) foi injetado globalmente no arquivo raiz (`main.jsx`).

2. **Client e Services (`etapasApi.js` e `fluxoApi.js`):**
    - A lógica de fetch foi completamente modularizada seguindo as restrições: nenhum fetch isolado ou URL de API hardcoded no corpo dos componentes visuais. O wrapper base `api.js` que consome `.env` é utilizado.

3. **Tradutores API <> React Flow (`flowMappers.js`):**
    - Desenvolvida a camada conversora de *payload*. Isso garante o isolamento da tipagem e semântica de interface visual (`Nodes` e `Edges` do React Flow) versus os contratos puristas definidos no Pydantic no Backend (onde `posicao_x` é um inteiro de backend e `id` na interface é uma String obrigatória, por exemplo).

4. **Componentes do Editor de Fluxo:**
    - `FlowEditor.jsx`: Orquestra o canvas central com estado do Painel e do Canvas, integrando Controles de Zoom e Mini-mapa nativos.
    - `EtapaNode.jsx`: Custom node desenhado com aspecto SaaS contendo *badges* dinâmicos de Risco e Gargalo. 
    - `EtapaPanel.jsx`: Componente de edição lateral que desliza ou encaixa sob o canvas para editar ou criar os meta-dados densos de uma Etapa Contábil.

5. **Interação com a Árvore de Aplicação:**
    - O botão do detalhe do Processo (antes indisponível) agora navega confiantemente para `/processos/:id/fluxo`.
    - Os estados visuais clássicos de Loading, Empty (zero etapas criadas) e Error estão embutidos. 

## Onde no código
Todo o desenvolvimento localizou-se no `frontend`:
- **Página do Editor:** `src/pages/FluxoEditor.jsx`
- **Motor do Canvas:** Diretório modular criado em `src/components/fluxo/`
- **Serviços:** `src/services/etapasApi.js`, `src/services/fluxoApi.js` e funções mappers em `src/utils/flowMappers.js`.
- **Roteador:** Em `src/App.jsx`.

## Como testar localmente
1. Com o backend e o frontend (npm run dev) em pé;
2. Acesse `Processos` e abra os **Detalhes** do processo.
3. Clique no recém-ativado botão **"Abrir Fluxo Visual"**.
4. Inicie sua experimentação:
    - Clique em **+ Nova etapa**, insira detalhes (um com risco, um com gargalo) e observe eles refletirem nos Nodes (cartões) sobre o Canvas;
    - Arraste a **Bolinha inferior** de um Node para a **Bolinha Superior** de outro Node criando o vínculo direcional;
    - Use a tecla DELETE para quebrar um vínculo se não gostou;
    - Arraste os cards para compor seu fluxo visual favorito;
    - Clique em **Salvar Fluxo** (isso disparará o PUT para o banco validando o Schema do Pydantic).
    - Dê um refresh (`F5`) no seu navegador ou clique em *Recarregar*! Seus cards ressurgirão exatamente nos pontos deixados.
