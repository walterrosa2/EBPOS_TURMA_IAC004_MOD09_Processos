# Arquitetura

O QDT Processos Contábeis é um monorepo dividido em:

- **Frontend**: Aplicação React estruturada com Vite, utilizando React Flow para visualização e edição de processos em formato de canvas.
- **Backend**: API Python utilizando FastAPI, SQLAlchemy para ORM e SQLite para persistência, estruturada em camadas lógicas (rotas, services, schemas, models, database).
- **Integração IA**: Comunicação com a API da OpenAI (GPT-4o) para análise do fluxo estruturado salvo no SQLite e geração de diagnóstico e recomendações em formato JSON estrito (Structured Outputs).

O deploy do sistema está configurado para a infraestrutura da Railway, onde a base de dados SQLite é mantida em um volume persistente.
