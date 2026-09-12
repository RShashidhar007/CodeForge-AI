"""
Embedding service for generating and caching embeddings.
Supports multiple embedding providers and batch processing.
"""
from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
import logging
import hashlib

logger = logging.getLogger(__name__)


class EmbeddingProvider(ABC):
    """Abstract base class for embedding providers."""

    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Text to embed

        Returns:
            Embedding vector (list of floats)
        """
        pass

    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for multiple texts efficiently.

        Args:
            texts: List of texts to embed

        Returns:
            List of embedding vectors
        """
        pass

    @abstractmethod
    async def validate_api_key(self) -> bool:
        """Validate that the API key is valid and accessible."""
        pass


class OpenAIEmbeddingProvider(EmbeddingProvider):
    """OpenAI text embedding provider."""

    def __init__(
        self,
        api_key: str,
        model: str = "text-embedding-3-small",
        embedding_dimension: int = 1536,
        timeout: int = 30,
    ):
        """
        Initialize OpenAI embedding provider.

        Args:
            api_key: OpenAI API key
            model: Model name (text-embedding-3-small, text-embedding-3-large, etc)
            embedding_dimension: Dimension of embeddings
            timeout: Request timeout in seconds
        """
        from openai import AsyncOpenAI

        self.api_key = api_key
        self.model = model
        self.embedding_dimension = embedding_dimension
        self.timeout = timeout
        self.client = AsyncOpenAI(
            api_key=api_key,
            timeout=timeout,
        )

    async def embed_text(self, text: str) -> List[float]:
        """Generate embedding for single text."""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=[text],
                dimensions=self.embedding_dimension,
            )
            return response.data[0].embedding
        except Exception as e:
            logger.error(f"OpenAI embedding error: {e}")
            raise

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Generate embeddings for multiple texts."""
        try:
            response = await self.client.embeddings.create(
                model=self.model,
                input=texts,
                dimensions=self.embedding_dimension,
            )
            # Sort by index to maintain order
            embeddings = sorted(response.data, key=lambda x: x.index)
            return [e.embedding for e in embeddings]
        except Exception as e:
            logger.error(f"OpenAI batch embedding error: {e}")
            raise

    async def validate_api_key(self) -> bool:
        """Validate OpenAI API key."""
        try:
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {e}")
            return False


class MockEmbeddingProvider(EmbeddingProvider):
    """
    Mock embedding provider for testing.
    Returns deterministic embeddings based on text hash.
    """

    def __init__(self, embedding_dimension: int = 1536):
        """Initialize mock provider."""
        self.embedding_dimension = embedding_dimension
        self.call_count = 0

    async def embed_text(self, text: str) -> List[float]:
        """Return mock embedding."""
        self.call_count += 1
        return self._generate_mock_embedding(text)

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Return mock embeddings for batch."""
        return [self._generate_mock_embedding(text) for text in texts]

    def _generate_mock_embedding(self, text: str) -> List[float]:
        """Generate deterministic mock embedding from text hash."""
        # Create deterministic but varied embeddings based on text
        hash_obj = hashlib.sha256(text.encode())
        hash_bytes = hash_obj.digest()

        # Convert hash bytes to float values in range [-1, 1]
        embedding = []
        for i in range(self.embedding_dimension):
            byte_index = i % len(hash_bytes)
            # Convert byte (0-255) to (-1, 1)
            value = (hash_bytes[byte_index] / 127.5) - 1.0
            embedding.append(value)

        return embedding

    async def validate_api_key(self) -> bool:
        """Mock validation always succeeds."""
        return True


