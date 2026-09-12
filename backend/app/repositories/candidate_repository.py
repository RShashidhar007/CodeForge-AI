"""
Candidate repository matching Java CandidateRepository interface.
"""
from typing import Optional
from sqlalchemy.orm import Session, joinedload

from app.models.candidate import Candidate, CandidateSkill


class CandidateRepository:
    """Data access layer for Candidate entity matching Java CandidateRepository."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def find_by_user_id(self, user_id: int) -> Optional[Candidate]:
        """Matches Java: Optional<Candidate> findByUser_Id(Long userId)"""
        return (
            self.db.query(Candidate)
            .options(joinedload(Candidate.user))
            .filter(Candidate.id == user_id)
            .first()
        )
    
    def find_by_user_email(self, email: str) -> Optional[Candidate]:
        """Matches Java: Optional<Candidate> findByUser_Email(String email)"""
        return (
            self.db.query(Candidate)
            .join(Candidate.user)
            .filter(Candidate.user.has(email=email))
            .first()
        )
    
    def save(self, candidate: Candidate) -> Candidate:
        """Save or update a candidate."""
        self.db.add(candidate)
        self.db.flush()
        self.db.refresh(candidate)
        return candidate
    
    def update_skills(self, candidate_id: int, skills: list[str]):
        """
        Update candidate skills.
        Replaces existing skills with new list (matching Java @ElementCollection behavior).
        """
        # Delete existing skills
        self.db.query(CandidateSkill).filter(
            CandidateSkill.candidate_id == candidate_id
        ).delete()
        
        # Add new skills
        for skill in skills:
            if skill and skill.strip():
                skill_entry = CandidateSkill(candidate_id=candidate_id, skill=skill.strip())
                self.db.add(skill_entry)
        
        self.db.flush()
    
    def get_skills(self, candidate_id: int) -> list[str]:
        """Get all skills for a candidate."""
        skills = (
            self.db.query(CandidateSkill.skill)
            .filter(CandidateSkill.candidate_id == candidate_id)
            .all()
        )
        return [s[0] for s in skills]
