# QDT Processos Contábeis - MVP

Aplicação web para gestores de operações contábeis mapearem, catalogarem, visualizarem e analisarem processos internos com auxílio de Inteligência Artificial para gerar diretrizes de automação.

## Stack
- **Backend:** Python, FastAPI, SQLAlchemy, SQLite, Uvicorn, OpenAI SDK.
- **Frontend:** React, Vite, React Router, React Flow (Diagramação de Processos).

## Estrutura do Projeto
O projeto segue a arquitetura de monorepo separando de forma isolada frontend, backend e documentação do produto.
- `/backend`: API construída com FastAPI.
- `/frontend`: SPA em React.
- `/docs`: Documentação técnica, requisitos, e registro de backlog.

## Fluxo Funcional (Homologado)
1. Criação e edição de um Processo.
2. Criação das Etapas do Processo.
3. Conexão visual das etapas no fluxo gerencial.
4. Geração de análise técnica através da IA (OpenAI GPT-4o).
5. Visualização do diagnóstico gerencial de gargalos, riscos, e nível de maturidade.
6. Acompanhamento do status das Diretrizes de Automação geradas pela IA.
7. **Importação inteligente de processos por documento (.docx):** upload de um manual operacional que é higienizado, interpretado por IA e cadastrado automaticamente (processo + etapas + conexões) em transação única. Endpoint: `POST /api/processos/importar`.

## Como rodar localmente

### Iniciar o Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Iniciar o Frontend
```bash
cd frontend
npm install
npm run dev
```

## Como rodar os testes
Para rodar os testes do backend via pytest:
```bash
cd backend
pytest
```

## Variáveis de Ambiente
Verifique os arquivos `.env.example` nas pastas `backend` e `frontend`. Para a IA funcionar localmente, adicione a sua própria `OPENAI_API_KEY` dentro de `backend/.env`. Não versione esta chave.

## Deploy (Railway)
A aplicação está preparada para ser publicada via Railway (veja `/docs/deployment.md` para instruções completas). Serviços separados usando comandos contidos nos `railway.toml`.

## Limitações do MVP
- Autenticação e gestão de múltiplos usuários não incluídos.
- A importação inteligente por documento suporta apenas o formato `.docx` (limite de 10 MB); outros formatos (PDF, imagens) ficam para a próxima fase.
- IA roda exclusivamente no escopo do `gpt-4o`.

## Roadmap
Consulte a documentação em `/docs/roadmap.md` para as etapas futuras do sistema.
