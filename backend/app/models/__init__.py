from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import logging

logger = logging.getLogger(__name__)

# Initialize SQLAlchemy components
engine = None
db_session = None
Base = declarative_base()

# Import models to expose them at the package level
from app.models.executive_order import ExecutiveOrder

def init_db(app):
    """
    Initialize the database connection.
    
    Args:
        app: Flask application instance
        
    Returns:
        SQLAlchemy session
    """
    global engine, db_session
    
    if engine is None:
        logger.info(f"Initializing database connection: {app.config['SQLALCHEMY_DATABASE_URI']}")
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'])
        db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))
        Base.query = db_session.query_property()
        
        # Register teardown function
        @app.teardown_appcontext
        def shutdown_session(exception=None):
            if db_session:
                db_session.remove()
    
    return db_session