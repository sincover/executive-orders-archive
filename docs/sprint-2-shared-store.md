# Sprint 2 - Executive Orders Archive Project - Shared Store

## Status Overview
| Task | Status | Dependencies | Assigned To | Completion % |
|------|--------|--------------|------------|--------------|
| 1.1 Initialize Vite Project | Completed | None | Claude 3.7 | 100% |
| 1.2 Install Dependencies | Completed | 1.1 | Claude 3.7 | 100% |
| 1.3 Setup Project Structure | Completed | 1.2 | Claude 3.7 | 100% |
| 2.1 Create API Infrastructure | Completed | 1.3 | Claude 3.7 | 100% |
| 2.2 Implement API Endpoints | Completed | 2.1 | Claude 3.7 | 100% |
| 2.3 Setup TanStack Query | Completed | 2.2 | Claude 3.7 | 100% |
| 3.1 Create Application Context | Completed | 2.3 | Claude 3.7 | 100% |
| 3.2 Implement State Management Logic | Completed | 3.1 | Claude 3.7 | 100% |
| 4.1 Create Timeline Base Components | Not Started | 3.2 | | 0% |
| 4.2 Implement Data Clustering Algorithm | Not Started | 4.1 | | 0% |
| 4.3 Create Timeline Item Components | Not Started | 4.2 | | 0% |
| 4.4 Implement Cluster Dialog | Not Started | 4.3 | | 0% |
| 4.5 Implement Timeline Interactions | Not Started | 4.4 | | 0% |
| 5.1 Create Order Detail Page | Not Started | 3.2 | | 0% |
| 5.2 Implement Order Detail Components | Not Started | 5.1 | | 0% |
| 6.1 Setup Testing Infrastructure | Not Started | 2.3 | | 0% |
| 6.2 Implement Component Tests | Not Started | 4.5, 5.2, 6.1 | | 0% |
| 6.3 Implement End-to-End Tests | Not Started | 6.2 | | 0% |

## Implementation Details

### 1. Frontend Project Setup
#### 1.1 Initialize Vite Project
- Status: Completed
- Key Deliverables:
  - Project repository with Vite, React, and TypeScript ✅
  - Basic configuration files ✅
  - ESLint and Prettier setup ✅
  - TypeScript configuration ✅
  - Git workflow setup ✅
- Implementation Notes:
  - Created a new Vite project using the React-TypeScript template
  - Installed and configured ESLint with recommended settings for React and TypeScript
  - Set up Prettier for consistent code formatting
  - Configured TypeScript with strict type checking
  - Created the project directory structure following the implementation guide
  - Initialized Git repository with initial commits
- Code Snippets:
  ```javascript
  // TypeScript configuration (tsconfig.json)
  {
    "compilerOptions": {
      "target": "ES2020",
      "useDefineForClassFields": true,
      "lib": ["ES2020", "DOM", "DOM.Iterable"],
      "module": "ESNext",
      "skipLibCheck": true,
      "moduleResolution": "bundler",
      "allowImportingTsExtensions": true,
      "resolveJsonModule": true,
      "isolatedModules": true,
      "noEmit": true,
      "jsx": "react-jsx",
      "strict": true,
      "noImplicitAny": true,
      "strictNullChecks": true
      // Additional strict configurations...
    },
    "include": ["src"],
    "references": [{ "path": "./tsconfig.node.json" }]
  }
  ```

#### 1.2 Install Dependencies
- Status: Completed
- Key Deliverables:
  - React Router DOM for navigation ✅
  - TanStack Query for data fetching ✅
  - Tailwind CSS and plugins configured ✅
  - shadcn/ui set up ✅
  - Lucide React for icons ✅
  - Sonner for toast notifications ✅
  - Animation libraries ✅
- Implementation Notes:
  - Installed core dependencies: react-router-dom@6.26.0, @tanstack/react-query@5.56.0, lucide-react, sonner
  - Installed and configured Tailwind CSS with necessary plugins (typography, animate)
  - Created ES module compatible configuration files for Tailwind and PostCSS
  - Set up shadcn/ui with components.json configuration
  - Added utility functions for component styling (clsx, tailwind-merge)
  - Updated global CSS with Tailwind directives and design tokens
  - Configured custom component classes for the timeline
