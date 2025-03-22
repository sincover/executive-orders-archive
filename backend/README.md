# Executive Orders Archive Backend

The backend service for the Executive Orders Archive project, built with Flask and PostgreSQL.

## Architecture

The backend follows a modular architecture:

```
backend/
├── app/                  # Application package
│   ├── __init__.py      # Application factory
│   ├── database.py      # Database setup
│   ├── models/          # Database models
│   │   └── executive_order.py  # Executive Order model
│   ├── routes/          # API routes
│   │   └── executive_orders.py # Executive Orders endpoints
│   ├── services/        # Business logic
│   │   ├── celery_app.py       # Celery configuration
│   │   ├── federal_register_client.py  # Federal Register API client
│   │   └── tasks/       # Celery tasks
│   │       └── eo_tasks.py     # Executive Order tasks
│   └── utils/           # Utility functions
│       ├── data_transformers.py  # Data transformation utilities
│       ├── http.py              # HTTP response utilities
│       └── logging.py           # Logging configuration
├── scripts/             # Utility scripts
│   └── fetch_data.py    # Initial data fetch script
├── tests/               # Test suite
│   ├── conftest.py      # Test fixtures
│   ├── test_api.py      # API tests
│   ├── test_models.py   # Model tests
│   └── test_transformers.py  # Transformer tests
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Example environment variables
├── app.py               # Application entry point
├── config.py            # Configuration settings
├── requirements.txt     # Python dependencies
└── README.md            # This file
```

## Setup

### Prerequisites

- Python 3.9+
- PostgreSQL 17+
- Redis (for Celery task queue)

### Installation

1. Create and activate virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

3. Configure environment:
   ```powershell
   cp .env.example .env
   # Edit .env with your settings
   ```

4. Create PostgreSQL database:
   ```sql
   CREATE DATABASE executive_orders_archive;
   CREATE USER eo_app_user WITH ENCRYPTED PASSWORD 'eo_app_password';
   GRANT ALL PRIVILEGES ON DATABASE executive_orders_archive TO eo_app_user;
   ```

5. Initialize database:
   ```powershell
   flask db init
   flask db migrate -m "Create executive_orders table"
   flask db upgrade
   ```

## Running the Application

1. Start the Flask development server:
   ```powershell
   flask run
   ```

2. Start Celery worker (optional, for background tasks):
   ```powershell
   celery -A app.services.celery_app.celery_app worker --loglevel=info
   ```

3. Start Celery beat (optional, for scheduled tasks):
   ```powershell
   celery -A app.services.celery_app.celery_app beat --loglevel=info
   ```

## Initial Data Load

To populate the database with executive orders from the Federal Register:

```powershell
python scripts/fetch_data.py --days-back 365
```

Options:
- `--days-back NUMBER`: Number of days to look back (default: 365)
- `--start-date YYYY-MM-DD`: Specific start date
- `--end-date YYYY-MM-DD`: Specific end date
- `--page-size NUMBER`: Results per page (default: 20)
- `--resume`: Resume from last saved state

## API Endpoints

### Get Executive Orders

```
GET /api/v1/executive-orders
```

Query Parameters:
- `president` (str): Filter by president name
- `year` (int): Filter by year of issuance
- `page` (int, default=1): Page number for pagination
- `per_page` (int, default=20): Items per page (max 100)
- `sort` (str, default='issuance_date'): Field to sort by (issuance_date, id, title, president)
- `order` (str, default='desc'): Sort order ('asc' or 'desc')

### Get Single Executive Order

```
GET /api/v1/executive-orders/{eo_id}
```

### Get Latest Executive Orders

```
GET /api/v1/latest-executive-orders
```

Query Parameters:
- `limit` (int, default=10): Number of orders to return (max 100)

## Testing

Run tests with pytest:
```powershell
pytest
```

For test coverage:
```powershell
pytest --cov=app tests/
```

## Development

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.