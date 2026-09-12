# Recruitment Platform - Python FastAPI Backend

This is a Python/FastAPI migration of the original Java Spring Boot backend, maintaining **complete functional parity**.

## Features

- **Authentication**: JWT-based with BCrypt password hashing
- **Authorization**: Role-based access control (CANDIDATE, RECRUITER, ADMIN)
- **User Management**: Registration, login, profile management
- **Admin Functions**: User management, company management, platform statistics
- **Database**: PostgreSQL with SQLAlchemy ORM
- **Migrations**: Alembic for database schema management
- **API Documentation**: Auto-generated Swagger UI at `/docs`

## Tech Stack

- **FastAPI** 0.109.0 - Modern Python web framework
- **SQLAlchemy** 2.0.25 - ORM for database operations
- **Alembic** 1.13.1 - Database migrations
- **Pydantic** 2.5.3 - Data validation and settings management
- **python-jose** - JWT token generation and validation
- **passlib** - Password hashing with BCrypt
- **PostgreSQL** - Primary database
- **pytest** - Testing framework

## Project Structure

```
backend-python/
├── app/
│   ├── api/
│   │   └── routes/          # API endpoints (controllers)
│   │       ├── auth.py      # Registration & login
│   │       ├── candidates.py # Candidate profile
│   │       ├── recruiters.py # Recruiter profile
│   │       └── admin.py     # Admin operations
│   ├── core/
│   │   ├── config.py        # Settings management
│   │   ├── security.py      # JWT & password hashing
│   │   └── dependencies.py  # FastAPI dependencies
│   ├── db/
│   │   ├── base.py          # Database engine & base
│   │   └── session.py       # Session management
│   ├── models/              # SQLAlchemy models (entities)
│   │   ├── user.py
│   │   ├── candidate.py
│   │   ├── recruiter.py
│   │   └── company.py
│   ├── repositories/        # Data access layer
│   ├── schemas/             # Pydantic schemas (DTOs)
│   ├── services/            # Business logic
│   ├── exceptions/          # Custom exceptions
│   ├── utils/               # Utility functions
│   └── main.py              # Application entry point
├── alembic/                 # Database migrations
├── tests/                   # Test suite
├── requirements.txt         # Python dependencies
├── .env.example             # Environment variables template
└── README.md
```

## Setup

### 1. Prerequisites

- Python 3.12+
- PostgreSQL 16+
- pip or uv

### 2. Install Dependencies

```bash
cd backend-python
pip install -r requirements.txt
```

Or using `uv`:

```bash
uv pip install -r requirements.txt
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

```env
DB_URL=postgresql://postgres:password@localhost:5432/recruitment_platform
JWT_SECRET=your-secret-key-at-least-32-characters-long
JWT_EXPIRATION_SECONDS=86400
CORS_ALLOWED_ORIGINS=http://localhost:5173
ADMIN_EMAIL=admin@example.com
ADMIN_PASSWORD=SecurePassword123!
ADMIN_NAME=Platform Admin
PORT=8080
```

**Important**: Generate a secure JWT secret:
```bash
openssl rand -hex 32
```

### 4. Setup Database

Start PostgreSQL (using Docker Compose from project root):

```bash
docker-compose up -d postgres
```

Or use your local PostgreSQL instance and create the database:

```sql
CREATE DATABASE recruitment_platform;
```

### 5. Run Migrations

```bash
# Create initial migration
alembic revision --autogenerate -m "Initial schema"

# Apply migrations
alembic upgrade head
```

### 6. Run the Application

```bash
# Development mode with hot reload
python -m app.main

