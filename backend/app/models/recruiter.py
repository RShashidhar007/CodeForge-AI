"""
Recruiter entity matching Java Recruiter.java.
One-to-one relationship with User using @MapsId pattern.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class Recruiter(Base):
    """
    Recruiter-specific profile data, one row per recruiter User.
    Same @MapsId 1:1 pattern as Candidate. Company is optional.
    """
    __tablename__ = "recruiters"
    
    id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True)
    phone = Column(String(20), nullable=True)
    designation = Column(String(150), nullable=True)
    company_id = Column(Integer, ForeignKey('companies.id', ondelete='SET NULL'), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="recruiter")
    company = relationship("Company", back_populates="recruiters", lazy="joined")
