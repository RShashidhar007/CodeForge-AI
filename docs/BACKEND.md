# CodeForge AI Backend - Spring Boot

Java/Spring Boot backend for the CodeForge AI recruitment platform. Migrated from Python FastAPI.

## Quick Start

### Prerequisites

- Java 17+
- Maven 3.9+
- Docker & Docker Compose (for containerized setup)
- MSSQL Server 2022 (or Docker)
- Redis 7+ (or Docker)

### Local Development (Without Docker)

1. **Set up environment variables:**
```bash
cp .env.example .env
# Edit .env with your configuration
```

2. **Build the project:**
```bash
mvn clean install
```

3. **Run the application:**
```bash
mvn spring-boot:run
```

The backend will be available at `http://localhost:8080/api`

### Docker Setup

1. **Build and run with Docker Compose:**
```bash
docker-compose up --build
```

This starts:
- MSSQL Server on port 1433
- Redis on port 6379
- Spring Boot backend on port 8080

2. **Access the API:**
```
http://localhost:8080/api
```

## Project Structure

```
backend/
├── pom.xml                          Maven build configuration
├── Dockerfile                       Multi-stage Docker build
├── docker-compose.yml              Container orchestration
├── .env.example                    Environment template
├── README.md                        This file
│
├── src/main/java/com/codeforge/
│   ├── CodeForgeApplication.java    Spring Boot entry point
│   │
│   ├── controller/                  REST API endpoints
│   │   ├── AuthController.java      Authentication (3 endpoints)
│   │   ├── CandidateController.java Candidate profile (2 endpoints)
│   │   ├── RecruiterController.java Recruiter profile (2 endpoints)
│   │   ├── AdminController.java     Admin operations (5 endpoints)
│   │   ├── AIController.java        AI/RAG services (7 endpoints)
│   │   ├── TaskController.java      AI task management (5 endpoints)
│   │   └── HealthController.java    Health check (1 endpoint)
│   │
│   ├── service/                     Business logic layer
│   │   ├── AuthService.java         User registration & login
│   │   ├── CandidateService.java    Candidate profile management
│   │   ├── RecruiterService.java    Recruiter profile management
│   │   ├── AdminService.java        Platform administration
│   │   ├── AIService.java           AI/RAG operations
│   │   └── TaskService.java         Multi-agent task execution
│   │
│   ├── repository/                  Data access layer
│   │   ├── UserRepository.java
│   │   ├── CandidateRepository.java
│   │   ├── RecruiterRepository.java
│   │   ├── CompanyRepository.java
│   │   ├── ProjectRepository.java
│   │   ├── FileRepository.java
│   │   ├── GithubTokenRepository.java
│   │   ├── CodeDocumentRepository.java
│   │   ├── CodeChunkRepository.java
│   │   ├── AIConversationRepository.java
│   │   ├── AIMessageRepository.java
│   │   ├── AIAnalysisRepository.java
│   │   ├── RepositoryIndexMetadataRepository.java
│   │   ├── AITaskRepository.java
│   │   ├── AgentExecutionRepository.java
│   │   ├── TaskPatchRepository.java
│   │   ├── TaskApprovalRepository.java
│   │   ├── TaskTestResultRepository.java
│   │   └── TaskWorkspaceRepository.java
│   │
│   ├── entity/                      JPA entities (20 total)
│   │   ├── User.java
│   │   ├── Candidate.java
│   │   ├── Recruiter.java
│   │   ├── Company.java
│   │   ├── Project.java
│   │   ├── File.java
│   │   ├── GithubToken.java
│   │   ├── CodeDocument.java
│   │   ├── CodeChunk.java
│   │   ├── AIConversation.java
│   │   ├── AIMessage.java
│   │   ├── AIAnalysis.java
│   │   ├── RepositoryIndexMetadata.java
│   │   ├── AITask.java
│   │   ├── AgentExecution.java
│   │   ├── TaskPatch.java
│   │   ├── TaskApproval.java
│   │   ├── TaskTestResult.java
│   │   ├── TaskWorkspace.java
│   │   └── Skill.java
│   │
│   ├── dto/                         Request/Response DTOs
│   │   ├── request/                 Request objects
│   │   │   ├── RegisterCandidateRequest.java
│   │   │   ├── RegisterRecruiterRequest.java
│   │   │   ├── LoginRequest.java
│   │   │   ├── CandidateProfileUpdateRequest.java
│   │   │   ├── RecruiterProfileUpdateRequest.java
│   │   │   ├── ChatRequest.java
│   │   │   ├── CodeAnalysisRequest.java
│   │   │   ├── CreateTaskRequest.java
│   │   │   ├── ApproveTaskRequest.java
│   │   │   └── CreateCompanyRequest.java
│   │   │
│   │   └── response/                Response objects
│   │       ├── LoginResponse.java
│   │       ├── UserResponse.java
│   │       ├── CandidateProfileResponse.java
│   │       ├── RecruiterProfileResponse.java
│   │       ├── ChatResponse.java
│   │       ├── CodeAnalysisResponse.java
│   │       ├── IndexStatusResponse.java
│   │       ├── AITaskResponse.java
│   │       ├── PlatformStatsResponse.java
│   │       ├── UserSummaryResponse.java
│   │       ├── PageResponse.java
│   │       └── CompanyResponse.java
│   │
│   ├── security/                    JWT & authentication
│   │   ├── JWTProvider.java         Token generation/validation
│   │   ├── JWTFilter.java           JWT extraction filter
│   │   ├── SecurityUser.java        Spring Security UserDetails
│   │   └── UserDetailsServiceImpl.java  User loading service
│   │
│   ├── exception/                   Error handling
│   │   ├── ResourceNotFoundException.java
│   │   ├── DuplicateResourceException.java
│   │   ├── BadCredentialsException.java
│   │   ├── AccessDeniedException.java
│   │   ├── ErrorResponse.java
│   │   └── GlobalExceptionHandler.java
│   │
│   └── config/                      Spring configuration
│       ├── AppProperties.java       Configuration properties
│       ├── SecurityConfig.java      Spring Security setup
│       ├── CorsConfig.java          CORS configuration
│       ├── RedisConfig.java         Redis integration
│       └── JpaConfig.java           JPA setup
│
└── src/main/resources/
    ├── application.properties       Main configuration
    ├── application-dev.properties   Development profile
    └── application-prod.properties  Production profile
```

