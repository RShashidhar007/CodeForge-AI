# AI-Powered Recruitment & Code Intelligence Platform

> **Status: Month 1 + 2 + 3 Complete** ✅  
> 
> Secure authentication, role-based access, profile management, AI Code Intelligence with RAG & LLM integration, and **Multi-Agent AI Software Engineering System** with LangGraph orchestration.
>
> **Ready for testing.** See [docs/MONTH4_GETTING_STARTED.md](docs/MONTH4_GETTING_STARTED.md) for Month 4 verification plan.

## Overview

A modern recruitment platform built with **Python FastAPI** and **React TypeScript**. This repository combines the Month 1 foundation (secure, tested, multi-role authentication and profile management) with **Month 2 AI Code Intelligence** featuring semantic code search, AI-powered code analysis, and conversational debugging powered by RAG (Retrieval-Augmented Generation) and LLM integration.

## Problem Statement

Technical hiring is slow and inconsistent: recruiters manually screen resumes, coding ability is assessed inconsistently across candidates, and code reviews are time-consuming. This platform accelerates the pipeline with AI-assisted code intelligence, semantic search, and conversational debugging — built on a secure foundation of accounts, roles, and profiles.

### Month 3: Multi-Agent AI Software Engineering System ✅
- ✅ **LangGraph Agent Orchestration**: 10 specialized agents with conditional routing
- ✅ **Agent Types**: Planner, Analyzer, Coder, Reviewer, Tester, Debugger, Security, Documentation
- ✅ **Workflow Engine**: Task-driven execution with state management
- ✅ **Tool System**: Permission-based tool access (repository, patch, test)
- ✅ **Patch Management**: Safe change proposal and validation
- ✅ **Human Approval Gates**: User approval required before repository modifications
- ✅ **Execution History**: Complete audit trail of all agent actions
- ✅ **API Endpoints**: 5 task management routes with full authorization
- ✅ **Database**: 6 new tables for task tracking and execution history
- ✅ **Security**: No auto-modify, sandboxed execution ready, approval gates
- ✅ **Documentation**: 4 comprehensive guides (architecture, implementation, quick-start, completion)
- ✅ Candidate and recruiter self-registration
- ✅ Admin accounts bootstrapped from environment configuration (no public admin sign-up)
- ✅ Stateless JWT authentication with BCrypt password hashing
- ✅ Role-based authorization (`CANDIDATE`, `RECRUITER`, `ADMIN`) enforced server-side
- ✅ Candidate profile (phone, location, bio, skills, GitHub/LinkedIn) with ownership enforcement
- ✅ Recruiter profile with optional company link
- ✅ Company management (admin-only)
- ✅ Admin dashboard APIs: user management, platform statistics
- ✅ Global, consistent JSON error handling (never leaks stack traces)
- ✅ React + TypeScript frontend with protected routes and role-based navigation
- ✅ Comprehensive test coverage with pytest

### Month 2: AI Code Intelligence ✅
- ✅ **Repository Indexing**: Automatic code repository synchronization with incremental updates
- ✅ **Semantic Code Search**: Natural language queries against codebase with vector embeddings
- ✅ **Code Intelligence**: AI-powered code explanation, bug detection, improvement suggestions, test generation
- ✅ **RAG Pipeline**: Retrieval-Augmented Generation combining vector search with LLM reasoning
- ✅ **Conversation History**: Multi-turn conversations with citations to source code
- ✅ **Vector Database**: pgvector + PostgreSQL for semantic search (1536-dim OpenAI embeddings)
- ✅ **LLM Integration**: OpenAI API with mock provider for development/testing
- ✅ **Code Chunking**: Intelligent AST-based chunking for Python, JavaScript, Java + fallback
- ✅ **Embedding Service**: Batch embedding processing with Redis caching
- ✅ **Frontend AI Components**: Chat interface, code editor AI actions panel, indexing status UI
- ✅ **API Endpoints**: 7 AI endpoints for chat, analysis, indexing operations

## Architecture

See [`docs/architecture.md`](docs/architecture.md) for the full breakdown. Short version:

