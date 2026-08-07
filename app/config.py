"""
Application Configuration
==========================
Holds all environment-specific configuration classes.
"""

import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class BaseConfig:
    """Base configuration shared across all environments."""
    SECRET_KEY = os.getenv("SECRET_KEY", "change-me-in-production")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mistral AI
    MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY")
    MISTRAL_MODEL = os.getenv("MISTRAL_MODEL", "mistral-large-latest")

    # Speech settings
    UPLOAD_FOLDER = os.path.join(BASE_DIR, "..", "uploads")
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB


class DevelopmentConfig(BaseConfig):
    """Development environment configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'aicareerconnect_dev.db')}"
    )


class TestingConfig(BaseConfig):
    """Testing environment configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = "sqlite:///:memory:"


class ProductionConfig(BaseConfig):
    """Production environment configuration."""
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv(
        "DATABASE_URL",
        f"sqlite:///{os.path.join(BASE_DIR, '..', 'instance', 'aicareerconnect.db')}"
    )


config_by_name = {
    "development": DevelopmentConfig,
    "testing": TestingConfig,
    "production": ProductionConfig,
}
