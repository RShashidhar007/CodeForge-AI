#!/bin/bash
# Starts the backend stack (SQL Server + Redis + Spring Boot API) with Docker,
# then tells you how to start the frontend.
# Usage: ./start.sh
set -e

if docker compose version > /dev/null 2>&1; then
  COMPOSE="docker compose"
elif command -v docker-compose > /dev/null 2>&1; then
  COMPOSE="docker-compose"
else
  echo "Docker Compose is not installed. Install Docker Desktop or the compose plugin." >&2
  exit 1
fi

if ! docker ps > /dev/null 2>&1; then
  echo "Docker is not running. Please start Docker and try again." >&2
  exit 1
fi


cat <<'MSG'

Starting backend stack (first run downloads images and builds the API: a few minutes)

  API:          http://localhost:8080/api
  Health check: http://localhost:8080/api/actuator/health

  Admin login:  admin@example.com / Admin123!   (set ADMIN_EMAIL / ADMIN_PASSWORD to change)
  Candidates and recruiters: create accounts from the Register page.

Frontend (in a second terminal):
  cd frontend && npm install && npm run dev      -> http://localhost:5173

MSG

$COMPOSE up --build