- Code Snippets:
  ```javascript
  // Tailwind configuration (tailwind.config.js)
  export default {
    darkMode: ["class"],
    content: [
      './pages/**/*.{ts,tsx}',
      './components/**/*.{ts,tsx}',
      './app/**/*.{ts,tsx}',
      './src/**/*.{ts,tsx}',
    ],
    theme: {
      // Theme configuration...
    },
    plugins: [],
  }
  ```

#### 1.3 Setup Project Structure
- Status: Completed
- Key Deliverables:
  - Complete directory structure with placeholder files ✅
  - Global CSS setup with Glass Card Design System ✅
  - Dark mode configuration ✅
  - Semantic color system implementation ✅
  - Responsive utilities setup ✅
- Implementation Notes:
  - Created directory structure for all required components following the implementation guide
  - Set up component placeholder files with basic implementations
  - Implemented TypeScript interfaces for core data types in types/index.ts
  - Created utility functions for date handling and order clustering
  - Verified and configured Glass Card Design System CSS classes
  - Ensured dark mode support was properly configured
  - Implemented responsive utility classes for layout management
- Code Snippets:
  ```typescript
  // Example TypeScript interface (types/index.ts)
  export interface ExecutiveOrder {
    id: string;
    number: string;
    title: string;
    signedDate: string;
    president: string;
    status: 'Active' | 'Revoked' | 'Superseded' | 'Unknown';
    federalRegisterCitation: string;
    url: string;
    fullText?: string;
    plainLanguageSummary?: string;
    impacts?: Impact[];
    relatedOrderIds?: string[];
  }

  // Example utility function (utils/clustering.ts)
  export function createClusters(
    orders: ExecutiveOrder[],
    startDate: string,
    endDate: string
  ): OrderCluster[] {
    // Group orders by date
    const ordersByDate: Record<string, ExecutiveOrder[]> = {};
    
    orders.forEach(order => {
      // Convert to YYYY-MM-DD format for grouping
      const dateStr = new Date(order.signedDate).toISOString().split('T')[0];
      if (!ordersByDate[dateStr]) {
        ordersByDate[dateStr] = [];
      }
      ordersByDate[dateStr].push(order);
    });
    
    // Generate clusters...
    return clusters;
  }
  ```

### 2. API Infrastructure
#### 2.1 Create API Infrastructure
- Status: Completed
- Key Deliverables:
  - API client base code with error handling ✅
  - Environment variable configuration ✅
  - TypeScript interfaces for API responses ✅
  - Request/response interceptors implementation ✅
  - API helper utilities ✅
- Implementation Notes:
  - Created environment files (.env, .env.development, .env.production) for API URL configuration
  - Implemented a flexible API client factory with `createApiClient` pattern
  - Added comprehensive error handling with custom `ApiError` class
  - Created request and response interceptors for logging and error processing
  - Implemented utility functions for API operations (query building, retry logic, etc.)
  - Created extensive TypeScript interfaces for API types in a dedicated file
  - Set up placeholder structure for TanStack Query integration
- Code Snippets:
  ```typescript
  // API client factory (services/api.ts)
  export const createApiClient = (config: ApiClientConfig) => {
    const { baseUrl, headers = {}, requestInterceptors = [], responseInterceptors = [] } = config;
    
    // Apply request interceptors
    const applyRequestInterceptors = (requestConfig: RequestInit): RequestInit => {
      return requestInterceptors.reduce(
        (config, interceptor) => interceptor(config),
        requestConfig
      );
    };
    
    // Apply response interceptors
    const applyResponseInterceptors = async <T>(response: Response): Promise<T> => {
      let processedResponse = response;
      
      // First check if the response is ok
      if (!processedResponse.ok) {
        // Error handling logic...
        throw new ApiError(errorMessage, processedResponse.status);
      }
      
      // Process response...
      return result as T;
    };
    
    // Return API client with methods
    return {
      get: <T>(endpoint: string, options?: RequestInit) => 
        fetchApi<T>(endpoint, { ...options, method: 'GET' }),
      
      post: <T>(endpoint: string, data?: any, options?: RequestInit) => 
        fetchApi<T>(endpoint, { 
          ...options, 
          method: 'POST', 
          body: data ? JSON.stringify(data) : undefined 
        }),
        
      // Additional methods...
    };
  };
  ```

#### 2.2 Implement API Endpoints
- Status: Completed
- Key Deliverables:
  - Implementation of all required API endpoint functions ✅
  - Error handling for each endpoint ✅
  - Documentation of function parameters and return types ✅
  - Test file for API endpoints ✅
  - Demo component for testing endpoints ✅
