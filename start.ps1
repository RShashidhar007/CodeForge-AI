# Windows PowerShell startup script for CodeForge AI
# Usage: .\start.ps1

Write-Host "🚀 Starting CodeForge AI Platform..." -ForegroundColor Cyan
Write-Host ""

# Check if Docker is running
Write-Host "Checking Docker status..." -ForegroundColor Yellow
try {
    $dockerStatus = docker ps 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host "❌ Docker is not running. Please start Docker Desktop and try again." -ForegroundColor Red
        exit 1
    }
} catch {
    Write-Host "❌ Docker is not installed. Please install Docker Desktop." -ForegroundColor Red
    exit 1
}

Write-Host "✅ Docker is running" -ForegroundColor Green
Write-Host ""

# Check if .env exists
Write-Host "Checking configuration..." -ForegroundColor Yellow
if (-not (Test-Path "backend\.env")) {
    Write-Host "⚠️  Creating backend/.env from template..." -ForegroundColor Yellow
    Copy-Item "backend\.env.example" "backend\.env"
    Write-Host "✅ backend/.env created" -ForegroundColor Green
} else {
    Write-Host "✅ backend/.env found" -ForegroundColor Green
}

Write-Host ""
Write-Host "Starting services with docker-compose..." -ForegroundColor Yellow
Write-Host ""

# Start docker-compose
docker-compose up --build

# Check exit code
if ($LASTEXITCODE -eq 0) {
    Write-Host ""
    Write-Host "✅ Services started successfully!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access points:" -ForegroundColor Cyan
    Write-Host "  • Frontend:   http://localhost:5173" -ForegroundColor Green
    Write-Host "  • Backend:    http://localhost:8080" -ForegroundColor Green
    Write-Host "  • API Docs:   http://localhost:8080/docs" -ForegroundColor Green
    Write-Host "  • ReDoc:      http://localhost:8080/redoc" -ForegroundColor Green
    Write-Host ""
    Write-Host "Demo Accounts:" -ForegroundColor Cyan
    Write-Host "  • Admin:      admin@example.com / Admin123!" -ForegroundColor Green
    Write-Host "  • Candidate:  alice@student.com / Student123!" -ForegroundColor Green
    Write-Host "  • Recruiter:  sarah@recruiter.com / Recruiter123!" -ForegroundColor Green
    Write-Host ""
    Write-Host "Press Ctrl+C to stop services" -ForegroundColor Yellow
} else {
    Write-Host ""
    Write-Host "❌ Failed to start services" -ForegroundColor Red
    exit 1
}
