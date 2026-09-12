"""
Candidate routes matching Java CandidateController.
All endpoints require CANDIDATE role authentication.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_candidate
from app.db.session import get_db
from app.models.user import User
from app.schemas.candidate import CandidateProfileResponse, CandidateProfileUpdateRequest
from app.services.candidate_service import CandidateService

router = APIRouter()


@router.get("/me", response_model=CandidateProfileResponse)
def get_my_profile(
    current_user: User = Depends(get_current_candidate),
    db: Session = Depends(get_db)
):
    """
    Get authenticated candidate's own profile.
    Matches Java: GET /api/candidates/me
    """
    service = CandidateService(db)
    return service.get_my_profile(current_user.id)


@router.put("/me", response_model=CandidateProfileResponse)
def update_my_profile(
    request: CandidateProfileUpdateRequest,
    current_user: User = Depends(get_current_candidate),
    db: Session = Depends(get_db)
):
    """
    Update authenticated candidate's own profile.
    Matches Java: PUT /api/candidates/me
    """
    service = CandidateService(db)
    return service.update_my_profile(current_user.id, request)
