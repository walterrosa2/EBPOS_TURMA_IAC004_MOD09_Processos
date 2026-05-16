# Revisão Técnica - Pacote 07

## Backend
- [x] main.py registra todas as rotas.
- [x] /health funciona.
- [x] CRUD de processos funciona.
- [x] CRUD de etapas funciona.
- [x] API de fluxo funciona.
- [x] API de análise IA funciona.
- [x] API de diretrizes funciona.
- [x] services concentram regra de negócio.
- [x] repositories concentram acesso ao banco.
- [x] schemas Pydantic validam entradas.
- [x] erros 400, 404, 422 e 500 são tratados.

## Frontend
- [x] rotas principais funcionam.
- [x] layout SaaS permanece consistente.
- [x] catálogo de processos funciona.
- [x] editor visual funciona.
- [x] análise IA funciona.
- [x] automações funcionam.
- [x] chamadas HTTP estão centralizadas em services.
- [x] VITE_API_URL é usado corretamente.

## IA
- [x] system prompt existe.
- [x] user prompt template existe.
- [x] resposta IA é validada antes de salvar.
- [x] JSON inválido não é persistido.
- [x] ausência de OPENAI_API_KEY gera erro controlado.

## Segurança
- [x] .env está ignorado.
- [x] chaves não estão no código.
- [x] logs não expõem dados sensíveis.
- [x] frontend não possui chave OpenAI.

## Deploy
- [x] backend possui comando de start.
- [x] frontend possui build funcional.
- [x] CORS está configurável.
- [x] SQLite usa caminho de volume em produção.
