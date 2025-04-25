"""
Utility modules for the application.

This package contains various utility functions and modules used throughout the application:

- http: HTTP response utilities for API endpoints
- db_utils: Database utility functions
- exceptions: Custom exception classes
- transformers: Data transformation utilities
- logging: Logging configuration
"""

# Import common utilities for easier access
from app.utils.exceptions import (ResourceNotFound, BadRequestError, 
                                 ApiError, DatabaseError)
