"""
Repository indexing service.
Handles repository synchronization, file filtering, chunking, and embedding generation.
"""
import os
import hashlib
from typing import List, Optional, Dict, Any, Set
from pathlib import Path
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from app.models.ai import (
    CodeDocument,
    CodeChunk,
    RepositoryIndexMetadata,
    IndexStatus,
)
from app.models.project import Project, File
from app.services.code_chunker import CodeChunker
from app.services.embedding_service import EmbeddingService
from app.db.vector_store import VectorStore
from app.core.config import settings

logger = logging.getLogger(__name__)


class RepositoryIndexer:
    """
    Main indexing service for repositories.
    Orchestrates file discovery, parsing, chunking, and embedding generation.
    """

    def __init__(
        self,
        session: Session,
        embedding_service: EmbeddingService,
        vector_store: VectorStore,
    ):
        """
        Initialize repository indexer.

        Args:
            session: Database session
            embedding_service: EmbeddingService instance
            vector_store: VectorStore instance
        """
        self.session = session
        self.embedding_service = embedding_service
        self.vector_store = vector_store
        self.chunker = CodeChunker()

    async def index_repository(
        self,
        project: Project,
        repository_path: str,
        update_progress_callback: Optional[callable] = None,
    ) -> Dict[str, Any]:
        """
        Index a local or cloned repository.

        Args:
            project: Project model instance
            repository_path: Path to repository
            update_progress_callback: Optional callback for progress updates

        Returns:
            Dict with indexing results and statistics
        """
        logger.info(f"Starting repository indexing for project {project.id}")

        # Initialize or get index metadata
        metadata = self.session.query(RepositoryIndexMetadata).filter_by(
            project_id=project.id
        ).first()

        if not metadata:
            metadata = RepositoryIndexMetadata(
                project_id=project.id,
                status=IndexStatus.INDEXING,
            )
            self.session.add(metadata)
            self.session.commit()
        else:
            metadata.status = IndexStatus.INDEXING
            metadata.last_error = None
            self.session.commit()

        try:
            # Discover files
            files_to_index = self._discover_files(repository_path)
            total_files = len(files_to_index)
            metadata.total_files = total_files
            self.session.commit()

            logger.info(f"Found {total_files} files to index")

            # Process each file
            indexed_files = 0
            total_chunks = 0
            errors = []

            for i, filepath in enumerate(files_to_index):
                try:
                    if update_progress_callback:
                        await update_progress_callback(
                            indexed=i,
                            total=total_files,
                            current_file=filepath,
                        )

                    chunks_added = await self._index_file(project, filepath)
                    if chunks_added > 0:
                        indexed_files += 1
                        total_chunks += chunks_added

                except Exception as e:
                    logger.error(f"Failed to index file {filepath}: {e}")
                    errors.append({"file": filepath, "error": str(e)})

            # Update metadata
            metadata.status = IndexStatus.INDEXED
            metadata.indexed_files = indexed_files
            metadata.total_chunks = total_chunks
            metadata.last_indexed_at = datetime.utcnow()
            metadata.embedding_model = settings.embedding_model

            if errors:
                metadata.last_error = f"Indexed {indexed_files}/{total_files} files with {len(errors)} errors"
                logger.warning(f"Indexing completed with {len(errors)} errors")

            self.session.commit()

            result = {
                "status": "success",
                "total_files": total_files,
                "indexed_files": indexed_files,
                "total_chunks": total_chunks,
                "errors": errors,
                "timestamp": datetime.utcnow().isoformat(),
            }

            logger.info(f"Repository indexing completed: {result}")
            return result

        except Exception as e:
            logger.error(f"Repository indexing failed: {e}")
            metadata.status = IndexStatus.FAILED
            metadata.last_error = str(e)
            self.session.commit()
            raise

    async def _index_file(self, project: Project, filepath: str) -> int:
        """
        Index a single file: parse, chunk, embed, and store.

        Args:
            project: Project instance
            filepath: Full file path

        Returns:
            Number of chunks created
        """
        # Read file
        try:
            with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
        except Exception as e:
            logger.error(f"Failed to read file {filepath}: {e}")
            return 0

        # Calculate content hash to detect changes
        content_hash = hashlib.sha256(content.encode()).hexdigest()

        # Check if file already indexed and unchanged
        existing_doc = self.session.query(CodeDocument).filter_by(
            project_id=project.id,
            path=filepath,
        ).first()

        if existing_doc and existing_doc.content_hash == content_hash:
            logger.debug(f"File unchanged, skipping: {filepath}")
            return 0

        # Delete existing document if it exists
        if existing_doc:
            self.vector_store.delete_embeddings_for_document(existing_doc.id)
            self.session.delete(existing_doc)
            self.session.commit()

        # Detect language
        language = self.chunker.detect_language(filepath)
        if language == "unknown":
            logger.debug(f"Unknown language, skipping: {filepath}")
            return 0

        # Chunk code
        code_chunks = self.chunker.chunk_code(
            content=content,
            language=language,
            filepath=filepath,
        )

        if not code_chunks:
            logger.debug(f"No chunks generated for file: {filepath}")
            return 0

        # Create document
        doc = CodeDocument(
            project_id=project.id,
            path=filepath,
            language=language,
            content_hash=content_hash,
            file_size=len(content),
            chunk_count=len(code_chunks),
            indexed_at=datetime.utcnow(),
        )
        self.session.add(doc)
        self.session.flush()  # Get the ID

        # Create and embed chunks
        chunks_to_embed = []
        for i, chunk in enumerate(code_chunks):
            db_chunk = CodeChunk(
                document_id=doc.id,
                project_id=project.id,
                chunk_index=i,
                content=chunk.content,
                start_line=chunk.start_line,
                end_line=chunk.end_line,
                symbol_name=chunk.symbol_name,
                language=language,
            )
            self.session.add(db_chunk)
            self.session.flush()

            chunks_to_embed.append({
                "chunk_id": db_chunk.id,
                "content": chunk.content,
            })

        self.session.commit()

        # Generate embeddings
        try:
            contents = [c["content"] for c in chunks_to_embed]
            embeddings = await self.embedding_service.embed_batch(contents)

            # Store embeddings
            for chunk_data, embedding in zip(chunks_to_embed, embeddings):
                self.vector_store.store_embedding(
                    chunk_id=chunk_data["chunk_id"],
                    embedding=embedding,
                )

            logger.info(f"Indexed {len(code_chunks)} chunks from {filepath}")
            return len(code_chunks)

        except Exception as e:
            logger.error(f"Failed to generate embeddings for {filepath}: {e}")
            # Still return success even if embedding fails
            return len(code_chunks)

    def _discover_files(self, repository_path: str) -> List[str]:
        """
        Discover source files in repository.
        Filters based on supported extensions and ignored paths.

        Args:
            repository_path: Root directory of repository

        Returns:
            List of file paths to index
        """
        files = []
        supported_exts = set(settings.supported_extensions_list)
        ignored_patterns = settings.ignored_paths_list

        def should_ignore(path: str) -> bool:
            """Check if path matches any ignore pattern."""
            path_parts = Path(path).parts
            for pattern in ignored_patterns:
                if pattern in path_parts or path.endswith(pattern):
                    return True
            return False

        try:
            for root, dirs, filenames in os.walk(repository_path):
                # Filter directories
                dirs[:] = [d for d in dirs if not should_ignore(d)]

                for filename in filenames:
                    filepath = os.path.join(root, filename)

                    # Check if should ignore
                    if should_ignore(filepath):
                        continue

                    # Check file size
                    try:
                        file_size_mb = os.path.getsize(filepath) / (1024 * 1024)
                        if file_size_mb > settings.max_file_size_mb:
                            continue
                    except OSError:
                        continue

                    # Check extension
                    _, ext = os.path.splitext(filename)
                    if ext in supported_exts:
                        files.append(filepath)

        except Exception as e:
            logger.error(f"Error discovering files: {e}")

        return files

    def get_indexing_status(self, project_id: int) -> Dict[str, Any]:
        """
        Get current indexing status for a project.

        Args:
            project_id: Project ID

        Returns:
            Status information
        """
        metadata = self.session.query(RepositoryIndexMetadata).filter_by(
            project_id=project_id
        ).first()

        if not metadata:
            return {
                "status": IndexStatus.NOT_INDEXED.value,
                "total_files": 0,
                "indexed_files": 0,
                "total_chunks": 0,
                "progress": 0.0,
            }

        progress = 0.0
        if metadata.total_files > 0:
            progress = (metadata.indexed_files / metadata.total_files) * 100

        return {
            "status": metadata.status.value,
            "total_files": metadata.total_files,
            "indexed_files": metadata.indexed_files,
            "total_chunks": metadata.total_chunks,
            "progress": progress,
            "last_indexed_at": metadata.last_indexed_at.isoformat() if metadata.last_indexed_at else None,
            "last_error": metadata.last_error,
            "embedding_model": metadata.embedding_model,
        }

    async def reindex_changed_files(
        self,
        project: Project,
        repository_path: str,
    ) -> Dict[str, Any]:
        """
        Reindex only files that have changed since last indexing.

        Args:
            project: Project instance
            repository_path: Path to repository

        Returns:
            Reindexing results
        """
        logger.info(f"Starting re-indexing for project {project.id}")

        # Get existing documents
        existing_docs = self.session.query(CodeDocument).filter_by(
            project_id=project.id
        ).all()
        existing_hashes = {doc.path: doc.content_hash for doc in existing_docs}

        # Discover current files
        current_files = self._discover_files(repository_path)

        # Find changed files
        changed_count = 0
        removed_count = 0

        for filepath in current_files:
            try:
                with open(filepath, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                content_hash = hashlib.sha256(content.encode()).hexdigest()

                if filepath not in existing_hashes or existing_hashes[filepath] != content_hash:
                    await self._index_file(project, filepath)
                    changed_count += 1
            except Exception as e:
                logger.error(f"Failed to check file {filepath}: {e}")

        # Remove documents for deleted files
        for filepath in existing_hashes:
            if filepath not in current_files:
                doc = self.session.query(CodeDocument).filter_by(
                    project_id=project.id,
                    path=filepath,
                ).first()
                if doc:
                    self.vector_store.delete_embeddings_for_document(doc.id)
                    self.session.delete(doc)
                    removed_count += 1

        self.session.commit()

        result = {
            "status": "success",
            "changed_files": changed_count,
            "removed_files": removed_count,
            "timestamp": datetime.utcnow().isoformat(),
        }

        logger.info(f"Re-indexing completed: {result}")
        return result
