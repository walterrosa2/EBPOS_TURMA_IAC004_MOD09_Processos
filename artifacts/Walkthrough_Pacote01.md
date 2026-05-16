# Walkthrough - Pacote 01

## O que foi feito
A estrutura base do monorepo **QDT Processos Contábeis** foi inicializada conforme os requisitos do Pacote 01.
1. **Estrutura de Pastas e Arquivos:** Foram criadas as subpastas `frontend`, `backend`, `docs` e os respectivos arquivos iniciais (`.gitkeep`, `__init__.py`, `.gitignore`, `README.md`, etc.).
2. **Backend FastAPI:** Criado o módulo em `backend/app/` seguindo a arquitetura em camadas (`api`, `core`, `database`, `models`, `schemas`, `services`, `repositories`).
3. **Banco de Dados:** Configurado o SQLite através do SQLAlchemy. O banco é gerado de forma segura criando a pasta `data/` primeiro, impedindo erros.
4. **Modelos:** Implementados em `backend/app/models/` as entidades `Processo`, `Etapa`, `Conexao`, `AnaliseIA` e `DiretrizAutomacao`.
5. **Schemas:** Implementados em `backend/app/schemas/` os modelos do Pydantic para validação de entrada/saída com suporte a ORM (`from_attributes=True`).
6. **API Base:** Endpoint `GET /health` construído em `backend/app/main.py`.
7. **Documentação:** Toda a estrutura descrita no PRD para o diretório `/docs` foi inicializada.

## Onde no código
- Inicialização do FastAPI e das Tabelas: `backend/app/main.py`
- Validações (Schemas Pydantic): `backend/app/schemas/*`
- Tabelas e Entidades: `backend/app/models/*`
- Configuração de DB e Variáveis de Ambiente: `backend/app/core/config.py` e `backend/app/database/session.py`

## Como validar
1. Acesse o diretório `backend` através do seu terminal.
2. Ative um ambiente virtual: `python -m venv venv` e `venv\Scripts\Activate`.
3. Instale as dependências: `pip install -r requirements.txt`.
4. Inicie o servidor localmente: `uvicorn app.main:app --reload`.
5. Valide acessando no navegador a documentação: `http://localhost:8000/docs` ou testando `http://localhost:8000/health`.
6. Você pode rodar a suite de testes base com o comando: `pytest`.
