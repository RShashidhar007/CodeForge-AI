# Setup Guide - Recruitment Platform

## Quick Start (5 minutes)

### Prerequisites
- Docker & Docker Compose installed
- Git installed

### 1. Clone Repository
```bash
git clone https://github.com/your-org/recruitment-platform.git
cd recruitment-platform
```

### 2. Configure Environment
```bash
# Copy example environment file
cp backend/.env.example backend/.env

# Edit backend/.env with your settings:
# - DB_URL: PostgreSQL connection string
# - JWT_SECRET: Strong random secret (min 32 chars)
# - ADMIN_EMAIL: Initial admin account
# - ADMIN_PASSWORD: Initial admin password
# - LLM_API_KEY: OpenAI API key (optional, for AI features)

nano backend/.env  # or use your editor
```

### 3. Start System
```bash
# Start all services (PostgreSQL, Redis, Backend, Frontend)
docker-compose up --build

# Wait for messages:
# - "postgres is ready"
# - "Backend running on 8080"
# - "Vite ready in Xms"
```

### 4. Access Application
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs

### 5. Login
```
Email:    admin@example.com
Password: Admin123!
```

---

## Full Setup (Local Development)

### Prerequisites
- Python 3.12+
- Node.js 18+
- PostgreSQL 16+ (or Docker)
- Git

### Backend Setup

**1. Navigate to backend:**
```bash
cd backend
```

**2. Create virtual environment:**
```bash
# Linux/Mac
python -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**3. Install dependencies:**
```bash
pip install -r requirements.txt
```

**4. Configure environment:**
```bash
cp .env.example .env
# Edit .env with your settings
```

**5. Initialize database:**
```bash
# Run migrations
alembic upgrade head

# Verify (should show all tables)
psql -U postgres -d recruitment_platform -c "\dt"
```

**6. Start backend:**
```bash
python -m app.main

# Or with uvicorn directly:
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

Backend will be available at:
- API: http://localhost:8080
- Docs: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Frontend Setup

**1. Navigate to frontend:**
```bash
cd frontend
```

**2. Install dependencies:**
```bash
npm install
```

**3. Configure environment (optional):**
```bash
# Create .env.local if backend is on non-standard port
echo "VITE_API_BASE_URL=http://localhost:8080/api" > .env.local
```

**4. Start development server:**
```bash
npm run dev

# Frontend will be at http://localhost:5173
```

---

## Environment Configuration

### Backend (.env)

**Required:**
```env
# Database
DB_URL=postgresql://postgres:password@localhost:5432/recruitment_platform

# Security
JWT_SECRET=your-super-secret-key-at-least-32-characters-long

# Admin Bootstrap
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SecurePassword123!
```

**Optional (AI Features):**
```env
# LLM Configuration
LLM_PROVIDER=openai           # or 'mock' for testing
LLM_MODEL=gpt-4-turbo
LLM_API_KEY=sk-your-api-key-here

# Embeddings
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=sk-your-api-key-here

# Cache
REDIS_URL=redis://localhost:6379

# Other
PORT=8080
JWT_EXPIRATION_SECONDS=86400
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
```

### Frontend (.env.local)

```env
VITE_API_BASE_URL=http://localhost:8080/api
```

---

## Database Setup

### Using Docker (Recommended)
```bash
# Start PostgreSQL with pgvector
docker-compose up -d postgres

# Verify it's running
docker exec recruitment-platform-postgres pg_isready -U postgres
```

### Using Local PostgreSQL
```bash
# Create database
createdb recruitment_platform

# Create pgvector extension
psql -d recruitment_platform -c "CREATE EXTENSION IF NOT EXISTS vector;"

# Run migrations
cd backend
alembic upgrade head
```

---

## Testing

### Backend Tests
```bash
cd backend

# Run all tests
pytest -v

# With coverage
pytest --cov=app --cov-report=html

# Specific test file
pytest tests/test_auth.py -v
```

### Frontend Tests
```bash
cd frontend

# Type checking
npx tsc -b --noEmit

# Build check
npm run build

# Linting
npm run lint
```

---

## Troubleshooting

### Port Already in Use

**Frontend (5173):**
```bash
# Find process
lsof -i :5173  # Mac/Linux
netstat -ano | findstr :5173  # Windows

# Kill process
kill -9 <PID>  # Mac/Linux
taskkill /PID <PID> /F  # Windows

# Or use different port
npm run dev -- --port 3000
```

**Backend (8080):**
```bash
# Similar process to frontend
lsof -i :8080
# Kill process
```

### Database Connection Failed

