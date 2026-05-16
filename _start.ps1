$ErrorActionPreference = "Stop"

Write-Host "=========================================="
Write-Host "Iniciando QDT Processos Contabeis (MVP)"
Write-Host "=========================================="

# Backend
Write-Host "`n[1/2] Preparando Backend..."
cd backend
if (-not (Test-Path ".venv")) {
    Write-Host "Criando virtual environment..."
    py -3 -m venv .venv
}
. .\.venv\Scripts\Activate.ps1

Write-Host "Instalando dependencias do backend..."
pip install -r requirements.txt -q

if (-not (Test-Path ".env") -and (Test-Path ".env.example")) {
    Write-Host "Criando arquivo .env a partir do .env.example..."
    Copy-Item ".env.example" ".env"
}
cd ..

# Frontend
Write-Host "`n[2/2] Preparando Frontend..."
cd frontend
if (-not (Test-Path "node_modules")) {
    Write-Host "Instalando dependencias do frontend..."
    npm install
}
cd ..

Write-Host "`nIniciando serviços..."
Start-Process powershell -ArgumentList "-NoExit -Command `"cd backend; . .\.venv\Scripts\Activate.ps1; python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000`"" -WindowStyle Normal
Start-Process powershell -ArgumentList "-NoExit -Command `"cd frontend; npm run dev`"" -WindowStyle Normal

Write-Host "Servicos iniciados em janelas separadas!"
Write-Host "Frontend (React): http://localhost:5173"
Write-Host "Backend (API): http://localhost:8000/docs"
