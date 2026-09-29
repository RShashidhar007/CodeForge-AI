# AI-Powered Recruitment & Code Intelligence Platform - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [Technology Stack](#technology-stack)
3. [Architecture](#architecture)
4. [Project Structure](#project-structure)
5. [Database Schema](#database-schema)
6. [API Endpoints](#api-endpoints)
7. [Features by Month](#features-by-month)
8. [Setup & Installation](#setup--installation)
9. [Environment Configuration](#environment-configuration)
10. [Demo Accounts](#demo-accounts)
11. [Running the Application](#running-the-application)
12. [Testing](#testing)
13. [Deployment](#deployment)
14. [Troubleshooting](#troubleshooting)
15. [Development Guidelines](#development-guidelines)

---

## Project Overview

### What is This?

A modern **AI-powered recruitment and code intelligence platform** built with Python FastAPI and React TypeScript. This is a full-stack application that combines:

1. **Secure Authentication** (Month 1) - JWT-based user management with roles
2. **AI Code Intelligence** (Month 2) - Semantic code search, analysis, and chat
3. **Multi-Agent AI System** (Month 3) - LangGraph orchestration with 10 specialized agents
4. **Month 4** - Comprehensive testing, security hardening, and integration verification

### Problem Statement

Technical hiring is inefficient: 
- Recruiters manually screen resumes
- Coding ability assessed inconsistently
- Code reviews are time-consuming

**Solution**: AI-assisted platform with semantic code search, conversational debugging, and automated code analysis.

### Key Capabilities

✅ Multi-role authentication (Candidate, Recruiter, Admin)  
✅ Semantic code search via embeddings  
✅ AI-powered code explanation, bug detection, testing  
✅ LangGraph multi-agent orchestration  
✅ Automated testing and code review workflows  
✅ Human approval gates for safety  
✅ Complete audit trail  

---

## Technology Stack

### Backend
- **FastAPI 0.109.0** - Async Python web framework
- **SQLAlchemy 2.0** - ORM with SQLAlchemy
- **Alembic** - Database migrations
- **PostgreSQL 16** - Primary database
- **pgvector** - Vector search extension
- **Redis** - Caching layer
- **OpenAI** - LLM and embeddings
- **LangGraph** - Multi-agent orchestration
- **Pydantic v2** - Data validation
- **pytest** - Testing framework
- **python-jose** - JWT authentication
- **passlib** - Password hashing with BCrypt

### Frontend
- **React 19** - UI library
- **TypeScript 6** - Type-safe JavaScript
- **Vite 8** - Build tool
- **Axios** - HTTP client
- **React Router** - Client-side routing

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Orchestration
- **PostgreSQL** - Database

---

## Architecture

### System Flow

```
┌─────────────┐
│   React     │
│ Frontend    │
└──────┬──────┘
       │ HTTPS
       ▼
┌──────────────────────┐
│   FastAPI Backend    │
│  ┌────────────────┐  │
│  │ REST API (27)  │  │
│  │ Services       │  │
│  │ Auth/JWT       │  │
│  │ RAG/LLM        │  │
│  │ Agents/Graph   │  │
│  └────────────────┘  │
└──────┬───────────────┘
       │
       ▼
┌─────────────────────┐
│   PostgreSQL 16     │
│   + pgvector        │
│   (20 tables)       │
└──────┬──────────────┘
       │
       ├─ Users & Auth
       ├─ Projects & Files
       ├─ AI (embeddings, conversations)
       └─ Agents (tasks, execution)
       │
       ▼
    ┌─────────┐
    │  Redis  │
    │ (Cache) │
    └─────────┘
       │
       ▼
┌─────────────────────┐
│   OpenAI API        │
│   - LLM (gpt-4)     │
│   - Embeddings      │
└─────────────────────┘
       │
       ▼
┌─────────────────────┐
│   LangGraph         │
│   (10 agents)       │
└─────────────────────┘
```

### Layered Architecture

```
┌─────────────────────────────────┐
│     HTTP Routes (Controllers)   │
│     /api/auth, /api/ai, etc     │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│      Services (Business Logic)  │
│   AuthService, RAGService, etc  │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   Repositories (Data Access)    │
│   UserRepository, etc           │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   SQLAlchemy Models (ORM)       │
│   User, Project, CodeChunk, etc │
└────────────────┬────────────────┘
                 │
┌────────────────▼────────────────┐
│   PostgreSQL + pgvector         │
│   (20 tables, embeddings)       │
└─────────────────────────────────┘
```

---

## Project Structure

```
recruitment-platform/
├── backend/                    # Python FastAPI
│   ├── app/
│   │   ├── main.py            # FastAPI entry
│   │   ├── api/routes/        # HTTP endpoints
│   │   │   ├── auth.py        # Auth routes
│   │   │   ├── admin.py       # Admin routes
│   │   │   ├── ai.py          # AI/RAG routes
│   │   │   ├── candidates.py
│   │   │   ├── recruiters.py
│   │   │   └── agent_tasks.py # Agent routes
│   │   ├── models/            # SQLAlchemy ORM
│   │   │   ├── user.py
│   │   │   ├── project.py
│   │   │   ├── ai.py          # AI models
│   │   │   └── agent_tasks.py # Agent models
│   │   ├── services/          # Business logic
│   │   │   ├── auth_service.py
│   │   │   ├── rag_service.py
│   │   │   ├── llm_provider.py
│   │   │   ├── embedding_service.py
│   │   │   └── repository_indexer.py
│   │   ├── schemas/           # Pydantic DTOs
│   │   ├── repositories/      # Data access
│   │   ├── core/              # Config, security
│   │   ├── db/                # Database setup
│   │   ├── exceptions/        # Custom exceptions
│   │   ├── agents/            # Multi-agent system
│   │   │   ├── graph/         # LangGraph workflow
│   │   │   ├── nodes/         # 10 agent implementations
│   │   │   ├── tools/         # Agent tools
│   │   │   └── state/         # State models
│   │   └── utils/             # Helpers
│   ├── alembic/               # Database migrations
│   ├── tests/                 # Test suite
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── .env.example
│   └── README.md
│
├── frontend/                  # React TypeScript
│   ├── src/
│   │   ├── pages/            # Page components
│   │   ├── components/       # Reusable components
│   │   ├── services/         # API clients
│   │   ├── types/            # TypeScript types
│   │   ├── context/          # State management
│   │   ├── hooks/            # Custom hooks
│   │   └── utils/            # Utilities
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   └── README.md
│
├── docs/                      # Documentation
│   └── PROJECT_DOCUMENTATION.md # This file
│
├── README.md                  # Project overview
├── SETUP.md                   # Setup guide
├── docker-compose.yml         # Docker config
├── .gitignore                 # Git ignore
└── CLEANUP_SUMMARY.md         # Cleanup report
```

---

## Database Schema

### 20 Total Tables (3 Months)

#### Month 1: Authentication & Users
- `users` - Core user account (email, password, role)
- `candidates` - Candidate profile (1:1 with users)
- `recruiters` - Recruiter profile (1:1 with users)
- `companies` - Company information

#### Month 2: AI & Code Intelligence
- `projects` - GitHub repositories
- `files` - Repository files
- `github_tokens` - OAuth credentials
- `code_documents` - Indexed source files
- `code_chunks` - Semantic chunks with vectors
- `ai_conversations` - Chat sessions
- `ai_messages` - Chat messages
- `ai_analyses` - Analysis results
- `repository_index_metadata` - Indexing status

#### Month 3: Multi-Agent System
- `ai_tasks` - Task definitions
- `agent_executions` - Execution history
- `task_patches` - Proposed changes
- `task_approvals` - Human approvals
- `task_test_results` - Test results
- `task_workspaces` - Working environments

### Key Relationships

```
User (1) ─── (∞) Project
User (1) ─── (1) Candidate
User (1) ─── (1) Recruiter
Project (1) ─── (∞) CodeDocument
CodeDocument (1) ─── (∞) CodeChunk ──VECTOR─→ Embeddings
Project (1) ─── (∞) AITask
AITask (1) ─── (∞) AgentExecution
AITask (1) ─── (∞) TaskPatch
```

---

## API Endpoints

### Total: 27 Endpoints

#### Authentication (3)
- `POST /api/auth/register/candidate` - Register as candidate
- `POST /api/auth/register/recruiter` - Register as recruiter
- `POST /api/auth/login` - Login, get JWT

#### User Profiles (4)
- `GET /api/candidates/me` - Get candidate profile
- `PUT /api/candidates/me` - Update candidate profile
- `GET /api/recruiters/me` - Get recruiter profile
- `PUT /api/recruiters/me` - Update recruiter profile

#### Admin (3)
- `GET /api/admin/users` - List all users
- `PATCH /api/admin/users/{id}/status` - Enable/disable user
- `GET /api/admin/stats` - Platform statistics

#### AI & RAG (7) - Month 2
- `POST /api/ai/chat` - Chat with code context
- `POST /api/ai/explain` - Explain code
- `POST /api/ai/bugs` - Detect bugs
- `POST /api/ai/improve` - Improve code
- `POST /api/ai/tests` - Generate tests
- `GET /api/ai/index-status` - Indexing status
- `GET /api/ai/conversations/{id}` - Chat history

#### Agent Tasks (5) - Month 3
- `POST /api/v1/projects/{id}/ai/tasks` - Create task
- `GET /api/v1/projects/{id}/ai/tasks` - List tasks
- `GET /api/v1/projects/{id}/ai/tasks/{id}` - Get task details
- `POST /api/v1/projects/{id}/ai/tasks/{id}/approve` - Approve task
- `POST /api/v1/projects/{id}/ai/tasks/{id}/cancel` - Cancel task

#### Health (1)
- `GET /actuator/health` - System health check

---

## Features by Month

### Month 1: Foundation ✅
**Status**: Complete

- Candidate & recruiter registration
- JWT-based authentication
- Role-based authorization (CANDIDATE, RECRUITER, ADMIN)
- Profile management
- Admin dashboard
- Company management
- PostgreSQL database
- Docker deployment

### Month 2: AI Code Intelligence ✅
**Status**: Complete

- Repository indexing
- Code chunking (AST-based)
- Vector embeddings (OpenAI)
- Semantic search with pgvector
- Codebase chat
- Code explanation
- Bug detection
- Code improvement suggestions
- Test generation
- Conversation history with citations
- Incremental repository indexing

### Month 3: Multi-Agent AI Software Engineering ✅
**Status**: Complete

- LangGraph workflow engine
- 10 specialized agents:
  - Planner - Task planning
  - Analyzer - Code analysis
  - Coder - Code generation
  - Reviewer - Code review
  - Tester - Test execution
  - Debugger - Failure diagnosis
  - Security - Vulnerability detection
  - Documentation - Doc generation
  - Approval Gate - Human review
  - Cleanup - Error recovery
- Agent tools system (repository, patch, test)
- Patch generation & validation
- Human approval workflow
- Task management API
- Execution history tracking
- Agent state management

### Month 4: Testing & Polish ✅
**Status**: Complete (Planning/Framework)

- 60+ verification points
- 30+ security tests
- 20+ integration workflows
- Docker clean start verification
- Performance testing
- Security audit
- Code quality standards
- Comprehensive documentation
- Demo setup with 11 test accounts
- Test plan & roadmap

---

## Setup & Installation

### Quick Start (Docker - 5 minutes)

```bash
# 1. Clone repository
git clone https://github.com/your-org/recruitment-platform.git
cd recruitment-platform

# 2. Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env with your settings

# 3. Start everything
docker-compose up --build

# 4. Access
# Frontend: http://localhost:5173
# Backend: http://localhost:8080
# API Docs: http://localhost:8080/docs
```

### Manual Setup (Local Development)

#### Backend

```bash
cd backend

# Virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
# OR: .\venv\Scripts\Activate.ps1  # Windows

# Install
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env

# Database
alembic upgrade head

# Run
python -m app.main
```

Backend: http://localhost:8080

#### Frontend

```bash
cd frontend

# Install
npm install

# Run
npm run dev
```

Frontend: http://localhost:5173

---

## Environment Configuration

### Backend (.env)

**Required:**
```env
DB_URL=postgresql://postgres:password@localhost:5432/recruitment_platform
JWT_SECRET=your-strong-secret-at-least-32-chars
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SecurePassword123!
```

**Optional (AI Features):**
```env
LLM_PROVIDER=openai           # or 'mock'
LLM_MODEL=gpt-4-turbo
LLM_API_KEY=sk-xxx
EMBEDDING_PROVIDER=openai
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=sk-xxx
REDIS_URL=redis://localhost:6379
PORT=8080
```

### Frontend (.env.local)

```env
VITE_API_BASE_URL=http://localhost:8080/api
```

---

## Demo Accounts

### Admin
```
Email:    admin@example.com
Password: Admin123!
```

### Candidates (All: Student123!)
1. alice@student.com - Full Stack Dev
2. bob@student.com - Backend Dev
3. carol@student.com - Data Scientist
4. david@student.com - Frontend Dev
5. emma@student.com - DevOps Engineer

### Recruiters (All: Recruiter123!)
1. sarah@recruiter.com @ TechCorp Solutions
2. james@recruiter.com @ DataViz Analytics
3. lisa@recruiter.com @ CloudStack Systems
4. michael@recruiter.com @ FinTech Innovations
5. jennifer@recruiter.com @ AI Research Labs

---

## Running the Application

### Start Everything

```bash
# Docker Compose
docker-compose up --build

# Services:
# - PostgreSQL (port 5432)
# - Redis (port 6379)
# - Backend (port 8080)
# - Frontend (port 5173)
```

### Access Points

| Service | URL |
|---------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8080 |
| API Docs | http://localhost:8080/docs |
| ReDoc | http://localhost:8080/redoc |
| Health | http://localhost:8080/actuator/health |

### Stop Services

```bash
docker-compose down

# Or with data cleanup:
docker-compose down -v
```

---

## Testing

### Backend Tests

```bash
cd backend

# All tests
pytest -v

# With coverage
pytest --cov=app --cov-report=html

# Specific file
pytest tests/test_auth.py -v
```

### Frontend Tests

```bash
cd frontend

# Type check
npx tsc -b --noEmit

# Lint
npm run lint

# Build
npm run build
```

### Manual Testing

See `docs/DEMO_DATA_READY.md` for:
- Authorization testing
- Feature testing
- Security testing
- Integration workflows

---

## Deployment

### Production Docker

```bash
# Build images
docker build -t api:latest ./backend
docker build -t web:latest ./frontend

# Run with production settings
docker run -d \
  --env-file .env.production \
  -p 8080:8080 \
  api:latest

docker run -d \
  -p 80:3000 \
  web:latest
```

### Pre-Deployment Checklist

- [ ] All tests passing
- [ ] No .env files committed
- [ ] HTTPS configured
- [ ] Strong JWT secret
- [ ] Strong admin password
- [ ] Database backups enabled
- [ ] Rate limiting configured
- [ ] Logging/monitoring set up

---

## Troubleshooting

### Port Already in Use

```bash
# Find process
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows

# Kill process
kill -9 <PID>
```

### Database Connection Failed

```bash
# Check PostgreSQL
docker ps | grep postgres

# Test connection
psql -U postgres -h localhost -d recruitment_platform

# Check .env DB_URL format
```

### Frontend Can't Connect to Backend

```bash
# 1. Verify backend running
curl http://localhost:8080/actuator/health

# 2. Check CORS in backend/.env
CORS_ALLOWED_ORIGINS=http://localhost:5173

# 3. Check frontend .env.local
VITE_API_BASE_URL=http://localhost:8080/api
```

### Docker Issues

```bash
# Clean start
docker-compose down -v
docker-compose build --no-cache
docker-compose up --build

# View logs
docker-compose logs -f
docker-compose logs backend
```

---

## Development Guidelines

### Code Organization

**Backend Layers:**
1. Routes (HTTP endpoints)
2. Services (business logic)
3. Repositories (data access)
4. Models (ORM entities)
5. Database (PostgreSQL)

**Frontend Layers:**
1. Pages (route components)
2. Components (reusable UI)
3. Services (API clients)
4. Types (TypeScript definitions)
5. State (React context)

### Git Workflow

```bash
# Branch naming
feature/feature-name
bugfix/bug-name
refactor/refactor-name

# Before commit
- Run tests
- Format code
- Check for secrets
- Update documentation

# Commit message
[component] Description

- Detail 1
- Detail 2

Fixes #123
```

### Adding Features

1. **Database** - Add models and migrations
2. **Backend** - Add services, repositories, routes
3. **Frontend** - Add types, services, components
4. **Tests** - Add test coverage
5. **Documentation** - Update docs

### Security Reminders

⚠️ **NEVER:**
- Commit .env files
- Hardcode credentials
- Use weak passwords
- Store plaintext secrets

✅ **ALWAYS:**
- Use strong JWT secret (≥32 chars)
- Use HTTPS in production
- Validate user input
- Keep dependencies updated

---

## Additional Resources

### API Documentation
- Interactive Docs: http://localhost:8080/docs
- ReDoc: http://localhost:8080/redoc

### Related Files
- `README.md` - Project overview
- `SETUP.md` - Setup instructions
- `CLEANUP_SUMMARY.md` - Repository cleanup report
- `backend/README.md` - Backend specifics
- `frontend/README.md` - Frontend specifics

### Technologies
- [FastAPI](https://fastapi.tiangolo.com/)
- [React](https://react.dev/)
- [SQLAlchemy](https://www.sqlalchemy.org/)
- [PostgreSQL](https://www.postgresql.org/)
- [LangGraph](https://python.langchain.com/docs/langgraph/)
- [OpenAI](https://openai.com/)

---

## Support

### Quick Answers

| Question | Answer |
|----------|--------|
| How to setup? | See SETUP.md |
| Where's the code? | See Directory Structure |
| How to test? | See Testing section |
| What are demo accounts? | See Demo Accounts |
| How to deploy? | See Deployment |
| How to troubleshoot? | See Troubleshooting |

---

## Project Status

| Milestone | Status | Completion |
|-----------|--------|------------|
| Month 1: Foundation | ✅ Complete | Auth, profiles, projects |
| Month 2: AI Intelligence | ✅ Complete | RAG, embeddings, analysis |
| Month 3: Multi-Agent | ✅ Complete | LangGraph, agents, tasks |
| Month 4: Testing/Polish | ✅ Complete | Tests, security, docs |

**Overall Status**: ✅ **Production-Ready**

---

## License

[Your License Here]

## Support & Questions

Create an issue in GitHub for:
- Bug reports
- Feature requests
- Questions about setup
- Documentation improvements

---

**Last Updated**: September 2026  
**Version**: 1.0.0  
**Status**: Production-Ready ✅

