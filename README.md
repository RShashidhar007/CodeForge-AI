# CodeForge AI

An intelligent recruitment platform combining traditional hiring workflows with AI-powered code analysis capabilities.

**Stack:** Java 21 · Spring Boot 3.2.3 · Spring Security 6 (JWT) · Spring Data JPA · SQL Server 2022 · Redis 7+ · React 19 · TypeScript · Vite

---

## 🚀 Features

✅ **Authentication & Authorization**
- JWT-based auth with BCrypt password hashing
- Role-based access control (CANDIDATE, RECRUITER, ADMIN)
- Secure session management with Redis

✅ **User Management**
- Candidate profiles with skills, bio, GitHub/LinkedIn links
- Recruiter profiles with company association
- Admin dashboard with platform statistics

✅ **AI Code Intelligence** (Mock/Scaffold)
- Code explanation and documentation
- Bug detection and analysis
- Code improvement suggestions
- Test case generation

✅ **Multi-Agent Task System** (Partial)
- Task creation and management
- Agent execution tracking
- Task approval workflows

---

## 📋 Quick Start

### Prerequisites
- **JDK 21** (for compilation)
- **Maven 3.9+**
- **Node.js 18+**
- **Docker Desktop** (recommended)

### Option 1: Docker (Recommended - 2 minutes)

```bash
git clone https://github.com/RShashidhar007/CodeForge-AI.git
cd CodeForge-AI
cp backend/.env.example backend/.env
docker-compose up --build
```

**Access:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080/api
- Health Check: http://localhost:8080/api/health

### Option 2: Local Development

**Backend:**
```bash
cd backend
$env:JAVA_HOME="C:\Program Files\Java\latest\jdk-21"  # Windows
export JAVA_HOME="/path/to/jdk-21"  # Linux/Mac
cp .env.example .env
mvn spring-boot:run
# Or use: .\mvn-jdk21.ps1 spring-boot:run (Windows)
```

**Frontend:**
```bash
cd frontend
npm install
cp .env.example .env.local
npm run dev
```

---

## 📚 Documentation

📖 **[PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)** - Complete technical reference including:
- Detailed system architecture
- Database schema and relationships
- Complete API documentation
- Security implementation details
- Testing guide
- Deployment instructions
- Troubleshooting guide

---

## 🎯 Demo Accounts

**Admin:**
- Email: `admin@example.com`
- Password: `Admin123!`

**Demo Candidates** (Password: `Demo123!`):
- `alice@student.com` - Full Stack Developer
- `bob@student.com` - Backend Developer  
- `carol@student.com` - Data Scientist
- `david@student.com` - Frontend Developer
- `emma@student.com` - DevOps Engineer

**Demo Recruiters** (Password: `Demo123!`):
- `sarah@recruiter.com` @ TechCorp Solutions
- `james@recruiter.com` @ DataViz Analytics
- `lisa@recruiter.com` @ CloudStack Systems

---

## 🏗️ Architecture Overview

```
React Frontend (Vite + TypeScript)
         ↓
   REST API (JWT Auth)
         ↓
Spring Boot Backend (Java 21)
    ↙         ↘
SQL Server   Redis Cache
```

**Backend Layers:**
- **Controllers**: 27 REST endpoints
- **Services**: Business logic layer
- **Repositories**: Spring Data JPA (20 entities)
- **Security**: JWT + Spring Security 6

See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md) for detailed architecture diagrams.

---

## 🔧 Configuration

**Backend** (`backend/.env`):
```env
DB_HOST=localhost
DB_PORT=1433
DB_NAME=recruitment_platform
DB_USERNAME=sa
DB_PASSWORD=YourSecurePassword

JWT_SECRET=your-secret-key-min-32-chars-long
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!
CORS_ALLOWED_ORIGINS=http://localhost:5173
```

**Frontend** (`frontend/.env.local`):
```env
VITE_API_BASE_URL=http://localhost:8080/api
```

---

## 📊 API Overview

| Endpoint | Method | Auth | Description |
|----------|--------|------|-------------|
| `/api/auth/register/candidate` | POST | ❌ | Register candidate |
| `/api/auth/register/recruiter` | POST | ❌ | Register recruiter |
| `/api/auth/login` | POST | ❌ | Login & get JWT |
| `/api/candidates/me` | GET/PUT | ✅ | Candidate profile |
| `/api/recruiters/me` | GET/PUT | ✅ | Recruiter profile |
| `/api/admin/users` | GET | ✅ ADMIN | List users |
| `/api/admin/stats` | GET | ✅ ADMIN | Platform stats |
| `/api/admin/companies` | GET/POST | ✅ ADMIN | Manage companies |
| `/api/health` | GET | ❌ | Health check |

