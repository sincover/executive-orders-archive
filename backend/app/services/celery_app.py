from celery import Celery
import os
from flask import Flask

def make_celery(app=None):
    """
    Create and configure a Celery application instance.
    
    Args:
        app (Flask, optional): Flask application instance. If None, config is loaded from environment.
        
    Returns:
        Celery: Configured Celery application
    """
    # Get Redis URL from environment or use default
    redis_url = os.environ.get('CELERY_BROKER_URL', 'redis://localhost:6379/0')
    
    celery = Celery(
        'executive_orders',
        broker=redis_url,
        backend=redis_url,
        include=['app.services.tasks.eo_tasks']
    )
    
    # Set default configuration
    celery.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    
    # Configure from Flask app if provided
    if app and isinstance(app, Flask):
        # Update with Flask app's config
        celery.conf.update(app.config)
        
        # Add Flask app context to tasks
        TaskBase = celery.Task
        
        class ContextTask(TaskBase):
            abstract = True
            
            def __call__(self, *args, **kwargs):
                with app.app_context():
                    return TaskBase.__call__(self, *args, **kwargs)
                    
        celery.Task = ContextTask
    
    return celery

celery_app = make_celery()

# Scheduled tasks configuration
celery_app.conf.beat_schedule = {
    'update-executive-orders-daily': {
        'task': 'app.services.tasks.eo_tasks.update_executive_orders',
        'schedule': 86400.0,  # Run once every 24 hours (in seconds)
        'options': {'expires': 3600}  # Task expires after 1 hour if not executed
    },
}