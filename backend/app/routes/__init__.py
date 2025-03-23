from flask import Blueprint

# Create API blueprint
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Import routes
from app.routes.executive_orders import bp as executive_orders_bp

# Register blueprints
api_bp.register_blueprint(executive_orders_bp)
