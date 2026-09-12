"""
AI-powered code intelligence API routes.
Implements Month 2 features: chat, code explanation, bug detection, etc.
"""
from typing import Optional, Dict, Any
from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
import logging

from app.db.session import get_db
from app.core.dependencies import get_current_user
from app.models.user import User
from app.models.project import Project
from app.models.ai import AIConversation
from app.services.rag_service import RAGService
from app.services.repository_indexer import RepositoryIndexer
from app.services.embedding_service import EmbeddingService, create_embedding_provider
from app.services.llm_provider import create_llm_provider
from app.db.vector_store import VectorStore
from app.core.config import settings

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/v1/projects", tags=["ai"])


# Request/Response Models
class ChatRequest(BaseModel):
    """Request for repository chat."""
    question: str = Field(..., min_length=1, max_length=2000)
    conversation_id: Optional[int] = None
    top_k: int = Field(10, ge=1, le=50)


class ChatResponse(BaseModel):
    """Response for repository chat."""
    conversation_id: int
    answer: str
    sources: list[Dict[str, Any]]
    chunks_retrieved: int


class CodeExplanationRequest(BaseModel):
    """Request for code explanation."""
    code: str = Field(..., min_length=1, max_length=5000)
    filepath: str = Field(..., min_length=1)
    start_line: int = Field(..., ge=1)
    end_line: int = Field(..., ge=1)
    language: str = Field(..., min_length=1)


class CodeExplanationResponse(BaseModel):
    """Response for code explanation."""
    explanation: str
    sources: list[Dict[str, Any]]


class BugDetectionRequest(BaseModel):
    """Request for bug detection."""
    code: str = Field(..., min_length=1, max_length=5000)
    filepath: str = Field(..., min_length=1)
    start_line: int = Field(..., ge=1)
    end_line: int = Field(..., ge=1)
    language: str = Field(..., min_length=1)


class BugDetectionResponse(BaseModel):
    """Response for bug detection."""
    analysis: str
    sources: list[Dict[str, Any]]


class CodeImprovementRequest(BaseModel):
    """Request for code improvement."""
    code: str = Field(..., min_length=1, max_length=5000)
    filepath: str = Field(..., min_length=1)
    start_line: int = Field(..., ge=1)
    end_line: int = Field(..., ge=1)
    language: str = Field(..., min_length=1)


class CodeImprovementResponse(BaseModel):
    """Response for code improvement."""
    suggestions: str
    sources: list[Dict[str, Any]]


class TestGenerationRequest(BaseModel):
    """Request for test generation."""
    code: str = Field(..., min_length=1, max_length=5000)
    filepath: str = Field(..., min_length=1)
    start_line: int = Field(..., ge=1)
    end_line: int = Field(..., ge=1)
    language: str = Field(..., min_length=1)
    test_framework: Optional[str] = None


class TestGenerationResponse(BaseModel):
    """Response for test generation."""
    tests: str
    test_framework: str
    sources: list[Dict[str, Any]]


class IndexStatusResponse(BaseModel):
    """Repository indexing status."""
    status: str
    total_files: int
    indexed_files: int
    total_chunks: int
    progress: float
    last_indexed_at: Optional[str] = None
    last_error: Optional[str] = None


class ConversationMessage(BaseModel):
    """Single message in conversation."""
    role: str
    content: str
    created_at: str
    sources: Optional[str] = None


# Dependency: Get RAG Service
def get_rag_service(db: Session = Depends(get_db)) -> RAGService:
    """Get RAG service instance."""
    # Create providers
    embedding_provider = create_embedding_provider(
        provider_name=settings.embedding_provider,
        api_key=settings.embedding_api_key,
        model=settings.embedding_model,
        embedding_dimension=settings.embedding_dimension,
        use_mock=settings.llm_api_key.startswith("sk-test"),
    )

    embedding_service = EmbeddingService(embedding_provider)

    llm_provider = create_llm_provider(
        provider_name=settings.llm_provider,
        api_key=settings.llm_api_key,
        model=settings.llm_model,
        temperature=settings.llm_temperature,
        max_tokens=settings.llm_max_tokens,
        use_mock=settings.llm_api_key.startswith("sk-test"),
    )

    vector_store = VectorStore(db)

    return RAGService(
        session=db,
        vector_store=vector_store,
        embedding_service=embedding_service,
        llm_provider=llm_provider,
    )


def get_repository_indexer(db: Session = Depends(get_db)) -> RepositoryIndexer:
    """Get repository indexer instance."""
    embedding_provider = create_embedding_provider(
        provider_name=settings.embedding_provider,
        api_key=settings.embedding_api_key,
        model=settings.embedding_model,
        embedding_dimension=settings.embedding_dimension,
        use_mock=settings.llm_api_key.startswith("sk-test"),
    )

    embedding_service = EmbeddingService(embedding_provider)
    vector_store = VectorStore(db)

    return RepositoryIndexer(
        session=db,
        embedding_service=embedding_service,
        vector_store=vector_store,
    )


