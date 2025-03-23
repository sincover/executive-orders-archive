import { ExecutiveOrder, OrdersResponse, OrderResponse } from '../types';

// Base API URL from environment variable
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:5000/api/v1';

// Error class for API errors
export class ApiError extends Error {
  status: number;
  
  constructor(message: string, status: number) {
    super(message);
    this.status = status;
    this.name = 'ApiError';
  }
}

// Request interceptor function type
type RequestInterceptor = (config: RequestInit) => RequestInit;

// Response interceptor function type
type ResponseInterceptor<T> = (response: Response) => Promise<T>;

// API client configuration
interface ApiClientConfig {
  baseUrl: string;
  headers?: Record<string, string>;
  requestInterceptors?: RequestInterceptor[];
  responseInterceptors?: ResponseInterceptor<any>[];
}

// Create API client factory
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
      // Try to get error message from response
      let errorMessage: string;
      try {
        const errorData = await processedResponse.json();
        errorMessage = errorData.message || errorData.error || `API error: ${processedResponse.status}`;
      } catch {
        errorMessage = `API error: ${processedResponse.status} ${processedResponse.statusText}`;
      }
      
      throw new ApiError(errorMessage, processedResponse.status);
    }
    
    // Parse JSON response
    const data = await processedResponse.json();
    
    // Apply response interceptors
    let result = data;
    for (const interceptor of responseInterceptors) {
      result = await interceptor(result);
    }
    
    return result as T;
  };
  
  // Core fetch function
  const fetchApi = async <T>(
    endpoint: string, 
    options: RequestInit = {}
  ): Promise<T> => {
    try {
      // Prepare request config
      const requestConfig: RequestInit = {
        ...options,
        headers: {
          'Content-Type': 'application/json',
          ...headers,
          ...options.headers,
        },
      };
      
      // Apply request interceptors
      const processedConfig = applyRequestInterceptors(requestConfig);
      
      // Execute request
      const response = await fetch(`${baseUrl}${endpoint}`, processedConfig);
      
      // Apply response interceptors and return data
      return await applyResponseInterceptors<T>(response);
    } catch (error) {
      // Handle fetch errors (network issues, etc.)
      if (!(error instanceof ApiError)) {
        console.error('API request failed:', error);
        throw new ApiError('Network error or unable to reach API', 0);
      }
      throw error;
    }
  };
  
  // Return API client methods
  return {
    get: <T>(endpoint: string, options?: RequestInit) => 
      fetchApi<T>(endpoint, { ...options, method: 'GET' }),
    
    post: <T>(endpoint: string, data?: any, options?: RequestInit) => 
      fetchApi<T>(endpoint, { 
        ...options, 
        method: 'POST', 
        body: data ? JSON.stringify(data) : undefined 
      }),
    
    put: <T>(endpoint: string, data?: any, options?: RequestInit) => 
      fetchApi<T>(endpoint, { 
        ...options, 
        method: 'PUT', 
        body: data ? JSON.stringify(data) : undefined 
      }),
    
    patch: <T>(endpoint: string, data?: any, options?: RequestInit) => 
      fetchApi<T>(endpoint, { 
        ...options, 
        method: 'PATCH', 
        body: data ? JSON.stringify(data) : undefined 
      }),
    
    delete: <T>(endpoint: string, options?: RequestInit) => 
      fetchApi<T>(endpoint, { ...options, method: 'DELETE' }),
      
    // Add interceptors dynamically
    addRequestInterceptor: (interceptor: RequestInterceptor) => {
      requestInterceptors.push(interceptor);
    },
    
    addResponseInterceptor: <T>(interceptor: ResponseInterceptor<T>) => {
      responseInterceptors.push(interceptor as ResponseInterceptor<any>);
    }
  };
};

// Create default API client
export const api = createApiClient({
  baseUrl: API_BASE_URL,
  headers: {
    'Accept': 'application/json',
  },
  // Add request logging in development
  requestInterceptors: [
    (config) => {
      if (import.meta.env.DEV) {
        console.log('API Request:', config);
      }
      return config;
    }
  ],
  // Add response logging in development
  responseInterceptors: [
    (response) => {
      if (import.meta.env.DEV) {
        console.log('API Response:', response);
      }
      return response;
    }
  ]
});

