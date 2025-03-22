from flask import jsonify
import logging

logger = logging.getLogger(__name__)

def error_response(status_code, message=None, error_type=None):
    """Create a standardized error response."""
    payload = {'error': True, 'status_code': status_code}
    
    if message:
        payload['message'] = message
    
    if error_type:
        payload['error_type'] = error_type
    
    logger.error(f"HTTP Error {status_code}: {message}")
    return jsonify(payload), status_code

def success_response(data=None, message=None, status_code=200):
    """Create a standardized success response."""
    payload = {'success': True}
    
    if data is not None:
        payload['data'] = data
    
    if message:
        payload['message'] = message
    
    return jsonify(payload), status_code

def paginated_response(items, page, per_page, total):
    """Create a standardized paginated response."""
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

def bad_request(message):
    """Return a 400 Bad Request error."""
    return error_response(400, message, "BadRequest")

def not_found(message="Resource not found"):
    """Return a 404 Not Found error."""
    return error_response(404, message, "NotFound")

def server_error(message="An unexpected error occurred"):
    """Return a 500 Internal Server Error."""
    return error_response(500, message, "ServerError")