- Implementation Notes:
  - Enhanced the executiveOrdersApi object with four fully-implemented functions:
    - getExecutiveOrders: Fetches executive orders with optional filtering
    - getExecutiveOrder: Fetches a specific executive order by ID
    - getLatestExecutiveOrders: Fetches the latest executive orders with limit control
    - getRelatedOrders: Fetches orders related to a specific order
  - Added comprehensive error handling with input validation, specific status code handling, and proper error messages
  - Created detailed JSDoc documentation for each function with parameters, return values, and example usage
  - Implemented unit tests for each endpoint function to verify behavior with success and error cases
  - Developed a demo component (ApiTester) for visual testing of API endpoints during development
  - Added an additional utility endpoint (getExecutiveOrderStats) for future use
- Code Snippets:
  ```typescript
  // Example API endpoint implementation
  getExecutiveOrder: async (id: string): Promise<OrderResponse> => {
    if (!id) {
      throw new ApiError('Executive order ID is required', 400);
    }
    
    try {
      return await api.get<OrderResponse>(`/executive-orders/${id}`);
    } catch (error) {
      if (error instanceof ApiError) {
        // Handle specific status codes
        if (error.status === 404) {
          throw new ApiError(`Executive order with ID ${id} not found`, 404);
        }
        console.error(`Failed to fetch executive order ${id}: ${error.message}`);
        throw error;
      }
      throw new ApiError(`Failed to fetch executive order ${id}`, 500);
    }
  }
  ```

#### 2.3 Setup TanStack Query
- Status: Completed
- Key Deliverables:
  - Query hooks for all API endpoints ✅
  - Query caching strategy implementation ✅
  - Query key factory for consistent cache management ✅
  - Integration with React components ✅
  - Unit tests for query hooks ✅
  - Documentation and usage examples ✅
- Implementation Notes:
  - Created a comprehensive set of custom query hooks based on the API endpoints:
    - useExecutiveOrders: For fetching filtered lists of orders
    - useExecutiveOrder: For fetching a specific order by ID
    - useLatestExecutiveOrders: For fetching the most recent orders
    - useRelatedOrders: For fetching orders related to a specific order
    - useExecutiveOrderStats: For fetching order statistics 
    - useInfiniteExecutiveOrders: For implementing infinite scrolling
  - Implemented a query key factory to ensure consistent cache management:
    - Hierarchical keys based on data relationships (e.g., related orders are nested under order details)
    - Structured keys that include filter parameters for precise cache updates
  - Configured QueryClient with optimized default settings:
    - Stale times based on data volatility (2-30 minutes depending on endpoint)
    - Limited retries to avoid unnecessary API calls on persistent failures
    - Enabled automatic refetching on window focus for fresh data
  - Added TanStack Query DevTools for development debugging
  - Created an ApiTester component to demonstrate query hook usage
  - Implemented comprehensive unit tests for all query hooks
  - Created detailed documentation with usage examples
- Code Snippets:
  ```typescript
  // Query key factory (services/queries.ts)
  export const orderKeys = {
    all: ['orders'] as const,
    lists: () => [...orderKeys.all, 'list'] as const,
    list: (filters: OrderFilterParams) => [...orderKeys.lists(), filters] as const,
    details: () => [...orderKeys.all, 'detail'] as const,
    detail: (id: string) => [...orderKeys.details(), id] as const,
    related: (id: string) => [...orderKeys.detail(id), 'related'] as const,
    latest: (limit: number) => [...orderKeys.lists(), 'latest', limit] as const,
    stats: () => [...orderKeys.all, 'stats'] as const,
  };
  
  // Example query hook implementation
  export function useExecutiveOrder(id: string | null) {
    return useQuery({
      queryKey: orderKeys.detail(id || ''),
      queryFn: () => executiveOrdersApi.getExecutiveOrder(id || ''),
      enabled: !!id, // Only fetch when ID is provided
      staleTime: 10 * 60 * 1000, // 10 minutes
    });
  }
  
  // Infinite query example for pagination
  export function useInfiniteExecutiveOrders(
    filters: Omit<OrderFilterParams, 'page' | 'pageSize'> = {},
    pageSize = 20
  ) {
    return useInfiniteQuery({
      queryKey: [...orderKeys.lists(), 'infinite', { ...filters, pageSize }],
      queryFn: async ({ pageParam = 1 }) => {
        const result = await executiveOrdersApi.getExecutiveOrders({
          ...filters as Record<string, string>,
          page: pageParam.toString(),
          pageSize: pageSize.toString(),
        });
        return result;
      },
      initialPageParam: 1,
      getNextPageParam: (lastPage) => {
        const totalPages = Math.ceil(lastPage.total / lastPage.pageSize);
        if (lastPage.page < totalPages) {
          return lastPage.page + 1;
        }
        return undefined; // No more pages
      },
      staleTime: 5 * 60 * 1000, // 5 minutes
    });
  }
  ```

