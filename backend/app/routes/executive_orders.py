from flask import Blueprint, request, jsonify, current_app
from app.models.executive_order import ExecutiveOrder
from app.utils.http import not_found, bad_request, server_error, paginated_response, success_response
from sqlalchemy import desc, extract
import logging

# Create Blueprint
bp = Blueprint('executive_orders', __name__)
logger = logging.getLogger(__name__)

@bp.route('/executive-orders', methods=['GET'])
def get_executive_orders():
    """Get a list of executive orders with filtering options."""
    try:
        # Parse query parameters
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 20, type=int)
        president = request.args.get('president')
        year = request.args.get('year', type=int)
        sort_field = request.args.get('sort', 'issuance_date')
        sort_order = request.args.get('order', 'desc')
        
        # Validate pagination parameters
        if page < 1:
            page = 1
        if per_page < 1 or per_page > 100:
            per_page = 20
        
        # Build query
        query = ExecutiveOrder.query
        
        # Apply filters
        if president:
            query = query.filter(ExecutiveOrder.president == president)
        
        if year:
            query = query.filter(extract('year', ExecutiveOrder.issuance_date) == year)
        
        # Validate sort field
        valid_sort_fields = ['issuance_date', 'id', 'title', 'president']
        if sort_field not in valid_sort_fields:
            return bad_request(f"Invalid sort field. Valid options are: {', '.join(valid_sort_fields)}")
        
        # Apply sorting
        if sort_order.lower() == 'asc':
            query = query.order_by(getattr(ExecutiveOrder, sort_field))
        else:
            query = query.order_by(desc(getattr(ExecutiveOrder, sort_field)))
        
        # Execute query with pagination
        total = query.count()
        items = query.limit(per_page).offset((page - 1) * per_page).all()
        
        # Format results
        results = [eo.to_dict() for eo in items]
        
        # Return paginated response
        return paginated_response(results, page, per_page, total)
    
    except Exception as e:
        logger.error(f"Error retrieving executive orders: {str(e)}")
        return server_error(f"An error occurred while retrieving executive orders: {str(e)}")

@bp.route('/executive-orders/<string:eo_id>', methods=['GET'])
def get_executive_order(eo_id):
    """Get a single executive order by ID."""
    try:
        executive_order = ExecutiveOrder.query.get(eo_id)
        
        if not executive_order:
            return not_found(f"Executive order with ID '{eo_id}' not found")
        
        return success_response(data=executive_order.to_dict())
    
    except Exception as e:
        logger.error(f"Error retrieving executive order {eo_id}: {str(e)}")
        return server_error(f"An error occurred while retrieving the executive order: {str(e)}")

@bp.route('/latest-executive-orders', methods=['GET'])
def get_latest_executive_orders():
    """Get the latest executive orders."""
    try:
        limit = request.args.get('limit', 10, type=int)
        
        if limit < 1 or limit > 100:
            limit = 10
        
        latest_orders = ExecutiveOrder.query \
            .order_by(desc(ExecutiveOrder.issuance_date)) \
            .limit(limit) \
            .all()
        
        results = [eo.to_dict() for eo in latest_orders]
        
        return success_response(data=results)
    
    except Exception as e:
        logger.error(f"Error retrieving latest executive orders: {str(e)}")
        return server_error(f"An error occurred while retrieving the latest executive orders: {str(e)}")