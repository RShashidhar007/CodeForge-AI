"""
Company entity matching Java Company.java.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from app.db.base import Base


class Company(Base):
    """
    Minimal company record. A recruiter belongs to (at most) one company.
    Matches Java Company.java entity structure.
    """
    __tablename__ = "companies"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(200), unique=True, nullable=False, index=True)
    description = Column(String(2000), nullable=True)
    website = Column(String(255), nullable=True)
    location = Column(String(150), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    recruiters = relationship("Recruiter", back_populates="company")
