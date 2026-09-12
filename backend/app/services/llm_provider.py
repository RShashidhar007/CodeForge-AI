"""
LLM Provider abstraction.
Supports multiple LLM backends through a common interface.
"""
from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any, AsyncIterator
from dataclasses import dataclass
import logging

logger = logging.getLogger(__name__)


@dataclass
class Message:
    """Represents a message in a conversation."""
    role: str  # "system", "user", "assistant"
    content: str


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_response(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """
        Generate a response from the LLM.

        Args:
            messages: List of Message objects
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Returns:
            Generated text response
        """
        pass

    @abstractmethod
    async def generate_response_streaming(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """
        Generate a streaming response from the LLM.

        Args:
            messages: List of Message objects
            temperature: Sampling temperature (0-1)
            max_tokens: Maximum tokens in response

        Yields:
            Text chunks as they're generated
        """
        pass

    @abstractmethod
    async def count_tokens(self, text: str) -> int:
        """
        Count tokens in a text string.

        Args:
            text: Text to count

        Returns:
            Number of tokens
        """
        pass

    @abstractmethod
    async def validate_api_key(self) -> bool:
        """Validate that the API key is valid and accessible."""
        pass


class OpenAIProvider(LLMProvider):
    """OpenAI GPT implementation."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4-turbo",
        temperature: float = 0.7,
        max_tokens: int = 2000,
        timeout: int = 30,
    ):
        """
        Initialize OpenAI provider.

        Args:
            api_key: OpenAI API key
            model: Model name (gpt-4-turbo, gpt-3.5-turbo, etc)
            temperature: Default temperature (0-1)
            max_tokens: Default max tokens
            timeout: Request timeout in seconds
        """
        from openai import AsyncOpenAI

        self.api_key = api_key
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.client = AsyncOpenAI(
            api_key=api_key,
            timeout=timeout,
        )

    async def generate_response(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Generate a response using OpenAI API."""
        try:
            formatted_messages = [{"role": m.role, "content": m.content} for m in messages]

            response = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )

            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise

    async def generate_response_streaming(
        self,
        messages: List[Message],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """Generate a streaming response using OpenAI API."""
        try:
            formatted_messages = [{"role": m.role, "content": m.content} for m in messages]

            stream = await self.client.chat.completions.create(
                model=self.model,
                messages=formatted_messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
                stream=True,
            )

            async for chunk in stream:
                if chunk.choices[0].delta.content:
                    yield chunk.choices[0].delta.content
        except Exception as e:
            logger.error(f"OpenAI streaming API error: {e}")
            raise

    async def count_tokens(self, text: str) -> int:
        """
        Estimate token count for text.
        For production, use tiktoken library for accuracy.
        """
        try:
            import tiktoken

            encoding = tiktoken.encoding_for_model(self.model)
            tokens = encoding.encode(text)
            return len(tokens)
        except ImportError:
            # Fallback: rough estimate (1 token ≈ 4 characters)
            return len(text) // 4

    async def validate_api_key(self) -> bool:
        """Validate OpenAI API key."""
        try:
            # Make a minimal API call to validate key
            await self.client.models.list()
            return True
        except Exception as e:
            logger.error(f"OpenAI API key validation failed: {e}")
            return False


class MockLLMProvider(LLMProvider):
    """
    Mock LLM provider for testing.
    Returns deterministic responses without making API calls.
    """

    def __init__(self):
        """Initialize mock provider."""
        self.call_count = 0

    async def generate_response(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> str:
        """Return a mock response."""
        self.call_count += 1

        # Return different responses based on context
        last_message = messages[-1].content if messages else ""

        if "bug" in last_message.lower():
            return (
                "🔍 **Potential Issues Found:**\n\n"
                "1. **Missing null check** (Line 42)\n"
                "   - Variable `user` could be None\n\n"
                "2. **Unreachable code** (Line 87)\n"
                "   - Code after return statement\n\n"
                "**Severity:** MEDIUM"
            )
        elif "improve" in last_message.lower():
            return (
                "💡 **Code Improvement Suggestions:**\n\n"
                "1. Extract duplicated logic into helper function\n"
                "2. Add type hints for better IDE support\n"
                "3. Consider using context manager for resource handling"
            )
        elif "explain" in last_message.lower():
            return (
                "📝 **Code Explanation:**\n\n"
                "This function validates user input and returns a boolean.\n"
                "- Takes email string as input\n"
                "- Checks format using regex pattern\n"
                "- Returns True if valid, False otherwise"
            )
        elif "test" in last_message.lower():
            return (
                "✅ **Generated Tests:**\n\n"
                "```python\n"
                "def test_valid_email():\n"
                "    assert is_valid_email('user@example.com') == True\n\n"
                "def test_invalid_email():\n"
                "    assert is_valid_email('invalid') == False\n"
                "```"
            )
        else:
            return (
                "This is a mock response. "
                "In production, this would be replaced with actual LLM output."
            )

    async def generate_response_streaming(
        self,
        messages: List[Message],
        temperature: float = 0.7,
        max_tokens: Optional[int] = None,
    ) -> AsyncIterator[str]:
        """Yield mock response in chunks."""
        response = await self.generate_response(messages, temperature, max_tokens)
        # Simulate streaming by yielding in chunks
        chunk_size = 10
        for i in range(0, len(response), chunk_size):
            yield response[i : i + chunk_size]

    async def count_tokens(self, text: str) -> int:
        """Return mock token count."""
        # Simple estimate: ~1 token per 4 characters
        return len(text) // 4

    async def validate_api_key(self) -> bool:
        """Mock validation always succeeds."""
        return True


def create_llm_provider(
    provider_name: str,
    api_key: str,
    model: str = "gpt-4-turbo",
    temperature: float = 0.7,
    max_tokens: int = 2000,
    use_mock: bool = False,
) -> LLMProvider:
    """
    Factory function to create appropriate LLM provider.

    Args:
        provider_name: "openai", "anthropic", etc.
        api_key: Provider API key
        model: Model identifier
        temperature: Sampling temperature
        max_tokens: Max tokens in response
        use_mock: If True, use mock provider for testing

    Returns:
        Configured LLMProvider instance
    """
    if use_mock:
        return MockLLMProvider()

    if provider_name.lower() == "openai":
        return OpenAIProvider(
            api_key=api_key,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
        )
    elif provider_name.lower() == "mock":
        return MockLLMProvider()
    else:
        raise ValueError(f"Unsupported LLM provider: {provider_name}")
