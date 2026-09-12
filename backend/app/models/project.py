"""
Project entity for organizing code repositories and AI analysis.
Each user can have multiple projects, each project connects to a GitHub repository.
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Index, Boolean
from sqlalchemy.orm import relationship

from app.db.base import Base


class Project(Base):
    """
    Represents a coding project connected to a GitHub repository.
    Used for organization and AI code intelligence features.
    """
    __tablename__ = "projects"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    github_url = Column(String(500), nullable=True)
    github_repo_name = Column(String(255), nullable=True)  # owner/repo format
    github_branch = Column(String(100), default="main")
    github_token_id = Column(Integer, ForeignKey('github_tokens.id', ondelete='SET NULL'), nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="projects")
    files = relationship("File", back_populates="project", cascade="all, delete-orphan")
    code_documents = relationship("CodeDocument", back_populates="project", cascade="all, delete-orphan")
    code_chunks = relationship("CodeChunk", back_populates="project", cascade="all, delete-orphan")
    ai_conversations = relationship("AIConversation", back_populates="project", cascade="all, delete-orphan")
    ai_analyses = relationship("AIAnalysis", back_populates="project", cascade="all, delete-orphan")
    index_metadata = relationship("RepositoryIndexMetadata", back_populates="project", uselist=False, cascade="all, delete-orphan")
    
    # Month 3: Multi-Agent AI
    ai_tasks_month3 = relationship("AITask", back_populates="project", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_projects_user_id', 'user_id'),
        Index('idx_projects_github_repo_name', 'github_repo_name'),
    )


class File(Base):
    """
    Represents a file in a project's repository.
    Tracks file metadata and synchronization status.
    """
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    path = Column(String(500), nullable=False)
    filename = Column(String(255), nullable=False)
    file_size = Column(Integer, nullable=True)
    content_hash = Column(String(64), nullable=True)  # SHA256
    language = Column(String(50), nullable=True)
    is_binary = Column(Boolean, default=False)
    last_synced_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="files")

    # Indexes
    __table_args__ = (
        Index('idx_files_project_id', 'project_id'),
        Index('idx_files_path', 'path'),
        Index('idx_files_content_hash', 'content_hash'),
    )


class GitHubToken(Base):
    """
    Stores GitHub OAuth tokens securely (encrypted in real implementation).
    For Month 2, we'll store plaintext in development.
    Production should encrypt these.
    """
    __tablename__ = "github_tokens"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    access_token = Column(Text, nullable=False)  # Should be encrypted in production
    refresh_token = Column(Text, nullable=True)
    token_type = Column(String(50), default="Bearer")
    scope = Column(String(500), nullable=True)
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="github_tokens")

    # Indexes
    __table_args__ = (
        Index('idx_github_tokens_user_id', 'user_id'),
    )
