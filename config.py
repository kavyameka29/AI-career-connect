"""
Application Configuration
-------------------------
Centralizes all configuration settings: secret keys, database URIs,
API keys, and feature flags. Uses environment variables for sensitive data.
"""

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


class Config:
    """Base configuration shared across all environments."""

    # Flask core
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-key-change-in-production")

    # Database configuration (supports SQLite locally, PostgreSQL on Render)
    BASEDIR = os.path.abspath(os.path.dirname(__file__))
    _database_url = os.environ.get("DATABASE_URL")
    if _database_url and _database_url.startswith("postgres://"):
        _database_url = _database_url.replace("postgres://", "postgresql://", 1)
    SQLALCHEMY_DATABASE_URI = _database_url or f"sqlite:///{os.path.join(BASEDIR, 'instance', 'ai_career_connect.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mistral AI API
    MISTRAL_API_KEY = os.environ.get("MISTRAL_API_KEY", "")
    MISTRAL_MODEL = os.environ.get("MISTRAL_MODEL", "mistral-large-latest")

    # Speech settings
    UPLOAD_FOLDER = os.path.join(BASEDIR, "instance", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload

    # TTS settings
    TTS_ENGINE = os.environ.get("TTS_ENGINE", "pyttsx3")  # pyttsx3 or gTTS


class DevelopmentConfig(Config):
    """Development-specific configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production-specific configuration."""
    DEBUG = False


class TestingConfig(Config):
    """Testing-specific configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


# Map config names to classes
config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}
