# Deploy na Railway

Este documento orienta o deploy da aplicação (Backend e Frontend) na Railway, com foco na configuração do banco de dados SQLite persistente.

## 1. Configurando o Projeto na Railway
1. Acesse o dashboard da Railway e crie um novo projeto "Empty Project".
2. Selecione "Deploy from GitHub repo" para o Backend e Frontend (pode ser o mesmo monorepo, usando pastas raiz diferentes).

## 2. Serviço Backend (`qdt-backend`)
- **Root Directory**: `backend`
- **Variáveis de Ambiente**:
  ```env
  APP_ENV=production
  DATABASE_URL=sqlite:////app/data/qdt_processos.db
  CORS_ORIGINS=https://SEU-DOMINIO-FRONTEND-AQUI.railway.app
  OPENAI_API_KEY=sua_chave_aqui
  OPENAI_MODEL=gpt-4o
  OPENAI_TIMEOUT_SECONDS=60
  ```
- **Volume Persistente**:
  Crie um novo volume e anexe-o ao serviço do backend.
  - **Mount path**: `/app/data`

## 3. Serviço Frontend (`qdt-frontend`)
- **Root Directory**: `frontend`
- **Variáveis de Ambiente**:
  ```env
  VITE_API_URL=https://SEU-DOMINIO-BACKEND-AQUI.railway.app
  ```

## 4. Ordem e Validação de Deploy
1. Suba o serviço Backend primeiro.
2. Certifique-se de que o domínio público foi gerado e acesse a rota `/health` para garantir funcionamento 200 OK.
3. Copie o domínio do Backend e cole na variável `VITE_API_URL` do Frontend.
4. Suba o serviço Frontend.
5. Copie o domínio gerado do Frontend e coloque-o na variável `CORS_ORIGINS` do Backend.
6. Faça um redeploy do Backend para assimilar as novas permissões do CORS.

## 5. Teste de Persistência SQLite
- Acesse o Frontend publicado.
- Cadastre um novo Processo com algumas Etapas e Salve o Fluxo.
- Force um redeploy do serviço Backend na Railway.
- Assim que ele voltar, acesse o frontend e verifique se o processo, as etapas e os fluxos permanecem salvos (provando que o volume em `/app/data` está funcionando e não foi zerado).
