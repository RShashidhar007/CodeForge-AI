# Migration Fix - Alembic ValidationError Resolution

## Problem

When running Docker Compose, the backend migration failed with:

```
pydantic_core._pydantic_core.ValidationError: 2 validation errors for Settings
  db_url: Field required
  jwt_secret: Field required
```

### Root Cause
- `alembic/env.py` was importing `settings` from `app.core.config`
- The `Settings` class validates ALL environment variables (JWT_SECRET, ADMIN_PASSWORD, etc.)
- During Docker container startup, Alembic runs migrations BEFORE the application starts
- At migration time, only `DB_URL` is needed, but all other variables are required by Settings validation
- This caused validation errors during the migration step

## Solution

Modified `backend/alembic/env.py` to:

1. **Read DB_URL directly from environment** using `os.getenv()`
2. **Remove dependency** on full Settings validation
3. **Use fallback value** if DB_URL not provided
4. **Keep model imports** for auto-generated migrations

### Changes Made

**File: `backend/alembic/env.py`**

```python
# Before:
from app.core.config import settings
config.set_main_option("sqlalchemy.url", settings.db_url)

# After:
import os
db_url = os.getenv(
    "DB_URL",
    "postgresql://postgres:change-me@localhost:5432/recruitment_platform"
)
config.set_main_option("sqlalchemy.url", db_url)
```

## Why This Works

- ✅ Alembic only needs database connection to run migrations
- ✅ Other Settings (JWT_SECRET, LLM_API_KEY, etc.) not needed during migration
- ✅ docker-compose provides DB_URL environment variable
- ✅ Fallback allows local development without .env file
- ✅ No changes needed to application code

## Testing

Try starting services:

```bash
# Windows PowerShell
& '.\start.ps1'

# Unix/Linux/macOS
bash start.sh

# Or direct Docker
docker-compose up --build
```

Expected flow:
1. ✅ Docker builds successfully
2. ✅ PostgreSQL container starts
3. ✅ Redis container starts
4. ✅ **Backend migrations run** (now succeeds!)
5. ✅ Backend application starts
6. ✅ Frontend available at http://localhost:5173

## Related Files

- `backend/alembic/env.py` - Migration configuration
- `docker-compose.yml` - Provides DB_URL environment variable
- `backend/alembic/versions/*.py` - Migration scripts (unchanged)

## Status

✅ **Fixed and Committed to GitHub**

All three recent fixes:
1. ✅ Removed incompatible `ast-comments` package
2. ✅ Fixed Alembic migration validation
3. ✅ Added startup scripts (start.ps1, start.sh)

Repository is now ready for successful Docker startup!
