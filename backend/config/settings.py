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
    MAX_CONTENT_LENGTH = 100 * 1024 * 1024  # 100MB
    
    # HuggingFace API
    HF_TOKEN = os.getenv('HF_TOKEN')
    
    # Llama API (for local models)
    LLAMA_API_URL = os.getenv('LLAMA_API_URL', 'http://localhost:11434/v1')
    
    # Gemini API (Google Generative AI)
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    GEMINI_MODEL = os.getenv('GEMINI_MODEL', 'gemini-1.5-flash')
    
    # CORS settings
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:3000,http://localhost:5173').split(',')
    
    # Pynguin settings
    PYNGUIN_DANGER_AWARE = "1"
    
    # MongoDB settings
    MONGODB_URL = os.getenv('MONGODB_URL', 'mongodb://localhost:27017')
    DATABASE_NAME = os.getenv('DATABASE_NAME', 'pyTestGenie')
    
    # JWT settings
    ALGORITHM = os.getenv('ALGORITHM', 'HS256')
    ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES', '30'))


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
