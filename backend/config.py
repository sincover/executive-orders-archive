import os
from datetime import timedelta
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Base configuration."""
    # Secret key for session management
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key-for-development-only')
    
    # Database settings
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Celery settings
    CELERY_BROKER_URL = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    CELERY_RESULT_BACKEND = os.environ.get('CELERY_RESULT_BACKEND', 'redis://localhost:6379/0')
    
    # API settings
    API_TITLE = 'Executive Orders Archive API'
    API_VERSION = 'v1'
    
    # Logging configuration
    LOG_LEVEL = 'INFO'

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DEV_DATABASE_URL', 
        'postgresql://eo_app_user:eo_app_password@localhost/executive_orders_archive'
    )

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'TEST_DATABASE_URL', 
        'sqlite:///:memory:'
    )
    
    # Disable CSRF tokens in testing
    WTF_CSRF_ENABLED = False

class ProductionConfig(Config):
    """Production configuration."""
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    
    # Use environment specific secret key
    SECRET_KEY = os.environ.get('SECRET_KEY')
    
    # More strict logging in production
    LOG_LEVEL = 'ERROR'
