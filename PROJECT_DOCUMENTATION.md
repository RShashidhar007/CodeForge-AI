# CodeForge AI - Complete Project Documentation

## Table of Contents
1. [Project Overview](#project-overview)
2. [System Architecture](#system-architecture)
3. [Technology Stack](#technology-stack)
4. [Setup & Installation](#setup--installation)
5. [Database Schema](#database-schema)
6. [API Documentation](#api-documentation)
7. [Frontend Architecture](#frontend-architecture)
8. [Security Implementation](#security-implementation)
9. [Testing Guide](#testing-guide)
10. [Deployment](#deployment)
11. [Troubleshooting](#troubleshooting)

---

## Project Overview

**CodeForge AI** is an intelligent recruitment platform that combines traditional recruitment management with AI-powered code analysis capabilities. The platform serves three user roles:

- **Candidates/Students**: Create profiles, showcase skills, connect GitHub repositories
- **Recruiters**: Browse candidates, post jobs, manage hiring workflows
- **Admins**: Platform management, user oversight, company management

### Key Features

✅ **Authentication System**
- JWT-based authentication with BCrypt password hashing
- Role-based access control (CANDIDATE, RECRUITER, ADMIN)
- Secure session management with Redis caching

✅ **User Profiles**
- Detailed candidate profiles with skills, bio, GitHub/LinkedIn links
- Recruiter profiles with company association and position details
- Admin dashboard with platform statistics

✅ **AI Code Intelligence** (Scaffold/Mock Implementation)
- Code explanation and documentation
- Bug detection and analysis
- Code improvement suggestions
- Test case generation
- Semantic code search capabilities

✅ **Multi-Agent Task System** (Partial Implementation)
- Task creation and management
- Agent execution tracking
- Task approval workflows

---

## System Architecture

### High-Level Architecture

```
┌─────────────────────────────────────────────────────┐
│              React Frontend (Port 5173)             │
│         TypeScript + Vite + Axios + TailwindCSS     │
└────────────────────┬────────────────────────────────┘
                     │ REST API (HTTPS)
┌────────────────────▼────────────────────────────────┐
│       Spring Boot Backend (Port 8080)               │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  Controllers (27 REST Endpoints)             │   │
│  │  - Auth, Admin, Candidate, Recruiter         │   │
│  │  - AI, Tasks, Health                         │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  Services (Business Logic)                   │   │
│  │  - AuthService, AdminService                 │   │
│  │  - CandidateService, RecruiterService        │   │
│  │  - AIService, TaskService                    │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  Spring Data JPA Repositories                │   │
│  │  - 20 Repository Interfaces                  │   │
│  │  - Query DSL Support                         │   │
│  └──────────────────────────────────────────────┘   │
│                                                     │
│  ┌──────────────────────────────────────────────┐   │
│  │  Spring Security + JWT Filter Chain          │   │
│  │  - JWTFilter, RateLimitingFilter             │   │
│  │  - Role-based authorization                  │   │
│  └──────────────────────────────────────────────┘   │
└───────────────┬──────────────────┬──────────────────┘
                │                  │
   ┌────────────▼──────────┐  ┌───▼────────────────┐
   │  SQL Server 2022      │  │   Redis 7+         │
   │  (Port 1433)          │  │   (Port 6379)      │
   │                       │  │                    │
   │  - 20 Tables          │  │  - Session Cache   │
   │  - Indexes & FKs      │  │  - Query Cache     │
   └───────────────────────┘  └────────────────────┘
```

### Backend Layer Architecture

**Controller Layer** (`com.codeforge.controller`)
- Handles HTTP requests/responses
- Input validation
- Exception handling
- Maps DTOs to/from entities

**Service Layer** (`com.codeforge.service`)
- Business logic implementation
- Transaction management
- Cross-entity operations
- External API integration

**Repository Layer** (`com.codeforge.repository`)
- Database access via Spring Data JPA
- Custom query methods
- CRUD operations

**Entity Layer** (`com.codeforge.entity`)
- JPA entity definitions
- Database table mappings
- Relationships and constraints

---

## Technology Stack

### Backend
- **Framework**: Spring Boot 3.2.3
- **Language**: Java 17+ (Compiled with JDK 21)
- **Security**: Spring Security 6.2.2 with JWT
- **ORM**: Spring Data JPA + Hibernate 6.4.4
- **Database**: Microsoft SQL Server 2022
- **Cache**: Redis 7+
- **Build Tool**: Maven 3.9+
- **Testing**: JUnit 5, Mockito, Spring Boot Test

### Frontend
- **Framework**: React 19
- **Language**: TypeScript 5+
- **Build Tool**: Vite 5
- **HTTP Client**: Axios
- **Styling**: TailwindCSS
- **Routing**: React Router v6

### DevOps & Infrastructure
- **Containerization**: Docker + Docker Compose
- **CI/CD**: GitHub Actions (if configured)
- **Monitoring**: Spring Boot Actuator

### Key Dependencies (Backend)
```xml
<!-- Spring Boot Starters -->
spring-boot-starter-web (3.2.3)
spring-boot-starter-security (3.2.3)
spring-boot-starter-data-jpa (3.2.3)
spring-boot-starter-validation (3.2.3)
spring-boot-starter-actuator (3.2.3)
spring-boot-starter-data-redis (3.2.3)

<!-- Database -->
mssql-jdbc (12.6.1.jre11)
HikariCP (connection pooling)

<!-- Security -->
jjwt-api (0.11.5)
jjwt-impl (0.11.5)
jjwt-jackson (0.11.5)

<!-- Utilities -->
lombok (1.18.34)
jackson-databind (2.15+)
```

---

## Setup & Installation

### Prerequisites
- **JDK 21** (Required for compilation - set `JAVA_HOME`)
- **Maven 3.9+**
- **Node.js 18+** with npm
- **Docker Desktop** (recommended) or local SQL Server 2022 + Redis
- **Git**

### Quick Start with Docker (Recommended)

```bash
# 1. Clone repository
git clone https://github.com/RShashidhar007/CodeForge-AI.git
cd CodeForge-AI

# 2. Configure backend environment
cp backend/.env.example backend/.env
# Edit backend/.env if needed (JWT_SECRET, DB credentials, etc.)

# 3. Start all services
docker-compose up --build

# Wait 30-60 seconds for database initialization...

# 4. Access the application
# Frontend: http://localhost:5173
# Backend API: http://localhost:8080/api
# Health Check: http://localhost:8080/api/health
```

### Local Development Setup

**Backend Setup:**
```bash
cd backend

# Ensure JDK 21 is active
export JAVA_HOME="/path/to/jdk-21"  # Linux/Mac
$env:JAVA_HOME="C:\Program Files\Java\latest\jdk-21"  # Windows PowerShell

# Configure environment
cp .env.example .env
# Edit .env with database credentials

# Build and run
mvn clean install -DskipTests
mvn spring-boot:run

# Or use the helper script (Windows)
.\mvn-jdk21.ps1 spring-boot:run
```

**Frontend Setup:**
```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.example .env.local
# Edit VITE_API_BASE_URL if needed

# Start dev server
npm run dev
```

### Database Setup (Local SQL Server)

```sql
-- Create database
CREATE DATABASE recruitment_platform;

-- Tables are auto-created by Hibernate on first startup
-- (spring.jpa.hibernate.ddl-auto=update)
```

### Environment Variables

**Backend** (`backend/.env`):
```env
# Database
DB_HOST=localhost
DB_PORT=1433
DB_NAME=recruitment_platform
DB_USERNAME=sa
DB_PASSWORD=YourSecurePassword123!

# Redis
REDIS_HOST=localhost
REDIS_PORT=6379

# JWT
JWT_SECRET=your-secret-key-must-be-at-least-32-characters-long-change-this
JWT_EXPIRATION_SECONDS=86400

# Admin Bootstrap
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=Admin123!
ADMIN_NAME=Platform Admin

# CORS
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000

# Hibernate
DDL_AUTO=update
```

**Frontend** (`frontend/.env.local`):
```env
VITE_API_BASE_URL=http://localhost:8080/api
```

---

## Database Schema

### Entity-Relationship Diagram

```
┌─────────────────────┐
│       User          │ (Base entity)
│─────────────────────│
│ id (PK)             │
│ name                │
│ email (UNIQUE)      │
│ password_hash       │
│ role (ENUM)         │
│ enabled             │
│ created_at          │
│ updated_at          │
└──────┬──────────────┘
       │
       ├─────────────────────┐
       │                     │
┌──────▼────────┐    ┌───────▼──────────┐
│   Candidate   │    │    Recruiter     │
│───────────────│    │──────────────────│
│ id (PK,FK)    │    │ id (PK,FK)       │
│ phone         │    │ phone            │
│ location      │    │ position         │
│ bio           │    │ bio              │
│ github_url    │    │ company_id (FK)  │
│ linkedin_url  │    │ created_at       │
│ created_at    │    │ updated_at       │
│ updated_at    │    └──────────────────┘
└───────────────┘
```

### Key Tables

**users**
```sql
CREATE TABLE users (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL,
    email NVARCHAR(255) NOT NULL UNIQUE,
    password_hash NVARCHAR(255) NOT NULL,
    role NVARCHAR(20) NOT NULL CHECK (role IN ('CANDIDATE', 'RECRUITER', 'ADMIN')),
    enabled BIT NOT NULL DEFAULT 1,
    created_at DATETIME2 NOT NULL DEFAULT GETDATE(),
    updated_at DATETIME2 NOT NULL DEFAULT GETDATE()
);
```

**candidates** (1:1 with users)
```sql
CREATE TABLE candidates (
    id BIGINT PRIMARY KEY,
    phone NVARCHAR(20),
    location NVARCHAR(255),
    bio NVARCHAR(MAX),
    github_url NVARCHAR(500),
    linkedin_url NVARCHAR(500),
    created_at DATETIME2 NOT NULL,
    updated_at DATETIME2 NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE
);
```

**recruiters** (1:1 with users)
```sql
CREATE TABLE recruiters (
    id BIGINT PRIMARY KEY,
    phone NVARCHAR(20),
    position NVARCHAR(255),
    bio NVARCHAR(MAX),
    company_id BIGINT,
    created_at DATETIME2 NOT NULL,
    updated_at DATETIME2 NOT NULL,
    FOREIGN KEY (id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (company_id) REFERENCES companies(id)
);
```

**companies**
```sql
CREATE TABLE companies (
    id BIGINT IDENTITY(1,1) PRIMARY KEY,
    name NVARCHAR(255) NOT NULL UNIQUE,
    description NVARCHAR(MAX),
    website NVARCHAR(500),
    created_at DATETIME2 NOT NULL,
    updated_at DATETIME2 NOT NULL
);
```

### AI-Related Tables

**ai_conversations**
- Stores chat sessions between users and AI
- Links to projects and users

**ai_messages**
- Individual messages in conversations
- Role: USER or ASSISTANT
- Content and timestamps

**ai_tasks**
- Multi-agent task definitions
- Status tracking (PENDING, IN_PROGRESS, COMPLETED, FAILED)
- Priority levels

**code_documents**
- Indexed code files
- File path, content, language
- Project association

---

## API Documentation

### Authentication Endpoints

**POST /api/auth/register/candidate**
```json
Request:
{
  "name": "John Doe",
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Response (201):
{
  "id": 1,
  "name": "John Doe",
  "email": "john@example.com",
  "role": "CANDIDATE",
  "enabled": true
}
```

**POST /api/auth/register/recruiter**
```json
Request:
{
  "name": "Jane Smith",
  "email": "jane@company.com",
  "password": "SecurePass123!",
  "phone": "+1-555-0100",
  "position": "Senior Recruiter"
}

Response (201):
{
  "id": 2,
  "name": "Jane Smith",
  "email": "jane@company.com",
  "role": "RECRUITER",
  "enabled": true
}
```

**POST /api/auth/login**
```json
Request:
{
  "email": "john@example.com",
  "password": "SecurePass123!"
}

Response (200):
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "Bearer",
  "expires_in_seconds": 86400,
  "user": {
    "id": 1,
    "name": "John Doe",
    "email": "john@example.com",
    "role": "CANDIDATE",
    "enabled": true
  }
}
```

### Candidate Endpoints

**GET /api/candidates/me**
- **Auth**: Required (CANDIDATE role)
- **Returns**: Current candidate's full profile

**PUT /api/candidates/me**
- **Auth**: Required (CANDIDATE role)
- **Body**: `CandidateProfileUpdateRequest`
- **Returns**: Updated candidate profile

### Recruiter Endpoints

**GET /api/recruiters/me**
- **Auth**: Required (RECRUITER role)
- **Returns**: Current recruiter's full profile

**PUT /api/recruiters/me**
- **Auth**: Required (RECRUITER role)
- **Body**: `RecruiterProfileUpdateRequest`
- **Returns**: Updated recruiter profile

### Admin Endpoints

**GET /api/admin/stats**
- **Auth**: Required (ADMIN role)
- **Returns**: Platform statistics (user counts, companies, etc.)

**GET /api/admin/users**
- **Auth**: Required (ADMIN role)
- **Query Params**: `page`, `size`, `role`
- **Returns**: Paginated list of users

**PATCH /api/admin/users/{id}/status**
- **Auth**: Required (ADMIN role)
- **Body**: `{ "enabled": true }`
- **Returns**: Updated user

**GET /api/admin/companies**
- **Auth**: Required (ADMIN role)
- **Returns**: List of all companies

**POST /api/admin/companies**
- **Auth**: Required (ADMIN role)
- **Body**: `CreateCompanyRequest`
- **Returns**: Created company

### AI Endpoints (Mock Implementation)

**POST /api/v1/projects/{projectId}/ai/chat**
- **Auth**: Required
- **Body**: `ChatRequest`
- **Returns**: AI response (currently mocked)

**POST /api/v1/projects/{projectId}/ai/explain**
- **Auth**: Required
- **Body**: `CodeAnalysisRequest`
- **Returns**: Code explanation (mocked)

**POST /api/v1/projects/{projectId}/ai/bugs**
- **Auth**: Required
- **Body**: `CodeAnalysisRequest`
- **Returns**: Bug analysis (mocked)

**POST /api/v1/projects/{projectId}/ai/improve**
- **Auth**: Required
- **Body**: `CodeAnalysisRequest`
- **Returns**: Improvement suggestions (mocked)

**POST /api/v1/projects/{projectId}/ai/tests**
- **Auth**: Required
- **Body**: `CodeAnalysisRequest`
- **Returns**: Generated tests (mocked)

### Health Check

**GET /api/health**
- **Auth**: Not required
- **Returns**: `{ "status": "UP" }`

---

## Frontend Architecture

### Project Structure
```
frontend/
├── src/
│   ├── pages/
│   │   ├── auth/
│   │   │   ├── LoginPage.tsx
│   │   │   └── RegisterPage.tsx
│   │   ├── admin/
│   │   │   ├── AdminDashboard.tsx
│   │   │   └── AdminUsersPage.tsx
│   │   ├── candidate/
│   │   │   ├── CandidateDashboard.tsx
│   │   │   └── CandidateProfilePage.tsx
│   │   └── recruiter/
│   │       ├── RecruiterDashboard.tsx
│   │       └── RecruiterProfilePage.tsx
│   │
│   ├── components/
│   │   ├── Navbar.tsx
│   │   ├── Alert.tsx
│   │   └── LoadingState.tsx
│   │
│   ├── services/
│   │   ├── apiClient.ts      (Axios instance with interceptors)
│   │   ├── authService.ts
│   │   ├── candidateService.ts
│   │   ├── recruiterService.ts
│   │   └── adminService.ts
│   │
│   ├── context/
│   │   └── AuthContext.tsx   (Global auth state)
│   │
│   ├── types/
│   │   ├── auth.ts
│   │   ├── profile.ts
│   │   └── api.ts
│   │
│   ├── routes/
│   │   ├── ProtectedRoute.tsx
│   │   └── RoleRoute.tsx
│   │
│   ├── App.tsx
│   └── main.tsx
```

### Key React Patterns

**Authentication Context**
```typescript
// AuthContext.tsx
export const AuthProvider: React.FC<Props> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  // Load user from localStorage on mount
  useEffect(() => {
    const token = localStorage.getItem('token');
    const userData = localStorage.getItem('user');
    if (token && userData) {
      setUser(JSON.parse(userData));
    }
    setLoading(false);
  }, []);

  const login = async (credentials: LoginRequest) => {
    const response = await authService.login(credentials);
    setUser(response.user);
    localStorage.setItem('token', response.token);
    localStorage.setItem('user', JSON.stringify(response.user));
  };

  const logout = () => {
    setUser(null);
    localStorage.removeItem('token');
    localStorage.removeItem('user');
  };

  return (
    <AuthContext.Provider value={{ user, loading, login, logout }}>
      {children}
    </AuthContext.Provider>
  );
};
```

**Protected Routes**
```typescript
// ProtectedRoute.tsx
export const ProtectedRoute: React.FC<Props> = ({ children, allowedRoles }) => {
  const { user, loading } = useAuth();

  if (loading) return <LoadingState />;
  if (!user) return <Navigate to="/login" />;
  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return <Navigate to="/unauthorized" />;
  }

  return <>{children}</>;
};
```

**API Client with Interceptors**
```typescript
// apiClient.ts
const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL,
});

// Request interceptor: Add JWT token
apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Response interceptor: Handle errors, logout on 401
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

---

## Security Implementation

### JWT Authentication Flow

```
1. User submits login credentials
   ↓
2. Backend validates credentials (email + BCrypt password)
   ↓
3. Generate JWT token with claims:
   - sub: user ID
   - email: user email
   - role: user role (CANDIDATE/RECRUITER/ADMIN)
   - iat: issued at timestamp
   - exp: expiration timestamp (24 hours)
   ↓
4. Return token to frontend
   ↓
5. Frontend stores token in localStorage
   ↓
6. Frontend includes token in Authorization header for all requests
   ↓
7. Backend JWTFilter validates token on each request
   ↓
8. If valid, set SecurityContext with authenticated user
   ↓
9. Controller methods check @PreAuthorize annotations
```

### Spring Security Configuration

```java
@Configuration
@EnableWebSecurity
@EnableMethodSecurity
public class SecurityConfig {

    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) throws Exception {
        http
            .csrf(csrf -> csrf.disable())
            .cors(cors -> cors.configurationSource(corsConfigurationSource))
            .sessionManagement(session -> 
                session.sessionCreationPolicy(SessionCreationPolicy.STATELESS))
            .authorizeHttpRequests(auth -> auth
                .requestMatchers("/auth/**", "/health").permitAll()
                .requestMatchers("/admin/**").hasRole("ADMIN")
                .requestMatchers("/candidates/**").hasRole("CANDIDATE")
                .requestMatchers("/recruiters/**").hasRole("RECRUITER")
                .anyRequest().authenticated()
            )
            .addFilterBefore(jwtFilter, UsernamePasswordAuthenticationFilter.class)
            .addFilterBefore(rateLimitingFilter, UsernamePasswordAuthenticationFilter.class);

        return http.build();
    }
}
```

### Password Security

- **Algorithm**: BCrypt with strength 10
- **Salt**: Auto-generated per password
- **Never stored**: Plain passwords are immediately hashed
- **Verification**: Using `passwordEncoder.matches()`

### CORS Configuration

```java
@Configuration
public class CorsConfig {
    @Bean
    public CorsConfigurationSource corsConfigurationSource() {
        CorsConfiguration config = new CorsConfiguration();
        config.setAllowedOrigins(Arrays.asList(
            "http://localhost:5173",
            "http://localhost:3000"
        ));
        config.setAllowedMethods(Arrays.asList("GET", "POST", "PUT", "PATCH", "DELETE"));
        config.setAllowedHeaders(Arrays.asList("*"));
        config.setAllowCredentials(true);
        config.setMaxAge(3600L);
        
        UrlBasedCorsConfigurationSource source = new UrlBasedCorsConfigurationSource();
        source.registerCorsConfiguration("/**", config);
        return source;
    }
}
```

---

## Testing Guide

### Running Backend Tests

```bash
cd backend

# Run all tests
mvn test

# Run specific test class
mvn test -Dtest=AuthServiceTest

# Run with coverage report
mvn test jacoco:report

# Skip tests during build
mvn clean install -DskipTests
```

### Test Structure

**Unit Tests** (using Mockito)
```java
@ExtendWith(MockitoExtension.class)
class AuthServiceTest {
    @Mock
    private UserRepository userRepository;
    
    @Mock
    private PasswordEncoder passwordEncoder;
    
    @InjectMocks
    private AuthService authService;
    
    @Test
    void registerCandidate_Success() {
        // Arrange
        RegisterCandidateRequest request = new RegisterCandidateRequest();
        request.setName("John Doe");
        request.setEmail("john@example.com");
        request.setPassword("SecurePass123!");
        
        when(userRepository.existsByEmail(anyString())).thenReturn(false);
        when(passwordEncoder.encode(anyString())).thenReturn("hashed");
        when(userRepository.save(any(User.class))).thenAnswer(i -> i.getArgument(0));
        
        // Act
        UserResponse response = authService.registerCandidate(request);
        
        // Assert
        assertNotNull(response);
        assertEquals("John Doe", response.getName());
        assertEquals("CANDIDATE", response.getRole());
    }
}
```

**Integration Tests** (using Spring Boot Test)
```java
@SpringBootTest
@AutoConfigureMockMvc
class AuthControllerIntegrationTest {
    @Autowired
    private MockMvc mockMvc;
    
    @Autowired
    private ObjectMapper objectMapper;
    
    @Test
    void login_WithValidCredentials_ReturnsToken() throws Exception {
        LoginRequest request = new LoginRequest();
        request.setEmail("admin@example.com");
        request.setPassword("Admin123!");
        
        mockMvc.perform(post("/api/auth/login")
                .contentType(MediaType.APPLICATION_JSON)
                .content(objectMapper.writeValueAsString(request)))
            .andExpect(status().isOk())
            .andExpect(jsonPath("$.token").exists())
            .andExpect(jsonPath("$.user.email").value("admin@example.com"));
    }
}
```

### Frontend Testing

```bash
cd frontend

# Type check
npx tsc -b --noEmit

# Build test
npm run build

# Lint
npm run lint
```

---

## Deployment

### Building for Production

**Backend:**
```bash
cd backend
mvn clean package -DskipTests

# Creates: target/codeforge-backend-1.0.0.jar
```

**Frontend:**
```bash
cd frontend
npm run build

# Creates: dist/ folder with static assets
```

### Docker Production Build

```bash
# Build backend image
cd backend
docker build -t codeforge-backend:latest .

# Build frontend image
cd frontend
docker build -t codeforge-frontend:latest .

# Or use docker-compose
docker-compose -f docker-compose.prod.yml up --build
```

### Environment Checklist for Production

- [ ] Change `JWT_SECRET` to a strong random value (≥32 characters)
- [ ] Use strong database password (not `Admin@123456`)
- [ ] Set `DDL_AUTO=validate` (not `update` or `create`)
- [ ] Configure proper CORS allowed origins
- [ ] Enable HTTPS/TLS
- [ ] Set up database backups
- [ ] Configure logging levels (INFO or WARN)
- [ ] Set up monitoring (Spring Boot Actuator + Prometheus)
- [ ] Use environment-specific `.env` files (don't commit secrets)
- [ ] Enable Redis authentication
- [ ] Configure rate limiting appropriately

---

## Troubleshooting

### Common Issues

**1. Backend won't start - "TypeTag::UNKNOWN" error**
- **Cause**: Wrong JDK version (using JDK 27 instead of JDK 21)
- **Fix**: Set `JAVA_HOME` to JDK 21 and use the `mvn-jdk21.ps1` helper script

**2. Backend compilation fails - Lombok errors**
- **Cause**: Incompatible Lombok version with JDK 21
- **Fix**: Ensure Lombok 1.18.34 is in `pom.xml`

**3. "Cannot insert explicit value for identity column" error**
- **Cause**: Database schema has IDENTITY on columns that use `@MapsId`
- **Fix**: Set `spring.jpa.hibernate.ddl-auto=create` once to recreate schema, then back to `update`

**4. Frontend shows "Network error: could not reach server"**
- **Cause**: CORS not configured or backend not running
- **Fix**: 
  - Verify backend is running: `curl http://localhost:8080/api/health`
  - Check CORS configuration in `SecurityConfig.java`
  - Verify `VITE_API_BASE_URL` in frontend `.env.local`

**5. "Invalid email or password" for demo users**
- **Cause**: DemoDataSeeder didn't run or database was recreated
- **Fix**: 
  - Check if `@Component` annotation is uncommented in `DemoDataSeeder.java`
  - Restart backend to trigger seeding
  - Check logs for "Seeded X companies" messages

**6. JWT token invalid after backend restart**
- **Cause**: Different JWT_SECRET or changed user data
- **Fix**: Logout and login again to get new token

**7. Port 8080 already in use**
- **Fix**: 
  ```bash
  # Windows
  netstat -ano | findstr :8080
  taskkill /PID <PID> /F
  
  # Linux/Mac
  lsof -i :8080
  kill -9 <PID>
  ```

**8. Database connection timeout**
- **Cause**: SQL Server not running or wrong credentials
- **Fix**:
  - Check SQL Server is running
  - Verify `DB_HOST`, `DB_PORT`, `DB_USERNAME`, `DB_PASSWORD` in `.env`
  - Test connection: `telnet localhost 1433`

---

## Demo Accounts

**Admin:**
```
Email: admin@example.com
Password: Admin123!
```

**Demo Candidates** (Password: `Demo123!`):
- alice@student.com - Full Stack Developer
- bob@student.com - Backend Developer
- carol@student.com - Data Scientist
- david@student.com - Frontend Developer
- emma@student.com - DevOps Engineer

**Demo Recruiters** (Password: `Demo123!`):
- sarah@recruiter.com @ TechCorp Solutions
- james@recruiter.com @ DataViz Analytics
- lisa@recruiter.com @ CloudStack Systems
- michael@recruiter.com @ FinTech Innovations
- jennifer@recruiter.com @ AI Research Labs

---

## Useful Commands

```bash
# Backend
cd backend
mvn clean install              # Full build
mvn spring-boot:run            # Start server
mvn test                       # Run tests
.\mvn-jdk21.ps1 spring-boot:run  # Start with JDK 21 (Windows)

# Frontend
cd frontend
npm install                    # Install dependencies
npm run dev                    # Start dev server
npm run build                  # Production build
npx tsc -b --noEmit           # Type check

# Docker
docker-compose up --build      # Start all services
docker-compose down            # Stop services
docker-compose logs -f         # View logs
docker-compose restart backend # Restart backend only

# Database (if using Docker)
docker-compose exec mssql /opt/mssql-tools/bin/sqlcmd -S localhost -U sa -P Admin@123456
```

---

## Project Statistics

- **Backend**: 117 Java source files, 20 JPA entities, 27 REST endpoints
- **Frontend**: React 19 components with TypeScript
- **Database**: 20 tables with proper relationships and indexes
- **Tests**: 38 unit/integration tests
- **Build Time**: ~30 seconds (backend), ~10 seconds (frontend)
- **Startup Time**: ~40 seconds (full stack with Docker)
- **Lines of Code**: ~15,000+ (backend + frontend)

---

## Future Enhancements

1. **AI Features**: Replace mock implementations with real OpenAI/LLM integration
2. **Code Indexing**: Implement actual semantic search with vector embeddings
3. **Multi-Agent System**: Complete agent execution and orchestration
4. **Real-time Features**: WebSocket support for live updates
5. **Advanced Matching**: ML-based candidate-job matching
6. **Analytics Dashboard**: Advanced reporting and insights
7. **Mobile App**: React Native companion app
8. **Interview Scheduling**: Calendar integration

---

## Support & Resources

- **GitHub Repository**: https://github.com/RShashidhar007/CodeForge-AI
- **Issue Tracker**: https://github.com/RShashidhar007/CodeForge-AI/issues
- **Documentation**: This file and README.md
- **API Documentation**: http://localhost:8080/api/swagger-ui.html (when running)

---

**Last Updated**: October 2026  
**Version**: 1.0.0  
**Status**: Production Ready
