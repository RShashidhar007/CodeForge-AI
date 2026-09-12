"""
Candidate service matching Java CandidateService.java.
"""
from sqlalchemy.orm import Session

from app.exceptions.custom_exceptions import ResourceNotFoundException
from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate import CandidateProfileResponse, CandidateProfileUpdateRequest


class CandidateService:
    """
    Every method here takes the authenticated user's id so a candidate can
    only ever read or modify their own profile.
    Matches Java CandidateService.java.
    """
    
    def __init__(self, db: Session):
        self.db = db
        self.candidate_repo = CandidateRepository(db)
    
    def get_my_profile(self, authenticated_user_id: int) -> CandidateProfileResponse:
        """
        Get candidate's own profile.
        Matches Java: @Transactional(readOnly = true) public CandidateProfileResponse getMyProfile(...)
        """
        candidate = self._find_by_user_id(authenticated_user_id)
        skills = self.candidate_repo.get_skills(candidate.id)
        
        return CandidateProfileResponse(
            user_id=candidate.user.id,
            name=candidate.user.name,
            email=candidate.user.email,
            phone=candidate.phone,
            location=candidate.location,
            bio=candidate.bio,
            skills=skills,
            github_url=candidate.github_url,
            linkedin_url=candidate.linkedin_url
        )
    
    def update_my_profile(
        self,
        authenticated_user_id: int,
        request: CandidateProfileUpdateRequest
    ) -> CandidateProfileResponse:
        """
        Update candidate's own profile.
        Matches Java: @Transactional public CandidateProfileResponse updateMyProfile(...)
        """
        candidate = self._find_by_user_id(authenticated_user_id)
        
        # Update fields
        candidate.phone = self._blank_to_none(request.phone)
        candidate.location = self._blank_to_none(request.location)
        candidate.bio = self._blank_to_none(request.bio)
        candidate.github_url = self._blank_to_none(request.github_url)
        candidate.linkedin_url = self._blank_to_none(request.linkedin_url)
        
        # Update skills
        if request.skills is not None:
            self.candidate_repo.update_skills(candidate.id, request.skills)
        
        self.candidate_repo.save(candidate)
        self.db.commit()
        
        # Return updated profile
        return self.get_my_profile(authenticated_user_id)
    
    def _find_by_user_id(self, user_id: int):
        """Find candidate by user ID or raise exception."""
        candidate = self.candidate_repo.find_by_user_id(user_id)
        if not candidate:
            raise ResourceNotFoundException("Candidate profile not found.")
        return candidate
    
    def _blank_to_none(self, value: str | None) -> str | None:
        """Convert blank strings to None (matching Java behavior)."""
        if value is None or not value.strip():
            return None
        return value.strip()
