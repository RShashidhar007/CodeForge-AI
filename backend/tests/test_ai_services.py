"""
Tests for AI services: embedding, LLM, and RAG.
"""
import pytest
from unittest.mock import Mock, AsyncMock, patch
from sqlalchemy.orm import Session

from app.services.embedding_service import (
    EmbeddingService,
    MockEmbeddingProvider,
    create_embedding_provider,
)
from app.services.llm_provider import (
    Message,
    MockLLMProvider,
    create_llm_provider,
)
from app.services.code_chunker import CodeChunker, CodeChunk
from app.db.vector_store import VectorStore
from app.models.ai import CodeDocument, CodeChunk as CodeChunkModel
from app.core.config import settings


class TestEmbeddingService:
    """Test embedding service."""

    def test_mock_embedding_provider_initialization(self):
        """Test MockEmbeddingProvider initialization."""
        provider = MockEmbeddingProvider(embedding_dimension=1536)
        assert provider.embedding_dimension == 1536
        assert provider.call_count == 0

    @pytest.mark.asyncio
    async def test_embed_text(self):
        """Test embedding a single text."""
        provider = MockEmbeddingProvider()
        embedding = await provider.embed_text("Hello world")

        assert isinstance(embedding, list)
        assert len(embedding) == 1536
        assert all(isinstance(x, (int, float)) for x in embedding)

    @pytest.mark.asyncio
    async def test_embed_batch(self):
        """Test embedding multiple texts."""
        provider = MockEmbeddingProvider()
        texts = ["Hello", "World", "Test"]
        embeddings = await provider.embed_batch(texts)

        assert len(embeddings) == 3
        assert all(len(e) == 1536 for e in embeddings)

    @pytest.mark.asyncio
    async def test_deterministic_embeddings(self):
        """Test that same text produces same embedding."""
        provider = MockEmbeddingProvider()
        text = "Deterministic test"

        embedding1 = await provider.embed_text(text)
        embedding2 = await provider.embed_text(text)

        assert embedding1 == embedding2

    @pytest.mark.asyncio
    async def test_embedding_service_caching(self):
        """Test embedding service caching."""
        provider = MockEmbeddingProvider()
        service = EmbeddingService(provider, batch_size=10)

        text = "Test text for caching"

        # First call
        embedding1 = await service.embed_text(text)
        assert service.cache_hits == 0
        assert service.total_requests == 1

        # Second call (should hit cache)
        embedding2 = await service.embed_text(text)
        assert service.cache_hits == 1
        assert service.total_requests == 1  # No new request

        assert embedding1 == embedding2

    @pytest.mark.asyncio
    async def test_embedding_service_batch(self):
        """Test embedding service batch processing."""
        provider = MockEmbeddingProvider()
        service = EmbeddingService(provider, batch_size=2)

        texts = ["A", "B", "C", "D"]
        embeddings = await service.embed_batch(texts)

        assert len(embeddings) == 4
        assert all(len(e) == 1536 for e in embeddings)

    @pytest.mark.asyncio
    async def test_mock_validation(self):
        """Test mock provider validation."""
        provider = MockEmbeddingProvider()
        is_valid = await provider.validate_api_key()
        assert is_valid is True

    def test_create_embedding_provider_mock(self):
        """Test creating mock embedding provider."""
        provider = create_embedding_provider(
            provider_name="openai",
            api_key="test-key",
            use_mock=True,
        )
        assert isinstance(provider, MockEmbeddingProvider)

    def test_create_embedding_provider_explicit_mock(self):
        """Test creating explicit mock provider."""
        provider = create_embedding_provider(
            provider_name="mock",
            api_key="test-key",
        )
        assert isinstance(provider, MockEmbeddingProvider)


class TestLLMProvider:
    """Test LLM provider."""

    def test_mock_llm_provider_initialization(self):
        """Test MockLLMProvider initialization."""
        provider = MockLLMProvider()
        assert provider.call_count == 0

    @pytest.mark.asyncio
    async def test_generate_response(self):
        """Test generating response."""
        provider = MockLLMProvider()
        messages = [
            Message(role="system", content="You are helpful"),
            Message(role="user", content="Explain this bug"),
        ]

        response = await provider.generate_response(messages)
        assert isinstance(response, str)
        assert len(response) > 0
        assert provider.call_count == 1

    @pytest.mark.asyncio
    async def test_generate_response_streaming(self):
        """Test streaming response."""
        provider = MockLLMProvider()
        messages = [Message(role="user", content="Hello")]

        chunks = []
        async for chunk in provider.generate_response_streaming(messages):
            chunks.append(chunk)

        assert len(chunks) > 0
        full_response = "".join(chunks)
        assert len(full_response) > 0

    @pytest.mark.asyncio
    async def test_count_tokens(self):
        """Test token counting."""
        provider = MockLLMProvider()
        text = "This is a test text with some words"
        tokens = await provider.count_tokens(text)

        assert isinstance(tokens, int)
        assert tokens > 0

    @pytest.mark.asyncio
    async def test_validate_api_key(self):
        """Test API key validation."""
        provider = MockLLMProvider()
        is_valid = await provider.validate_api_key()
        assert is_valid is True

    def test_create_llm_provider_mock(self):
        """Test creating mock LLM provider."""
        provider = create_llm_provider(
            provider_name="openai",
            api_key="test-key",
            use_mock=True,
        )
        assert isinstance(provider, MockLLMProvider)


