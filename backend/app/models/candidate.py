"""
Candidate entity matching Java Candidate.java.
One-to-one relationship with User using @MapsId pattern.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Candidate(Base):
    """
    Candidate-specific profile data, one row per candidate User.
    
    The 1:1 link to User uses the User's own primary key as the foreign key
    (matching Java @MapsId pattern): candidates.id is both the PK and a FK to users.id.
    """
    __tablename__ = "candidates"
    
    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    phone = Column(String(20), nullable=True)
    location = Column(String(150), nullable=True)
    bio = Column(String(2000), nullable=True)
    github_url = Column(String(255), nullable=True)
    linkedin_url = Column(String(255), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="candidate")
    
    # Skills managed via CandidateSkill ORM model
    _skills = relationship(
        "CandidateSkill",
        cascade="all, delete-orphan",
        lazy="joined"
    )
    
    @property
    def skills(self) -> list[str]:
        """Get skills as a list of strings."""
        return [skill.skill for skill in self._skills]
    
    @skills.setter
    def skills(self, value: list[str]):
        """Set skills from a list of strings."""
        # This will be handled in the repository layer
        pass


# Helper model for skills management
class CandidateSkill(Base):
    """Helper model to manage candidate skills through ORM."""
    __tablename__ = "candidate_skills"
    
    candidate_id = Column(Integer, ForeignKey('candidates.id', ondelete='CASCADE'), primary_key=True)
    skill = Column(String(100), primary_key=True)
