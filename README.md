# Executive Orders Archive

An interactive web application for browsing and analyzing U.S. Presidential Executive Orders.

## Project Overview

The Executive Orders Archive provides a comprehensive platform for accessing, analyzing, and understanding U.S. Presidential Executive Orders. The application features an interactive timeline visualization and detailed information about each executive order.

### Key Features

- Interactive timeline visualization of Executive Orders
- Detailed information about each Executive Order
- Search and filter capabilities
- Integration with Federal Register data
- Regular updates for new Executive Orders

## Project Structure

```
executive-orders-archive/
├── backend/           # Flask backend application
│   ├── app/          # Application code
│   ├── tests/        # Test suite
│   └── README.md     # Backend documentation
├── frontend/         # React frontend application (coming in Sprint 2)
│   └── README.md     # Frontend documentation
├── docs/            # Project documentation
├── .gitignore       # Git ignore rules
├── LICENSE          # MIT license
└── README.md        # This file
```

## Setup Instructions

### Prerequisites

- Python 3.10+
- PostgreSQL 14+
- Node.js 18+ (for frontend, coming in Sprint 2)
- Redis (for task queue)

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv venv
   .\venv\Scripts\Activate.ps1
   ```

3. Install dependencies:
   ```powershell
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your configuration

5. Initialize the database:
   ```powershell
   flask db upgrade
   ```

6. Run the development server:
   ```powershell
   flask run
   ```

### Frontend Setup

Frontend setup instructions will be added in Sprint 2.

## Development

### Branching Strategy

We follow a modified Git Flow branching strategy:

- `main`: Production-ready code
- `develop`: Integration branch for features
- `feature/*`: Feature branches
- `bugfix/*`: Bug fix branches
- `release/*`: Release preparation branches

### Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed contribution guidelines.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.