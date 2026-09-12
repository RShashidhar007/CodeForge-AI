"""
Recruiter service matching Java RecruiterService.java.
"""
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ResourceNotFoundException
from app.repositories.recruiter_repository import RecruiterRepository
from app.schemas.recruiter import RecruiterProfileResponse, RecruiterProfileUpdateRequest


class RecruiterService:
    """
    Recruiter-specific operations.
    Matches Java RecruiterService.java.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.recruiter_repo = RecruiterRepository(db)
    
    def get_my_profile(self, authenticated_user_id: int) -> RecruiterProfileResponse:
        """
        Get recruiter's own profile.
        Matches Java: @Transactional(readOnly = true) public RecruiterProfileResponse getMyProfile(...)
        """
        recruiter = self._find_by_user_id(authenticated_user_id)
        
        return RecruiterProfileResponse(
            user_id=recruiter.user.id,
            name=recruiter.user.name,
            email=recruiter.user.email,
            phone=recruiter.phone,
            designation=recruiter.designation,
            company_id=recruiter.company_id,
            company_name=recruiter.company.name if recruiter.company else None
        )
    
    def update_my_profile(
        self,
        authenticated_user_id: int,
        request: RecruiterProfileUpdateRequest
    ) -> RecruiterProfileResponse:
        """
        Update recruiter's own profile.
        Matches Java: @Transactional public RecruiterProfileResponse updateMyProfile(...)
        """
        recruiter = self._find_by_user_id(authenticated_user_id)
        
        # Update fields
        recruiter.phone = request.phone.strip() if request.phone and request.phone.strip() else None
        recruiter.designation = request.designation.strip() if request.designation and request.designation.strip() else None
        
        self.recruiter_repo.save(recruiter)
        self.db.commit()
        
        return self.get_my_profile(authenticated_user_id)
    
    def _find_by_user_id(self, user_id: int):
        """Find recruiter by user ID or raise exception."""
        recruiter = self.recruiter_repo.find_by_user_id(user_id)
        if not recruiter:
            raise ResourceNotFoundException("Recruiter profile not found.")
        return recruiter
