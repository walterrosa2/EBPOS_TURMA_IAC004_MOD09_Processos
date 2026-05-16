@echo off
echo ==========================================
echo Iniciando QDT Processos Contabeis (MVP)
echo ==========================================

echo.
echo [1/2] Preparando Backend...
cd backend
if not exist ".venv" (
    echo Criando virtual environment...
    py -3 -m venv .venv
)
call .venv\Scripts\activate.bat

echo Instalando dependencias do backend...
pip install -r requirements.txt -q

if not exist ".env" (
    if exist ".env.example" (
        echo Criando arquivo .env a partir do .env.example...
        copy .env.example .env
    )
)
cd ..

echo.
echo [2/2] Preparando Frontend...
cd frontend
if not exist "node_modules" (
    echo Instalando dependencias do frontend...
    call npm install
)
cd ..

echo.
echo Iniciando Backend e Frontend...
start cmd /k "cd backend & .venv\Scripts\activate.bat & python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000"
start cmd /k "cd frontend & npm run dev"

echo Servicos iniciados em janelas separadas!
echo Frontend (React): http://localhost:5173
echo Backend (API): http://localhost:8000/docs
