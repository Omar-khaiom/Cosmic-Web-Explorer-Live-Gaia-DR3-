# Cosmic-Web Explorer - Startup Script (Windows PowerShell)
# Starts both backend (FastAPI on 5000) and frontend (HTTP server on 3000)
# Run: cd d:\space; ./start_all.ps1

$ErrorActionPreference = "Stop"

Write-Host "`n" -NoNewline
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "   🚀 Cosmic-Web Explorer (Gaia DR3 Live)" -ForegroundColor Blue
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Check Python
Write-Host "🔍 Checking Python..." -NoNewline
try {
    $pythonVersion = python --version 2>&1
    Write-Host " ✓ $pythonVersion" -ForegroundColor Green
}
catch {
    Write-Host " ✗ Python not found!" -ForegroundColor Red
    Write-Host "   Please install Python 3.10+ from python.org" -ForegroundColor Yellow
    exit 1
}

# Get script directory
$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path

# Check backend exists
if (-not (Test-Path "$scriptDir\backend")) {
    Write-Host "❌ Error: 'backend' directory not found" -ForegroundColor Red
    exit 1
}

# Check requirements file
if (-not (Test-Path "$scriptDir\backend\requirements.txt")) {
    Write-Host "❌ Error: 'backend/requirements.txt' not found" -ForegroundColor Red
    exit 1
}

# Install/verify dependencies
Write-Host "📦 Checking backend dependencies..." -ForegroundColor Yellow
$hasDeps = $false
try {
    python -c "import fastapi, uvicorn, astroquery" 2>$null
    $hasDeps = $true
    Write-Host "   ✓ All dependencies present" -ForegroundColor Green
}
catch {
    Write-Host "   Installing requirements (this may take a minute)..." -ForegroundColor Yellow
    pip install -q -r "$scriptDir\backend\requirements.txt"
    Write-Host "   ✓ Dependencies installed" -ForegroundColor Green
}

# Check for Gaia catalog
if (-not (Test-Path "$scriptDir\data\gaia_catalog.db")) {
    Write-Host ""
    Write-Host "⚠️  Gaia catalog not found: data/gaia_catalog.db" -ForegroundColor Yellow
    Write-Host "   Download with:" -ForegroundColor Yellow
    Write-Host "   python backend\scripts\download_gaia_catalog.py --mag-limit 7.0 --output d:\space\data\gaia_catalog.db" -ForegroundColor Cyan
    Write-Host "   Using offline fallback for now (limited stars)" -ForegroundColor Yellow
    Write-Host ""
}

# Start Backend
Write-Host "🔧 Starting Backend (FastAPI on 5000)..." -ForegroundColor Cyan
$backendCmd = "Set-Location '$scriptDir\backend'; `$env:PYTHONPATH='$scriptDir\backend'; python -m uvicorn app:app --host 0.0.0.0 --port 5000 --reload"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $backendCmd

Start-Sleep -Seconds 2

# Start Frontend
Write-Host "🎨 Starting Frontend (HTTP server on 3000)..." -ForegroundColor Cyan
$frontendCmd = "Set-Location '$scriptDir'; python -m http.server 3000"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $frontendCmd

Start-Sleep -Seconds 1

Write-Host ""
Write-Host "==========================================" -ForegroundColor Green
Write-Host "   ✅ Both servers running!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Green
Write-Host ""
Write-Host "📡 Backend API:   " -NoNewline
Write-Host "http://localhost:5000" -ForegroundColor Cyan
Write-Host "📚 API Docs:      " -NoNewline
Write-Host "http://localhost:5000/docs" -ForegroundColor Cyan
Write-Host "🌌 Viewer:        " -NoNewline
Write-Host "http://localhost:3000/viewer/index.html" -ForegroundColor Cyan
Write-Host ""
Write-Host "Press Ctrl+C in any window to stop servers" -ForegroundColor Yellow
Write-Host ""