# Or using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8080
```

The API will be available at:
- **API**: http://localhost:8080
- **Swagger Docs**: http://localhost:8080/docs
- **ReDoc**: http://localhost:8080/redoc

## API Endpoints

### Authentication (Public)

- `POST /api/auth/register/candidate` - Register new candidate
- `POST /api/auth/register/recruiter` - Register new recruiter
- `POST /api/auth/login` - Login and get JWT token

### Candidate (Requires CANDIDATE role)

- `GET /api/candidates/me` - Get own profile
- `PUT /api/candidates/me` - Update own profile

### Recruiter (Requires RECRUITER role)

- `GET /api/recruiters/me` - Get own profile
- `PUT /api/recruiters/me` - Update own profile

### Admin (Requires ADMIN role)

- `GET /api/admin/users` - List users (with pagination)
- `PATCH /api/admin/users/{id}/status` - Enable/disable user
- `GET /api/admin/stats` - Platform statistics
- `POST /api/admin/companies` - Create company
- `GET /api/admin/companies` - List companies (with pagination)

### Health

- `GET /actuator/health` - Health check endpoint

## Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/test_auth.py

# Run with verbose output
pytest -v
```

## Development Workflow

### 1. Making Database Changes

```bash
# After modifying models, create a migration
alembic revision --autogenerate -m "Description of changes"

# Review the generated migration file
# Then apply it
alembic upgrade head

# Rollback if needed
alembic downgrade -1
```

### 2. Adding New Endpoints

1. Create/update Pydantic schemas in `app/schemas/`
2. Add business logic to services in `app/services/`
3. Create route handler in `app/api/routes/`
4. Add tests in `tests/`

### 3. Code Quality

```bash
# Format code
black app/ tests/

# Lint code
ruff check app/ tests/

# Type checking (if using mypy)
mypy app/
```

## Migration from Java

This backend is a complete migration from the original Java Spring Boot implementation with **functional parity**:

| Java Component | Python Equivalent |
|----------------|-------------------|
| `@RestController` | FastAPI `APIRouter` |
| `@Service` | Service classes |
| `JpaRepository` | Repository classes with SQLAlchemy |
| `@Entity` | SQLAlchemy models |
| Java Records (DTOs) | Pydantic schemas |
| `@PreAuthorize("hasRole")` | FastAPI `Depends` with role checkers |
| Spring Security JWT | python-jose JWT |
| BCryptPasswordEncoder | passlib bcrypt |
| `@RestControllerAdvice` | FastAPI exception handlers |
| Hibernate | SQLAlchemy ORM |
| application.yml | pydantic-settings |
| Maven | pip/requirements.txt |
| JUnit | pytest |

## Environment Variables

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| `DB_URL` | PostgreSQL connection string | Yes | - |
| `JWT_SECRET` | Secret key for JWT signing (≥32 chars) | Yes | - |
| `JWT_EXPIRATION_SECONDS` | JWT token expiration time | No | 86400 (24h) |
| `CORS_ALLOWED_ORIGINS` | Comma-separated allowed origins | No | http://localhost:5173 |
| `ADMIN_EMAIL` | Bootstrap admin email | Yes | - |
| `ADMIN_PASSWORD` | Bootstrap admin password | Yes | - |
| `ADMIN_NAME` | Bootstrap admin name | No | Platform Admin |
| `PORT` | Server port | No | 8080 |

## Troubleshooting

### Database Connection Errors

Ensure PostgreSQL is running and the connection string is correct:

```bash
# Test connection
psql -h localhost -U postgres -d recruitment_platform
```

### Migration Errors

If you encounter migration conflicts:

```bash
# Check current migration status
alembic current

# View migration history
alembic history

# Stamp database at specific revision
alembic stamp head
```

### JWT Secret Errors

Ensure JWT_SECRET is at least 32 characters long:

```bash
# Generate a secure secret
openssl rand -hex 32
```

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t recruitment-platform-api .

# Run container
docker run -d \
  -p 8080:8080 \
  --env-file .env \
  --name recruitment-api \
  recruitment-platform-api
```

### Important Security Notes

1. **Never** commit `.env` files
2. Use strong JWT secrets in production
3. Use HTTPS in production (not HTTP)
4. Set `CORS_ALLOWED_ORIGINS` to specific domains
5. Consider using a secrets manager (AWS Secrets Manager, HashiCorp Vault)
6. Enable database SSL connections in production
7. Keep dependencies updated for security patches

## License

Same as the main project.

## Support

For issues, questions, or contributions, please refer to the main project repository.
