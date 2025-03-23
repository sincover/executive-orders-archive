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

## Project Status

### Sprint 1 Completed
- ✅ Environment setup
- ✅ Backend setup
- ✅ Database setup
- ✅ Federal Register API integration
- ✅ Backend API endpoints
- ✅ Data fetching functionality
- ✅ Backend tests

### Sprint 2 In Progress
- ✅ Frontend project setup
- ✅ API client infrastructure
- ✅ TanStack Query integration
- 🔄 User interface components
- 🔄 Interactive visualizations
- 🔄 Authentication system
- 🔄 Advanced search capabilities

## Project Structure

```
executive-orders-archive/
├── backend/           # Flask backend application
│   ├── app/          # Application code
│   │   ├── models/   # Database models
│   │   ├── routes/   # API routes
│   │   ├── services/ # Business logic
│   │   └── utils/    # Utility functions
│   ├── tests/        # Test suite
│   └── README.md     # Backend documentation
├── frontend/         # React frontend application
│   ├── src/          # Source code
│   │   ├── components/ # React components
│   │   ├── pages/      # Page components
│   │   ├── services/   # API services and queries
│   │   ├── types/      # TypeScript definitions
│   │   └── utils/      # Utility functions
│   ├── public/       # Static assets
│   └── README.md     # Frontend documentation
├── docs/            # Project documentation
├── .gitignore       # Git ignore rules
├── LICENSE          # MIT license
└── README.md        # This file
```

## Setup Instructions

### Prerequisites

- Python 3.9+
- PostgreSQL 17+
- Redis (for task queue)
- Node.js 18+ (for frontend)

### Backend Setup

1. Navigate to the backend directory:
   ```powershell
   cd backend
   ```

2. Create and activate a virtual environment:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
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
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. Run the development server:
   ```powershell
   flask run
   ```

7. Optional: Run data fetch script to populate the database:
   ```powershell
   python scripts/fetch_data.py --days-back 365
   ```

### Frontend Setup

1. Navigate to the frontend directory:
   ```powershell
   cd frontend
   ```

2. Install dependencies:
   ```powershell
   npm install
   ```

3. Configure environment variables:
   - Copy `.env.example` to `.env.local`
   - Update the values if needed (defaults should work with local backend)

4. Run the development server:
   ```powershell
   npm run dev
   ```

## API Endpoints

The backend provides the following API endpoints:

- `GET /api/v1/executive-orders`: Get a list of executive orders with filtering, sorting, and pagination
- `GET /api/v1/executive-orders/{eo_id}`: Get a single executive order by ID
- `GET /api/v1/latest-executive-orders`: Get the latest executive orders
- `GET /api/v1/executive-orders/stats`: Get statistics about executive orders
- `GET /api/v1/executive-orders/{eo_id}/related`: Get orders related to a specific executive order

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