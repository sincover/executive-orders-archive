import { useQuery, useInfiniteQuery } from '@tanstack/react-query';
import { executiveOrdersApi, ApiError } from './api';
import { ExecutiveOrder, OrdersResponse, OrderResponse, FilterState } from '../types';
import { OrderFilterParams } from '../types/api';

/**
 * Query key factory for executive orders queries
 * This helps maintain consistent cache keys across the application
 */
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

/**
 * Hook to fetch executive orders with optional filtering
 * @param filters - Optional query parameters to filter the orders
 * @returns Query result object with data, loading state, and error
 * 
 * @example
 * const { data, isLoading, error } = useExecutiveOrders({ 
 *   president: 'Biden', 
 *   status: 'Active' 
 * });
 */
export function useExecutiveOrders(filters: FilterState = {}) {
  return useQuery({
    queryKey: orderKeys.list(filters as OrderFilterParams),
    queryFn: () => executiveOrdersApi.getExecutiveOrders(filters as Record<string, string>),
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}

/**
 * Hook to fetch a specific executive order by ID
 * @param id - The ID of the executive order to fetch
 * @returns Query result object with data, loading state, and error
 * 
 * @example
 * const { data, isLoading, error } = useExecutiveOrder('123');
 */
export function useExecutiveOrder(id: string | null) {
  return useQuery({
    queryKey: orderKeys.detail(id || ''),
    queryFn: () => executiveOrdersApi.getExecutiveOrder(id || ''),
    enabled: !!id, // Only fetch when ID is provided
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

/**
 * Hook to fetch latest executive orders
 * @param limit - Maximum number of orders to fetch (default: 10)
 * @returns Query result object with data, loading state, and error
 * 
 * @example
 * const { data, isLoading, error } = useLatestExecutiveOrders(5);
 */
export function useLatestExecutiveOrders(limit = 10) {
  return useQuery({
    queryKey: orderKeys.latest(limit),
    queryFn: () => executiveOrdersApi.getLatestExecutiveOrders(limit),
    staleTime: 2 * 60 * 1000, // 2 minutes
  });
}

/**
 * Hook to fetch orders related to a specific executive order
 * @param id - The ID of the reference executive order
 * @returns Query result object with data, loading state, and error
 * 
 * @example
 * const { data, isLoading, error } = useRelatedOrders('123');
 */
export function useRelatedOrders(id: string | null) {
  return useQuery({
    queryKey: orderKeys.related(id || ''),
    queryFn: () => executiveOrdersApi.getRelatedOrders(id || ''),
    enabled: !!id, // Only fetch when ID is provided
    staleTime: 10 * 60 * 1000, // 10 minutes
  });
}

/**
 * Hook to fetch executive order statistics
 * @returns Query result object with stats data, loading state, and error
 * 
 * @example
 * const { data, isLoading, error } = useExecutiveOrderStats();
 */
export function useExecutiveOrderStats() {
  return useQuery({
    queryKey: orderKeys.stats(),
    queryFn: () => executiveOrdersApi.getExecutiveOrderStats(),
    staleTime: 30 * 60 * 1000, // 30 minutes
  });
}

/**
 * Hook to fetch paginated executive orders with infinite scrolling support
 * @param filters - Base filter parameters
 * @param pageSize - Number of items per page
 * @returns Infinite query result object with pages of data
 * 
 * @example
 * const { 
 *   data, 
 *   fetchNextPage, 
 *   hasNextPage, 
 *   isFetchingNextPage 
 * } = useInfiniteExecutiveOrders({ status: 'Active' });
 */
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
      // Calculate if there are more pages
      const totalPages = Math.ceil(lastPage.total / lastPage.pageSize);
      if (lastPage.page < totalPages) {
        return lastPage.page + 1;
      }
      return undefined; // No more pages
    },
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
}