**Full API docs**: See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#api-documentation)

---

## 🧪 Testing

```bash
# Backend tests (38 tests)
cd backend
mvn test

# Frontend type check
cd frontend
npx tsc -b --noEmit
npm run build
```

---

## 🐳 Docker Commands

```bash
docker-compose up --build       # Start all services
docker-compose logs -f          # View logs
docker-compose down             # Stop services
docker-compose restart backend  # Restart backend only
```

---

## 🆘 Troubleshooting

**Backend won't compile?**
- Ensure JDK 21 is installed and `JAVA_HOME` is set correctly
- Use `mvn-jdk21.ps1` helper script on Windows

**Network error from frontend?**
- Check backend is running: `curl http://localhost:8080/api/health`
- Verify CORS configuration in `backend/src/main/java/com/codeforge/config/SecurityConfig.java`

**Demo users not working?**
- Check if `DemoDataSeeder` has `@Component` annotation enabled
- Restart backend to trigger seeding

**Database errors?**
- Verify SQL Server is running
- Check credentials in `backend/.env`
- For schema issues, try setting `DDL_AUTO=create` once, then back to `update`

**More solutions**: See [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md#troubleshooting)

---

## 📈 Project Stats

- **Backend**: 117 Java files, 20 JPA entities, 27 REST endpoints
- **Database**: 20 tables with relationships
- **Tests**: 38 unit/integration tests
- **Security**: JWT + BCrypt + Spring Security 6
- **Frontend**: React 19 with TypeScript

---

## 📂 Key Files

```
CodeForge-AI/
├── PROJECT_DOCUMENTATION.md    ← Complete technical reference
├── README.md                   ← This file (quick start)
├── docker-compose.yml          ← Docker orchestration
│
├── backend/
│   ├── mvn-jdk21.ps1          ← JDK 21 helper script (Windows)
│   ├── pom.xml                ← Maven dependencies
│   ├── .env.example           ← Environment template
│   └── src/main/java/com/codeforge/
│       ├── controller/        ← REST API endpoints
│       ├── service/           ← Business logic
│       ├── repository/        ← Database access
│       ├── entity/            ← JPA entities
│       ├── security/          ← JWT & Spring Security
│       └── config/            ← Spring configuration
│
└── frontend/
    ├── package.json           ← npm dependencies
    ├── .env.example           ← Environment template
    └── src/
        ├── pages/             ← React pages
        ├── components/        ← React components
        ├── services/          ← API clients
        └── context/           ← Global state
```

---

## 🔐 Security

- ✅ JWT tokens (24-hour expiry)
- ✅ BCrypt password hashing (strength 10)
- ✅ Role-based access control
- ✅ CORS configuration
- ✅ SQL injection protection (JPA)
- ✅ No secrets in git (`.gitignore`)

---

## 🚢 Production Checklist

- [ ] Change `JWT_SECRET` to strong random value (≥32 chars)
- [ ] Use strong database password
- [ ] Set `DDL_AUTO=validate` (not `update`)
- [ ] Configure proper CORS origins
- [ ] Enable HTTPS/TLS
- [ ] Set up database backups
- [ ] Configure monitoring (Spring Actuator)
- [ ] Enable Redis authentication
- [ ] Review rate limiting settings

---

## 📞 Support

- **Documentation**: [PROJECT_DOCUMENTATION.md](PROJECT_DOCUMENTATION.md)
- **Issues**: [GitHub Issues](https://github.com/RShashidhar007/CodeForge-AI/issues)
- **Health Check**: http://localhost:8080/api/health

---

## 🎓 What This Project Demonstrates

**Backend:**
- Spring Boot 3.2 with Java 21
- Spring Security 6 with JWT authentication
- Spring Data JPA with Hibernate 6
- RESTful API design
- Layered architecture (Controller → Service → Repository)
- JPA entity relationships and mappings
- Exception handling with `@ControllerAdvice`
- Maven multi-module project structure

**Frontend:**
- React 19 with hooks
- TypeScript for type safety
- Axios with request/response interceptors
- Protected routing with React Router
- Context API for global state
- Vite for fast builds

**DevOps:**
- Docker containerization
- Docker Compose orchestration
- Environment-based configuration
- Multi-stage Docker builds

---

**Made with ❤️ for better technical recruitment**

**Version**: 1.0.0 | **Status**: ✅ Production Ready | **Last Updated**: October 2026