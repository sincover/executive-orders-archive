# Executive Orders Archive Backend

The backend service for the Executive Orders Archive project, built with Flask and PostgreSQL.

## Architecture

The backend follows a modular architecture:

```
backend/
├── app/                # Application package
│   ├── __init__.py    # Application factory
│   ├── models/        # Database models
│   ├── routes/        # API routes
│   ├── services/      # Business logic
│   └── utils/         # Utility functions
├── tests/             # Test suite
├── migrations/        # Database migrations
├── requirements.txt   # Python dependencies
└── README.md         # This file
```

## Setup

1. Create and activate virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
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

4. Initialize database:
   ```powershell
   flask db upgrade
   ```

5. Run development server:
   ```powershell
   flask run
   ```

## API Documentation

API documentation will be available at `/api/docs` when the server is running.

## Testing

Run tests with pytest:
```powershell
pytest
```

## Development

See the main [CONTRIBUTING.md](../CONTRIBUTING.md) for development guidelines.