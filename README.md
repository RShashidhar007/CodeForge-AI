# CodeForge AI - AI-Powered Recruitment & Code Intelligence Platform

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Python](https://img.shields.io/badge/Python-3.12%2B-blue)]()
[![React](https://img.shields.io/badge/React-19-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.109-blue)]()
[![License](https://img.shields.io/badge/License-MIT-green)]()

> **An AI-powered platform for intelligent recruitment and code analysis** combining secure authentication, semantic code search, and multi-agent AI software engineering.

## 🎯 What is CodeForge AI?

CodeForge AI transforms technical recruitment by combining:

- **Secure Multi-Role Platform** - Role-based authentication for candidates, recruiters, and admins
- **AI Code Intelligence** - Semantic search, analysis, and explanation of codebases via RAG + LLM
- **Multi-Agent System** - 10 specialized AI agents (planner, coder, reviewer, tester, debugger, security, etc.)
- **Conversational Debugging** - Ask questions about code, get AI-powered explanations with citations
- **Safe Automation** - Human approval gates before any code modifications

**Why?** Technical hiring is slow and inconsistent. CodeForge AI accelerates the pipeline with:
- Automated code analysis for better candidate screening
- Instant semantic search across entire repositories
- AI-powered code review and improvement suggestions
- Conversational debugging for faster troubleshooting

## ✨ Features

### Month 1: Secure Foundation ✅
- Multi-role authentication (Candidate, Recruiter, Admin)
- JWT-based stateless authentication with BCrypt
- Profile management with ownership enforcement
- Admin dashboard and user management
- Company directory management

### Month 2: AI Code Intelligence ✅
- **Semantic Code Search** - Natural language queries against entire codebases
- **Repository Indexing** - Automatic GitHub sync with incremental updates
- **Vector Embeddings** - pgvector + OpenAI embeddings (1536-dim)
- **RAG Pipeline** - Retrieval-Augmented Generation for context-aware responses
- **Code Analysis** - AI-powered explanation, bug detection, improvements, test generation
- **Conversation History** - Multi-turn chat with citations to source code
- **Intelligent Chunking** - AST-based code segmentation for Python, JavaScript, Java

### Month 3: Multi-Agent AI System ✅
- **10 Specialized Agents**: Planner, Analyzer, Coder, Reviewer, Tester, Debugger, Security, Documentation, Approval Gate, Cleanup
- **LangGraph Orchestration** - Conditional routing and state management
- **Workflow Engine** - Task-driven execution with human approval gates
- **Patch Management** - Safe change proposals and validation
- **Execution History** - Complete audit trail of all AI operations
- **Permission Model** - Granular tool access and repository permissions

## 🛠 Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Backend** | FastAPI | 0.109.0 |
| **Language** | Python | 3.12+ |
| **ORM** | SQLAlchemy | 2.0 |
| **Database** | PostgreSQL + pgvector | 16 |
| **Cache** | Redis | Latest |
| **Authentication** | JWT + BCrypt | - |
| **AI/LLM** | OpenAI API | GPT-4 Turbo |
| **Embeddings** | OpenAI | text-embedding-3-small |
| **Agent Orchestration** | LangGraph | - |
| **Frontend** | React | 19 |
| **Language** | TypeScript | 6 |
| **Build Tool** | Vite | 8 |
| **HTTP Client** | Axios | Latest |
| **Routing** | React Router | Latest |
| **Infrastructure** | Docker Compose | Latest |

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│              (TypeScript, Vite, Axios)              │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS/REST
┌────────────────────────▼────────────────────────────┐
│              FastAPI Backend                         │
│  ┌─────────────────────────────────────────────┐  │
│  │  27 REST API Endpoints                      │  │
│  │  - Auth (3), Users (4), Admin (3)          │  │
│  │  - AI/RAG (7), Agent Tasks (5)             │  │
│  │  - Health (1)                              │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │  Service Layer                              │  │
│  │  - AuthService, RAGService, LLMProvider    │  │
│  │  - EmbeddingService, RepositoryIndexer    │  │
│  │  - AgentOrchestrator                       │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │  Multi-Agent System (LangGraph)             │  │
│  │  - 10 Specialized Agents                    │  │
│  │  - Task Workflow Engine                     │  │
│  │  - Human Approval Gates                     │  │
│  └─────────────────────────────────────────────┘  │
└────────────────┬────────────────────┬──────────────┘
                 │                    │
    ┌────────────▼──────────┐  ┌──────▼─────────────┐
    │   PostgreSQL 16       │  │    Redis Cache     │
    │   + pgvector          │  │    (Embeddings)    │
    │   20 Tables           │  │                    │
    │   1536-dim Vectors    │  └────────────────────┘
    └───────────────────────┘
         │
         └─────────────────────────────────────────┐
                                                  │
                                        ┌──────────▼─────────┐
                                        │  OpenAI API        │
                                        │  - LLM (GPT-4)     │
                                        │  - Embeddings      │
                                        └────────────────────┘
```

## 📁 Project Structure

```
CodeForge-AI/
├── 📄 README.md                      ← You are here
├── 📄 SETUP.md                       ← Setup & installation guide
├── 📄 .gitignore                     ← Excludes secrets, caches, dependencies
├── 📄 docker-compose.yml             ← Complete local dev environment
│
├── 📁 backend/                       ← FastAPI Python backend
│   ├── app/
│   │   ├── main.py                   ← FastAPI entry point
│   │   ├── api/routes/               ← HTTP endpoints (27 total)
│   │   │   ├── auth.py               ├─ Authentication (login, register)
│   │   │   ├── admin.py              ├─ Admin operations (users, stats)
│   │   │   ├── candidates.py         ├─ Candidate profiles
│   │   │   ├── recruiters.py         ├─ Recruiter profiles
│   │   │   ├── ai.py                 ├─ AI/RAG endpoints (chat, analysis)
│   │   │   └── agent_tasks.py        └─ Multi-agent task management
│   │   │
│   │   ├── models/                   ← SQLAlchemy ORM entities
│   │   │   ├── user.py, candidate.py, recruiter.py
│   │   │   ├── ai.py                 ← AI conversations, messages, analyses
│   │   │   ├── agent_tasks.py        ← Agent execution tracking
│   │   │   └── company.py
│   │   │
│   │   ├── services/                 ← Business logic layer
│   │   │   ├── auth_service.py       ├─ JWT, BCrypt, login/register
│   │   │   ├── rag_service.py        ├─ RAG pipeline (search + LLM)
│   │   │   ├── embedding_service.py  ├─ Vector embeddings with caching
│   │   │   ├── llm_provider.py       ├─ LLM abstraction (OpenAI/mock)
│   │   │   ├── code_chunker.py       ├─ AST-based code chunking
│   │   │   ├── repository_indexer.py ├─ GitHub sync & indexing
│   │   │   └── admin_service.py      └─ Admin operations
│   │   │
│   │   ├── agents/                   ← Multi-agent AI system (Month 3)
│   │   │   ├── graph/
│   │   │   │   ├── workflow.py       ├─ LangGraph main workflow
│   │   │   │   ├── state.py          ├─ Agent state models
│   │   │   │   └── routing.py        └─ Conditional agent routing
│   │   │   │
│   │   │   ├── nodes/                ← 10 specialized agent implementations
│   │   │   │   ├── planner.py
│   │   │   │   ├── analyzer.py
│   │   │   │   ├── coder.py
│   │   │   │   ├── reviewer.py
│   │   │   │   ├── tester.py
│   │   │   │   ├── debugger.py
│   │   │   │   ├── security.py
│   │   │   │   ├── documentation.py
│   │   │   │   ├── approval_gate.py  ← Human approval
│   │   │   │   └── cleanup.py
│   │   │   │
│   │   │   ├── tools/
│   │   │   │   ├── registry.py       ├─ Tool definitions
│   │   │   │   ├── repository.py     ├─ Repository operations
│   │   │   │   ├── patch.py          ├─ Code change proposals
│   │   │   │   └── test.py           └─ Test execution
│   │   │   │
│   │   │   └── state/
│   │   │       └── models.py         ← Agent state & message definitions
│   │   │
│   │   ├── schemas/                  ← Pydantic request/response models
│   │   ├── repositories/             ← Data access layer
│   │   ├── db/
│   │   │   ├── session.py            ├─ Database connection
│   │   │   ├── vector_store.py       ├─ pgvector operations
│   │   │   └── base.py               └─ Base model declaration
│   │   │
│   │   ├── core/
│   │   │   ├── config.py             ├─ Environment configuration
│   │   │   ├── security.py           ├─ JWT, password hashing
│   │   │   └── dependencies.py       └─ FastAPI dependency injection
│   │   │
│   │   └── utils/                    ← Helper utilities
│   │
│   ├── tests/                        ← pytest test suite
│   │   ├── test_auth.py
│   │   ├── test_ai_services.py
│   │   └── test_candidate.py
│   │
│   ├── alembic/                      ← Database migrations
│   │   └── versions/
│   │       ├── 001_month2_ai_features.py
│   │       └── 002_month3_multi_agent_system.py
│   │
│   ├── requirements.txt              ← Python dependencies
│   ├── Dockerfile
│   ├── pytest.ini
│   ├── .env.example
│   └── README.md
│
├── 📁 frontend/                      ← React TypeScript frontend
│   ├── src/
│   │   ├── pages/
│   │   │   ├── auth/
│   │   │   │   ├── LoginPage.tsx
│   │   │   │   └── RegisterPage.tsx
│   │   │   ├── admin/
│   │   │   │   ├── AdminDashboard.tsx
│   │   │   │   └── AdminUsersPage.tsx
│   │   │   ├── candidate/
│   │   │   │   ├── CandidateDashboard.tsx
│   │   │   │   └── CandidateProfilePage.tsx
│   │   │   ├── recruiter/
│   │   │   │   ├── RecruiterDashboard.tsx
│   │   │   │   └── RecruiterProfilePage.tsx
│   │   │   └── ai/
│   │   │       └── AIPage.tsx         ← Semantic search & chat UI
│   │   │
│   │   ├── components/
│   │   │   ├── Navbar.tsx
│   │   │   ├── Alert.tsx
│   │   │   ├── LoadingState.tsx
│   │   │   └── CodeEditor/
│   │   │       └── AIActionsPanel.tsx ← AI actions (explain, bug detect, improve)
│   │   │
│   │   ├── services/
│   │   │   ├── apiClient.ts          ← Axios with JWT interceptor
│   │   │   ├── authService.ts
│   │   │   ├── api/aiService.ts      ← AI API calls
│   │   │   ├── adminService.ts
│   │   │   ├── candidateService.ts
│   │   │   └── recruiterService.ts
│   │   │
│   │   ├── context/
│   │   │   └── AuthContext.tsx       ← Global auth state
│   │   │
│   │   ├── types/                    ← TypeScript interfaces
│   │   │   ├── auth.ts
│   │   │   ├── profile.ts
│   │   │   ├── api.ts
│   │   │   └── admin.ts
│   │   │
│   │   ├── routes/
│   │   │   ├── ProtectedRoute.tsx    ← JWT check
│   │   │   ├── RoleRoute.tsx         ← Role-based access
│   │   │   └── HomeRedirect.tsx
│   │   │
│   │   ├── App.tsx
│   │   ├── App.css
│   │   └── main.tsx
│   │
│   ├── package.json
│   ├── tsconfig.json
│   ├── vite.config.ts
│   ├── .env.example
│   ├── .gitignore
│   └── README.md
│
├── 📁 docs/                          ← Complete documentation
│   └── PROJECT_DOCUMENTATION.md      ← 400+ lines, all project info
│
└── 📄 CLEANUP_SUMMARY.md             ← Repository cleanup report
```

**Key Design Patterns:**
- **Layered Architecture**: Routes → Services → Repositories → Models
- **Pydantic Schemas**: Never return ORM models directly from API
- **Dependency Injection**: FastAPI dependencies for auth, db sessions
- **Service Encapsulation**: Business logic isolated from HTTP layer
- **Vector Database**: pgvector for semantic search (1536-dim embeddings)

## 🚀 Quick Start

### Prerequisites
- **Python** 3.12+
- **Node.js** 18+
- **Docker** (recommended) or local PostgreSQL 16+
- **Git**

### Option 1: Docker (Recommended - 2 minutes)

```bash
# Clone repository
git clone https://github.com/RShashidhar007/CodeForge-AI.git
cd CodeForge-AI

# Configure environment
cp backend/.env.example backend/.env
# Edit backend/.env if needed (JWT_SECRET, admin credentials, etc.)

# Start everything
docker-compose up --build

# Wait 30 seconds for services to initialize...
```

**Access points:**
- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8080
- **API Docs**: http://localhost:8080/docs (Swagger)
- **ReDoc**: http://localhost:8080/redoc
- **Health**: http://localhost:8080/actuator/health

### Option 2: Local Development

**Backend:**
```bash
cd backend

# Setup Python environment
python -m venv venv
source venv/bin/activate              # Linux/Mac
# OR: .\venv\Scripts\Activate.ps1     # Windows

# Install dependencies
pip install -r requirements.txt

# Configure
cp .env.example .env
# Edit .env with required variables

# Run migrations
alembic upgrade head

# Start server
python -m app.main
```

**Frontend (in another terminal):**
```bash
cd frontend

npm install
npm run dev
```

## 📖 Demo Accounts

**Admin:**
```
Email:    admin@example.com
Password: Admin123!
```

**Candidates** (all passwords: `Student123!`):
- alice@student.com - Full Stack Developer
- bob@student.com - Backend Developer
- carol@student.com - Data Scientist
- david@student.com - Frontend Developer
- emma@student.com - DevOps Engineer

**Recruiters** (all passwords: `Recruiter123!`):
- sarah@recruiter.com @ TechCorp Solutions
- james@recruiter.com @ DataViz Analytics
- lisa@recruiter.com @ CloudStack Systems
- michael@recruiter.com @ FinTech Innovations
- jennifer@recruiter.com @ AI Research Labs

## 💬 Try the AI Features

1. **Login** as any user (candidate or recruiter)
2. **Navigate to AI** tab
3. **Ask questions** about code:
   - "What does this function do?"
   - "Find potential bugs"
   - "How can we improve this?"
   - "Generate unit tests"

## 📚 Documentation

- **[SETUP.md](SETUP.md)** - Detailed setup & configuration (15 pages)
- **[docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)** - Complete reference (400+ lines)
- **[backend/README.md](backend/README.md)** - Backend specifics
- **[frontend/README.md](frontend/README.md)** - Frontend specifics
- **API Docs**: http://localhost:8080/docs (interactive Swagger)

## 🔧 Configuration

### Environment Variables

**Backend** (`backend/.env`):
```env
# Required
DB_URL=postgresql://postgres:password@localhost:5432/recruitment_platform
JWT_SECRET=your-secret-at-least-32-characters-long
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!

# Optional - AI Features (OpenAI)
LLM_PROVIDER=openai
LLM_MODEL=gpt-4-turbo
LLM_API_KEY=sk-xxx...
EMBEDDING_MODEL=text-embedding-3-small
EMBEDDING_API_KEY=sk-xxx...

# Optional - Infrastructure
REDIS_URL=redis://localhost:6379
PORT=8080
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Frontend** (`frontend/.env.local`):
```env
VITE_API_BASE_URL=http://localhost:8080/api
```

See `.env.example` files for all available options.

## 📊 API Overview

| Endpoint | Method | Purpose | Auth |
|----------|--------|---------|------|
| `/api/auth/register/candidate` | POST | Register as candidate | ❌ |
| `/api/auth/register/recruiter` | POST | Register as recruiter | ❌ |
| `/api/auth/login` | POST | Get JWT token | ❌ |
| `/api/candidates/me` | GET/PUT | Candidate profile | ✅ CANDIDATE |
| `/api/recruiters/me` | GET/PUT | Recruiter profile | ✅ RECRUITER |
| `/api/admin/users` | GET | List all users | ✅ ADMIN |
| `/api/admin/stats` | GET | Platform stats | ✅ ADMIN |
| `/api/ai/chat` | POST | Chat with AI | ✅ ANY |
| `/api/ai/explain` | POST | Explain code | ✅ ANY |
| `/api/ai/bugs` | POST | Detect bugs | ✅ ANY |
| `/api/ai/improve` | POST | Improve code | ✅ ANY |
| `/api/ai/tests` | POST | Generate tests | ✅ ANY |
| `/api/v1/projects/{id}/ai/tasks` | POST | Create AI task | ✅ ANY |
| `/api/v1/projects/{id}/ai/tasks/{id}/approve` | POST | Approve task | ✅ ANY |

**Full API documentation:** http://localhost:8080/docs

## 🧪 Testing

**Backend:**
```bash
cd backend
pytest -v                    # Run all tests
pytest --cov=app             # With coverage
pytest tests/test_auth.py    # Specific file
```

**Frontend:**
```bash
cd frontend
npx tsc -b --noEmit   # Type check
npm run build         # Build test
```

## 🐳 Docker Commands

```bash
# Start all services
docker-compose up --build

# View logs
docker-compose logs -f
docker-compose logs backend
docker-compose logs frontend

# Stop services
docker-compose down

# Clean shutdown (remove data too)
docker-compose down -v

# Restart specific service
docker-compose restart backend
```

## 🔐 Security Checklist

- ✅ No `.env` files in git (`.gitignore` protection)
- ✅ JWT secrets must be ≥32 characters
- ✅ Passwords hashed with BCrypt (never stored plain)
- ✅ Role-based access control enforced server-side
- ✅ SQL injection protected (SQLAlchemy ORM)
- ✅ CORS configured to specific domains
- ✅ Error messages don't leak stack traces
- ✅ Sensitive data (embeddings, API keys) never logged

## 🚢 Deployment

See [SETUP.md](SETUP.md) for production deployment guide including:
- Gunicorn + Uvicorn configuration
- Docker image building
- Environment secrets management
- Database backup strategy
- Monitoring and logging setup

## 🎯 Project Timeline

| Month | Focus | Status |
|-------|-------|--------|
| **Month 1** | Authentication & Profiles | ✅ Complete |
| **Month 2** | AI Code Intelligence (RAG) | ✅ Complete |
| **Month 3** | Multi-Agent System | ✅ Complete |
| **Month 4** | Testing & Polish | ✅ Complete |

## 📈 System Stats

- **156+ files** across backend, frontend, docs
- **27 API endpoints** fully documented
- **20 database tables** with proper relationships
- **10 specialized AI agents** with task orchestration
- **10,000+ lines** of production code
- **60+ test points** for verification
- **0 secrets** in git (secure .gitignore)

## 🤝 Contributing

Found a bug? Have a suggestion? Great!

1. **Check existing issues** first
2. **Describe your problem/idea** in a new issue
3. **Create a pull request** for bug fixes or small features
4. **Discuss major changes** in an issue first

## 📄 License

MIT License - See LICENSE file for details

## 🆘 Support & Troubleshooting

**Port conflicts?**
```bash
# Find process using port 8080
lsof -i :8080  # macOS/Linux
netstat -ano | findstr :8080  # Windows
```

**Database connection error?**
```bash
# Check PostgreSQL running
docker ps | grep postgres

# Verify connection string in .env
# Format: postgresql://user:password@host:port/database
```

**AI features not working?**
```bash
# Ensure Redis is running
docker ps | grep redis

# Check OpenAI API key in .env (if using real provider)
# Or set LLM_PROVIDER=mock for development without API keys
```

**Frontend can't connect to backend?**
```bash
# Verify backend is running
curl http://localhost:8080/actuator/health

# Check frontend .env.local
cat frontend/.env.local

# Verify CORS_ALLOWED_ORIGINS in backend/.env
```

## 📞 Quick Links

- **GitHub Issues**: [Report bugs](https://github.com/RShashidhar007/CodeForge-AI/issues)
- **Discussions**: [Ask questions](https://github.com/RShashidhar007/CodeForge-AI/discussions)
- **API Docs**: http://localhost:8080/docs
- **Full Docs**: [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)

## 🎓 Learning Resources

This project demonstrates:
- **Backend**: FastAPI async patterns, SQLAlchemy ORM, JWT auth, RAG pipelines, LangGraph orchestration
- **Frontend**: React hooks, TypeScript types, Axios interceptors, protected routes
- **AI/ML**: Vector embeddings, semantic search, multi-agent systems, LLM integration
- **DevOps**: Docker Compose, database migrations, environment management
- **Security**: Password hashing, JWT tokens, CORS, role-based access control

## 🚀 Getting Started Paths

**New to the project?**
```
1. Read this README
2. Run docker-compose up
3. Login with demo account
4. Try the AI chat feature
5. Read PROJECT_DOCUMENTATION.md for deeper dive
```

**Backend developer?**
```
1. Read backend/README.md
2. Check app/services/* for business logic
3. Review app/api/routes/* for endpoint patterns
4. See tests/ for test examples
5. Explore agents/ for multi-agent system
```

**Frontend developer?**
```
1. Read frontend/README.md
2. Check src/pages/* for page structure
3. Review src/services/api/* for API integration
4. See src/components/* for component patterns
5. Explore src/types/* for TypeScript definitions
```

**AI/ML focused?**
```
1. See app/services/rag_service.py for RAG pipeline
2. Check app/agents/ for multi-agent orchestration
3. Review app/services/embedding_service.py for vectors
4. See app/services/llm_provider.py for LLM abstraction
5. Explore app/db/vector_store.py for pgvector operations
```

---

## ⚡ One-Liner Commands

```bash
# Clone and start
git clone https://github.com/RShashidhar007/CodeForge-AI.git && cd CodeForge-AI && docker-compose up --build

# Run backend tests
cd backend && pytest -v --cov=app

# Type-check frontend
cd frontend && npx tsc -b --noEmit

# View API docs (when running)
curl http://localhost:8080/docs

# Check database
docker-compose exec postgres psql -U postgres -d recruitment_platform
```

---

**Made with ❤️ for better technical recruitment**

**Status**: ✅ Production-Ready | **Version**: 1.0.0 | **Last Updated**: September 2026