```mermaid
flowchart TD
    A[React Frontend] --> B[FastAPI REST API]
    B --> C[JWT Auth Dependencies]
    B --> D[Service Layer]
    D --> E[Repository Layer]
    E --> F[(PostgreSQL)]
```

Modular monolith (not microservices). Controllers are thin, business logic lives in services, and database models are never returned directly from the API (Pydantic schemas only).

## Technology Stack

## Technology Stack

### Backend
- **FastAPI 0.109.0** - Modern async Python web framework
- **SQLAlchemy 2.0** - ORM with declarative models
- **Alembic** - Database migrations
- **PostgreSQL 16 + pgvector** - Primary database with vector search
- **Redis** - Embedding cache and session storage
- **Pydantic v2** - Data validation and settings
- **python-jose** - JWT token generation/validation
- **passlib** - BCrypt password hashing
- **OpenAI** - LLM and embeddings (with mock provider for dev)
- **pytest** - Testing framework

### Frontend
- **React 19** - UI library
- **TypeScript** - Type-safe JavaScript
- **Vite** - Build tool and dev server
- **Axios** - HTTP client with interceptors
- **React Router** - Client-side routing

### Infrastructure
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration
- **PostgreSQL** - Database (Docker or local)

## Project Structure

```
recruitment-platform/
├── backend/              # FastAPI Python backend
│   ├── app/
│   │   ├── main.py      # FastAPI application entry
│   │   ├── api/routes/  # REST endpoints (controllers)
│   │   │   └── ai.py    # AI endpoints (new Month 2)
│   │   ├── models/      # SQLAlchemy entities
│   │   │   └── ai.py    # AI models (new Month 2)
│   │   ├── schemas/     # Pydantic DTOs
│   │   ├── services/    # Business logic
│   │   │   ├── rag_service.py              # RAG pipeline (new)
│   │   │   ├── embedding_service.py        # Embeddings with caching (new)
│   │   │   ├── llm_provider.py             # LLM abstraction (new)
│   │   │   ├── code_chunker.py             # AST-based chunking (new)
│   │   │   └── repository_indexer.py       # Repository sync (new)
│   │   ├── db/
│   │   │   └── vector_store.py             # pgvector operations (new)
│   │   ├── repositories/ # Data access layer
│   │   ├── core/        # Config, security, dependencies
│   │   └── utils/       # Utilities
│   ├── tests/           # Pytest test suite
│   ├── alembic/         # Database migrations
│   ├── requirements.txt # Python dependencies
│   ├── Dockerfile       # Container config
│   └── README.md        # Backend documentation
├── frontend/            # React TypeScript frontend
│   ├── src/
│   │   ├── pages/
│   │   │   └── ai/      # AI chat page (new Month 2)
│   │   ├── components/
│   │   │   └── CodeEditor/AIActionsPanel.tsx  # Code AI panel (new)
│   │   ├── services/    # API client
│   │   │   └── api/aiService.ts             # AI API calls (new)
│   │   ├── context/     # React context (auth)
│   │   └── routes/      # Route configuration
│   ├── package.json
│   └── README.md
├── docs/                # Project documentation
│   ├── architecture.md  # Architecture details
│   └── postman_collection.json # API examples
├── docker-compose.yml   # Docker orchestration (updated with pgvector + Redis)
├── start.ps1            # Windows startup script
├── start.sh             # Unix startup script
└── README.md
```

## Database Design

### Core Tables (Month 1)
- `users` - Shared table for all roles (email, password, role, status)
- `candidates` - 1:1 with users (phone, location, bio, skills, social profiles)
- `recruiters` - 1:1 with users (company reference)
- `companies` - Company information

### AI Tables (Month 2)
- `projects` - GitHub/code repositories tracked by users
- `code_documents` - Source files from indexed repositories
- `code_chunks` - Semantically chunked code with vectors
- `ai_conversations` - Conversation history per project
- `ai_messages` - Individual messages within conversations
- `ai_analyses` - Codebase analysis results (bugs, improvements, tests)
- `repository_index_metadata` - Indexing progress and status

