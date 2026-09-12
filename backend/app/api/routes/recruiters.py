"""
Recruiter routes matching Java RecruiterController.
All endpoints require RECRUITER role authentication.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_recruiter
from app.db.session import get_db
from app.models.user import User
from app.schemas.recruiter import RecruiterProfileResponse, RecruiterProfileUpdateRequest
from app.services.recruiter_service import RecruiterService

router = APIRouter()


@router.get("/me", response_model=RecruiterProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """
    Get authenticated recruiter's own profile.
    Matches Java: GET /api/recruiters/me
    """
    service = RecruiterService(db)
    return service.get_my_profile(current_user.id)


@router.put("/me", response_model=RecruiterProfileResponse)
def update_my_profile(
    request: RecruiterProfileUpdateRequest,
    current_user: User = Depends(get_current_recruiter),
    db: Session = Depends(get_db)
):
    """
    Update authenticated recruiter's own profile.
    Matches Java: PUT /api/recruiters/me
    """
    service = RecruiterService(db)
    return service.update_my_profile(current_user.id, request)
