"""
RAG (Retrieval-Augmented Generation) service.
Orchestrates semantic retrieval and LLM-based response generation.
"""
from typing import List, Dict, Any, Optional
from datetime import datetime
import logging
from sqlalchemy.orm import Session

from app.models.ai import CodeChunk, AIConversation, AIMessage
from app.db.vector_store import VectorStore
from app.services.llm_provider import LLMProvider, Message
from app.services.embedding_service import EmbeddingService
from app.ai.prompts import Prompts

logger = logging.getLogger(__name__)


class RAGService:
    """
    Retrieval-Augmented Generation service.
    Handles semantic search, context retrieval, and LLM-based response generation.
    """

    def __init__(
        self,
        session: Session,
        vector_store: VectorStore,
        embedding_service: EmbeddingService,
        llm_provider: LLMProvider,
    ):
        """
        Initialize RAG service.

        Args:
            session: Database session
            vector_store: VectorStore instance
            embedding_service: EmbeddingService instance
            llm_provider: LLMProvider instance
        """
        self.session = session
        self.vector_store = vector_store
        self.embedding_service = embedding_service
        self.llm_provider = llm_provider

    async def chat(
        self,
        project_id: int,
        user_id: int,
        question: str,
        conversation_id: Optional[int] = None,
        top_k: int = 10,
        similarity_threshold: float = 0.3,
        max_context_length: int = 8000,
    ) -> Dict[str, Any]:
        """
        Process a user question and generate an answer using RAG.

        Args:
            project_id: Project ID
            user_id: User ID
            question: User's question
            conversation_id: Optional existing conversation ID
            top_k: Number of chunks to retrieve
            similarity_threshold: Minimum similarity score
            max_context_length: Maximum context characters to include

        Returns:
            Dict with answer, sources, and conversation metadata
        """
        logger.info(f"Processing chat question for project {project_id}")

        try:
            # Create or get conversation
            if not conversation_id:
                conversation = AIConversation(
                    user_id=user_id,
                    project_id=project_id,
                    title=question[:100],  # Use first 100 chars as title
                    context_type="repository",
                )
                self.session.add(conversation)
                self.session.flush()
                conversation_id = conversation.id
            else:
                conversation = self.session.query(AIConversation).filter_by(
                    id=conversation_id,
                    project_id=project_id,
                ).first()
                if not conversation:
                    raise ValueError(f"Conversation {conversation_id} not found")

            # Retrieve conversation history
            history_messages = self.session.query(AIMessage).filter_by(
                conversation_id=conversation_id,
            ).order_by(AIMessage.created_at).all()

            # Generate query embedding
            query_embedding = await self.embedding_service.embed_text(question)

            # Retrieve relevant code chunks
            relevant_chunks = self.vector_store.semantic_search(
                query_embedding=query_embedding,
                project_id=project_id,
                top_k=top_k,
                similarity_threshold=similarity_threshold,
            )

            # Build context from chunks
            context, sources = self._build_context(
                relevant_chunks,
                max_context_length,
            )

            # Build messages for LLM
            system_prompt = Prompts.get_system_prompt("repository_chat")

            messages = [Message(role="system", content=system_prompt)]

            # Add conversation history (last N messages)
            for msg in history_messages[-4:]:  # Keep last 4 messages for context
                messages.append(Message(role=msg.role, content=msg.content))

            # Add current question with context
            user_message = Prompts.render_repository_chat(question, context)
            messages.append(Message(role="user", content=user_message))

            # Generate response
            response_text = await self.llm_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )

            # Store messages in conversation
            user_msg = AIMessage(
                conversation_id=conversation_id,
                role="user",
                content=question,
                sources=self._sources_to_json(sources),
                token_count=len(question.split()),
                model_used=None,
            )
            self.session.add(user_msg)

            assistant_msg = AIMessage(
                conversation_id=conversation_id,
                role="assistant",
                content=response_text,
                sources=self._sources_to_json(sources),
                token_count=len(response_text.split()),
                model_used="gpt-4-turbo",
            )
            self.session.add(assistant_msg)

            # Update conversation timestamp
            conversation.updated_at = datetime.utcnow()

            self.session.commit()

            return {
                "conversation_id": conversation_id,
                "answer": response_text,
                "sources": sources,
                "chunks_retrieved": len(relevant_chunks),
                "context_length": len(context),
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Chat processing failed: {e}")
            self.session.rollback()
            raise

    async def explain_code(
        self,
        project_id: int,
        user_id: int,
        selected_code: str,
        filepath: str,
        start_line: int,
        end_line: int,
        language: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate an explanation for selected code.

        Args:
            project_id: Project ID
            user_id: User ID
            selected_code: The code to explain
            filepath: Path to the file
            start_line: Starting line number
            end_line: Ending line number
            language: Programming language
            top_k: Number of related chunks to retrieve

        Returns:
            Dict with explanation and sources
        """
        logger.info(f"Generating code explanation for {filepath}:{start_line}-{end_line}")

        try:
            # Generate embedding for the selected code
            code_embedding = await self.embedding_service.embed_text(selected_code)

            # Retrieve related code chunks
            related_chunks = self.vector_store.semantic_search(
                query_embedding=code_embedding,
                project_id=project_id,
                top_k=top_k,
                similarity_threshold=0.2,
            )

            # Filter out the selected code itself
            related_chunks = [
                c for c in related_chunks
                if not (c.start_line == start_line and c.end_line == end_line)
            ][:top_k - 1]

            # Build context
            context = self._format_chunks_for_context(related_chunks)

            # Generate explanation prompt
            system_prompt = Prompts.get_system_prompt("code_explanation")
            prompt = Prompts.render_code_explanation(
                selected_code=selected_code,
                language=language,
                filepath=filepath,
                start_line=start_line,
                end_line=end_line,
                context=context,
            )

            # Generate explanation
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]

            explanation = await self.llm_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=1000,
            )

            # Format sources
            sources = [
                {
                    "file": c.document.path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                    "symbol": c.symbol_name,
                }
                for c in related_chunks
            ]

            return {
                "explanation": explanation,
                "sources": sources,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Code explanation failed: {e}")
            raise

    async def detect_bugs(
        self,
        project_id: int,
        user_id: int,
        selected_code: str,
        filepath: str,
        start_line: int,
        end_line: int,
        language: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Analyze code for potential bugs.

        Args:
            project_id: Project ID
            user_id: User ID
            selected_code: The code to analyze
            filepath: Path to the file
            start_line: Starting line number
            end_line: Ending line number
            language: Programming language
            top_k: Number of related chunks to retrieve

        Returns:
            Dict with bugs analysis and severity levels
        """
        logger.info(f"Analyzing code for bugs in {filepath}:{start_line}-{end_line}")

        try:
            # Retrieve related code for context
            code_embedding = await self.embedding_service.embed_text(selected_code)
            related_chunks = self.vector_store.semantic_search(
                query_embedding=code_embedding,
                project_id=project_id,
                top_k=top_k,
                similarity_threshold=0.2,
            )

            context = self._format_chunks_for_context(related_chunks)

            # Generate bug analysis prompt
            system_prompt = Prompts.get_system_prompt("bug_detection")
            prompt = Prompts.render_bug_detection(
                selected_code=selected_code,
                language=language,
                filepath=filepath,
                start_line=start_line,
                end_line=end_line,
                context=context,
            )

            # Generate analysis
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]

            analysis = await self.llm_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )

            # Format sources
            sources = [
                {
                    "file": c.document.path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                }
                for c in related_chunks
            ]

            return {
                "analysis": analysis,
                "sources": sources,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Bug detection failed: {e}")
            raise

    async def improve_code(
        self,
        project_id: int,
        user_id: int,
        selected_code: str,
        filepath: str,
        start_line: int,
        end_line: int,
        language: str,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Suggest code improvements.

        Args:
            project_id: Project ID
            user_id: User ID
            selected_code: The code to improve
            filepath: Path to the file
            start_line: Starting line number
            end_line: Ending line number
            language: Programming language
            top_k: Number of related chunks to retrieve

        Returns:
            Dict with improvement suggestions
        """
        logger.info(f"Generating code improvements for {filepath}:{start_line}-{end_line}")

        try:
            # Retrieve related code
            code_embedding = await self.embedding_service.embed_text(selected_code)
            related_chunks = self.vector_store.semantic_search(
                query_embedding=code_embedding,
                project_id=project_id,
                top_k=top_k,
                similarity_threshold=0.2,
            )

            context = self._format_chunks_for_context(related_chunks)

            # Generate improvement prompt
            system_prompt = Prompts.get_system_prompt("code_improvement")
            prompt = Prompts.render_code_improvement(
                selected_code=selected_code,
                language=language,
                filepath=filepath,
                start_line=start_line,
                end_line=end_line,
                context=context,
            )

            # Generate suggestions
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]

            suggestions = await self.llm_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=1500,
            )

            sources = [
                {
                    "file": c.document.path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                }
                for c in related_chunks
            ]

            return {
                "suggestions": suggestions,
                "sources": sources,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Code improvement failed: {e}")
            raise

    async def generate_tests(
        self,
        project_id: int,
        user_id: int,
        selected_code: str,
        filepath: str,
        start_line: int,
        end_line: int,
        language: str,
        test_framework: Optional[str] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        """
        Generate unit tests for selected code.

        Args:
            project_id: Project ID
            user_id: User ID
            selected_code: The code to test
            filepath: Path to the file
            start_line: Starting line number
            end_line: Ending line number
            language: Programming language
            test_framework: Testing framework (pytest, jest, etc.)
            top_k: Number of related chunks to retrieve

        Returns:
            Dict with generated tests
        """
        logger.info(f"Generating tests for {filepath}:{start_line}-{end_line}")

        try:
            # Determine test framework if not provided
            if not test_framework:
                test_framework = "pytest" if language.lower() == "python" else "jest"

            # Retrieve related code
            code_embedding = await self.embedding_service.embed_text(selected_code)
            related_chunks = self.vector_store.semantic_search(
                query_embedding=code_embedding,
                project_id=project_id,
                top_k=top_k,
                similarity_threshold=0.2,
            )

            context = self._format_chunks_for_context(related_chunks)

            # Generate test prompt
            system_prompt = Prompts.get_system_prompt("test_generation")
            prompt = Prompts.render_test_generation(
                selected_code=selected_code,
                language=language,
                filepath=filepath,
                start_line=start_line,
                end_line=end_line,
                test_framework=test_framework,
                context=context,
            )

            # Generate tests
            messages = [
                Message(role="system", content=system_prompt),
                Message(role="user", content=prompt),
            ]

            tests = await self.llm_provider.generate_response(
                messages=messages,
                temperature=0.7,
                max_tokens=2000,
            )

            sources = [
                {
                    "file": c.document.path,
                    "start_line": c.start_line,
                    "end_line": c.end_line,
                }
                for c in related_chunks
            ]

            return {
                "tests": tests,
                "test_framework": test_framework,
                "sources": sources,
                "timestamp": datetime.utcnow().isoformat(),
            }

        except Exception as e:
            logger.error(f"Test generation failed: {e}")
            raise

    def _build_context(
        self,
        chunks: List[CodeChunk],
        max_length: int = 8000,
    ) -> tuple[str, List[Dict[str, Any]]]:
        """
        Build context string from retrieved chunks.

        Args:
            chunks: List of CodeChunk objects
            max_length: Maximum context length in characters

        Returns:
            Tuple of (context_string, sources_list)
        """
        context_parts = []
        sources = []
        total_length = 0

        for chunk in chunks:
            chunk_text = f"File: {chunk.document.path} (Lines {chunk.start_line}-{chunk.end_line})\n```{chunk.language}\n{chunk.content}\n```\n"

            if total_length + len(chunk_text) > max_length:
                break

            context_parts.append(chunk_text)
            total_length += len(chunk_text)

            sources.append({
                "file": chunk.document.path,
                "start_line": chunk.start_line,
                "end_line": chunk.end_line,
                "symbol": chunk.symbol_name,
                "language": chunk.language,
            })

        context = "\n".join(context_parts) if context_parts else "No relevant code context found."

        return context, sources

    def _format_chunks_for_context(self, chunks: List[CodeChunk]) -> str:
        """Format chunks into readable context string."""
        if not chunks:
            return "No related code context found."

        parts = []
        for chunk in chunks[:5]:  # Limit to top 5
            parts.append(
                f"File: {chunk.document.path} (Lines {chunk.start_line}-{chunk.end_line})\n"
                f"```{chunk.language}\n{chunk.content}\n```"
            )

        return "\n\n".join(parts)

    def _sources_to_json(self, sources: List[Dict[str, Any]]) -> str:
        """Convert sources list to JSON string."""
        import json
        return json.dumps(sources)

    def get_conversation_history(
        self,
        conversation_id: int,
        project_id: int,
        limit: int = 50,
    ) -> List[Dict[str, Any]]:
        """
        Get conversation history.

        Args:
            conversation_id: Conversation ID
            project_id: Project ID
            limit: Maximum number of messages to return

        Returns:
            List of messages
        """
        conversation = self.session.query(AIConversation).filter_by(
            id=conversation_id,
            project_id=project_id,
        ).first()

        if not conversation:
            return []

        messages = self.session.query(AIMessage).filter_by(
            conversation_id=conversation_id,
        ).order_by(AIMessage.created_at.desc()).limit(limit).all()

        return [
            {
                "role": msg.role,
                "content": msg.content,
                "created_at": msg.created_at.isoformat(),
                "sources": msg.sources,
            }
            for msg in reversed(messages)
        ]