## API Endpoints (27 Total)

### Authentication (3)
- `POST /auth/register/candidate` - Register candidate
- `POST /auth/register/recruiter` - Register recruiter
- `POST /auth/login` - User login

### Candidate Profile (2)
- `GET /candidates/me` - Get candidate profile (protected)
- `PUT /candidates/me` - Update candidate profile (protected)

### Recruiter Profile (2)
- `GET /recruiters/me` - Get recruiter profile (protected)
- `PUT /recruiters/me` - Update recruiter profile (protected)

### Admin Operations (5)
- `GET /admin/stats` - Platform statistics (admin only)
- `GET /admin/users` - List users (admin only)
- `PATCH /admin/users/{id}/status` - Set user status (admin only)
- `POST /admin/companies` - Create company (admin only)
- `GET /admin/companies` - List companies (admin only)

### AI/RAG Services (7)
- `POST /v1/projects/{projectId}/ai/chat` - Chat with AI
- `POST /v1/projects/{projectId}/ai/explain` - Explain code
- `POST /v1/projects/{projectId}/ai/bugs` - Detect bugs
- `POST /v1/projects/{projectId}/ai/improve` - Suggest improvements
- `POST /v1/projects/{projectId}/ai/tests` - Generate tests
- `GET /v1/projects/{projectId}/ai/status` - Indexing status
- `GET /v1/projects/{projectId}/ai/conversations/{conversationId}/history` - Chat history

### Multi-Agent Tasks (5)
- `POST /v1/projects/{projectId}/ai/tasks` - Create task
- `GET /v1/projects/{projectId}/ai/tasks` - List tasks
- `GET /v1/projects/{projectId}/ai/tasks/{taskId}` - Get task
- `POST /v1/projects/{projectId}/ai/tasks/{taskId}/approve` - Approve task
- `POST /v1/projects/{projectId}/ai/tasks/{taskId}/cancel` - Cancel task

### Health (1)
- `GET /actuator/health` - Health check

## Configuration

### application.properties

Key settings:

```properties
# Server
server.port=8080
server.servlet.context-path=/api

# Database
spring.datasource.url=jdbc:sqlserver://mssql:1433;...
spring.datasource.username=sa
spring.datasource.password=${DB_PASSWORD}

# JPA/Hibernate
spring.jpa.hibernate.ddl-auto=validate
spring.jpa.database-platform=org.hibernate.dialect.SQLServerDialect

# Redis
spring.redis.host=${REDIS_HOST:localhost}
spring.redis.port=${REDIS_PORT:6379}

# JWT
app.jwt.secret=${JWT_SECRET}
app.jwt.expiration=${JWT_EXPIRATION_SECONDS:86400}
app.jwt.algorithm=HS256

# CORS
app.cors.allowed-origins=${CORS_ALLOWED_ORIGINS}

# Admin Bootstrap
app.admin.email=${ADMIN_EMAIL}
app.admin.password=${ADMIN_PASSWORD}
```

## Authentication

All protected endpoints require a JWT token in the `Authorization` header:

```
Authorization: Bearer <token>
```

### Token Generation

1. Register or login to get a token
2. Token includes user ID, email, and role (CANDIDATE, RECRUITER, ADMIN)
3. Token expires in 24 hours (configurable)

### Role-Based Access

- **CANDIDATE**: Access candidate endpoints
- **RECRUITER**: Access recruiter endpoints
- **ADMIN**: Full access to admin operations

