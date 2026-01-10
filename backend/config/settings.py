"""Configuration settings for the application."""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Config:
    """Base configuration."""
    
    # Flask settings
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    
    # Upload settings
    UPLOAD_FOLDER = 'uploads'
    REPORT_FOLDER = 'report'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB
    
    # HuggingFace API
    HF_TOKEN = os.getenv('HF_TOKEN')
    
    # Llama API (for local models)
    LLAMA_API_URL = os.getenv('LLAMA_API_URL', 'http://localhost:11434/v1')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Pynguin settings
    PYNGUIN_DANGER_AWARE = "1"


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False


# Config dictionary
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
