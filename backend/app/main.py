import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base

# Ensure all models are imported before creating tables
from app.models import processo, etapa, conexao, analise, diretriz

from app.api.routes import processos, etapas, fluxos, analises, diretrizes, importacao_processos

# Ensure the data directory exists
db_url = settings.DATABASE_URL
if db_url.startswith("sqlite:///"):
    # Extrair o caminho absoluto ou relativo após "sqlite:///"
    db_path = db_url.replace("sqlite:///", "")
    db_dir = os.path.dirname(os.path.abspath(db_path))
    if db_dir:
        os.makedirs(db_dir, exist_ok=True)

# Create all tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="QDT Processos Contábeis API",
    version="1.0.0",
)

# Configure CORS
origins = [origin.strip() for origin in settings.CORS_ORIGINS.split(",")] if settings.CORS_ORIGINS else []
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(processos.router)
app.include_router(etapas.router)
app.include_router(fluxos.router)
app.include_router(analises.router)
app.include_router(diretrizes.router)
app.include_router(importacao_processos.router)

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "qdt-backend"}

# ── Integração SPA (FastAPI + React) ──────────────────────────────────────────
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

# Tenta caminhos prováveis para o diretório dist do frontend (robusto local/produção)
possible_paths = [
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "frontend", "dist")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "frontend", "dist")),
    os.path.abspath(os.path.join(os.getcwd(), "frontend", "dist")),
]

frontend_path = None
for path in possible_paths:
    if os.path.exists(os.path.join(path, "index.html")):
        frontend_path = path
        break

if frontend_path:
    # Serve a pasta /assets com os estáticos compilados do React
    assets_dir = os.path.join(frontend_path, "assets")
    if os.path.exists(assets_dir):
        app.mount("/assets", StaticFiles(directory=assets_dir), name="assets")
    
    # Catch-all para servir o SPA React nas demais rotas de frontend
    @app.get("/{rest_of_path:path}")
    async def serve_frontend(rest_of_path: str):
        # Ignora rotas da API para não mascarar erros 404 reais do backend
        if rest_of_path.startswith("api/"):
            from fastapi import HTTPException
            raise HTTPException(status_code=404, detail="API endpoint not found")
        return FileResponse(os.path.join(frontend_path, "index.html"))

