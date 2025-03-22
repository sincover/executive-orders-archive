from app.services.celery_app import celery_app
from app.services.federal_register_client import FederalRegisterClient
from app.utils.data_transformers import transform_federal_register_document_to_model
from app.models.executive_order import ExecutiveOrder
from app.database import db
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

@celery_app.task(bind=True, max_retries=3, default_retry_delay=300)
def update_executive_orders(self, days_back=30):
    """
    Celery task to fetch and update executive orders from the Federal Register API.
    
    Args:
        days_back (int, optional): Number of days back to look for updates. Defaults to 30.
    
    Returns:
        dict: Summary of the update operation
    """
    try:
        logger.info(f"Starting executive orders update task (looking back {days_back} days)")
        
        # Calculate the date range
        end_date = datetime.utcnow().date()
        start_date = end_date - timedelta(days=days_back)
        
        # Initialize the API client
        client = FederalRegisterClient()
        
        # Initialize counters
        new_count = 0
        updated_count = 0
        error_count = 0
        
        # Fetch from the API
        page = 1
        per_page = 50
        total_pages = 1  # Start with 1, will be updated after first request
        
        while page <= total_pages:
            try:
                logger.info(f"Fetching page {page} of executive orders")
                
                # Make the API request
                response = client.get_executive_orders(
                    page=page,
                    per_page=per_page,
                    start_date=start_date.isoformat(),
                    end_date=end_date.isoformat()
                )
                
                # Update total pages if available
                if response and 'total_pages' in response:
                    total_pages = response['total_pages']
                
                # Process each result
                for document in response.get('results', []):
                    try:
                        # Transform to our model format
                        transformed = transform_federal_register_document_to_model(document)
                        
                        if not transformed or not transformed.get('id'):
                            logger.warning(f"Skipping document with missing ID: {document.get('document_number', 'Unknown')}")
                            continue
                        
                        # Check if this executive order already exists
                        existing = ExecutiveOrder.query.get(transformed['id'])
                        
                        if existing:
                            # Update existing record
                            for key, value in transformed.items():
                                if key != 'id' and hasattr(existing, key):
                                    setattr(existing, key, value)
                            updated_count += 1
                        else:
                            # Create new record
                            new_eo = ExecutiveOrder(**transformed)
                            db.session.add(new_eo)
                            new_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error processing document: {str(e)}")
                
                # Commit changes for this page
                db.session.commit()
                
                # Move to next page
                page += 1
                
            except Exception as e:
                logger.error(f"Error fetching page {page}: {str(e)}")
                error_count += 1
                break
        
        # Log summary
        summary = {
            'new_records': new_count,
            'updated_records': updated_count,
            'errors': error_count,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Executive orders update completed: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        self.retry(exc=e)

@celery_app.task(bind=True)
def fetch_historical_executive_orders(self, start_year=1994, end_year=None):
    """
    Celery task to fetch historical executive orders from the Federal Register API.
    
    Args:
        start_year (int, optional): Year to start fetching from. Defaults to 1994 (earliest in Federal Register API).
        end_year (int, optional): Year to end fetching at. Defaults to current year.
    
    Returns:
        dict: Summary of the fetch operation
    """
    try:
        # Use current year if end_year not specified
        if not end_year:
            end_year = datetime.utcnow().year
            
        logger.info(f"Starting historical executive orders fetch for years {start_year}-{end_year}")
        
        # Initialize the API client
        client = FederalRegisterClient()
        
        # Initialize counters
        total_count = 0
        error_years = []
        
        # Process each year
        for year in range(start_year, end_year + 1):
            try:
                logger.info(f"Fetching executive orders for year {year}")
                
                # Process this year in a separate task
                result = fetch_executive_orders_by_year.delay(year)
                
                # Wait for the task to complete
                year_result = result.get(timeout=3600)  # 1 hour timeout
                
                total_count += year_result.get('total_records', 0)
                logger.info(f"Completed year {year}, fetched {year_result.get('total_records', 0)} records")
                
            except Exception as e:
                logger.error(f"Error processing year {year}: {str(e)}")
                error_years.append(year)
        
        # Log summary
        summary = {
            'total_records': total_count,
            'years_processed': (end_year - start_year + 1) - len(error_years),
            'error_years': error_years,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Historical executive orders fetch completed: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Task failed: {str(e)}")
        self.retry(exc=e)

@celery_app.task(bind=True)
def fetch_executive_orders_by_year(self, year):
    """
    Celery task to fetch executive orders for a specific year.
    
    Args:
        year (int): Year to fetch executive orders for
    
    Returns:
        dict: Summary of the fetch operation for this year
    """
    try:
        logger.info(f"Starting executive orders fetch for year {year}")
        
        # Initialize the API client
        client = FederalRegisterClient()
        
        # Initialize counters
        new_count = 0
        updated_count = 0
        error_count = 0
        
        # Fetch from the API
        page = 1
        per_page = 50
        total_pages = 1  # Start with 1, will be updated after first request
        
        while page <= total_pages:
            try:
                logger.info(f"Fetching page {page} of executive orders for year {year}")
                
                # Make the API request
                response = client.get_executive_orders(
                    page=page,
                    per_page=per_page,
                    year=year
                )
                
                # Update total pages if available
                if response and 'total_pages' in response:
                    total_pages = response['total_pages']
                
                # Process each result
                for document in response.get('results', []):
                    try:
                        # Transform to our model format
                        transformed = transform_federal_register_document_to_model(document)
                        
                        if not transformed or not transformed.get('id'):
                            logger.warning(f"Skipping document with missing ID: {document.get('document_number', 'Unknown')}")
                            continue
                        
                        # Check if this executive order already exists
                        existing = ExecutiveOrder.query.get(transformed['id'])
                        
                        if existing:
                            # Update existing record
                            for key, value in transformed.items():
                                if key != 'id' and hasattr(existing, key):
                                    setattr(existing, key, value)
                            updated_count += 1
                        else:
                            # Create new record
                            new_eo = ExecutiveOrder(**transformed)
                            db.session.add(new_eo)
                            new_count += 1
                        
                    except Exception as e:
                        error_count += 1
                        logger.error(f"Error processing document: {str(e)}")
                
                # Commit changes for this page
                db.session.commit()
                
                # Move to next page
                page += 1
                
            except Exception as e:
                logger.error(f"Error fetching page {page} for year {year}: {str(e)}")
                error_count += 1
                break
        
        # Log summary
        summary = {
            'year': year,
            'new_records': new_count,
            'updated_records': updated_count,
            'total_records': new_count + updated_count,
            'errors': error_count,
            'completed_at': datetime.utcnow().isoformat()
        }
        
        logger.info(f"Executive orders fetch for year {year} completed: {summary}")
        return summary
        
    except Exception as e:
        logger.error(f"Task failed for year {year}: {str(e)}")
        self.retry(exc=e)