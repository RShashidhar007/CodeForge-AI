"""
Application configuration using Pydantic Settings.
Environment variables are loaded from .env file or system environment.
"""
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database
    db_url: str
    
    # JWT
    jwt_secret: str
    jwt_expiration_seconds: int = 86400  # 24 hours
    jwt_algorithm: str = "HS256"
    
    # CORS
    cors_allowed_origins: str = "http://localhost:5173"
    
    # Admin Bootstrap
    admin_email: str = ""
    admin_password: str = ""
    admin_name: str = "Platform Admin"
    
    # Server
    port: int = 8080
    
    # Month 2: AI & LLM Configuration
    llm_provider: str = "openai"
    llm_model: str = "gpt-4-turbo"
    llm_api_key: str = ""
    llm_max_tokens: int = 2000
    llm_temperature: float = 0.7
    
    # Embedding Configuration
    embedding_provider: str = "openai"
    embedding_model: str = "text-embedding-3-small"
    embedding_api_key: str = ""
    embedding_dimension: int = 1536
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379"
    
    # Repository Indexing
    max_file_size_mb: int = 10
    supported_extensions: str = ".py,.js,.ts,.tsx,.jsx,.java,.go,.rs,.cpp,.c,.cs,.html,.css,.sql,.json,.yaml,.yml,.md"
    ignored_paths: str = "node_modules,.git,dist,build,__pycache__,.venv,target,.next,.pytest_cache,*.pyc,*.egg-info"
    
    # Month 3: Multi-Agent AI Configuration
    ai_max_task_duration_seconds: int = 1800  # 30 minutes
    ai_max_agent_iterations: int = 10
    ai_max_tool_calls_per_task: int = 100
    ai_max_llm_calls_per_task: int = 50
    ai_max_test_iterations: int = 3
    ai_max_debug_attempts: int = 3
    ai_max_review_cycles: int = 3
    
    # Execution Service
    ai_execution_timeout_seconds: int = 300
    ai_execution_memory_limit_mb: int = 512
    ai_execution_docker_image: str = "recruitment-platform-backend:latest"
    ai_enable_mock_execution: bool = False
    
    # LLM Behavior (Temperature for different agents)
    ai_llm_temperature_planning: float = 0.5
    ai_llm_temperature_coding: float = 0.3
    ai_llm_temperature_review: float = 0.2
    ai_llm_temperature_analysis: float = 0.4
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    @property
    def cors_origins_list(self) -> list[str]:
        """Parse comma-separated CORS origins into a list."""
        return [origin.strip() for origin in self.cors_allowed_origins.split(",")]
    
    @property
    def supported_extensions_list(self) -> list[str]:
        """Parse supported file extensions."""
        return [ext.strip() for ext in self.supported_extensions.split(",")]
    
    @property
    def ignored_paths_list(self) -> list[str]:
        """Parse ignored paths patterns."""
        return [path.strip() for path in self.ignored_paths.split(",")]


# Global settings instance
settings = Settings()
