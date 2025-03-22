#!/usr/bin/env python
import os
import sys
import argparse
import time
import json
from datetime import datetime, timedelta

# Add parent directory to path to import app modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import create_app
from app.database import db
from app.models.executive_order import ExecutiveOrder
from app.services.federal_register_client import FederalRegisterClient
from app.utils.data_transformers import transform_federal_register_document_to_model
from app.utils.logging import get_data_fetch_logger

# Set up logging
logger = get_data_fetch_logger()

# Create a file to store progress state
STATE_FILE = 'fetch_state.json'

def save_state(state):
    """Save current fetch state to a file."""
    with open(STATE_FILE, 'w') as f:
        json.dump(state, f)
    logger.info(f"Saved state: {state}")

def load_state():
    """Load saved fetch state from file."""
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE, 'r') as f:
                state = json.load(f)
            logger.info(f"Loaded state: {state}")
            return state
        except (json.JSONDecodeError, IOError) as e:
            logger.error(f"Error loading state file: {e}")
    return None

def fetch_executive_orders(start_date=None, end_date=None, page_size=20, max_pages=None, resume=False):
    """Fetch executive orders from the Federal Register API."""
    # Initialize the Flask app
    app = create_app('development')
    
    # Create a request context
    with app.app_context():
        # Initialize API client
        client = FederalRegisterClient()
        
        # Initialize counters
        new_count = 0
        updated_count = 0
        error_count = 0
        total_count = 0
        
        # Set up pagination
        current_page = 1
        total_pages = 1  # Will be updated after first API call
        
        # Load state if resuming
        if resume:
            state = load_state()
            if state:
                current_page = state.get('current_page', 1)
                new_count = state.get('new_count', 0)
                updated_count = state.get('updated_count', 0)
                error_count = state.get('error_count', 0)
                total_count = state.get('total_count', 0)
                logger.info(f"Resuming from page {current_page}")
        
        # Set up date range for API call
        date_params = {}
        if start_date:
            date_params['start_date'] = start_date
        if end_date:
            date_params['end_date'] = end_date
        
        # Main fetch loop
        while current_page <= total_pages:
            if max_pages and current_page > max_pages:
                logger.info(f"Reached maximum pages limit ({max_pages})")
                break
            
            try:
                logger.info(f"Fetching page {current_page}")
                
                # Make API call
                response = client.get_executive_orders(
                    page=current_page,
                    per_page=page_size,
                    **date_params
                )
                
                # Update total pages
                if 'total_pages' in response:
                    total_pages = response['total_pages']
                    logger.info(f"Total pages: {total_pages}")
                
                # Process results
                page_new = 0
                page_updated = 0
                page_error = 0
                
                for document in response.get('results', []):
                    try:
                        # Transform document to our model format
                        transformed = transform_federal_register_document_to_model(document)
                        
                        if not transformed or not transformed.get('id'):
                            logger.warning(f"Skipping document with missing ID: {document.get('document_number', 'Unknown')}")
                            continue
                        
                        # Check if it already exists
                        existing = ExecutiveOrder.query.get(transformed['id'])
                        
                        if existing:
                            # Update existing record
                            for key, value in transformed.items():
                                if key != 'id' and hasattr(existing, key):
                                    setattr(existing, key, value)
                            page_updated += 1
                        else:
                            # Create new record
                            new_eo = ExecutiveOrder(**transformed)
                            db.session.add(new_eo)
                            page_new += 1
                            
                    except Exception as e:
                        logger.error(f"Error processing document: {str(e)}")
                        page_error += 1
                
                # Commit changes for this page
                db.session.commit()
                
                # Update counters
                new_count += page_new
                updated_count += page_updated
                error_count += page_error
                total_count = new_count + updated_count
                
                logger.info(f"Page {current_page} processed: {page_new} new, {page_updated} updated, {page_error} errors")
                
                # Save state
                save_state({
                    'current_page': current_page, 
                    'total_pages': total_pages,
                    'new_count': new_count, 
                    'updated_count': updated_count, 
                    'error_count': error_count,
                    'total_count': total_count,
                    'last_updated': datetime.utcnow().isoformat()
                })
                
                # Move to next page
                current_page += 1
                
                # Small delay to avoid overwhelming the API
                time.sleep(1)
                
            except Exception as e:
                logger.error(f"Error fetching page {current_page}: {str(e)}")
                error_count += 1
                
                # Save error state
                save_state({
                    'current_page': current_page, 
                    'total_pages': total_pages,
                    'new_count': new_count, 
                    'updated_count': updated_count, 
                    'error_count': error_count,
                    'total_count': total_count,
                    'last_error': str(e),
                    'last_updated': datetime.utcnow().isoformat()
                })
                
                # Retry after a delay
                time.sleep(5)
        
        # Completed
        logger.info(f"Fetch completed: {new_count} new, {updated_count} updated, {error_count} errors")
        return total_count

def main():
    """Main entry point for the data fetch script."""
    parser = argparse.ArgumentParser(description='Fetch executive orders from the Federal Register API')
    parser.add_argument('--start-date', help='Start date (YYYY-MM-DD)')
    parser.add_argument('--end-date', help='End date (YYYY-MM-DD)')
    parser.add_argument('--days-back', type=int, default=365, help='Number of days to look back (default: 365)')
    parser.add_argument('--page-size', type=int, default=20, help='Results per page (default: 20)')
    parser.add_argument('--max-pages', type=int, help='Maximum number of pages to fetch')
    parser.add_argument('--resume', action='store_true', help='Resume from last saved state')
    args = parser.parse_args()
    
    # Set up date range
    start_date = args.start_date
    end_date = args.end_date
    
    if not start_date and args.days_back:
        # Calculate start date based on days_back
        start_date = (datetime.utcnow() - timedelta(days=args.days_back)).strftime('%Y-%m-%d')
    
    if not end_date:
        # Use today as the end date
        end_date = datetime.utcnow().strftime('%Y-%m-%d')
    
    logger.info(f"Starting fetch for date range: {start_date} to {end_date}")
    
    # Perform the fetch
    total_count = fetch_executive_orders(
        start_date=start_date,
        end_date=end_date,
        page_size=args.page_size,
        max_pages=args.max_pages,
        resume=args.resume
    )
    
    logger.info(f"Fetch script completed successfully. Total records: {total_count}")

if __name__ == '__main__':
    main()