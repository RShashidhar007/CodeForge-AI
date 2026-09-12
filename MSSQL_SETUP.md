# MSSQL Setup Guide - CodeForge AI Demo

This project now uses **MSSQL Server 2022** instead of PostgreSQL for local development and demo purposes.

## Quick Start

### Using Docker (Recommended)

```bash
# Start all services (MSSQL, Redis, Backend, Frontend)
& '.\start.ps1'              # Windows
bash start.sh                # Unix/Linux/macOS

# Or direct docker-compose
docker-compose up --build
```

**Access points:**
- Frontend: http://localhost:5173
- Backend API: http://localhost:8080
- API Docs: http://localhost:8080/docs
- MSSQL: localhost:1433 (sa / Admin@123456)

---

## Database Configuration

### Docker MSSQL Container

```yaml
Image: mcr.microsoft.com/mssql/server:2022-latest
SA_PASSWORD: Admin@123456
Database: recruitment_platform
Port: 1433
```

### Connection String

```
mssql+pyodbc://sa:Admin@123456@localhost:1433/recruitment_platform?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

### Environment Variable

```bash
DB_URL=mssql+pyodbc://sa:Admin@123456@localhost:1433/recruitment_platform?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

---

## Local MSSQL Installation (Optional)

If you want to use a local MSSQL installation instead of Docker:

### Windows

**1. Install SQL Server Developer Edition** (free)
```
https://www.microsoft.com/en-us/sql-server/sql-server-downloads
```

**2. Install SQL Server Management Studio** (SSMS)
```
https://learn.microsoft.com/en-us/sql/ssms/download-sql-server-management-studio-ssms
```

**3. Create Database and User**
```sql
CREATE DATABASE recruitment_platform;

-- Create a new login
CREATE LOGIN app_user WITH PASSWORD = 'YourStrongPassword123!';

-- Create database user
USE recruitment_platform;
CREATE USER app_user FOR LOGIN app_user;

-- Grant permissions
ALTER ROLE db_owner ADD MEMBER app_user;
```

**4. Update .env**
```env
DB_URL=mssql+pyodbc://app_user:YourStrongPassword123!@localhost:1433/recruitment_platform?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes
```

**5. Install ODBC Driver 17**
```
https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server
```

### macOS

Using Homebrew and Docker for MSSQL (recommended):

```bash
# Install SQL Server CLI (optional)
brew tap microsoft/mssql-release https://github.com/Microsoft/homebrew-mssql-release
brew install mssql-tools

# Or use Docker (easier)
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Admin@123456' \
  -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest
```

### Linux

Using Docker (recommended):

```bash
docker run -e 'ACCEPT_EULA=Y' -e 'SA_PASSWORD=Admin@123456' \
  -p 1433:1433 -d mcr.microsoft.com/mssql/server:2022-latest

# Install ODBC driver
curl https://packages.microsoft.com/keys/microsoft.asc | sudo apt-key add -
curl https://packages.microsoft.com/config/ubuntu/20.04/prod.list | sudo tee /etc/apt/sources.list.d/mssql-release.list
sudo apt-get update
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
```

---

## Connecting to MSSQL

### Using SQL Server Management Studio (SSMS)

1. Open SSMS
2. **Server name**: localhost,1433 or localhost\SQLEXPRESS
3. **Authentication**: SQL Server Authentication
4. **Login**: sa
5. **Password**: Admin@123456
6. Click **Connect**

### Using Command Line

**sqlcmd** (Windows/Linux/macOS with mssql-tools):

```bash
sqlcmd -S localhost -U sa -P Admin@123456 -d recruitment_platform
```

**python** with pyodbc:

```python
import pyodbc

conn = pyodbc.connect(
    'Driver={ODBC Driver 17 for SQL Server};'
    'Server=localhost;'
    'Database=recruitment_platform;'
    'UID=sa;'
    'PWD=Admin@123456;'
    'TrustServerCertificate=yes'
)
cursor = conn.cursor()
cursor.execute("SELECT COUNT(*) FROM users")
print(cursor.fetchone())
```

---

## What Changed from PostgreSQL

| Feature | PostgreSQL | MSSQL |
|---------|-----------|-------|
| **Driver** | psycopg2 | pyodbc |
| **Vector Search** | pgvector extension | Mock provider (in-memory) |
| **Connection Pool** | psycopg2 pool | pyodbc pool |
| **Semantic Search** | Native pgvector | Simulated with fuzzy search |
| **JSON Support** | JSONB columns | JSON columns |
| **Enum Support** | ENUM type | VARCHAR with constraints |

