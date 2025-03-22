import requests
import logging
import time
import random
import re
from datetime import datetime

logger = logging.getLogger(__name__)

class APIError(Exception):
    """Base class for API-related errors."""
    pass

class FederalRegisterAPIError(APIError):
    """Exception raised for Federal Register API errors."""
    def __init__(self, message, status_code=None, response=None):
        self.message = message
        self.status_code = status_code
        self.response = response
        super().__init__(self.message)

class FederalRegisterClient:
    """Client for interacting with the Federal Register API."""
    
    BASE_URL = "https://www.federalregister.gov/api/v1/"
    
    def __init__(self, base_url=None):
        self.base_url = base_url or self.BASE_URL
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'User-Agent': 'ExecutiveOrdersArchive/1.0'
        })
    
    def _make_request(self, endpoint, method='GET', params=None, data=None, retry_count=3, retry_delay=1):
        """Make a request to the Federal Register API with retry logic."""
        url = f"{self.base_url.rstrip('/')}/{endpoint.lstrip('/')}"
        
        for attempt in range(retry_count + 1):
            try:
                logger.info(f"Making {method} request to {url} (attempt {attempt + 1})")
                
                response = self.session.request(
                    method=method,
                    url=url,
                    params=params,
                    json=data,
                    timeout=30  # 30 seconds timeout
                )
                
                # Log the response status
                logger.info(f"Received response: {response.status_code}")
                
                # Check for rate limiting
                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 60))
                    logger.warning(f"Rate limited. Retrying after {retry_after} seconds")
                    time.sleep(retry_after)
                    continue
                
                # Check for other retryable errors
                if response.status_code >= 500:
                    if attempt < retry_count:
                        # Calculate exponential backoff with jitter
                        backoff = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                        logger.warning(f"Server error {response.status_code}. Retrying after {backoff:.2f} seconds")
                        time.sleep(backoff)
                        continue
                
                # Check for successful response
                if response.status_code in (200, 201, 204):
                    if response.content:
                        return response.json()
                    return None
                
                # Handle client errors (4xx)
                error_message = f"API Error {response.status_code}"
                try:
                    error_data = response.json()
                    if isinstance(error_data, dict) and 'errors' in error_data:
                        error_message = f"{error_message}: {error_data['errors']}"
                except:
                    error_message = f"{error_message}: {response.text}"
                
                raise FederalRegisterAPIError(
                    message=error_message,
                    status_code=response.status_code,
                    response=response
                )
                
            except (requests.RequestException, requests.Timeout) as e:
                if attempt < retry_count:
                    backoff = retry_delay * (2 ** attempt) + random.uniform(0, 1)
                    logger.warning(f"Request failed: {str(e)}. Retrying after {backoff:.2f} seconds")
                    time.sleep(backoff)
                    continue
                raise FederalRegisterAPIError(f"Request failed after {retry_count} retries: {str(e)}")
        
        # This should not be reached, but just in case
        raise FederalRegisterAPIError(f"Max retries exceeded for {url}")
    
    def get_executive_orders(self, page=1, per_page=20, president=None, year=None, start_date=None, end_date=None):
        """
        Fetch executive orders from the Federal Register API.
        
        Args:
            page (int): Page number for pagination
            per_page (int): Number of results per page
            president (str): Filter by president name
            year (int): Filter by year of issuance
            start_date (str): Filter by start date (YYYY-MM-DD)
            end_date (str): Filter by end date (YYYY-MM-DD)
            
        Returns:
            dict: API response containing executive orders
        """
        params = {
            'page': page,
            'per_page': per_page,
            'order': 'newest',
            'conditions[presidential_document_type][]': 'executive_order'
        }
        
        # Add optional filters
        if president:
            params['conditions[president][]'] = president
        
        if year:
            params['conditions[publication_date][year]'] = year
        
        if start_date:
            params['conditions[publication_date][gte]'] = start_date
        
        if end_date:
            params['conditions[publication_date][lte]'] = end_date
        
        return self._make_request('documents', params=params)
    
    def get_executive_order_by_number(self, executive_order_number):
        """
        Fetch a specific executive order by its number.
        
        Args:
            executive_order_number (str): Executive order number (e.g., '13985')
            
        Returns:
            dict: API response containing the executive order details, or None if not found
        """
        params = {
            'conditions[presidential_document_type][]': 'executive_order',
            'conditions[executive_order_number]': executive_order_number,
        }
        
        response = self._make_request('documents', params=params)
        
        if response and response.get('count', 0) > 0 and 'results' in response:
            return response['results'][0]
        
        return None
    
    def search_executive_orders(self, query, page=1, per_page=20):
        """
        Search for executive orders containing the specified query.
        
        Args:
            query (str): Search query
            page (int): Page number for pagination
            per_page (int): Number of results per page
            
        Returns:
            dict: API response containing matching executive orders
        """
        params = {
            'page': page,
            'per_page': per_page,
            'order': 'relevance',
            'conditions[presidential_document_type][]': 'executive_order',
            'conditions[term]': query
        }
        
        return self._make_request('documents', params=params)