class EmbeddingService:
    """
    High-level embedding service with caching and batch processing.
    Handles text chunking and embedding generation.
    """

    def __init__(
        self,
        provider: EmbeddingProvider,
        cache: Optional[Dict[str, List[float]]] = None,
        batch_size: int = 10,
    ):
        """
        Initialize embedding service.

        Args:
            provider: EmbeddingProvider instance
            cache: Optional cache dict for storing embeddings
            batch_size: Size of batches for batch processing
        """
        self.provider = provider
        self.cache = cache or {}
        self.batch_size = batch_size
        self.total_requests = 0
        self.cache_hits = 0

    async def embed_text(
        self,
        text: str,
        use_cache: bool = True,
    ) -> List[float]:
        """
        Embed a text string with optional caching.

        Args:
            text: Text to embed
            use_cache: Whether to use cache

        Returns:
            Embedding vector
        """
        self.total_requests += 1

        # Check cache
        if use_cache:
            cache_key = self._get_cache_key(text)
            if cache_key in self.cache:
                self.cache_hits += 1
                logger.debug(f"Cache hit for embedding (total hits: {self.cache_hits})")
                return self.cache[cache_key]

        # Generate embedding
        embedding = await self.provider.embed_text(text)

        # Store in cache
        if use_cache:
            self.cache[cache_key] = embedding

        return embedding

    async def embed_batch(
        self,
        texts: List[str],
        use_cache: bool = True,
    ) -> List[List[float]]:
        """
        Embed multiple texts efficiently.

        Args:
            texts: List of texts to embed
            use_cache: Whether to use cache

        Returns:
            List of embedding vectors
        """
        embeddings = []
        to_embed = []
        to_embed_indices = []

        # Check cache for each text
        for i, text in enumerate(texts):
            if use_cache:
                cache_key = self._get_cache_key(text)
                if cache_key in self.cache:
                    embeddings.append(self.cache[cache_key])
                    self.cache_hits += 1
                else:
                    to_embed.append(text)
                    to_embed_indices.append(i)
            else:
                to_embed.append(text)
                to_embed_indices.append(i)

        # Process texts that need embedding
        if to_embed:
            # Process in batches
            for batch_start in range(0, len(to_embed), self.batch_size):
                batch_end = min(batch_start + self.batch_size, len(to_embed))
                batch_texts = to_embed[batch_start:batch_end]

                batch_embeddings = await self.provider.embed_batch(batch_texts)

                # Cache and store results
                for text, embedding in zip(batch_texts, batch_embeddings):
                    if use_cache:
                        cache_key = self._get_cache_key(text)
                        self.cache[cache_key] = embedding
                    embeddings.append(embedding)

            self.total_requests += len(to_embed)

        # Sort results back to original order
        result = [None] * len(texts)
        embedding_idx = 0
        for i, text in enumerate(texts):
            if use_cache:
                cache_key = self._get_cache_key(text)
                if cache_key in self.cache:
                    result[i] = self.cache[cache_key]
                else:
                    # Find this text in the embeddings list
                    for j, orig_idx in enumerate(to_embed_indices):
                        if orig_idx == i and j < len(embeddings):
                            result[i] = embeddings[j]
                            break
            else:
                # Results are in order
                result[i] = embeddings[embedding_idx]
                embedding_idx += 1

        return result

    def _get_cache_key(self, text: str) -> str:
        """Generate cache key for text."""
        return hashlib.sha256(text.encode()).hexdigest()

    def get_cache_stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        hit_rate = (self.cache_hits / self.total_requests * 100) if self.total_requests > 0 else 0
        return {
            "total_requests": self.total_requests,
            "cache_hits": self.cache_hits,
            "cache_size": len(self.cache),
            "hit_rate": f"{hit_rate:.1f}%",
        }

    async def validate(self) -> bool:
        """Validate provider connection."""
        return await self.provider.validate_api_key()


def create_embedding_provider(
    provider_name: str,
    api_key: str,
    model: str = "text-embedding-3-small",
    embedding_dimension: int = 1536,
    use_mock: bool = False,
) -> EmbeddingProvider:
    """
    Factory function to create embedding provider.

    Args:
        provider_name: "openai", etc.
        api_key: Provider API key
        model: Model identifier
        embedding_dimension: Dimension of embeddings
        use_mock: If True, use mock provider for testing

    Returns:
        Configured EmbeddingProvider instance
    """
    if use_mock:
        return MockEmbeddingProvider(embedding_dimension)

    if provider_name.lower() == "openai":
        return OpenAIEmbeddingProvider(
            api_key=api_key,
            model=model,
            embedding_dimension=embedding_dimension,
        )
    elif provider_name.lower() == "mock":
        return MockEmbeddingProvider(embedding_dimension)
    else:
        raise ValueError(f"Unsupported embedding provider: {provider_name}")
