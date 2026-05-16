"""
conftest.py — Fixtures compartilhadas para toda a suíte de testes.

Estratégia:
- Usa SQLite em memória com URL única por sessão de teste (:memory: com URI mode)
  para garantir que as tabelas existam no engine correto que o TestClient usa.
- O override de get_db aponta para o mesmo engine_test que tem as tabelas criadas.
"""
import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from fastapi.testclient import TestClient

from app.database.base import Base
from app.database.session import get_db
from app.main import app

# SQLite em memória com StaticPool garante que a mesma conexão
# seja reutilizada pelo TestClient e pelas fixtures.
TEST_DATABASE_URL = "sqlite://"

engine_test = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,   # <- conexão única compartilhada; crítico para :memory:
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function", autouse=True)
def setup_test_db():
    """Cria e destrói todas as tabelas a cada teste — isolamento garantido."""
    Base.metadata.create_all(bind=engine_test)
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture(scope="function")
def db_session(setup_test_db):
    """Sessão de banco de dados para injeção direta nos testes."""
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture(scope="function")
def client(setup_test_db):
    """TestClient com override do get_db apontando para o banco em memória."""
    with TestClient(app) as c:
        yield c
