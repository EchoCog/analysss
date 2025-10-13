"""
Centralized Configuration Management

This module provides centralized configuration management for the analysis system,
supporting environment-based settings and secure secrets management.
"""

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class DatabaseConfig:
    """Database configuration settings."""

    # Supabase configuration
    supabase_url: str
    supabase_key: str
    supabase_service_role_key: Optional[str] = None

    # Neon configuration
    neon_host: Optional[str] = None
    neon_database: Optional[str] = None
    neon_user: Optional[str] = None
    neon_password: Optional[str] = None
    neon_connection_string: Optional[str] = None

    # Connection pooling
    pool_size: int = 10
    max_overflow: int = 20
    pool_timeout: int = 30
    pool_recycle: int = 3600

    # Retry configuration
    max_retries: int = 3
    retry_delay: float = 1.0
    retry_backoff: float = 2.0


@dataclass
class APIConfig:
    """API configuration settings."""

    # OpenAI configuration
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4"
    openai_temperature: float = 0.7
    openai_max_tokens: int = 2000

    # Flask API configuration
    flask_host: str = "0.0.0.0"
    flask_port: int = 5000
    flask_debug: bool = False

    # Rate limiting
    rate_limit_enabled: bool = True
    rate_limit_per_minute: int = 60


@dataclass
class SystemConfig:
    """System-wide configuration settings."""

    # Environment
    environment: str = "development"
    debug: bool = False

    # Logging
    log_level: str = "INFO"
    log_format: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    log_file: Optional[str] = None

    # Paths
    repository_root: Path = Path(__file__).parent.parent
    data_dir: Path = repository_root / "data"
    logs_dir: Path = repository_root / "logs"
    cache_dir: Path = repository_root / ".cache"

    # Performance
    enable_caching: bool = True
    cache_ttl: int = 3600
    batch_size: int = 100

    # Security
    encrypt_sensitive_data: bool = True
    audit_logging: bool = True


class Config:
    """
    Main configuration class that loads and manages all configuration settings.
    """

    def __init__(self):
        self.database = self._load_database_config()
        self.api = self._load_api_config()
        self.system = self._load_system_config()

    def _load_database_config(self) -> DatabaseConfig:
        """Load database configuration from environment variables."""
        return DatabaseConfig(
            supabase_url=os.getenv("SUPABASE_URL", ""),
            supabase_key=os.getenv("SUPABASE_KEY", ""),
            supabase_service_role_key=os.getenv("SUPABASE_SERVICE_ROLE_KEY"),
            neon_host=os.getenv("NEON_HOST"),
            neon_database=os.getenv("NEON_DATABASE"),
            neon_user=os.getenv("NEON_USER"),
            neon_password=os.getenv("NEON_PASSWORD"),
            neon_connection_string=os.getenv("NEON_CONNECTION_STRING"),
            pool_size=int(os.getenv("DB_POOL_SIZE", "10")),
            max_overflow=int(os.getenv("DB_MAX_OVERFLOW", "20")),
            pool_timeout=int(os.getenv("DB_POOL_TIMEOUT", "30")),
            pool_recycle=int(os.getenv("DB_POOL_RECYCLE", "3600")),
            max_retries=int(os.getenv("DB_MAX_RETRIES", "3")),
            retry_delay=float(os.getenv("DB_RETRY_DELAY", "1.0")),
            retry_backoff=float(os.getenv("DB_RETRY_BACKOFF", "2.0")),
        )

    def _load_api_config(self) -> APIConfig:
        """Load API configuration from environment variables."""
        return APIConfig(
            openai_api_key=os.getenv("OPENAI_API_KEY"),
            openai_model=os.getenv("OPENAI_MODEL", "gpt-4"),
            openai_temperature=float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
            openai_max_tokens=int(os.getenv("OPENAI_MAX_TOKENS", "2000")),
            flask_host=os.getenv("FLASK_HOST", "0.0.0.0"),
            flask_port=int(os.getenv("FLASK_PORT", "5000")),
            flask_debug=os.getenv("FLASK_DEBUG", "False").lower() == "true",
            rate_limit_enabled=os.getenv("RATE_LIMIT_ENABLED", "True").lower()
            == "true",
            rate_limit_per_minute=int(os.getenv("RATE_LIMIT_PER_MINUTE", "60")),
        )

    def _load_system_config(self) -> SystemConfig:
        """Load system configuration from environment variables."""
        config = SystemConfig(
            environment=os.getenv("ENVIRONMENT", "development"),
            debug=os.getenv("DEBUG", "False").lower() == "true",
            log_level=os.getenv("LOG_LEVEL", "INFO"),
            log_format=os.getenv(
                "LOG_FORMAT", "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            ),
            log_file=os.getenv("LOG_FILE"),
            enable_caching=os.getenv("ENABLE_CACHING", "True").lower() == "true",
            cache_ttl=int(os.getenv("CACHE_TTL", "3600")),
            batch_size=int(os.getenv("BATCH_SIZE", "100")),
            encrypt_sensitive_data=os.getenv("ENCRYPT_SENSITIVE_DATA", "True").lower()
            == "true",
            audit_logging=os.getenv("AUDIT_LOGGING", "True").lower() == "true",
        )

        # Ensure directories exist
        config.data_dir.mkdir(exist_ok=True, parents=True)
        config.logs_dir.mkdir(exist_ok=True, parents=True)
        config.cache_dir.mkdir(exist_ok=True, parents=True)

        return config

    def validate(self) -> bool:
        """
        Validate that all required configuration values are present.

        Returns:
            bool: True if configuration is valid, False otherwise
        """
        required_fields = [
            (self.database.supabase_url, "SUPABASE_URL"),
            (self.database.supabase_key, "SUPABASE_KEY"),
        ]

        missing_fields = [name for value, name in required_fields if not value]

        if missing_fields:
            print(f"Missing required configuration: {', '.join(missing_fields)}")
            return False

        return True


# Global configuration instance
config = Config()


def get_config() -> Config:
    """
    Get the global configuration instance.

    Returns:
        Config: The global configuration instance
    """
    return config
