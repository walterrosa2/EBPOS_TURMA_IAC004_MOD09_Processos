# QDT Processos Contábeis - Backend

API responsável pela regra de negócios de processos, fluxos e pela orquestração com a IA da OpenAI.

## Stack
- FastAPI, Pydantic, SQLAlchemy, Uvicorn.
- DB local: SQLite (`qdt_processos.db`).

## Instalação e Execução
1. Criar ambiente virtual: `python -m venv venv`
2. Ativar ambiente: `venv\Scripts\activate` (Windows) ou `source venv/bin/activate` (Mac/Linux).
3. Instalar dependências: `pip install -r requirements.txt`
4. Configurar `.env` baseando-se em `.env.example`.
5. Rodar o servidor: `uvicorn app.main:app --reload`

## Testes Automatizados
O backend possui suíte com testes. A OpenAI é "mockada" de forma que os testes rodam em milissegundos sem cobrar custo real.
Rode os testes com:
```bash
pytest
```

## Cuidados com a Chave da OpenAI
A variável `OPENAI_API_KEY` é o motor de diagnóstico da plataforma. Nunca versione ou exiba nos logs o conteúdo desta variável.

## Configuração SQLite em Produção
Em produção (ex: Railway), evite usar `./data` para prevenir recriações de bancos e perda de dados.
A variável no deploy deve ser setada para utilizar um Volume de persistência:
`DATABASE_URL=sqlite:////app/data/qdt_processos.db`
Onde o `/app/data` deve ser o Mount Path do Volume mapeado.
