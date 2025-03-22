from app import create_app
from app.database import db, init_db

# Create the Flask application
app = create_app()

# Initialize the database
with app.app_context():
    init_db(app)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
