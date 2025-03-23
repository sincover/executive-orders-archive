# Executive Orders Archive Frontend

The frontend application for the Executive Orders Archive project.

## Current Status

The frontend is a React-based single-page application featuring:

- ✅ API client infrastructure with error handling
- ✅ TanStack Query integration
- ✅ TypeScript type definitions
- 🔄 Interactive timeline visualization
- 🔄 Executive Order details view
- 🔄 Search and filter functionality
- 🔄 Modern, responsive design

## Architecture

```
frontend/
├── src/
│   ├── components/    # React components
│   ├── pages/         # Page components
│   ├── services/      # API services and queries
│   │   ├── api.ts     # API client infrastructure
│   │   ├── queries.ts # TanStack Query hooks
│   │   └── api-helpers.ts # Helper utilities for API
│   ├── types/         # TypeScript definitions
│   ├── utils/         # Utility functions
│   ├── context/       # React context providers
│   └── assets/        # Static assets
├── public/            # Public assets
├── tests/             # Test suite
├── package.json       # Dependencies
└── README.md          # This file
```

## Development

### Prerequisites

- Node.js 18+ and npm

### Setup

1. Install dependencies:
   ```bash
   npm install
   ```

2. Start the development server:
   ```bash
   npm run dev
   ```

3. Run tests:
   ```bash
   npm test
   ```

## Features

### API Client

The API client provides a robust interface to communicate with the backend:

- Error handling and typed responses
- Request and response interceptors
- Configurable base URL based on environment
- TypeScript integration for type safety

### TanStack Query Integration

The application uses TanStack Query for data fetching and state management:

- Query hooks for all API endpoints:
  - `useExecutiveOrders`: Fetch orders with filtering
  - `useExecutiveOrder`: Fetch a specific order by ID
  - `useLatestExecutiveOrders`: Fetch the most recent orders
  - `useRelatedOrders`: Fetch orders related to a specific one
  - `useExecutiveOrderStats`: Fetch statistics
  - `useInfiniteExecutiveOrders`: Infinite scrolling for orders list

- Query key factory for consistent cache management:
  ```typescript
  export const orderKeys = {
    all: ['orders'],
    lists: () => [...orderKeys.all, 'list'],
    list: (filters) => [...orderKeys.lists(), filters],
    // ...more keys
  };
  ```

- Optimized caching strategies:
  - Latest orders: 2 minutes stale time
  - Filtered lists: 5 minutes stale time
  - Order details: 10 minutes stale time
  - Statistics: 30 minutes stale time

### Type System

The application uses TypeScript for type safety:

- `ExecutiveOrder`: The core data model
- `OrdersResponse`: Response containing a list of orders
- `OrderResponse`: Response containing a single order
- `FilterState`: Parameters for filtering orders
- `OrderStats`: Statistics about executive orders

## Contribution

Follow the main project [contribution guidelines](../CONTRIBUTING.md) when developing for the frontend.