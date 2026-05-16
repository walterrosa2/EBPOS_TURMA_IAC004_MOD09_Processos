# Walkthrough - Pacote 03

## O que foi feito
A primeira versão funcional do frontend (React + Vite) do MVP da plataforma **QDT Processos Contábeis** foi criada seguindo as diretrizes do Pacote 03. O layout implementado foca num design de Dashboard SaaS utilizando CSS Vanilla robusto com variáveis organizadas, dispensando no momento a necessidade de frameworks CSS pesados.

### Principais Entregas
1. **Estrutura Base React + Vite:**
    - Inicializado via comando CLI padrão Vite e adicionado o React Router Dom.
    - Criado ambiente com separação semântica no `src` em `components`, `pages`, `services`, `utils` e `styles`.
    - Lógica de apontamento de API flexível via `.env.example` apontando para a porta 8000.
2. **Layout SaaS e Componentes Genéricos:**
    - **DashboardLayout**, **Header** e **Sidebar**: Layout responsivo com navegação contextual. Sidebar inclui indicações visuais de 'Em breve' para módulos futuros.
    - **Common**: Criada biblioteca nativa contendo `Card`, `Button`, `Badge`, `ConfirmDialog`, `LoadingState`, `ErrorState` e `EmptyState`.
3. **Módulo de Dashboard:**
    - Criados os cards estatísticos (Total, Criticidade Alta, Rascunhos, Analisados).
    - Lista prévia com os processos recentes mapeados.
4. **Módulo de Catálogo de Processos (CRUD UI):**
    - Listagem em tabela customizada de Processos mapeando status e criticidade em Badges coloridos.
    - Filtros por Nome, Área, Criticidade e Status ligados ao `fetch` nativo no Backend FastAPI.
    - Formulários de Inserção e Edição unificados no `ProcessoForm`, contendo todos os selects e validações.
    - Tela de Detalhamento rica exibindo os metadados em grid cardápio.
5. **Comunicação Segura Backend:**
    - Arquivo `/services/api.js` contendo envolucro para parse HTTP. Aborda graciosamente status 204 (Delete) e tratamento de erros (Offline, ou Status HTTP de falha).

## Onde no código
A base recém-criada localiza-se estritamente sob o escopo de `frontend/`:
- **Rotas Globais**: Mapeadas no arquivo de entrada principal `frontend/src/App.jsx`.
- **Serviços REST**: Interações centralizadas em `frontend/src/services/processosApi.js`.
- **Estilização**: Concentrada em `frontend/src/styles/global.css`.

## Como testar localmente
1. **Ativando o Backend:**
   No diretório principal ou no `backend/`, inicie a API:
   ```bash
   cd backend
   uvicorn app.main:app --reload
   ```
2. **Ativando o Frontend:**
   No diretório do frontend, verifique se a instalação npm transcorreu corretamente. 
   *(Nota: Se houver problemas de cache local com npm no Windows, verifique se a pasta `frontend/node_modules` tem os privilégios apropriados).*
   ```bash
   cd frontend
   npm install --force
   npm run dev
   ```
   Acesse a URL gerada (geralmente `http://localhost:5173`).

A interface gráfica deve conversar em tempo real com a base do SQLite. Crie um processo, edite, observe as exibições vazias ao apagar todos e utilize a caixa de pesquisa.
