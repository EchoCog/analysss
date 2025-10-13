"""
Application Configuration Settings
==================================

Centralized configuration management for the analysis framework.
Supports environment-specific overrides and secure credential handling.
"""

import os
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import timedelta


class Config:
    """Base configuration class"""
    
    # Application settings
    APP_NAME = "Criminal Case Analysis Framework"
    VERSION = "1.0.0-refined"
    
    # Paths
    BASE_DIR = Path(__file__).parent.parent
    DATA_DIR = BASE_DIR / "data"
    UPLOAD_DIR = DATA_DIR / "uploads"
    TEMP_DIR = DATA_DIR / "temp"
    
    # Database
    DATABASE_PATH = os.environ.get(
        "DATABASE_PATH", 
        str(BASE_DIR / "analysis_framework.db")
    )
    DATABASE_POOL_SIZE = 5
    DATABASE_POOL_TIMEOUT = 30
    
    # Framework settings
    FRAMEWORK_CONFIG = {
        "risk_weights": {
            "high_connectivity": 0.3,
            "temporal_clustering": 0.2,
            "evidence_quality": 0.5
        },
        "confidence_thresholds": {
            "high": 0.8,
            "medium": 0.5,
            "low": 0.2
        },
        "analysis_limits": {
            "max_network_size": 10000,
            "max_events": 50000,
            "max_time_range_days": 3650
        }
    }
    
    # API settings
    API_RATE_LIMIT = "100 per hour"
    API_MAX_PAGE_SIZE = 100
    API_DEFAULT_PAGE_SIZE = 20
    
    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    BCRYPT_LOG_ROUNDS = 12
    
    # File handling
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    ALLOWED_EXTENSIONS = {
        'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 
        'doc', 'docx', 'csv', 'json', 'xml'
    }
    
    # Logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "INFO")
    LOG_FORMAT = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE = BASE_DIR / "logs" / "application.log"
    
    # Cache settings
    CACHE_TYPE = "simple"
    CACHE_DEFAULT_TIMEOUT = 300  # 5 minutes
    CACHE_KEY_PREFIX = "caf_"
    
    # Analysis settings
    ANALYSIS_TIMEOUT = 300  # 5 minutes
    ANALYSIS_CACHE_DURATION = 3600  # 1 hour
    
    # Evidence verification
    EVIDENCE_HASH_ALGORITHM = "sha256"
    EVIDENCE_VERIFICATION_REQUIRED = True
    
    # Performance settings
    WORKER_PROCESSES = os.cpu_count() or 4
    THREAD_POOL_SIZE = 10
    
    @classmethod
    def init_app(cls, app):
        """Initialize application with configuration"""
        # Create necessary directories
        cls.DATA_DIR.mkdir(exist_ok=True)
        cls.UPLOAD_DIR.mkdir(exist_ok=True)
        cls.TEMP_DIR.mkdir(exist_ok=True)
        (cls.BASE_DIR / "logs").mkdir(exist_ok=True)


class DevelopmentConfig(Config):
    """Development configuration"""
    
    DEBUG = True
    TESTING = False
    
    # Relaxed security for development
    REQUIRE_AUTH = False
    CORS_ORIGINS = "*"
    
    # More verbose logging
    LOG_LEVEL = "DEBUG"
    
    # Shorter cache times for development
    CACHE_DEFAULT_TIMEOUT = 60
    ANALYSIS_CACHE_DURATION = 300


class TestingConfig(Config):
    """Testing configuration"""
    
    DEBUG = False
    TESTING = True
    
    # Use in-memory database for tests
    DATABASE_PATH = ":memory:"
    
    # Disable authentication for tests
    REQUIRE_AUTH = False
    
    # Minimal logging
    LOG_LEVEL = "ERROR"
    
    # No caching during tests
    CACHE_TYPE = "null"


class ProductionConfig(Config):
    """Production configuration"""
    
    DEBUG = False
    TESTING = False
    
    # Strict security
    REQUIRE_AUTH = True
    CORS_ORIGINS = os.environ.get("CORS_ORIGINS", "").split(",")
    
    # Production database
    DATABASE_PATH = os.environ.get("DATABASE_PATH")
    if not DATABASE_PATH:
        raise ValueError("DATABASE_PATH must be set in production")
    
    # Production secrets
    SECRET_KEY = os.environ.get("SECRET_KEY")
    if not SECRET_KEY:
        raise ValueError("SECRET_KEY must be set in production")
    
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", SECRET_KEY)
    
    # Production logging
    LOG_LEVEL = os.environ.get("LOG_LEVEL", "WARNING")
    
    # Redis cache in production
    CACHE_TYPE = "redis"
    CACHE_REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379/0")
    
    # Stricter limits
    API_RATE_LIMIT = "50 per hour"
    ANALYSIS_TIMEOUT = 600  # 10 minutes


# Configuration factory
config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}


def get_config(env: Optional[str] = None) -> Config:
    """
    Get configuration object based on environment
    
    Args:
        env: Environment name (development, testing, production)
        
    Returns:
        Configuration object
    """
    if env is None:
        env = os.environ.get('FLASK_ENV', 'development')
    
    return config.get(env, config['default'])


# Validation schemas for configuration
RISK_WEIGHT_SCHEMA = {
    "type": "object",
    "properties": {
        "high_connectivity": {"type": "number", "minimum": 0, "maximum": 1},
        "temporal_clustering": {"type": "number", "minimum": 0, "maximum": 1},
        "evidence_quality": {"type": "number", "minimum": 0, "maximum": 1}
    },
    "required": ["high_connectivity", "temporal_clustering", "evidence_quality"]
}


def validate_config(config_dict: Dict[str, Any]) -> bool:
    """
    Validate configuration dictionary
    
    Args:
        config_dict: Configuration to validate
        
    Returns:
        True if valid
        
    Raises:
        ValueError: If configuration is invalid
    """
    # Validate risk weights sum to 1.0
    if 'risk_weights' in config_dict:
        weights = config_dict['risk_weights']
        total = sum(weights.values())
        if abs(total - 1.0) > 0.001:
            raise ValueError(f"Risk weights must sum to 1.0, got {total}")
    
    # Validate thresholds are in order
    if 'confidence_thresholds' in config_dict:
        thresholds = config_dict['confidence_thresholds']
        if not (thresholds['low'] < thresholds['medium'] < thresholds['high']):
            raise ValueError("Confidence thresholds must be in ascending order")
    
    return True