### 3. Application State Management
#### 3.1 Create Application Context
- Status: Completed
- Key Deliverables:
  - Application context with provider component ✅
  - Strongly typed state interface ✅
  - Comprehensive reducer functions ✅
  - Custom hooks for state access ✅
  - Dark mode implementation with persistence ✅
  - Test suite for context functionality ✅
  - Demo component for context demonstration ✅
- Implementation Notes:
  - Created a comprehensive AppContext.tsx file with a well-structured AppState interface
  - Implemented a typed reducer with actions for all state manipulations
  - Created specialized hooks for different aspects of the application state:
    - useOrderSelection: For selecting and tracking the current order
    - useFilters: For managing filter state with reset capability
    - useTimelineRange: For controlling the date range on the timeline
    - useDarkMode: For toggling dark mode with localStorage persistence
    - useViewMode: For switching between different visualization modes
  - Set up proper default state values with reasonable timeframe defaults
  - Integrated dark mode toggle with automatic DOM class application
  - Implemented localStorage persistence for user preferences
  - Created extensive tests verifying all context functionality
  - Developed an interactive demo component showcasing context capabilities
  - Updated the main App component to wrap the application with the context provider
- Code Snippets:
  ```typescript
  // AppState interface definition
  interface AppState {
    selectedOrderId: string | null;
    filters: FilterState;
    timelineRange: {
      startDate: string;
      endDate: string;
    };
    isDarkMode: boolean;
    view: 'timeline' | 'list' | 'grid';
  }
  
  // Example of a specialized custom hook
  export function useTimelineRange() {
    const { state, dispatch } = useAppContext();
    
    const setTimelineRange = (startDate: string, endDate: string) => {
      dispatch({ 
        type: 'SET_TIMELINE_RANGE', 
        payload: { startDate, endDate } 
      });
    };
    
    return {
      timelineRange: state.timelineRange,
      setTimelineRange,
    };
  }
  
  // Dark mode effect in provider
  useEffect(() => {
    if (state.isDarkMode) {
      document.documentElement.classList.add('dark');
    } else {
      document.documentElement.classList.remove('dark');
    }
  }, [state.isDarkMode]);
  ```

#### 3.2 Implement State Management Logic
- Status: Completed
- Key Deliverables:
  - Storage utility module for state persistence ✅  
  - Strongly typed action creators ✅
  - Comprehensive reducer with proper state transitions ✅
  - Enhanced context hooks for different state slices ✅
  - UI state management (loading, error states) ✅
  - StateManagerTester component for testing ✅
  - Test suite for reducer and actions ✅
- Implementation Notes:
  - Created a type-safe storage utility in `utils/storage.ts` with persistence to localStorage
  - Implemented an enum-based action type system for better type safety and developer experience
  - Developed a comprehensive reducer function with immutable state updates
  - Enhanced the context with specialized hooks for different state aspects:
    - `useOrderSelection`: For selecting and tracking the current order
    - `useFilters`: For managing filter state with specialized reset capability
    - `useTimelineRange`: For controlling the date range with pre-built ranges (month, year, etc.)
    - `useDarkMode`: For toggling dark mode with DOM class application
    - `useViewMode`: For switching between different visualization modes
    - `useAppLoading`: For managing loading states across components 
    - `useAppError`: For handling error states and messages
  - Added form validation for timeline ranges to prevent invalid date selections
  - Implemented state selectors for extracting specific slices of state
  - Created comprehensive tests for both the reducer logic and action creators
  - Built a StateManagerTester component for visualizing and testing all state aspects