class TestCodeChunker:
    """Test code chunking."""

    def test_chunker_initialization(self):
        """Test CodeChunker initialization."""
        chunker = CodeChunker()
        assert chunker.max_chunk_size == 500
        assert chunker.min_chunk_size == 50

    def test_detect_language_python(self):
        """Test language detection for Python."""
        chunker = CodeChunker()
        lang = chunker.detect_language("example.py")
        assert lang == "python"

    def test_detect_language_javascript(self):
        """Test language detection for JavaScript."""
        chunker = CodeChunker()
        lang = chunker.detect_language("example.js")
        assert lang == "javascript"

    def test_detect_language_unknown(self):
        """Test language detection for unknown file."""
        chunker = CodeChunker()
        lang = chunker.detect_language("example.unknown")
        assert lang == "unknown"

    def test_chunk_python_code(self):
        """Test chunking Python code."""
        chunker = CodeChunker()
        code = """
def hello():
    print("Hello")

def world():
    print("World")
"""
        chunks = chunker.chunk_code(code, "python")
        assert len(chunks) >= 1
        assert all(isinstance(c, CodeChunk) for c in chunks)

    def test_chunk_empty_code(self):
        """Test chunking empty code."""
        chunker = CodeChunker()
        chunks = chunker.chunk_code("", "python")
        assert len(chunks) == 0

    def test_chunk_generic_code(self):
        """Test generic chunking for unsupported language."""
        chunker = CodeChunker()
        code = "\n".join([f"line {i}" for i in range(200)])
        chunks = chunker.chunk_code(code, "unknown")
        assert len(chunks) > 0

    def test_python_function_detection(self):
        """Test Python function detection."""
        chunker = CodeChunker()
        code = """
def add(a, b):
    '''Add two numbers.'''
    return a + b

def multiply(a, b):
    '''Multiply two numbers.'''
    return a * b
"""
        chunks = chunker.chunk_code(code, "python")
        assert len(chunks) >= 2
        # Check that function names are captured
        symbols = [c.symbol_name for c in chunks if c.symbol_name]
        assert len(symbols) > 0

    def test_python_class_detection(self):
        """Test Python class detection."""
        chunker = CodeChunker()
        code = """
class Calculator:
    def add(self, a, b):
        return a + b
    
    def subtract(self, a, b):
        return a - b
"""
        chunks = chunker.chunk_code(code, "python")
        assert len(chunks) >= 1


class TestVectorStore:
    """Test vector store operations."""

    def test_vector_store_initialization(self):
        """Test VectorStore initialization."""
        mock_session = Mock(spec=Session)
        store = VectorStore(mock_session)
        assert store.session is mock_session

    @pytest.mark.asyncio
    async def test_enable_pgvector(self):
        """Test enabling pgvector extension."""
        mock_session = Mock(spec=Session)
        mock_session.execute = Mock()
        mock_session.commit = Mock()

        store = VectorStore(mock_session)
        result = await store.enable_pgvector()

        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()

    def test_store_embedding_success(self):
        """Test storing an embedding."""
        mock_session = Mock(spec=Session)
        mock_session.execute = Mock()
        mock_session.commit = Mock()

        store = VectorStore(mock_session)
        embedding = [0.1, 0.2, 0.3] * 512  # 1536 dims

        result = store.store_embedding(
            chunk_id=1,
            embedding=embedding,
            model="test-model",
        )

        assert result is True
        mock_session.execute.assert_called_once()
        mock_session.commit.assert_called_once()


class TestRAGIntegration:
    """Integration tests for RAG components."""

    @pytest.mark.asyncio
    async def test_embedding_and_retrieval_flow(self):
        """Test full embedding and retrieval flow."""
        # Create mock embedding provider
        embedding_provider = MockEmbeddingProvider()
        embedding_service = EmbeddingService(embedding_provider)

        # Create embeddings for sample texts
        texts = [
            "The authentication system uses JWT tokens",
            "Users are stored in the database",
            "Projects contain multiple files",
        ]

        embeddings = await embedding_service.embed_batch(texts)
        assert len(embeddings) == 3
        assert all(len(e) == 1536 for e in embeddings)

    @pytest.mark.asyncio
    async def test_code_chunking_and_embedding(self):
        """Test code chunking followed by embedding."""
        chunker = CodeChunker()
        embedding_provider = MockEmbeddingProvider()
        embedding_service = EmbeddingService(embedding_provider)

        code = """
def authenticate(username, password):
    user = find_user(username)
    if user and verify_password(password, user.password_hash):
        return create_jwt_token(user)
    return None
"""

        # Chunk the code
        chunks = chunker.chunk_code(code, "python")
        assert len(chunks) > 0

        # Generate embeddings for chunks
        chunk_contents = [c.content for c in chunks]
        embeddings = await embedding_service.embed_batch(chunk_contents)
        assert len(embeddings) == len(chunks)

    @pytest.mark.asyncio
    async def test_mock_llm_different_prompts(self):
        """Test mock LLM with different prompts."""
        provider = MockLLMProvider()

        # Test different prompt types
        prompts = [
            ("bug", "Analyze this bug"),
            ("improve", "Improve this code"),
            ("explain", "Explain this function"),
            ("test", "Generate tests"),
        ]

        for keyword, prompt in prompts:
            messages = [Message(role="user", content=prompt)]
            response = await provider.generate_response(messages)
            assert isinstance(response, str)
            assert len(response) > 0
