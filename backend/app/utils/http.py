from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def error_response(status_code, message=None, error_type=None):
    """
    Create a standardized error response.
    
    Args:
        status_code (int): HTTP status code
        message (str, optional): Error message
        error_type (str, optional): Type of error
        
    Returns:
        tuple: JSON response and status code
    """
    payload = {'error': True, 'status_code': status_code}
    
    if message:
        payload['message'] = message
    
    if error_type:
        payload['error_type'] = error_type
    
    logger.error(f"HTTP Error {status_code}: {message}")
    return jsonify(payload), status_code

def success_response(data=None, message=None, status_code=200):
    """
    Create a standardized success response.
    
    Args:
        data (dict or list, optional): Response data
        message (str, optional): Success message
        status_code (int): HTTP status code (default: 200)
        
    Returns:
        tuple: JSON response and status code
    """
    payload = {'success': True}
    
    if data is not None:
        payload['data'] = data
    
    if message:
        payload['message'] = message
    
    return jsonify(payload), status_code

def paginated_response(items, page, per_page, total):
    """
    Create a standardized paginated response.
    
    Args:
        items (list): List of items for current page
        page (int): Current page number
        per_page (int): Number of items per page
        total (int): Total number of items
        
    Returns:
        tuple: JSON response and status code
    """
    total_pages = (total + per_page - 1) // per_page if total > 0 else 0
    
    payload = {
        'items': items,
        'pagination': {
            'page': page,
            'per_page': per_page,
            'total_items': total,
            'total_pages': total_pages,
            'has_next': page < total_pages,
            'has_prev': page > 1
        }
    }
    
    return jsonify(payload), 200

def bad_request(message="Bad request", error_type=None):
    """400 Bad Request response."""
    return error_response(400, message, error_type)

def unauthorized(message="Unauthorized", error_type=None):
    """401 Unauthorized response."""
    return error_response(401, message, error_type)

def forbidden(message="Forbidden", error_type=None):
    """403 Forbidden response."""
    return error_response(403, message, error_type)

def not_found(message="Resource not found", error_type=None):
    """404 Not Found response."""
    return error_response(404, message, error_type)

def server_error(message="Internal server error", error_type=None):
    """500 Internal Server Error response."""
    return error_response(500, message, error_type)