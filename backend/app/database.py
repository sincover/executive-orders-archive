from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

# Create database instance
db = SQLAlchemy()
migrate = Migrate()

def init_db(app):
    """Initialize database with the Flask app."""
    db.init_app(app)
    migrate.init_app(app, db)