// Executive Order API endpoints
export const executiveOrdersApi = {
  /**
   * Fetches executive orders with optional filtering, sorting, and pagination
   * @param filters - Optional filter parameters (president, dates, status, search query, etc.)
   * @returns Promise containing OrdersResponse with orders and pagination metadata
   * @throws ApiError if the request fails
   * 
   * @example
   * // Fetch all executive orders
   * executiveOrdersApi.getExecutiveOrders()
   *   .then(data => console.log(data))
   *   .catch(error => console.error(error));
   * 
   * @example
   * // Fetch with filters
   * executiveOrdersApi.getExecutiveOrders({
   *   president: 'Biden',
   *   startDate: '2021-01-20',
   *   status: 'Active',
   *   page: 1,
   *   pageSize: 20
   * })
   */
  getExecutiveOrders: async (filters?: Record<string, string>): Promise<OrdersResponse> => {
    try {
      const queryParams = filters 
        ? `?${new URLSearchParams(filters).toString()}`
        : '';
        
      return await api.get<OrdersResponse>(`/executive-orders${queryParams}`);
    } catch (error) {
      if (error instanceof ApiError) {
        console.error(`Failed to fetch executive orders: ${error.message}`);
        throw error;
      }
      throw new ApiError('Failed to fetch executive orders', 500);
    }
  },
  
  /**
   * Fetches a specific executive order by ID
   * @param id - The unique identifier of the executive order
   * @returns Promise containing OrderResponse with the requested order
   * @throws ApiError if the request fails or the order doesn't exist
   * 
   * @example
   * // Fetch a specific order
   * executiveOrdersApi.getExecutiveOrder('12345')
   *   .then(data => console.log(data.order))
   *   .catch(error => console.error(error));
   */
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
  },
  
  /**
   * Fetches the latest executive orders, optionally limited by count
   * @param limit - Optional maximum number of orders to return (default: 10)
   * @returns Promise containing OrdersResponse with the latest orders
   * @throws ApiError if the request fails
   * 
   * @example
   * // Fetch the 5 latest orders
   * executiveOrdersApi.getLatestExecutiveOrders(5)
   *   .then(data => console.log(data.orders))
   *   .catch(error => console.error(error));
   */
  getLatestExecutiveOrders: async (limit: number = 10): Promise<OrdersResponse> => {
    try {
      return await api.get<OrdersResponse>(`/latest-executive-orders?limit=${limit}`);
    } catch (error) {
      if (error instanceof ApiError) {
        console.error(`Failed to fetch latest executive orders: ${error.message}`);
        throw error;
      }
      throw new ApiError('Failed to fetch latest executive orders', 500);
    }
  },
  
  /**
   * Fetches executive orders related to a specific order
   * @param id - The ID of the reference executive order
   * @returns Promise containing OrdersResponse with related orders
   * @throws ApiError if the request fails
   * 
   * @example
   * // Fetch orders related to order 12345
   * executiveOrdersApi.getRelatedOrders('12345')
   *   .then(data => console.log(data.orders))
   *   .catch(error => console.error(error));
   */
  getRelatedOrders: async (id: string): Promise<OrdersResponse> => {
    if (!id) {
      throw new ApiError('Executive order ID is required', 400);
    }
    
    try {
      return await api.get<OrdersResponse>(`/executive-orders/${id}/related`);
    } catch (error) {
      if (error instanceof ApiError) {
        console.error(`Failed to fetch related orders for ${id}: ${error.message}`);
        throw error;
      }
      throw new ApiError(`Failed to fetch related orders for ${id}`, 500);
    }
  },
  
  /**
   * Fetches executive order statistics
   * @returns Promise containing statistics data
   * @throws ApiError if the request fails
   * 
   * @example
   * // Fetch order statistics
   * executiveOrdersApi.getExecutiveOrderStats()
   *   .then(data => console.log(data))
   *   .catch(error => console.error(error));
   */
  getExecutiveOrderStats: async () => {
    try {
      return await api.get('/executive-orders/stats');
    } catch (error) {
      if (error instanceof ApiError) {
        console.error(`Failed to fetch executive order stats: ${error.message}`);
        throw error;
      }
      throw new ApiError('Failed to fetch executive order stats', 500);
    }
  }
};