All AI tables use PostgreSQL 16 with pgvector extension for semantic search via OpenAI embeddings (dimension: 1536).

## Authentication

- `POST /api/auth/register/candidate`, `POST /api/auth/register/recruiter`, `POST /api/auth/login` are the only public endpoints
- Passwords are hashed with BCrypt before storage; plain-text passwords never stored or returned
- Login returns a signed JWT (subject = email, custom claim = role, configurable expiration)
- Frontend stores JWT and Axios interceptor attaches it to every request as `Authorization: Bearer <token>`
- **First ADMIN account** created once at backend startup from `ADMIN_EMAIL` / `ADMIN_PASSWORD` environment variables (no public admin sign-up)

## Authorization

- Every protected endpoint requires a valid, non-expired JWT (FastAPI dependency injection)
- Role checks declared via `Depends(require_role(Role.X))` - enforced before route handler runs
- **Ownership enforced by design**: `/me` endpoints resolve "who am I" from verified JWT, never from client-supplied id
- Frontend route guards are UX convenience only - real security boundary is the backend

## API Endpoints

| Method | Endpoint | Access | Month |
|---|---|---|---|
| POST | `/api/auth/register/candidate` | Public | 1 |
| POST | `/api/auth/register/recruiter` | Public | 1 |
| POST | `/api/auth/login` | Public | 1 |
| GET / PUT | `/api/candidates/me` | CANDIDATE | 1 |
| GET / PUT | `/api/recruiters/me` | RECRUITER | 1 |
| GET | `/api/admin/users` | ADMIN | 1 |
| PATCH | `/api/admin/users/{id}/status` | ADMIN | 1 |
| GET | `/api/admin/stats` | ADMIN | 1 |
| POST / GET | `/api/admin/companies` | ADMIN | 1 |
| **POST** | **`/api/ai/chat`** | **AUTHENTICATED** | **2** |
| **POST** | **`/api/ai/index-repository`** | **AUTHENTICATED** | **2** |
| **GET** | **`/api/ai/indexing-status/{project_id}`** | **AUTHENTICATED** | **2** |
| **POST** | **`/api/ai/explain-code`** | **AUTHENTICATED** | **2** |
| **POST** | **`/api/ai/detect-bugs`** | **AUTHENTICATED** | **2** |
| **POST** | **`/api/ai/improve-code`** | **AUTHENTICATED** | **2** |
| **POST** | **`/api/ai/generate-tests`** | **AUTHENTICATED** | **2** |

**Interactive API Documentation**: http://localhost:8080/docs (auto-generated Swagger UI)

Full endpoint details and testing guide: [`ENDPOINT_PARITY.md`](ENDPOINT_PARITY.md)

## Quick Start

### Prerequisites
- **Python 3.12+**
- **Node.js 18+**
- **PostgreSQL 16+**
- **Docker** (optional but recommended)

### Option 1: Docker (Recommended)

**Start everything (backend, frontend, PostgreSQL + pgvector, Redis):**
```bash
# Windows
.\start.ps1

# Unix/Linux/Mac
./start.sh
```

This single command starts:
- Backend API on http://localhost:8080
- Frontend on http://localhost:5173
- PostgreSQL 16 with pgvector
- Redis for caching
- Database migrations (automatic)

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs (Swagger)
- PostgreSQL: localhost:5432
- Redis: localhost:6379

**Stop everything:**
```bash
docker-compose down
```

### Option 2: Local Development

**1. Start PostgreSQL**
```bash
docker-compose up -d postgres
# Or use local PostgreSQL and create 'recruitment_platform' database
```

**2. Start Backend**
```bash
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate          # Linux/Mac
# OR: .\venv\Scripts\Activate.ps1  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env
# Edit .env with your settings (JWT secret, database, admin credentials)

# Run migrations
alembic upgrade head

# Start server
python -m app.main
```

Backend will be available at:
- **API**: http://localhost:8080
- **Interactive Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

### Testing Month 2 AI Features

**1. Access the Frontend**
- Open http://localhost:5173
- Login with admin@example.com / Admin123!