```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection string in .env
# Should be: postgresql://user:password@host:port/dbname

# Test connection
psql -U postgres -h localhost -d recruitment_platform

# If using Docker
docker exec recruitment-platform-postgres psql -U postgres -d recruitment_platform -c "\dt"
```

### Frontend Can't Connect to Backend

```bash
# 1. Verify backend is running
curl http://localhost:8080/actuator/health

# 2. Check CORS configuration in backend/.env
# Should include http://localhost:5173

# 3. Check .env.local in frontend
# VITE_API_BASE_URL should be http://localhost:8080/api

# 4. Clear frontend cache
# Delete node_modules and .next (if exists)
rm -rf frontend/node_modules
npm install --prefix frontend
```

### Docker Issues

```bash
# Clean everything and start fresh
docker-compose down -v

# Rebuild images
docker-compose build --no-cache

# Start again
docker-compose up --build

# View logs
docker-compose logs -f

# Check specific service
docker-compose logs backend
docker-compose logs postgres
```

---

## Git Workflow

### Before Committing

**1. Check for secrets:**
```bash
# Make sure no .env files are staged
git status | grep -i env

# Remove if accidentally added
git rm --cached backend/.env
git rm --cached frontend/.env.local
```

**2. Run tests:**
```bash
# Backend
cd backend && pytest -v && cd ..

# Frontend
cd frontend && npm run lint && cd ..
```

**3. Format code:**
```bash
# Backend
cd backend && black . && ruff check . && cd ..

# Frontend
cd frontend && npm run format && cd ..
```

### Making a Commit

```bash
# Stage specific files (not whole directories)
git add backend/app/services/new_service.py
git add frontend/src/pages/NewPage.tsx
git add README.md

# Commit with descriptive message
git commit -m "Add feature: implement X component"

# Push to remote
git push origin feature/your-feature
```

### Creating Pull Request

1. Push your branch to GitHub
2. Create PR with:
   - Clear title
   - Description of changes
   - Testing performed
   - Screenshots (if UI changes)
3. Request review
4. Address feedback

---

## Common Tasks

### Adding Dependencies

**Backend:**
```bash
cd backend

# Add package
pip install new-package

# Update requirements
pip freeze > requirements.txt

# Commit changes
git add requirements.txt
git commit -m "Add dependency: new-package"
```

**Frontend:**
```bash
cd frontend

# Add package
npm install new-package

# Commit changes
git add package.json package-lock.json
git commit -m "Add dependency: new-package"
```

### Database Migrations

```bash
cd backend

# Create migration after model changes
alembic revision --autogenerate -m "Add new column to users table"

# Review migration file
vim alembic/versions/001_add_new_column.py

# Apply migration
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### Resetting Development Environment

```bash
# Stop Docker
docker-compose down -v

# Delete Python cache
find . -type d -name __pycache__ -exec rm -r {} +
find . -name "*.pyc" -delete

# Delete Node modules
rm -rf frontend/node_modules

# Start fresh
docker-compose up --build
```

---

## Production Deployment

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] No uncommitted changes
- [ ] Environment variables configured
- [ ] Database backups enabled
- [ ] HTTPS configured
- [ ] Rate limiting configured
- [ ] Logging/monitoring set up

### Deployment Steps

```bash
# 1. Build production images
docker build -t recruitment-platform-api:v1.0 ./backend
docker build -t recruitment-platform-web:v1.0 ./frontend

# 2. Push to registry
docker push your-registry/recruitment-platform-api:v1.0
docker push your-registry/recruitment-platform-web:v1.0

# 3. Deploy with production compose file
docker-compose -f docker-compose.prod.yml up -d

# 4. Run migrations
docker exec recruitment-platform-api alembic upgrade head

# 5. Verify health
curl https://your-domain.com/actuator/health
```

---

## Support & Documentation

- **README.md** - Project overview
- **docs/MONTH4_GETTING_STARTED.md** - Testing guide
- **docs/MONTH4_EXECUTIVE_SUMMARY.md** - Architecture overview
- **docs/MONTH4_TEST_PLAN.md** - Comprehensive test scenarios
- **API Docs**: http://localhost:8080/docs (when running)

---

## Security Reminders

⚠️ **NEVER:**
- Commit `.env` files
- Commit `.env.local` files
- Hardcode credentials in code
- Use weak passwords
- Skip security checks

✅ **ALWAYS:**
- Use strong, random JWT secrets
- Use strong admin passwords
- Use HTTPS in production
- Keep dependencies updated
- Review security warnings

---

**Ready to start?** → Follow the Quick Start section above! 🚀

