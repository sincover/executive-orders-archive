from flask import Flask
from flask_cors import CORS
import logging
import os

def create_app(config_name='default'):
    """
    Create and configure the Flask application.
    
    Args:
        config_name (str): Configuration name ('development', 'testing', 'production')
        
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    
    # Configure app from config.py
    try:
        from config import config
        app.config.from_object(config.get(config_name, config['default']))
    except ImportError:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get('SECRET_KEY', 'dev-key'),
            SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL', 'sqlite:///app.db'),
            SQLALCHEMY_TRACK_MODIFICATIONS=False
        )
    
    # Force SQLite for testing to avoid PostgreSQL dependency issues
    if config_name == 'testing':
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    # Enable CORS
    CORS(app)
    
    # Configure logging
    configure_logging(app)
    
    # Initialize database
    from app.models import init_db
    init_db(app)
    
    # Register blueprints
    from app.routes import api_bp
    app.register_blueprint(api_bp)
    
    # Register global error handlers
    @app.errorhandler(404)
    def not_found(e):
        from app.utils.http import not_found
        return not_found(str(e))
    
    @app.errorhandler(500)
    def server_error(e):
        from app.utils.http import server_error
        return server_error(str(e))
    
    app.logger.info('Application initialized')
    
    return app

def configure_logging(app):
    """Configure logging for the application."""
    log_level = app.config.get('LOG_LEVEL', 'INFO')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'logs')
    os.makedirs(log_dir, exist_ok=True)
    
    # Configure logging
    log_file = os.path.join(log_dir, 'app.log')
    handler = logging.FileHandler(log_file)
    handler.setLevel(logging.getLevelName(log_level))
    
    # Set formatter
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)
    
    # Add handler to app logger
    app.logger.addHandler(handler)
    app.logger.setLevel(logging.getLevelName(log_level))
    
    # Add handler to root logger
    root_logger = logging.getLogger()
    root_logger.addHandler(handler)
    root_logger.setLevel(logging.getLevelName(log_level))
