"""
User entity matching Java User.java.
Core account record shared by all roles.
"""
import enum
from datetime import datetime
from sqlalchemy import Column, Integer, String, Boolean, DateTime, Enum as SQLEnum
from sqlalchemy.orm import relationship

from app.db.base import Base


class Role(str, enum.Enum):
    """User roles matching Java Role enum."""
    CANDIDATE = "CANDIDATE"
    RECRUITER = "RECRUITER"
    ADMIN = "ADMIN"


class User(Base):
    """
    Core account record shared by every role (candidate, recruiter, admin).
    
    Matches Java User.java entity with same table structure and relationships.
    """
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(150), nullable=False)
    email = Column(String(255), unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)  # BCrypt hash only
    role = Column(SQLEnum(Role), nullable=False)
    enabled = Column(Boolean, nullable=False, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships (one-to-one with Candidate or Recruiter)
    candidate = relationship("Candidate", back_populates="user", uselist=False, cascade="all, delete-orphan")
    recruiter = relationship("Recruiter", back_populates="user", uselist=False, cascade="all, delete-orphan")
    
    # Month 2: AI Features
    projects = relationship("Project", back_populates="user", cascade="all, delete-orphan")
    github_tokens = relationship("GitHubToken", back_populates="user", cascade="all, delete-orphan")
    ai_conversations = relationship("AIConversation", back_populates="user", cascade="all, delete-orphan")
    
    # Month 3: Multi-Agent AI
    ai_tasks = relationship("AITask", back_populates="user", cascade="all, delete-orphan")