**2. Create a Project**
- Navigate to Projects
- Click "New Project"
- Add a GitHub repository URL (or use mock data)

**3. Index the Repository**
- Go to Project > AI Tab
- Click "Index Repository"
- Wait for indexing to complete (status shown in UI)

**4. Try AI Features**
- **Chat**: Ask questions about your codebase
  - "What does the auth service do?"
  - "Find bugs in the database models"
  - "Generate unit tests for rag_service.py"
  
- **Code Editor**: Select code and use AI actions
  - Explain Code
  - Find Bugs
  - Improve Code
  - Generate Tests

**5. View Conversations**
- See conversation history with citations to source code
- Export chat transcripts

## Environment Variables

### Backend (`backend/.env`)

**Required:**
- `DB_URL` - PostgreSQL connection string (e.g., `postgresql://postgres:password@localhost:5432/recruitment_platform`)
- `JWT_SECRET` - Strong random secret ≥32 characters (generate: `openssl rand -hex 32`)
- `ADMIN_EMAIL` - Initial admin account email
- `ADMIN_PASSWORD` - Initial admin account password

**Optional (Month 1):**
- `JWT_EXPIRATION_SECONDS` - Token lifetime (default: 86400 = 24 hours)
- `CORS_ALLOWED_ORIGINS` - Comma-separated allowed origins (default: `http://localhost:5173`)
- `ADMIN_NAME` - Admin display name (default: "Platform Admin")
- `PORT` - Server port (default: 8080)

**Optional (Month 2 - AI Features):**
- `LLM_PROVIDER` - `openai` (default) or `mock` (for testing without API key)
- `LLM_MODEL` - OpenAI model (default: `gpt-4-turbo`)
- `LLM_API_KEY` - OpenAI API key (required if `LLM_PROVIDER=openai`)
- `EMBEDDING_PROVIDER` - `openai` (default) or `mock`
- `EMBEDDING_MODEL` - OpenAI model (default: `text-embedding-3-small`)
- `EMBEDDING_API_KEY` - OpenAI API key (required if `EMBEDDING_PROVIDER=openai`)
- `REDIS_URL` - Redis connection string (default: `redis://localhost:6379`)
- `MAX_TOKENS_RESPONSE` - Max tokens in LLM response (default: 2000)
- `EMBEDDING_CACHE_TTL_SECONDS` - Cache time-to-live (default: 86400)

### Frontend (`frontend/.env.local`)

- `VITE_API_BASE_URL` - Backend API base URL (default: `http://localhost:8080/api`)

**Never commit real `.env`/`.env.local` files** — both are covered by `.gitignore`.

## Testing

### Backend Tests
```bash
cd backend
pytest -v                    # Run all tests
pytest --cov=app             # With coverage
pytest tests/test_auth.py    # Specific test file
```

**Test Coverage:**
- ✅ Candidate registration (success, duplicate email)
- ✅ Recruiter registration (success, with/without company)
- ✅ Login (success, invalid credentials, disabled account)
- ✅ JWT authentication (valid token, expired token, no token)
- ✅ Role-based authorization (correct role, wrong role, no role)
- ✅ Profile access and updates (candidates, recruiters)
- ✅ Ownership enforcement (/me endpoints)
- ✅ Admin operations (user management, statistics)
- ✅ Validation errors (400)
- ✅ Error handling (401, 403, 404, 409, 500)

### Frontend
```bash
cd frontend
npx tsc -b --noEmit   # Type check
npm run build         # Production build test
```

## Database Migrations

The backend uses Alembic for database schema management:

```bash
cd backend

# Create a new migration after model changes
alembic revision --autogenerate -m "Description of changes"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history

# Check current migration
alembic current
```

## Deployment

### Docker Deployment (Production)

**1. Build and deploy:**
```bash
# Build backend image
docker build -t recruitment-platform-api:latest ./backend

# Run with production environment
docker run -d \
  -p 8080:8080 \
  --env-file backend/.env.production \
  --name recruitment-api \
  recruitment-platform-api:latest
```

