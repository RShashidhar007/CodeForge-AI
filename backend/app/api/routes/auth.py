"""
Authentication routes matching Java AuthController.
The only three public (unauthenticated) endpoints in the whole API.
"""
from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.auth import (
    RegisterCandidateRequest,
    RegisterRecruiterRequest,
    LoginRequest,
    LoginResponse,
    UserResponse
)
from app.services.auth_service import AuthService

router = APIRouter()


@router.post("/register/candidate", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_candidate(
    request: RegisterCandidateRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new candidate user.
    Matches Java: POST /api/auth/register/candidate
    """
    service = AuthService(db)
    return service.register_candidate(request)


@router.post("/register/recruiter", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_recruiter(
    request: RegisterRecruiterRequest,
    db: Session = Depends(get_db)
):
    """
    Register a new recruiter user.
    Matches Java: POST /api/auth/register/recruiter
    """
    service = AuthService(db)
    return service.register_recruiter(request)


@router.post("/login", response_model=LoginResponse)
def login(
    request: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Authenticate user and receive JWT token.
    Matches Java: POST /api/auth/login
    """
    service = AuthService(db)
    return service.login(request)
