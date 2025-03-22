from app.routes.executive_orders import bp as executive_orders_bp

def register_routes(app):
    """Register all route blueprints with the Flask app."""
    app.register_blueprint(executive_orders_bp, url_prefix='/api/v1')