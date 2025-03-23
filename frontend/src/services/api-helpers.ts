/**
 * Helper functions for API interactions
 */

import { ApiError } from './api';

/**
 * Creates a query string from filter parameters
 * @param params - Object with filter parameters
 * @returns URL query string
 */
export const createQueryString = (params: Record<string, string | number | boolean | undefined>): string => {
  const cleanParams = Object.entries(params)
    .filter(([_, value]) => value !== undefined && value !== '')
    .reduce((acc, [key, value]) => {
      acc[key] = String(value);
      return acc;
    }, {} as Record<string, string>);
    
  return new URLSearchParams(cleanParams).toString();
};

/**
 * Handles API errors consistently
 * @param error - The caught error
 * @param defaultMessage - Default message to use if not an ApiError
 * @returns ApiError instance
 */
export const handleApiError = (error: unknown, defaultMessage: string): ApiError => {
  if (error instanceof ApiError) {
    return error;
  }
  
  // Log unexpected errors
  console.error('Unexpected API error:', error);
  return new ApiError(defaultMessage, 500);
};

/**
 * Formats date for API requests
 * @param date - Date to format
 * @returns Formatted date string (YYYY-MM-DD)
 */
export const formatApiDate = (date: Date): string => {
  return date.toISOString().split('T')[0];
};

/**
 * Retries a promise-based operation with exponential backoff
 * @param operation - Function that returns a promise
 * @param retries - Maximum number of retries
 * @param delay - Initial delay in ms
 * @param backoffFactor - Multiplier for each subsequent retry delay
 * @returns Promise from the operation
 */
export const retryWithBackoff = async <T>(
  operation: () => Promise<T>,
  retries = 3,
  delay = 300,
  backoffFactor = 2
): Promise<T> => {
  try {
    return await operation();
  } catch (error) {
    // Don't retry for client errors (4xx)
    if (error instanceof ApiError && error.status >= 400 && error.status < 500) {
      throw error;
    }
    
    if (retries <= 0) {
      throw error;
    }
    
    await new Promise(resolve => setTimeout(resolve, delay));
    
    return retryWithBackoff(operation, retries - 1, delay * backoffFactor, backoffFactor);
  }
};