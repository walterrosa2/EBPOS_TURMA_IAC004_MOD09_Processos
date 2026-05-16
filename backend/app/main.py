import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base

# Ensure all models are imported before creating tables
from app.models import processo, etapa, conexao, analise, diretriz

from app.api.routes import processos, etapas, fluxos, analises, diretrizes

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

@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "service": "qdt-backend"}
