# PRD v2.0 — QDT Processos Contábeis (SaaS Multi-Tenant)

## 1. Visão do Produto
Após a validação bem-sucedida do MVP, a plataforma QDT Processos Contábeis avança para a versão 2.0. O objetivo agora é transformar a ferramenta monousuário em um SaaS multi-tenant seguro e preparado para operação B2B. Além do isolamento de dados e gestão de acessos, o sistema agregará a capacidade de ingerir documentos reais (PDFs e imagens) via OCR/IA Multimodal para enriquecer o contexto dos processos mapeados.

## 2. Problema Atual
O MVP provou o valor da modelagem visual e da IA gerando insights e diretrizes. No entanto:
- O sistema não possui controle de acesso (qualquer pessoa vê todos os dados).
- Não há separação de dados entre diferentes empresas (Tenants).
- O mapeamento atual depende de preenchimento 100% manual. Não há suporte a documentos de suporte (ex: PDFs de manuais, laudos ou prints de tela).

## 3. Objetivo da Fase 2.0
- Implementar **Autenticação (JWT)** e **Autorização baseada em Papéis (RBAC)**.
- Implementar arquitetura **Multi-Tenant** (separação lógica de dados por Empresa).
- Permitir **Upload de Arquivos** (PDF, Imagens) vinculados a Processos e Etapas.
- Implementar **Leitura Multimodal/OCR** (ex: Google Cloud Vision ou Gemini 1.5) para extrair texto de anexos e melhorar a análise da IA.
- Expandir a persistência para suportar armazenamento de arquivos (ex: S3/Supabase ou volume estático na Railway).

## 4. Escopo Funcional (Dentro do Escopo)
| Módulo | Descrição |
|--------|-----------|
| **Autenticação** | Login, Cadastro, Recuperação de Senha, JWT Tokens. |
| **Multi-Tenancy** | Criação de "Empresas". Todos os processos pertencerão a uma Empresa. Isolamento de dados em todas as consultas. |
| **RBAC** | Perfis: `SystemAdmin`, `TenantAdmin`, `TenantUser`. |
| **Gestão de Usuários** | Tela para o `TenantAdmin` convidar e gerenciar sua equipe. |
| **Gestão de Anexos** | Upload de arquivos (PDF/PNG/JPG) nas Etapas ou Processos. Visualização/download dos mesmos. |
| **Ingestão Documental (IA)** | Extração de texto dos anexos via OCR/Visão para compor o System Prompt antes de rodar a análise de melhorias. |

## 5. Escopo Funcional (Fora do Escopo)
- Exportação automatizada de fluxos para PDF (Fase 3).
- Integração via API direta com ERPs contábeis (Sistemas Terceiros).
- Faturamento / Checkout de assinaturas (SaaS Billing fica para depois).

## 6. Decisões Técnicas
- **Autenticação:** FastAPI Users ou PyJWT para geração e validação de tokens no Backend.
- **Banco de Dados:** O SQLite deve ser avaliado; caso haja necessidade de alta concorrência por conta de muitos tenants, migrar para **PostgreSQL**.
- **Armazenamento de Arquivos:** S3 Compatível (AWS S3, MinIO, Cloudflare R2 ou Supabase Storage).
- **OCR/Visão:** Utilizar **Gemini 1.5 Flash/Pro Multimodal** ou **Google Cloud Vision** para processar os arquivos anexos antes de enviar para o GPT-4o.

## 7. Requisitos Funcionais (Novos)
- **RF23**: O sistema deve permitir o registro e login de usuários.
- **RF24**: O sistema deve agrupar usuários em Empresas (Tenants).
- **RF25**: Todas as listagens de processos, etapas, análises e diretrizes devem ser filtradas pelo Tenant logado.
- **RF26**: O sistema deve permitir upload de arquivos atrelados a um Processo.
- **RF27**: O sistema deve processar o conteúdo do arquivo (texto/imagem) e incluí-lo como contexto no envio para a IA de Análise.

## 8. Segurança e Privacidade
- Senhas salvas com hash seguro (Bcrypt).
- Tokens JWT com expiração de curto/médio prazo e Refresh Tokens.
- Arquivos em nuvem protegidos (Acesso privado ou com URLs assinadas temporárias).
- Dados de uma empresa NUNCA devem ser acessados por usuários de outra empresa.