## Database

### Schema

The application uses an existing MSSQL database with 20 tables:

- Users & Profiles: `users`, `candidates`, `recruiters`
- Organizations: `companies`, `projects`
- Code Management: `files`, `code_documents`, `code_chunks`, `github_tokens`
- AI/RAG: `ai_conversations`, `ai_messages`, `ai_analyses`, `repository_index_metadata`
- Multi-Agent Tasks: `ai_tasks`, `agent_executions`, `task_patches`, `task_approvals`, `task_test_results`, `task_workspaces`

### Migrations

No automatic migrations are run. The application validates the existing schema using Hibernate's `ddl-auto=validate`.

To add new migrations:
1. Create SQL files in `src/main/resources/db/migration/`
2. Follow Flyway naming: `V001__description.sql`

## Redis Integration

Used for:
- Session caching
- Embedding vector caching
- Rate limiting (future)

Configuration:
```properties
spring.redis.host=redis
spring.redis.port=6379
spring.cache.type=redis
```

## AI/LLM Integration

### Current Implementation

- Mock LLM provider for development/testing
- OpenAI provider ready (configure with `LLM_PROVIDER=openai`)
- Embeddings for semantic search (currently mock)

### Configuration

```properties
app.ai.llm.provider=mock|openai
app.ai.llm.model=gpt-4-turbo
app.ai.llm.api-key=sk-...

app.ai.embedding.provider=mock|openai
app.ai.embedding.model=text-embedding-3-small
```

### Month 3 Multi-Agent System

The LangGraph agent orchestration is kept as a separate Python service (not migrated).

## Error Handling

All endpoints return standardized error responses:

```json
{
  "timestamp": "2026-09-11T12:00:00Z",
  "status": 400,
  "error": "Bad Request",
  "message": "Validation failed",
  "path": "/api/auth/login",
  "details": ["email: must not be blank"]
}
```

HTTP Status Codes:
- `200 OK` - Success
- `201 Created` - Resource created
- `400 Bad Request` - Validation error
- `401 Unauthorized` - Invalid credentials or expired token
- `403 Forbidden` - Insufficient permissions
- `404 Not Found` - Resource not found
- `409 Conflict` - Duplicate resource
- `500 Internal Server Error` - Server error

## Testing

Run tests:
```bash
mvn test
```

Test coverage includes:
- Unit tests for services
- Integration tests for repositories
- Controller tests for API endpoints
- Security tests for JWT and role-based access

## Build & Deployment

### Local JAR Build

```bash
mvn clean package
java -jar target/codeforge-backend-1.0.0.jar
```

### Docker Build

```bash
docker build -t codeforge-backend:latest .
```

### Production Deployment

1. Set environment variables securely
2. Use production database (separate MSSQL instance)
3. Configure Redis for caching
4. Set JWT_SECRET to a strong random value
5. Configure CORS_ALLOWED_ORIGINS for frontend domain
6. Set admin credentials securely

## Monitoring

Health endpoint: `GET /actuator/health`

Response:
```json
{
  "status": "UP",
  "timestamp": 1694425200000
}
```

## Troubleshooting

### Database connection issues

```
Check MSSQL_HOST, DB_PASSWORD, and MSSQL_DB settings
Verify network connectivity: telnet mssql:1433
```

### Redis connection issues

```
Check REDIS_HOST and REDIS_PORT
Verify Redis is running: redis-cli ping
```

### JWT token issues

```
Ensure JWT_SECRET is at least 32 characters
Check token expiration: JWT_EXPIRATION_SECONDS
Verify Authorization header format: "Bearer <token>"
```

### CORS issues

```
Add frontend URL to CORS_ALLOWED_ORIGINS (comma-separated)
Verify Authorization header is exposed
```

## Technologies

- **Framework:** Spring Boot 3.2.3
- **Java Version:** 17
- **Build Tool:** Maven
- **Database:** MSSQL Server 2022
- **Cache:** Redis 7
- **Authentication:** JWT (HS256)
- **Validation:** Jakarta Validation API
- **JSON Serialization:** Jackson
- **ORM:** Spring Data JPA / Hibernate

## Changelog

### Version 1.0.0 (Migration Release)

- ✅ Migrated from Python FastAPI to Spring Boot
- ✅ All 27 API endpoints implemented
- ✅ JWT authentication with role-based access
- ✅ Redis integration for caching
- ✅ MSSQL database preserved (20 tables)
- ✅ Error handling and validation
- ✅ CORS configuration
- ✅ Docker support
- ✅ API documentation (this README)

## Support

For issues or questions:

1. Check this README and troubleshooting section
2. Review application logs: `docker logs recruitment-platform-api`
3. Check database connectivity: MSSQL logs
4. Check Redis: `redis-cli info`
5. Review Spring Boot actuator endpoints: `/actuator/metrics`

## License

Proprietary - CodeForge AI Platform
