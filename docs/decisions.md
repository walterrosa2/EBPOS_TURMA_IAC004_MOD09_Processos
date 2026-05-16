# Decisões Técnicas

As decisões arquiteturais são definidas na seção "4. Decisões Técnicas Fixadas" do `prd.md`. Algumas relevantes:

- Sem login no MVP
- Visual SaaS moderno em React
- API em Python/FastAPI
- Persistência em SQLite
- Deploy na Railway
- Repositório monorepo no GitHub
- Uso do modelo LLM OpenAI GPT-4o
- Canvas com React Flow

## DEC-008 — OpenAI GPT-4o como modelo LLM do MVP.
## DEC-009 — Prompt especialista versionado no backend.
## DEC-011 — Resposta da IA validada com Pydantic antes de persistir.
## DEC-012 — Testes de IA usam mock e não chamam API externa.