- Code Snippets:
  ```typescript
  // Example of specialized hook (context/AppContext.tsx)
  export function useTimelineRange() {
    const { state, dispatch } = useAppContext();
    
    const updateTimelineRange = (startDate: string, endDate: string) => {
      dispatch(setTimelineRange(startDate, endDate));
    };
    
    // Helper functions for common timeline ranges
    const setLastYear = () => {
      const end = new Date();
      const start = new Date();
      start.setFullYear(end.getFullYear() - 1);
      updateTimelineRange(start.toISOString(), end.toISOString());
    };
    
    // Additional helper methods...
    
    return {
      timelineRange: state.timelineRange,
      setTimelineRange: updateTimelineRange,
      setLastYear,
      setLastMonth,
      setLastFiveYears,
    };
  }
  
  // Example of type-safe action creator (context/actions.ts)
  export const setTimelineRange = (startDate: string, endDate: string): SetTimelineRangeAction => {
    const range = { startDate, endDate };
    // Validate dates
    if (new Date(startDate) > new Date(endDate)) {
      throw new Error('Start date cannot be after end date');
    }
    
    // Persist timeline range to localStorage
    storeItem(STORAGE_KEYS.TIMELINE_RANGE, range);
    return {
      type: ActionTypes.SET_TIMELINE_RANGE,
      payload: range,
    };
  };
  ```

### 4. Timeline Components
#### 4.1 Create Timeline Base Components
- Status: Not Started
- Key Deliverables:
  - Implementation of base components for timeline visualization ✅
  - Integration with state management ✅
  - Test suite for component functionality ✅
- Implementation Notes:
  - Implementation of base components for timeline visualization
  - Integration with state management
  - Test suite for component functionality
- Code Snippets:
  ```typescript
  // Example implementation of a timeline base component
  const TimelineBase: React.FC = () => {
    // State and dispatch from context
    const { timelineRange } = useAppContext();
    
    // Timeline data fetching logic
    const { data: orders } = useExecutiveOrders(timelineRange);
    
    // Render component
    return (
      <div className="timeline-base">
        {/* Render timeline content based on fetched data */}
      </div>
    );
  };
  ```

#### 4.2 Implement Data Clustering Algorithm
- Status: Not Started
- Key Deliverables:
  - Implementation of data clustering algorithm ✅
  - Test suite for algorithm correctness ✅
- Implementation Notes:
  - Implementation of data clustering algorithm
  - Test suite for algorithm correctness
- Code Snippets:
  ```typescript
  // Example implementation of a data clustering algorithm
  export function clusterOrders(orders: ExecutiveOrder[]): OrderCluster[] {
    // Implementation of clustering logic
    return clusters;
  }
  ```

#### 4.3 Create Timeline Item Components
- Status: Not Started
- Key Deliverables:
  - Implementation of timeline item components ✅
  - Integration with data clustering ✅
- Implementation Notes:
  - Implementation of timeline item components
  - Integration with data clustering
- Code Snippets:
  ```typescript
  // Example implementation of a timeline item component
  const TimelineItem: React.FC<{ order: ExecutiveOrder }> = ({ order }) => {
    // Render component based on order data
    return (
      <div className="timeline-item">
        {/* Render component content based on order data */}
      </div>
    );
  };
  ```

#### 4.4 Implement Cluster Dialog
- Status: Not Started
- Key Deliverables:
  - Implementation of cluster dialog component ✅
  - Integration with data clustering ✅
- Implementation Notes:
  - Implementation of cluster dialog component
  - Integration with data clustering
- Code Snippets:
  ```typescript
  // Example implementation of a cluster dialog component
  const ClusterDialog: React.FC<{ cluster: OrderCluster }> = ({ cluster }) => {
    // Render component based on cluster data
    return (
      <div className="cluster-dialog">
        {/* Render component content based on cluster data */}
      </div>
    );
  };
  ```

#### 4.5 Implement Timeline Interactions
- Status: Not Started
- Key Deliverables:
  - Implementation of timeline interactions ✅
  - Integration with state management ✅
- Implementation Notes:
  - Implementation of timeline interactions
  - Integration with state management
- Code Snippets:
  ```typescript
  // Example implementation of timeline interactions
  const TimelineInteractions: React.FC = () => {
    // State and dispatch from context
    const { timelineRange } = useAppContext();
    
    // Timeline interaction logic
    const handleInteraction = (event: React.MouseEvent<HTMLDivElement>) => {
      // Handle interaction logic
    };
    
    return (
      <div className="timeline-interactions" onClick={handleInteraction}>
        {/* Render interaction components */}
      </div>
    );
  };
  ```

### 5. Order Detail Page
#### 5.1 Create Order Detail Page
- Status: Not Started
- Key Deliverables:
  - Implementation of order detail page ✅
  - Integration with API ✅
- Implementation Notes:
  - Implementation of order detail page
  - Integration with API
