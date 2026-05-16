# Plano de Tasks v2.0 — Autenticação, Multi-Tenancy e OCR

Este backlog detalha os passos para evolução do sistema para SaaS B2B Multi-tenant com Ingestão Documental.

## Épico 10 — Infraestrutura Base V2
- [ ] **TASK-111** — Migração de Banco: Avaliar e migrar SQLite para PostgreSQL (Railway) caso o volume previsto justifique, ou garantir arquitetura flexível.
- [ ] **TASK-112** — Schema Base: Criar tabela `Tenants` (Empresas) e `Users` (Usuários com roles).
- [ ] **TASK-113** — Alterações nas tabelas existentes: Adicionar `tenant_id` em Processos, Etapas, Análises e Diretrizes.

## Épico 11 — Autenticação e Autorização (Backend)
- [ ] **TASK-120** — Configurar camada de segurança: Instalar Passlib, Bcrypt e PyJWT.
- [ ] **TASK-121** — Criar endpoints de Auth: `POST /api/auth/register`, `POST /api/auth/login`.
- [ ] **TASK-122** — Criar Middleware/Dependência do FastAPI (`get_current_user`) para validar JWT.
- [ ] **TASK-123** — Implementar lógica de escopo de Tenant: A dependência de Auth deve garantir que todas as queries de Processo tenham `.filter(tenant_id == current_user.tenant_id)`.

## Épico 12 — Autenticação (Frontend)
- [ ] **TASK-130** — Configurar Contexto de Auth no React (`AuthContext`).
- [ ] **TASK-131** — Criar telas públicas: Login e Cadastro de Empresa/Usuário.
- [ ] **TASK-132** — Proteger rotas privadas: Criar `ProtectedRoute` envolvendo as telas do Dashboard.
- [ ] **TASK-133** — Persistir e Injetar Token: Configurar Axios Interceptors para enviar o token JWT no header `Authorization`.

## Épico 13 — Storage e Arquivos
- [ ] **TASK-140** — Criar tabela `Documentos` vinculada a Processos/Etapas.
- [ ] **TASK-141** — Configurar provedor de Storage (ex: bucket S3 / Railway Volume via FastAPI UploadFile).
- [ ] **TASK-142** — Endpoint `POST /api/processos/{id}/documentos` para receber e salvar os anexos.
- [ ] **TASK-143** — Componente React UI para gerenciar (Drag & Drop) uploads na tela de Detalhes do Processo.

## Épico 14 — Ingestão Documental IA
- [ ] **TASK-150** — Integrar Google Cloud Vision API ou Gemini Multimodal SDK para processamento OCR de arquivos PDF/Imagens.
- [ ] **TASK-151** — Criar task de background que lê o arquivo recém-subido, extrai o texto e salva o extrato no banco de dados.
- [ ] **TASK-152** — Evoluir `system_process_mapper.md`: Otimizar o prompt da Análise GPT-4o para consumir a "Transcrição dos Documentos", identificando automaticamente regras contábeis ocultas.
- [ ] **TASK-153** — Homologação da IA combinada (OCR + Geração de JSON estruturado).

## Épico 15 — Qualidade e Deploy
- [ ] **TASK-160** — Atualizar testes unitários e de integração forçando Autenticação.
- [ ] **TASK-161** — Revisão de Segurança (Hardening contra vazamento de tenant).
- [ ] **TASK-162** — Deploy V2.0 na Railway.
