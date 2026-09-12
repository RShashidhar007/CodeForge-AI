"""
Vector store abstraction for semantic search and embeddings.
Implements pgvector support for PostgreSQL.
"""
from typing import Optional, List, Dict, Any
from sqlalchemy import text, select, func
from sqlalchemy.orm import Session
from sqlalchemy.dialects.postgresql import array
import logging

from app.models.ai import CodeChunk
from app.core.config import settings

logger = logging.getLogger(__name__)


class VectorStore:
    """
    Vector store for semantic search using pgvector.
    Handles embedding storage and similarity search.
    """

    def __init__(self, session: Session):
        """Initialize vector store with database session."""
        self.session = session

    async def enable_pgvector(self) -> bool:
        """
        Enable pgvector extension in PostgreSQL.
        Must be called once at application startup.
        """
        try:
            self.session.execute(text("CREATE EXTENSION IF NOT EXISTS vector"))
            self.session.commit()
            logger.info("pgvector extension enabled")
            return True
        except Exception as e:
            logger.error(f"Failed to enable pgvector: {e}")
            return False

    def store_embedding(
        self,
        chunk_id: int,
        embedding: List[float],
        model: str = None,
    ) -> bool:
        """
        Store an embedding for a code chunk.

        Args:
            chunk_id: ID of the CodeChunk
            embedding: Vector embedding (list of floats)
            model: Model used to generate embedding

        Returns:
            True if successful, False otherwise
        """
        try:
            stmt = (
                text(
                    """
                UPDATE code_chunks
                SET embedding = :embedding::vector,
                    embedding_model = :model
                WHERE id = :chunk_id
                """
                )
                .bindparams(
                    embedding=str(embedding),  # Convert to string for pgvector
                    model=model or settings.embedding_model,
                    chunk_id=chunk_id,
                )
            )
            self.session.execute(stmt)
            self.session.commit()
            return True
        except Exception as e:
            logger.error(f"Failed to store embedding for chunk {chunk_id}: {e}")
            self.session.rollback()
            return False

    def store_embeddings_batch(
        self,
        embeddings_data: List[Dict[str, Any]],
    ) -> int:
        """
        Store multiple embeddings in batch.

        Args:
            embeddings_data: List of dicts with keys:
                - chunk_id: int
                - embedding: List[float]
                - model: str (optional)

        Returns:
            Number of embeddings stored successfully
        """
        stored_count = 0
        for data in embeddings_data:
            if self.store_embedding(
                chunk_id=data["chunk_id"],
                embedding=data["embedding"],
                model=data.get("model"),
            ):
                stored_count += 1
        return stored_count

    def semantic_search(
        self,
        query_embedding: List[float],
        project_id: int,
        top_k: int = 10,
        similarity_threshold: float = 0.3,
    ) -> List[CodeChunk]:
        """
        Search for similar code chunks using vector similarity.

        Args:
            query_embedding: Query vector embedding
            project_id: Project ID for filtering
            top_k: Number of results to return
            similarity_threshold: Minimum similarity score (0-1)

        Returns:
            List of similar CodeChunk objects
        """
        try:
            embedding_str = str(query_embedding)

            # Use cosine similarity for semantic search
            # pgvector operator <-> computes cosine distance (lower = more similar)
            # We convert to similarity score: 1 - distance
            stmt = text(
                """
                SELECT id, document_id, project_id, chunk_index, content,
                       start_line, end_line, symbol_name, language,
                       embedding_model, token_count, created_at, updated_at,
                       (1 - (embedding <-> :embedding::vector)) as similarity
                FROM code_chunks
                WHERE project_id = :project_id
                  AND embedding IS NOT NULL
                  AND (1 - (embedding <-> :embedding::vector)) > :threshold
                ORDER BY embedding <-> :embedding::vector
                LIMIT :top_k
                """
            ).bindparams(
                embedding=embedding_str,
                project_id=project_id,
                threshold=similarity_threshold,
                top_k=top_k,
            )

            results = self.session.execute(stmt).fetchall()

            # Convert results to CodeChunk objects
            chunks = []
            for row in results:
                chunk = CodeChunk(
                    id=row.id,
                    document_id=row.document_id,
                    project_id=row.project_id,
                    chunk_index=row.chunk_index,
                    content=row.content,
                    start_line=row.start_line,
                    end_line=row.end_line,
                    symbol_name=row.symbol_name,
                    language=row.language,
                    embedding_model=row.embedding_model,
                    token_count=row.token_count,
                    created_at=row.created_at,
                    updated_at=row.updated_at,
                )
                chunks.append(chunk)

            return chunks
        except Exception as e:
            logger.error(f"Semantic search failed: {e}")
            return []

    def search_by_symbol(
        self,
        symbol_name: str,
        project_id: int,
        language: Optional[str] = None,
    ) -> List[CodeChunk]:
        """
        Search for code chunks by symbol name (function, class, etc).

        Args:
            symbol_name: Symbol name to search for
            project_id: Project ID for filtering
            language: Optional language filter

        Returns:
            List of matching CodeChunk objects
        """
        try:
            query = select(CodeChunk).where(
                (CodeChunk.project_id == project_id)
                & (CodeChunk.symbol_name.ilike(f"%{symbol_name}%"))
            )

            if language:
                query = query.where(CodeChunk.language == language)

            return self.session.execute(query).scalars().all()
        except Exception as e:
            logger.error(f"Symbol search failed: {e}")
            return []

    def delete_embeddings_for_document(self, document_id: int) -> int:
        """
        Delete all embeddings for a document (used during re-indexing).

        Args:
            document_id: CodeDocument ID

        Returns:
            Number of embeddings deleted
        """
        try:
            stmt = select(CodeChunk).where(CodeChunk.document_id == document_id)
            chunks = self.session.execute(stmt).scalars().all()

            for chunk in chunks:
                self.session.delete(chunk)

            self.session.commit()
            return len(chunks)
        except Exception as e:
            logger.error(f"Failed to delete embeddings for document {document_id}: {e}")
            self.session.rollback()
            return 0

    def get_embedding_stats(self, project_id: int) -> Dict[str, Any]:
        """
        Get statistics about embeddings for a project.

        Args:
            project_id: Project ID

        Returns:
            Dict with stats (total_chunks, indexed_chunks, avg_token_count, etc)
        """
        try:
            total = self.session.query(func.count(CodeChunk.id)).filter(
                CodeChunk.project_id == project_id
            ).scalar()

            indexed = self.session.query(func.count(CodeChunk.id)).filter(
                CodeChunk.project_id == project_id,
                CodeChunk.embedding != None,
            ).scalar()

            avg_tokens = self.session.query(func.avg(CodeChunk.token_count)).filter(
                CodeChunk.project_id == project_id
            ).scalar()

            return {
                "total_chunks": total or 0,
                "indexed_chunks": indexed or 0,
                "avg_token_count": float(avg_tokens) if avg_tokens else 0,
                "indexing_progress": (indexed or 0) / (total or 1) * 100,
            }
        except Exception as e:
            logger.error(f"Failed to get embedding stats: {e}")
            return {}
