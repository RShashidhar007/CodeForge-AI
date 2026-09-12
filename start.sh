#!/bin/bash
# Unix/Linux/macOS startup script for CodeForge AI
# Usage: ./start.sh

echo "🚀 Starting CodeForge AI Platform..."
echo ""

# Check if Docker is running
echo "Checking Docker status..."
if ! docker ps > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker and try again."
    exit 1
fi

echo "✅ Docker is running"
echo ""

# Check if .env exists
echo "Checking configuration..."
if [ ! -f "backend/.env" ]; then
    echo "⚠️  Creating backend/.env from template..."
    cp backend/.env.example backend/.env
    echo "✅ backend/.env created"
else
    echo "✅ backend/.env found"
fi

echo ""
echo "Starting services with docker-compose..."
echo ""

# Start docker-compose
docker-compose up --build

# Check exit code
if [ $? -eq 0 ]; then
    echo ""
    echo "✅ Services started successfully!"
    echo ""
    echo "Access points:"
    echo "  • Frontend:   http://localhost:5173"
    echo "  • Backend:    http://localhost:8080"
    echo "  • API Docs:   http://localhost:8080/docs"
    echo "  • ReDoc:      http://localhost:8080/redoc"
    echo ""
    echo "Demo Accounts:"
    echo "  • Admin:      admin@example.com / Admin123!"
    echo "  • Candidate:  alice@student.com / Student123!"
    echo "  • Recruiter:  sarah@recruiter.com / Recruiter123!"
    echo ""
    echo "Press Ctrl+C to stop services"
else
    echo ""
    echo "❌ Failed to start services"
    exit 1
fi
