# CodeForge AI - AI-Powered Recruitment & Code Intelligence Platform

[![Status](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)]()
[![Java](https://img.shields.io/badge/Java-17%2B-red)]()
[![Spring Boot](https://img.shields.io/badge/Spring%20Boot-3.2.3-brightgreen)]()
[![React](https://img.shields.io/badge/React-19-blue)]()
[![MSSQL](https://img.shields.io/badge/MSSQL%20Server-2022-blue)]()
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
| **Backend** | Spring Boot | 3.2.3 |
| **Language** | Java | 17+ |
| **Framework** | Spring Framework 6 | Latest |
| **Database** | MSSQL Server | 2022+ |
| **ORM** | Spring Data JPA + Hibernate | 6.4.4 |
| **Cache** | Redis | 7+ |
| **Authentication** | Auth0 JWT | 4.4.0 |
| **Password Hashing** | BCrypt | - |
| **Build Tool** | Maven | 3.9+ |
| **AI/LLM** | OpenAI API | GPT-4 Turbo |
| **Frontend** | React | 19 |
| **Language** | TypeScript | 6 |
| **Build Tool** | Vite | 8 |
| **HTTP Client** | Axios | Latest |
| **Infrastructure** | Docker Compose | Latest |

## 🏗 Architecture

```
┌─────────────────────────────────────────────────────┐
│                   React Frontend                     │
│              (TypeScript, Vite, Axios)              │
└────────────────────────┬────────────────────────────┘
                         │ HTTPS/REST
┌────────────────────────▼────────────────────────────┐
│          Spring Boot 3.2.3 Backend (Java 17+)       │
│  ┌─────────────────────────────────────────────┐  │
│  │  27 REST API Endpoints (Spring MVC)         │  │
│  │  - Auth (3), Candidates (2), Recruiters (2) │  │
│  │  - Admin (5), AI/RAG (7), Tasks (5)         │  │
│  │  - Health (1)                              │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │  Service Layer                              │  │
│  │  - AuthService, CandidateService           │  │
│  │  - RecruiterService, AdminService          │  │
│  │  - AIService, TaskService                  │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │  Spring Data JPA + Hibernate 6.4.4          │  │
│  │  - 20 Entity Classes (Users, Candidates...)│  │
│  │  - 20 Repository Interfaces                │  │
│  │  - Transaction Management                  │  │
│  └─────────────────────────────────────────────┘  │
│  ┌─────────────────────────────────────────────┐  │
│  │  Spring Security 6.x                        │  │
│  │  - JWT Authentication                      │  │
│  │  - Role-Based Access Control               │  │
│  │  - Method-Level Security                   │  │
│  └─────────────────────────────────────────────┘  │
└────────────────┬────────────────────┬──────────────┘
                 │                    │
    ┌────────────▼──────────┐  ┌──────▼─────────────┐
    │   MSSQL Server 2022   │  │    Redis 7+        │
    │                       │  │    (Cache)         │
    │   20 Tables           │  │                    │
    │   Relationships       │  │                    │
    │   Indexes             │  └────────────────────┘
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
├── 📄 docker-compose.yml             ← Complete local dev environment
├── 📄 .gitignore                     ← Excludes secrets, caches, dependencies
│
├── 📁 backend/                       ← Spring Boot Java backend
│   ├── src/main/java/com/codeforge/
│   │   ├── CodeForgeApplication.java ← Spring Boot entry point
│   │   ├── controller/               ← Spring MVC controllers (27 endpoints)
│   │   │   ├── AuthController.java       ├─ Authentication (login, register)
│   │   │   ├── AdminController.java      ├─ Admin operations (users, stats)
│   │   │   ├── CandidateController.java  ├─ Candidate profiles
│   │   │   ├── RecruiterController.java  ├─ Recruiter profiles
│   │   │   ├── AIController.java         ├─ AI/RAG endpoints (chat, analysis)
│   │   │   ├── TaskController.java       ├─ Multi-agent task management
│   │   │   └── HealthController.java     └─ Health check endpoint
│   │   │
│   │   ├── entity/                   ← JPA Entity classes (20 total)
│   │   │   ├── User.java, Candidate.java, Recruiter.java
│   │   │   ├── Company.java, Project.java
│   │   │   ├── AIConversation.java, AIMessage.java
│   │   │   ├── AITask.java, TaskApproval.java
│   │   │   ├── AIAnalysis.java, CodeDocument.java
│   │   │   └── RepositoryIndexMetadata.java
│   │   │
│   │   ├── repository/               ← Spring Data JPA Repositories
│   │   │   ├── UserRepository.java
│   │   │   ├── CandidateRepository.java
│   │   │   ├── RecruiterRepository.java
│   │   │   ├── AdminRepository.java
│   │   │   ├── AIConversationRepository.java
│   │   │   ├── AITaskRepository.java
│   │   │   └── CompanyRepository.java
│   │   │
│   │   ├── service/                 ← Business logic layer
│   │   │   ├── AuthService.java          ├─ JWT, BCrypt, login/register
│   │   │   ├── CandidateService.java     ├─ Candidate operations
│   │   │   ├── RecruiterService.java     ├─ Recruiter operations
│   │   │   ├── AdminService.java         ├─ Admin operations
│   │   │   ├── AIService.java            ├─ AI chat & analysis
│   │   │   └── TaskService.java          └─ Agent task management
│   │   │
│   │   ├── dto/                      ← Data Transfer Objects
│   │   │   ├── request/
│   │   │   │   ├── LoginRequest.java
│   │   │   │   ├── RegisterCandidateRequest.java
│   │   │   │   ├── CandidateProfileUpdateRequest.java
│   │   │   │   ├── ChatRequest.java
│   │   │   │   ├── CreateTaskRequest.java
│   │   │   │   └── CreateCompanyRequest.java
│   │   │   └── response/
│   │   │       ├── LoginResponse.java
│   │   │       ├── UserResponse.java
│   │   │       ├── CandidateProfileResponse.java
│   │   │       ├── ChatResponse.java
│   │   │       ├── AITaskResponse.java
│   │   │       └── PlatformStatsResponse.java
│   │   │
│   │   ├── security/                 ← Spring Security & JWT
│   │   │   ├── JWTProvider.java           ├─ JWT token generation/validation
│   │   │   ├── JWTFilter.java            ├─ Servlet filter for JWT
│   │   │   ├── UserDetailsServiceImpl.java├─ Spring Security user loader
│   │   │   ├── SecurityConfig.java       ├─ Spring Security configuration
│   │   │   └── SecurityUser.java         └─ Authentication principal
│   │   │
│   │   ├── exception/                ← Exception handling
│   │   │   ├── GlobalExceptionHandler.java
│   │   │   ├── ResourceNotFoundException.java
│   │   │   ├── DuplicateResourceException.java
│   │   │   ├── BadCredentialsException.java
│   │   │   ├── AccessDeniedException.java
│   │   │   └── ErrorResponse.java
│   │   │
│   │   ├── config/                   ← Spring Boot configuration
│   │   │   ├── AppProperties.java        ├─ @ConfigurationProperties
│   │   │   ├── SecurityConfig.java       ├─ Spring Security beans
│   │   │   ├── CorsConfig.java           ├─ CORS configuration
│   │   │   ├── RedisConfig.java          ├─ Redis connection pool
│   │   │   └── JpaConfig.java            └─ JPA/Hibernate configuration
│   │   │
│   │   └── util/                     ← Utility classes
│   │
│   ├── src/test/java/com/codeforge/  ← JUnit 5 + Mockito tests
│   │   ├── AuthServiceTest.java
│   │   ├── AuthControllerTest.java
│   │   ├── JWTProviderTest.java
│   │   └── UserRepositoryTest.java
│   │
│   ├── src/main/resources/
│   │   ├── application.properties      ← Spring Boot configuration
│   │   ├── application-test.properties ← Test configuration (H2 DB)
│   │   └── db/migration/               ← Flyway migrations (optional)
│   │
│   ├── pom.xml                        ← Maven dependencies & plugins
│   ├── Dockerfile                     ← Multi-stage Docker build
│   ├── .env.example                   ← Environment template
│   └── .dockerignore
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
│   ├── PROJECT_DOCUMENTATION.md      ← Full project reference
│   ├── BACKEND.md                    ← Backend setup & architecture
│   └── TESTING.md                    ← Testing guide
│
└── 📄 docker-compose.yml             ← MSSQL, Redis, Spring Boot, React
```

**Key Design Patterns:**
- **Layered Architecture**: Controller → Service → Repository → Entity
- **DTO Pattern**: Never return JPA entities directly from API
- **Dependency Injection**: Spring @Autowired for loose coupling
- **Service Encapsulation**: Business logic isolated from HTTP layer
- **Spring Data JPA**: Type-safe queries without raw SQL
- **Spring Security**: Method-level and endpoint-level authorization

## 🚀 Quick Start

### Prerequisites
- **Java** 17+ (with Maven 3.9+)
- **Node.js** 18+
- **Docker** (recommended) or local MSSQL Server 2022
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
- **Backend API**: http://localhost:8080/api
- **API Docs**: http://localhost:8080/api/swagger-ui.html (Swagger)
- **Health**: http://localhost:8080/api/actuator/health

### Option 2: Local Development

**Backend:**
```bash
cd backend

# Prerequisites
# - Java 17+ installed
# - MSSQL Server 2022 running (or use Docker for DB only)
# - Redis running (or use Docker)

# Build with Maven
mvn clean install

# Configure
cp .env.example .env
# Edit .env with required variables

# Start server
java -jar target/codeforge-backend-1.0.0.jar
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

- **[docs/BACKEND.md](docs/BACKEND.md)** - Backend architecture, setup, API endpoints
- **[docs/TESTING.md](docs/TESTING.md)** - Testing guide for backend & frontend
- **[docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md)** - Complete reference (400+ lines)
- **API Docs**: http://localhost:8080/api/swagger-ui.html (interactive Swagger)
- **Health Check**: http://localhost:8080/api/actuator/health

## 🔧 Configuration

### Environment Variables

**Backend** (`backend/.env`):
```env
# Required
spring.datasource.url=jdbc:sqlserver://mssql:1433;databaseName=recruitment_platform;encrypt=true;trustServerCertificate=true;
spring.datasource.username=sa
spring.datasource.password=Admin@123456
app.jwt.secret=your-secret-at-least-32-characters-long
app.admin.email=admin@example.com
app.admin.password=Admin123!

# Optional - AI Features (OpenAI)
app.ai.llm.provider=openai
app.ai.llm.model=gpt-4-turbo
app.ai.llm.api-key=sk-xxx...
app.ai.embedding.provider=openai
app.ai.embedding.model=text-embedding-3-small
app.ai.embedding.api-key=sk-xxx...

# Infrastructure
spring.redis.host=redis
spring.redis.port=6379
app.cors.allowed-origins=http://localhost:5173,http://localhost:3000
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
| `/api/admin/companies` | GET/POST | Company management | ✅ ADMIN |
| `/api/actuator/health` | GET | Health check | ❌ |

**Full API documentation:** http://localhost:8080/api/swagger-ui.html

## 🧪 Testing

**Backend:**
```bash
cd backend
mvn test                              # Run all tests
mvn test -Dtest=AuthServiceTest       # Specific test class
mvn test -DargLine="-Duser.timezone=UTC"  # With timezone
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

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md) for production deployment guide including:
- Docker image building and pushing
- Kubernetes configuration
- MSSQL database setup
- Redis cache configuration
- Environment secrets management
- Health monitoring and logging setup

## 🎯 Project Timeline

| Month | Focus | Status |
|-------|-------|--------|
| **Month 1** | Authentication & Profiles | ✅ Complete |
| **Month 2** | AI Code Intelligence (RAG) | ✅ Complete |
| **Month 3** | Multi-Agent System | ✅ Complete |
| **Month 4** | Testing & Polish | ✅ Complete |

## 📈 System Stats

- **90+ Java classes** (entities, controllers, services, DTOs)
- **20 JPA entities** (User, Candidate, Recruiter, Company, etc.)
- **27 REST API endpoints** fully documented
- **20 MSSQL database tables** with proper relationships
- **4 test classes** (AuthService, AuthController, JWT, Repository)
- **Spring Boot 3.2.3** with Java 17+
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
- **Backend**: Spring Boot 3 async patterns, Spring Data JPA, JWT auth, Spring Security 6
- **Frontend**: React hooks, TypeScript types, Axios interceptors, protected routes
- **Database**: MSSQL Server, JPA entity mapping, Hibernate configuration
- **DevOps**: Docker Compose, Maven builds, environment management
- **Security**: Password hashing (BCrypt), JWT tokens, CORS, role-based access control

## 🚀 Getting Started Paths

**New to the project?**
```
1. Read this README
2. Run docker-compose up
3. Login with demo account
4. Try the AI chat feature
5. Read docs/PROJECT_DOCUMENTATION.md for deeper dive
```

**Backend developer?**
```
1. Read docs/BACKEND.md
2. Check src/main/java/com/codeforge/service/* for business logic
3. Review src/main/java/com/codeforge/controller/* for endpoint patterns
4. See src/test/java/* for test examples
5. Explore pom.xml for dependency configuration
```

**Frontend developer?**
```
1. Read frontend/README.md
2. Check src/pages/* for page structure
3. Review src/services/* for API integration
4. See src/components/* for component patterns
5. Explore src/types/* for TypeScript definitions
```

**DevOps/Infrastructure?**
```
1. Review docker-compose.yml for service orchestration
2. Check backend/Dockerfile for multi-stage builds
3. See backend/.env.example for configuration
4. Review backend/pom.xml for Maven configuration
5. Explore backend/.dockerignore for build optimization
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