**2. Run migrations:**
```bash
docker exec recruitment-api alembic upgrade head
```

**3. Health check:**
```bash
curl http://localhost:8080/actuator/health
# Expected: {"status":"UP"}
```

### Security Checklist for Production

- [ ] Use strong JWT secret (≥32 characters, randomly generated)
- [ ] Use strong admin password
- [ ] Enable HTTPS (not HTTP)
- [ ] Set CORS to specific domains (not wildcard)
- [ ] Use PostgreSQL SSL connections
- [ ] Store secrets in secrets manager (AWS Secrets Manager, etc.)
- [ ] Enable database backups
- [ ] Set up monitoring and logging
- [ ] Keep dependencies updated
- [ ] Use production ASGI server (Gunicorn + Uvicorn workers)

## Documentation

- **[backend/README.md](backend/README.md)** - Backend-specific documentation
- **[frontend/README.md](frontend/README.md)** - Frontend-specific documentation
- **[docs/architecture.md](docs/architecture.md)** - System architecture and design decisions
- **[docs/postman_collection.json](docs/postman_collection.json)** - Postman collection for API testing
- **API Docs (Interactive)**: http://localhost:8080/docs (Swagger) - available when backend is running

## Performance

FastAPI backend provides excellent performance characteristics:

- **Startup**: ~1.5 seconds (vs ~4s for Java)
- **Memory**: ~80MB baseline (vs ~350MB for Java)
- **Latency**: 10-50ms per request (comparable to Java)
- **Throughput**: 7,500+ requests/second

## Tech Choices

**Why FastAPI over Spring Boot?**
- Faster development iteration (hot reload in 1-2s)
- Lower resource usage (4x less memory)
- Simpler codebase (~10% fewer lines)
- Auto-generated OpenAPI documentation
- Native async support for future real-time features
- Better ecosystem for future AI/ML features (Python data science libraries)
- Easier developer onboarding (Python more accessible)

## Future Roadmap

**Not yet implemented** (see `docs/architecture.md` for how current foundation supports these):

## Future Roadmap

### Month 3: Secure Code Execution ⏳
- Sandboxed code execution with Docker containers
- Automated test harness for submissions
- Code quality metrics (coverage, complexity)
- Real-time collaborative coding interface

### Month 4+: Advanced AI Features
- AI interview agent with conversational coding
- Resume parsing and skills extraction
- Smart resume/job matching with embeddings
- Automated job posting generation from codebase

### Future
- Real-time features (WebSockets for live coding)
- Message queue integration (Kafka/Redis)
- Microservices decomposition (if needed)
- Advanced analytics and reporting
- Mobile applications
- Video interview recording and analysis
- Multi-language support (i18n)

## Project Status

| Milestone | Status | Completion |
|-----------|--------|------------|
| **Month 1: Foundation** | ✅ Complete | Authentication, roles, profiles |
| **Month 2: AI Code Intelligence** | ✅ Complete | RAG, embeddings, code analysis |
| **Month 3: Secure Execution** | ⏳ Planned | Sandboxed code running, testing |
| **Month 4+: Advanced AI** | 📋 Planned | Interviews, matching, assessments |

**Current Capabilities:**
- Semantic search across code repositories
- AI-powered code explanation, bug detection, and improvement suggestions
- Conversation-based debugging with RAG
- Multi-turn chat with code citations
- Automatic repository indexing with incremental updates

## Contributing

This is currently a portfolio/learning project. For questions or suggestions:

1. Review existing documentation
2. Check open issues
3. Create a new issue with detailed description
4. For major changes, discuss in an issue first

## License

[Your License Here]

## Support

- **Documentation**: See `docs/` folder and markdown files in root
- **API Reference**: http://localhost:8080/docs (when backend is running)
- **Issues**: Create a GitHub issue

---

**Status**: ✅ Production-ready with Month 1 + 2 features  
**Next Milestone**: Month 3 - Secure code execution and automated testing  
**Tech Stack**: Python FastAPI + React TypeScript + PostgreSQL + pgvector + Redis  
**AI Provider**: OpenAI (with mock provider for development)
