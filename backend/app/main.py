"""
FastAPI application entry point.
Matches Java RecruitmentPlatformApplication.java and SecurityConfig.java.
"""
import logging
from contextlib import asynccontextmanager
from datetime import datetime

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import IntegrityError

from app.core.config import settings
from app.db.base import engine, Base
from app.db.session import SessionLocal
from app.utils.admin_initializer import bootstrap_admin
from app.api.routes import auth, candidates, recruiters, admin, ai
from app.exceptions.custom_exceptions import (
    ResourceNotFoundException,
    DuplicateResourceException,
    AccessDeniedCustomException,
    BadCredentialsException,
    DisabledException
)

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Startup and shutdown logic.
    Matches Java CommandLineRunner (AdminInitializer).
    """
    # Startup: create tables and bootstrap admin
    logger.info("Starting up...")
    Base.metadata.create_all(bind=engine)
    
    # Bootstrap admin account
    db = SessionLocal()
    try:
        bootstrap_admin(db)
    finally:
        db.close()
    
    logger.info("Startup complete")
    
    yield
    
    # Shutdown
    logger.info("Shutting down...")


# Create FastAPI application
app = FastAPI(
    title="Recruitment Platform API",
    description="Month 1 foundation: auth, roles, profiles for AI-Powered Coding Assessment & Interview Platform",
    version="0.1.0",
    lifespan=lifespan
)

# CORS Middleware (matching Java SecurityConfig CORS configuration)
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "PATCH", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
    max_age=3600
)

# Include routers (matching Java @RestController mappings)
app.include_router(auth.router, prefix="/api/auth", tags=["Authentication"])
app.include_router(candidates.router, prefix="/api/candidates", tags=["Candidates"])
app.include_router(recruiters.router, prefix="/api/recruiters", tags=["Recruiters"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])
app.include_router(ai.router, tags=["AI & RAG"])

# Month 3: AI Tasks
from app.api.routes import agent_tasks
app.include_router(agent_tasks.router, tags=["AI Tasks - Month 3"])


# --- Global Exception Handlers (matching Java @RestControllerAdvice) ---

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """
    Handle Pydantic validation errors.
    Matches Java MethodArgumentNotValidException handler.
    """
    details = []
    for error in exc.errors():
        field = ".".join(str(loc) for loc in error["loc"] if loc != "body")
        message = error["msg"]
        details.append(f"{field}: {message}")
    
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 400,
            "error": "Bad Request",
            "message": "Validation Error",
            "path": request.url.path,
            "details": details
        }
    )


@app.exception_handler(ResourceNotFoundException)
async def resource_not_found_handler(request: Request, exc: ResourceNotFoundException):
    """Matches Java ResourceNotFoundException handler."""
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 404,
            "error": "Not Found",
            "message": exc.message,
            "path": request.url.path
        }
    )


@app.exception_handler(DuplicateResourceException)
async def duplicate_resource_handler(request: Request, exc: DuplicateResourceException):
    """Matches Java DuplicateResourceException handler."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 409,
            "error": "Conflict",
            "message": exc.message,
            "path": request.url.path
        }
    )


@app.exception_handler(IntegrityError)
async def integrity_error_handler(request: Request, exc: IntegrityError):
    """Matches Java DataIntegrityViolationException handler."""
    return JSONResponse(
        status_code=status.HTTP_409_CONFLICT,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 409,
            "error": "Conflict",
            "message": "The request could not be completed because it conflicts with existing data.",
            "path": request.url.path
        }
    )


@app.exception_handler(AccessDeniedCustomException)
async def access_denied_custom_handler(request: Request, exc: AccessDeniedCustomException):
    """Matches Java AccessDeniedCustomException handler."""
    return JSONResponse(
        status_code=status.HTTP_403_FORBIDDEN,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 403,
            "error": "Forbidden",
            "message": exc.message,
            "path": request.url.path
        }
    )


@app.exception_handler(BadCredentialsException)
async def bad_credentials_handler(request: Request, exc: BadCredentialsException):
    """Matches Java BadCredentialsException handler."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 401,
            "error": "Unauthorized",
            "message": exc.message,
            "path": request.url.path
        }
    )


@app.exception_handler(DisabledException)
async def disabled_handler(request: Request, exc: DisabledException):
    """Matches Java DisabledException handler."""
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 401,
            "error": "Unauthorized",
            "message": exc.message,
            "path": request.url.path
        }
    )


@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    """
    Catch-all for unexpected errors.
    Matches Java generic Exception handler.
    """
    logger.error(f"Unexpected error: {exc}", exc_info=True)
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "status": 500,
            "error": "Internal Server Error",
            "message": "An unexpected error occurred. Please try again later.",
            "path": request.url.path
        }
    )


# Health check endpoint (matching Java actuator/health)
@app.get("/actuator/health")
def health_check():
    """Simple health check endpoint."""
    return {"status": "UP"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.port,
        reload=True  # Enable hot reload for development
    )