# Routes

@router.post("/{project_id}/ai/chat", response_model=ChatResponse)
async def chat(
    project_id: int,
    request: ChatRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Chat with AI about the repository.
    Uses semantic search and RAG to answer questions grounded in code.
    """
    # Verify project ownership
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    try:
        result = await rag_service.chat(
            project_id=project_id,
            user_id=current_user.id,
            question=request.question,
            conversation_id=request.conversation_id,
            top_k=request.top_k,
        )

        return ChatResponse(
            conversation_id=result["conversation_id"],
            answer=result["answer"],
            sources=result["sources"],
            chunks_retrieved=result["chunks_retrieved"],
        )
    except Exception as e:
        logger.error(f"Chat failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process chat request",
        )


@router.post("/{project_id}/ai/explain", response_model=CodeExplanationResponse)
async def explain_code(
    project_id: int,
    request: CodeExplanationRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Explain selected code with context from repository.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    try:
        result = await rag_service.explain_code(
            project_id=project_id,
            user_id=current_user.id,
            selected_code=request.code,
            filepath=request.filepath,
            start_line=request.start_line,
            end_line=request.end_line,
            language=request.language,
        )

        return CodeExplanationResponse(
            explanation=result["explanation"],
            sources=result["sources"],
        )
    except Exception as e:
        logger.error(f"Code explanation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate explanation",
        )


@router.post("/{project_id}/ai/bugs", response_model=BugDetectionResponse)
async def detect_bugs(
    project_id: int,
    request: BugDetectionRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Analyze code for potential bugs.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    try:
        result = await rag_service.detect_bugs(
            project_id=project_id,
            user_id=current_user.id,
            selected_code=request.code,
            filepath=request.filepath,
            start_line=request.start_line,
            end_line=request.end_line,
            language=request.language,
        )

        return BugDetectionResponse(
            analysis=result["analysis"],
            sources=result["sources"],
        )
    except Exception as e:
        logger.error(f"Bug detection failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to detect bugs",
        )


@router.post("/{project_id}/ai/improve", response_model=CodeImprovementResponse)
async def improve_code(
    project_id: int,
    request: CodeImprovementRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Suggest improvements to code.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    try:
        result = await rag_service.improve_code(
            project_id=project_id,
            user_id=current_user.id,
            selected_code=request.code,
            filepath=request.filepath,
            start_line=request.start_line,
            end_line=request.end_line,
            language=request.language,
        )

        return CodeImprovementResponse(
            suggestions=result["suggestions"],
            sources=result["sources"],
        )
    except Exception as e:
        logger.error(f"Code improvement failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate improvements",
        )


@router.post("/{project_id}/ai/tests", response_model=TestGenerationResponse)
async def generate_tests(
    project_id: int,
    request: TestGenerationRequest,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Generate unit tests for selected code.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    try:
        result = await rag_service.generate_tests(
            project_id=project_id,
            user_id=current_user.id,
            selected_code=request.code,
            filepath=request.filepath,
            start_line=request.start_line,
            end_line=request.end_line,
            language=request.language,
            test_framework=request.test_framework,
        )

        return TestGenerationResponse(
            tests=result["tests"],
            test_framework=result["test_framework"],
            sources=result["sources"],
        )
    except Exception as e:
        logger.error(f"Test generation failed: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to generate tests",
        )


@router.get("/{project_id}/ai/status", response_model=IndexStatusResponse)
async def get_indexing_status(
    project_id: int,
    current_user: User = Depends(get_current_user),
    indexer: RepositoryIndexer = Depends(get_repository_indexer),
    db: Session = Depends(get_db),
):
    """
    Get repository indexing status.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    status_info = indexer.get_indexing_status(project_id)
    return IndexStatusResponse(**status_info)


@router.get("/{project_id}/ai/conversations/{conversation_id}/history")
async def get_conversation_history(
    project_id: int,
    conversation_id: int,
    current_user: User = Depends(get_current_user),
    rag_service: RAGService = Depends(get_rag_service),
    db: Session = Depends(get_db),
):
    """
    Get conversation history.
    """
    project = db.query(Project).filter_by(
        id=project_id,
        user_id=current_user.id,
    ).first()

    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    # Verify conversation belongs to project
    conversation = db.query(AIConversation).filter_by(
        id=conversation_id,
        project_id=project_id,
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found",
        )

    history = rag_service.get_conversation_history(conversation_id, project_id)
    return {"messages": history, "conversation_id": conversation_id}
