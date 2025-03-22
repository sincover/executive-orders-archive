import os
import logging
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler
import json
from datetime import datetime

# Base directory for logs
LOG_DIR = os.environ.get('LOG_DIR', 'logs')

# Ensure log directory exists
os.makedirs(LOG_DIR, exist_ok=True)

def configure_app_logging(app):
    """
    Configure logging for the Flask application.
    
    Args:
        app: Flask application instance
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(app.root_path, '..', '..', LOG_DIR)
    os.makedirs(log_dir, exist_ok=True)
    
    # Application log
    app_log_file = os.path.join(log_dir, 'app.log')
    app_handler = RotatingFileHandler(
        app_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    app_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    app_handler.setLevel(logging.INFO)
    
    # Error log with more details
    error_log_file = os.path.join(log_dir, 'error.log')
    error_handler = RotatingFileHandler(
        error_log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    error_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s'
    ))
    error_handler.setLevel(logging.ERROR)
    
    # Set overall log level
    app.logger.setLevel(logging.INFO)
    
    # Add handlers
    app.logger.addHandler(app_handler)
    app.logger.addHandler(error_handler)
    
    # Also add handlers to the root logger for other modules
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to avoid duplicates
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)
    
    # Add a stream handler for console output
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    ))
    console_handler.setLevel(logging.INFO)
    root_logger.addHandler(console_handler)
    
    # Add file handlers
    root_logger.addHandler(app_handler)
    root_logger.addHandler(error_handler)
    
    # Log application startup
    app.logger.info('Executive Orders Archive startup')

def get_data_fetch_logger():
    """
    Get a logger configured for data fetching scripts.
    
    Returns:
        logging.Logger: Configured logger instance
    """
    # Create logs directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)
    
    # Create logger
    logger = logging.getLogger('data_fetch')
    logger.setLevel(logging.INFO)
    
    # Remove any existing handlers to avoid duplicates
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
    
    # Add a rotating file handler for data fetch logs
    log_file = os.path.join(LOG_DIR, 'data_fetch.log')
    file_handler = RotatingFileHandler(
        log_file,
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(file_handler)
    
    # Add a console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s'
    ))
    logger.addHandler(console_handler)
    
    return logger