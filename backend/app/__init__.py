from flask import Flask
from flask_cors import CORS
from app.database import db
from app.routes import register_routes
import logging
from app.utils.logging import configure_app_logging

def create_app(config_name='default'):
    """Factory function to create Flask application instance."""
    app = Flask(__name__)
    
    # Load configuration based on environment
    if config_name == 'production':
        app.config.from_object('config.ProductionConfig')
    elif config_name == 'testing':
        app.config.from_object('config.TestingConfig')
    else:
        app.config.from_object('config.DevelopmentConfig')
    
    # Enable CORS
    CORS(app)
    
    # Initialize extensions
    db.init_app(app)
    
    # Register blueprints
    register_routes(app)
    
    # Configure logging
    configure_app_logging(app)
    
    # Log application startup
    app.logger.info(f'Executive Orders Archive API initialized in {config_name} mode')
    
    return app