---

## Troubleshooting

### Connection Error: "Connection refused"

**Check if MSSQL is running:**
```bash
# Docker
docker ps | grep mssql

# SSMS
# Try connecting locally first, check firewall settings
```

### "ODBC Driver 17 not found"

**Install ODBC driver:**
```bash
# Windows
# Download: https://learn.microsoft.com/en-us/sql/connect/odbc/download-odbc-driver-for-sql-server

# macOS
brew install unixodbc

# Linux
sudo ACCEPT_EULA=Y apt-get install msodbcsql17
```

### Alembic Migration Fails

**Verify connection:**
```bash
# Run test query
python -c "
import pyodbc
conn = pyodbc.connect('mssql+pyodbc://sa:Admin@123456@localhost:1433/recruitment_platform?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes')
print('Connection successful!')
"
```

### "Database 'recruitment_platform' does not exist"

**MSSQL Container auto-creates database on first connection, but if not:**

```bash
# Connect to master database first
docker-compose exec mssql /opt/mssql-tools18/bin/sqlcmd -S localhost -U sa -P Admin@123456 -d master

# Then create database
CREATE DATABASE recruitment_platform;
GO
```

---

## Database Schema

The same schema works on both PostgreSQL and MSSQL:

**Tables created by Alembic migrations:**
- `users` - Core accounts (CANDIDATE, RECRUITER, ADMIN)
- `candidates` - Candidate profiles
- `recruiters` - Recruiter profiles
- `companies` - Company directory
- `projects` - GitHub repositories (Month 2)
- `code_documents` - Source files
- `code_chunks` - Code segments with embeddings
- `ai_conversations` - Chat history
- `ai_messages` - Individual messages
- `ai_analyses` - Code analysis results
- `ai_tasks` - Agent task execution (Month 3)
- `ai_task_history` - Task execution audit trail

---

## Demo Accounts

After migrations run, demo data is seeded:

| Account | Email | Password | Role |
|---------|-------|----------|------|
| Admin | admin@example.com | Admin123! | ADMIN |
| Alice | alice@student.com | Student123! | CANDIDATE |
| Bob | bob@student.com | Student123! | CANDIDATE |
| Carol | carol@student.com | Student123! | CANDIDATE |
| David | david@student.com | Student123! | CANDIDATE |
| Emma | emma@student.com | Student123! | CANDIDATE |
| Sarah | sarah@recruiter.com | Recruiter123! | RECRUITER |
| James | james@recruiter.com | Recruiter123! | RECRUITER |
| Lisa | lisa@recruiter.com | Recruiter123! | RECRUITER |
| Michael | michael@recruiter.com | Recruiter123! | RECRUITER |
| Jennifer | jennifer@recruiter.com | Recruiter123! | RECRUITER |

---

## Switching Back to PostgreSQL

If you want to switch back to PostgreSQL:

1. **Update docker-compose.yml:**
   - Restore `postgres` service
   - Change backend `DB_URL` to `postgresql://...`

2. **Update backend/requirements.txt:**
   - Remove: `pyodbc`, `pyodbc-stubs`
   - Add: `psycopg2-binary==2.9.9`, `pgvector==0.2.4`

3. **Update backend/Dockerfile:**
   - Remove ODBC installation
   - Add `postgresql-client` back

4. **Update backend/alembic/env.py:**
   - Change fallback DB_URL to PostgreSQL connection string

5. **Restart:**
   ```bash
   docker-compose down -v
   docker-compose up --build
   ```

---

## Performance Notes

- **MSSQL**: ~1-2ms per query (cached), good for local development
- **Semantic Search**: Uses mock provider (simulated)
- **Vector Search**: Not available in MSSQL demo (use PostgreSQL with pgvector for real semantic search)
- **AI Features**: Using mock LLM and embedding providers (no API calls)

---

## Production Recommendations

For production deployment:

1. **Use PostgreSQL** with pgvector for real semantic search
2. **Use Azure SQL Database** if you want managed MSSQL in cloud
3. **Enable SSL/TLS** for all connections
4. **Use secrets manager** for database credentials
5. **Enable backups** and disaster recovery
6. **Monitor performance** and query execution plans

---

## Next Steps

- Read [README.md](README.md) for project overview
- Check [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md) for full documentation
- Login and explore demo accounts
- Try AI features with mock LLM provider

---

**Status**: ✅ MSSQL support added for demo purposes
**Database**: MSSQL Server 2022 (Docker)
**Backend Driver**: pyodbc with ODBC Driver 17