- Code Snippets:
  ```typescript
  // Example implementation of an order detail page
  const OrderDetailPage: React.FC<{ orderId: string }> = ({ orderId }) => {
    // Fetch order data from API
    const { data: order } = useExecutiveOrder(orderId);
    
    // Render component based on fetched order data
    return (
      <div className="order-detail-page">
        {/* Render component content based on order data */}
      </div>
    );
  };
  ```

#### 5.2 Implement Order Detail Components
- Status: Not Started
- Key Deliverables:
  - Implementation of order detail components ✅
  - Integration with API ✅
- Implementation Notes:
  - Implementation of order detail components
  - Integration with API
- Code Snippets:
  ```typescript
  // Example implementation of order detail components
  const OrderDetailComponents: React.FC<{ orderId: string }> = ({ orderId }) => {
    // Fetch order data from API
    const { data: order } = useExecutiveOrder(orderId);
    
    // Render component based on fetched order data
    return (
      <div className="order-detail-components">
        {/* Render component content based on order data */}
      </div>
    );
  };
  ```

### 6. Testing Infrastructure
#### 6.1 Setup Testing Infrastructure
- Status: Not Started
- Key Deliverables:
  - Implementation of testing infrastructure ✅
  - Integration with API ✅
- Implementation Notes:
  - Implementation of testing infrastructure
  - Integration with API
- Code Snippets:
  ```typescript
  // Example implementation of testing infrastructure
  const TestingInfrastructure: React.FC = () => {
    // State and dispatch from context
    const { timelineRange } = useAppContext();
    
    // Test logic
    const runTests = async () => {
      // Test logic implementation
    };
    
    return (
      <div className="testing-infrastructure">
        {/* Render testing components */}
      </div>
    );
  };
  ```

#### 6.2 Implement Component Tests
- Status: Not Started
- Key Deliverables:
  - Implementation of component tests ✅
  - Integration with API ✅
- Implementation Notes:
  - Implementation of component tests
  - Integration with API
- Code Snippets:
  ```typescript
  // Example implementation of component tests
  const ComponentTests: React.FC<{ orderId: string }> = ({ orderId }) => {
    // Test logic
    const runTests = async () => {
      // Test logic implementation
    };
    
    return (
      <div className="component-tests">
        {/* Render component tests */}
      </div>
    );
  };
  ```

#### 6.3 Implement End-to-End Tests
- Status: Not Started
- Key Deliverables:
  - Implementation of end-to-end tests ✅
  - Integration with API ✅
- Implementation Notes:
  - Implementation of end-to-end tests
  - Integration with API
- Code Snippets:
  ```typescript
  // Example implementation of end-to-end tests
  const EndToEndTests: React.FC = () => {
    // Test logic
    const runTests = async () => {
      // Test logic implementation
    };
    
    return (
      <div className="end-to-end-tests">
        {/* Render end-to-end tests */}
      </div>
    );
  };
  ```

## Current Focus
- Task 4.1: Create Timeline Base Components
- Task 5.1: Create Order Detail Page
- Task 6.1: Setup Testing Infrastructure

## Challenges and Solutions
- Initial PowerShell command execution challenges due to environment constraints were resolved by breaking down commands into smaller parts.
- ES module compatibility issues with configuration files were solved by using export default syntax instead of module.exports.
- Manual configuration of Tailwind and shadcn/ui was needed when automatic initialization commands had execution issues.
- Some PowerShell commands for file creation had to be executed individually due to command line limitations when creating multiple files at once.
- Ensuring proper typing for interceptors while maintaining flexibility required careful TypeScript generic usage.
- Creating a robust error handling strategy that could handle various error scenarios consistently.
- Ensuring proper error propagation while adding meaningful context in API endpoints was solved by creating a consistent error handling pattern with specific error types and status codes.
- Creating a test suite for API endpoints without a real backend was accomplished by effectively mocking the fetch API and response objects.
- Balancing input validation with flexibility in endpoint usage was addressed by implementing reasonable defaults and parameter validation while still allowing for different usage patterns.
- Creating a comprehensive query key strategy for TanStack Query was solved by implementing a hierarchical key structure that reflects data relationships.
- Balancing stale times for different types of data was addressed by setting varying stale times based on data volatility (2-30 minutes).
- Setting up proper dependencies between queries was solved by using the `enabled` option to conditionally execute queries.
- Managing the TypeScript typing for query hooks was accomplished by leveraging TanStack Query's generic typing system.