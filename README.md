# CodeForge AI

A recruitment platform with role-based access (Candidate / Recruiter / Admin) and an AI code-intelligence module (scaffold).

**Stack:** Java 17 · Spring Boot 3.2 · Spring Security (JWT) · Spring Data JPA · Microsoft SQL Server · Redis · React 19 + TypeScript + Vite

## What works today

| Area | Status |
|---|---|
| Registration & login (candidate, recruiter) with BCrypt + JWT | Implemented |
| Admin bootstrap from `ADMIN_EMAIL` / `ADMIN_PASSWORD` on first start | Implemented |
| Candidate profile (bio, skills, links) and recruiter profile (phone, position, bio) | Implemented |
| Admin dashboard: platform stats, user list, enable/disable users, company creation API | Implemented |
| Role-protected routes (frontend) and endpoints (backend), CORS for the Vite dev server | Implemented |
| AI endpoints: chat, explain, bugs, improve, tests, index status | **Scaffold: returns mock responses**, no LLM is called |
| Repository indexing / embeddings / semantic search | **Not implemented** (data model only) |
| Multi-agent task workflow | **Partial**: task endpoints and entities exist, no agents run |
| Project & company creation UI, AI chat page routing | Not wired: the AI page/components exist in `frontend/src` but are not routed, and there is no API to create a `Project` |

Design notes for the intended full system are in [`docs/ROADMAP_AND_DESIGN_NOTES.md`](docs/ROADMAP_AND_DESIGN_NOTES.md).

## Quick start

Requirements: Docker (with Compose), Node 20+.

```bash
# 1. Backend stack: SQL Server + Redis + API  (http://localhost:8080/api)
./start.sh                 # or: docker compose up --build

# 2. Frontend (second terminal)
cd frontend
cp .env.example .env.local
npm install
npm run dev                # http://localhost:5173
```

Sign in as the admin (`admin@example.com` / `Admin123!`, configurable) or register a candidate/recruiter.

Health check: `GET http://localhost:8080/api/actuator/health`

### Running the backend without Docker
Requires JDK 17-21 and Maven 3.9+, plus a SQL Server with an empty database named `recruitment_platform` and Redis:

```bash
cd backend
cp .env.example .env       # then export the variables, or set them in your IDE
DB_HOST=localhost REDIS_HOST=localhost mvn spring-boot:run
```

Tables are created by Hibernate (`spring.jpa.hibernate.ddl-auto=update`, override with `DDL_AUTO`).

## Configuration (backend environment variables)

| Variable | Default | Purpose |
|---|---|---|
| `DB_HOST` / `DB_PORT` / `DB_NAME` | `localhost` / `1433` / `recruitment_platform` | SQL Server connection |
| `DB_USERNAME` / `DB_PASSWORD` | `sa` / `Admin@123456` | Database credentials |
| `REDIS_HOST` / `REDIS_PORT` | `localhost` / `6379` | Redis |
| `JWT_SECRET` | dev placeholder | **Change in production** (32+ chars) |
| `CORS_ALLOWED_ORIGINS` | `http://localhost:5173,...` | Allowed browser origins |
| `ADMIN_EMAIL` / `ADMIN_PASSWORD` / `ADMIN_NAME` | `admin@example.com` / `Admin123!` / `Platform Admin` | Bootstrap admin |
| `LLM_PROVIDER`, `EMBEDDING_PROVIDER` | `mock` | Only `mock` exists today |

Frontend: `VITE_API_BASE_URL` (default `http://localhost:8080/api`).

## API overview (context path `/api`)

- `POST /auth/register/candidate`, `POST /auth/register/recruiter`, `POST /auth/login`
- `GET|PUT /candidates/me`, `GET|PUT /recruiters/me`
- `GET /admin/stats`, `GET /admin/users`, `PATCH /admin/users/{id}/status`, `GET|POST /admin/companies`
- `/v1/projects/{projectId}/ai/...` chat, explain, bugs, improve, tests, status, tasks (mock)
- `GET /actuator/health`

## Tests

```bash
cd backend && mvn test          # uses H2 (profile "test")
cd frontend && npm run build && npm run lint
```

## Notes on the JSON contract
The backend emits some fields in `snake_case` (e.g. `token_type`, `user_id`). The frontend converts response keys to `camelCase` in a single Axios interceptor (`frontend/src/services/apiClient.ts`); request bodies are `camelCase`.
