"""
Recruiter repository matching Java RecruiterRepository interface.
"""
from typing import Optional
from sqlalchemy.orm import Session, joinedload

from app.models.recruiter import Recruiter


class RecruiterRepository:
    """Data access layer for Recruiter entity matching Java RecruiterRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_user_id(self, user_id: int) -> Optional[Recruiter]:
        """Matches Java: Optional<Recruiter> findByUser_Id(Long userId)"""
        return (
            self.db.query(Recruiter)
            .options(joinedload(Recruiter.user), joinedload(Recruiter.company))
            .filter(Recruiter.id == user_id)
            .first()
        )
    
    def find_by_user_email(self, email: str) -> Optional[Recruiter]:
        """Matches Java: Optional<Recruiter> findByUser_Email(String email)"""
        return (
            self.db.query(Recruiter)
            .join(Recruiter.user)
            .options(joinedload(Recruiter.company))
            .filter(Recruiter.user.has(email=email))
            .first()
        )
    
    def save(self, recruiter: Recruiter) -> Recruiter:
        """Save or update a recruiter."""
        self.db.add(recruiter)
        self.db.flush()
        self.db.refresh(recruiter)
        return recruiter
