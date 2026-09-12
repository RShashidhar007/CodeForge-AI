"""
AI-related entities for repository indexing, embeddings, and conversations.
Supports Month 2: AI Code Intelligence and RAG.
"""
from datetime import datetime
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    DateTime,
    ForeignKey,
    Index,
    Boolean,
    LargeBinary,
    Enum as SQLEnum,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, VECTOR
import enum
import uuid

from app.db.base import Base


class IndexStatus(str, enum.Enum):
    """Repository indexing status."""
    NOT_INDEXED = "NOT_INDEXED"
    INDEXING = "INDEXING"
    INDEXED = "INDEXED"
    UPDATE_AVAILABLE = "UPDATE_AVAILABLE"
    FAILED = "FAILED"


class CodeDocument(Base):
    """
    Represents a source file in the indexed repository.
    One document per file.
    """
    __tablename__ = "code_documents"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    file_id = Column(Integer, ForeignKey('files.id', ondelete='CASCADE'), nullable=True)
    path = Column(String(500), nullable=False)
    language = Column(String(50), nullable=False)  # python, javascript, typescript, java, etc.
    content_hash = Column(String(64), nullable=False)  # SHA256 of file content
    file_size = Column(Integer, nullable=True)
    chunk_count = Column(Integer, default=0)
    indexed_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="code_documents")
    chunks = relationship("CodeChunk", back_populates="document", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_code_documents_project_id', 'project_id'),
        Index('idx_code_documents_path', 'path'),
        Index('idx_code_documents_content_hash', 'content_hash'),
    )


class CodeChunk(Base):
    """
    Represents a chunk of code from a document.
    Supports semantic retrieval and RAG.
    """
    __tablename__ = "code_chunks"

    id = Column(Integer, primary_key=True)
    document_id = Column(Integer, ForeignKey('code_documents.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    chunk_index = Column(Integer, nullable=False)  # Position in document
    content = Column(Text, nullable=False)  # The actual code
    start_line = Column(Integer, nullable=False)
    end_line = Column(Integer, nullable=False)
    symbol_name = Column(String(255), nullable=True)  # Function/class name if available
    language = Column(String(50), nullable=False)
    # Vector embedding - will be populated after pgvector setup
    embedding = Column(VECTOR(1536), nullable=True)  # 1536 dims for OpenAI Ada
    embedding_model = Column(String(100), nullable=True)  # Track which model generated this
    token_count = Column(Integer, nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    document = relationship("CodeDocument", back_populates="chunks")
    project = relationship("Project", back_populates="code_chunks")

    # Indexes
    __table_args__ = (
        Index('idx_code_chunks_document_id', 'document_id'),
        Index('idx_code_chunks_project_id', 'project_id'),
        Index('idx_code_chunks_symbol_name', 'symbol_name'),
    )


class AIConversation(Base):
    """
    Represents an AI conversation session about a repository.
    Supports multi-turn interactions with source context.
    """
    __tablename__ = "ai_conversations"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    title = Column(String(255), nullable=True)
    context_type = Column(String(50), default="repository")  # repository, file, selection
    context_data = Column(Text, nullable=True)  # JSON metadata about context
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    user = relationship("User", back_populates="ai_conversations")
    project = relationship("Project", back_populates="ai_conversations")
    messages = relationship("AIMessage", back_populates="conversation", cascade="all, delete-orphan")

    # Indexes
    __table_args__ = (
        Index('idx_ai_conversations_user_id', 'user_id'),
        Index('idx_ai_conversations_project_id', 'project_id'),
    )


class AIMessage(Base):
    """
    Represents a message in an AI conversation.
    Stores role (user/assistant) and content.
    """
    __tablename__ = "ai_messages"

    id = Column(Integer, primary_key=True)
    conversation_id = Column(Integer, ForeignKey('ai_conversations.id', ondelete='CASCADE'), nullable=False)
    role = Column(String(20), nullable=False)  # "user" or "assistant"
    content = Column(Text, nullable=False)
    # Metadata about retrieved context for this message
    sources = Column(Text, nullable=True)  # JSON array of source citations
    token_count = Column(Integer, nullable=True)
    model_used = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)

    # Relationships
    conversation = relationship("AIConversation", back_populates="messages")

    # Indexes
    __table_args__ = (
        Index('idx_ai_messages_conversation_id', 'conversation_id'),
    )


class AIAnalysis(Base):
    """
    Stores results of AI analysis operations.
    Supports caching and historical analysis tracking.
    """
    __tablename__ = "ai_analyses"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False)
    document_id = Column(Integer, ForeignKey('code_documents.id', ondelete='CASCADE'), nullable=True)
    analysis_type = Column(String(50), nullable=False)  # "bug_detection", "improvement", "explanation", etc.
    target_code = Column(Text, nullable=True)  # The code that was analyzed
    result = Column(Text, nullable=False)  # JSON result
    severity = Column(String(20), nullable=True)  # "LOW", "MEDIUM", "HIGH", "CRITICAL"
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="ai_analyses")

    # Indexes
    __table_args__ = (
        Index('idx_ai_analyses_project_id', 'project_id'),
        Index('idx_ai_analyses_document_id', 'document_id'),
        Index('idx_ai_analyses_analysis_type', 'analysis_type'),
    )


class RepositoryIndexMetadata(Base):
    """
    Tracks repository indexing status and metadata.
    """
    __tablename__ = "repository_index_metadata"

    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey('projects.id', ondelete='CASCADE'), nullable=False, unique=True)
    status = Column(SQLEnum(IndexStatus), default=IndexStatus.NOT_INDEXED, nullable=False)
    total_files = Column(Integer, default=0)
    indexed_files = Column(Integer, default=0)
    total_chunks = Column(Integer, default=0)
    last_indexed_at = Column(DateTime, nullable=True)
    last_error = Column(Text, nullable=True)
    embedding_model = Column(String(100), nullable=True)
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    project = relationship("Project", back_populates="index_metadata")

    # Indexes
    __table_args__ = (
        Index('idx_repository_index_metadata_project_id', 'project_id'),
        Index('idx_repository_index_metadata_status', 'status'),
    )
