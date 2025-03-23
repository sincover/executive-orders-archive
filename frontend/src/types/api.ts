/**
 * API related types for the Executive Orders Archive
 */

import { OrderStatus } from './executive-orders';

// Parameters for filtering executive orders
export interface OrderFilterParams {
  president?: string;
  status?: OrderStatus;
  startDate?: string;
  endDate?: string;
  policyArea?: string;
  search?: string;
  sortBy?: 'date' | 'number' | 'title';
  sortDirection?: 'asc' | 'desc';
  page?: string;
  pageSize?: string;
}

// API Response structure with pagination
export interface PaginatedResponse<T> {
  data: T[];
  total: number;
  page: number;
  pageSize: number;
  totalPages: number;
}

// Error response from API
export interface ApiErrorResponse {
  error: string;
  message: string;
  status: number;
  timestamp?: string;
  path?: string;
}
