# ╔══════════════════════════════════════════════════════════════════════════╗
# ║  EBPOS — Dockerfile Multi-Stage                                         ║
# ║  Stage 1 (node-builder): compila o frontend React/Vite                 ║
# ║  Stage 2 (python-runtime): instala FastAPI e serve o bundle estático   ║
# ╚══════════════════════════════════════════════════════════════════════════╝

# ── Stage 1: Build do Frontend ──────────────────────────────────────────────
FROM node:20-alpine AS node-builder

WORKDIR /app/frontend

# Instala dependências primeiro (aproveita cache do Docker)
COPY frontend/package.json frontend/package-lock.json ./
RUN npm ci

# Copia o restante do código-fonte e gera o bundle de produção
COPY frontend/ ./
RUN npm run build
# Resultado em: /app/frontend/dist/


# ── Stage 2: Runtime Python (FastAPI + assets estáticos) ────────────────────
FROM python:3.11-slim AS python-runtime

# Evita buffers e cria utilizador não-root por segurança
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

WORKDIR /app

# Instala dependências Python
COPY backend/requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código do backend
COPY backend/ ./

# Copia o bundle compilado do frontend para dentro do backend
# O FastAPI vai servir esses arquivos via StaticFiles
COPY --from=node-builder /app/frontend/dist ./frontend/dist

# Cria o diretório de dados persistentes (SQLite)
RUN mkdir -p /app/data

# Expõe a porta (Railway injeta $PORT em runtime)
EXPOSE 8000

# Comando de inicialização: Railway define $PORT automaticamente
CMD ["sh", "-c", "uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}"]
