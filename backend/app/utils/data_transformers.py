import re
from datetime import datetime, date
import logging

logger = logging.getLogger(__name__)

def transform_federal_register_document_to_model(document):
    """
    Transform a Federal Register API document to a format compatible with the ExecutiveOrder model.
    
    Args:
        document (dict): Document data from Federal Register API
        
    Returns:
        dict: Dictionary with fields matching the ExecutiveOrder model
    """
    # Extract the Executive Order number
    eo_number = document.get('executive_order_number')
    
    # If executive_order_number is not available, try to extract from notes or document_number
    if not eo_number and document.get('executive_order_notes'):
        # Try to extract from notes (e.g., "Executive Order 13985")
        notes = document.get('executive_order_notes', '')
        match = re.search(r'Executive Order (\d+)', notes)
        if match:
            eo_number = match.group(1)
    
    # Format ID as "EO-XXXXX"
    if eo_number:
        eo_id = f"EO-{eo_number}"
    elif document.get('document_number'):
        eo_id = document.get('document_number')
    else:
        eo_id = None
    
    # Parse issuance date
    issuance_date = None
    if document.get('signing_date'):
        try:
            issuance_date = datetime.strptime(document.get('signing_date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            logger.warning(f"Invalid signing_date format for EO {eo_id}: {document.get('signing_date')}")
    
    # If signing_date is not available, try publication_date
    if not issuance_date and document.get('publication_date'):
        try:
            issuance_date = datetime.strptime(document.get('publication_date'), '%Y-%m-%d').date()
        except (ValueError, TypeError):
            logger.warning(f"Invalid publication_date format for EO {eo_id}: {document.get('publication_date')}")
    
    # Default to today if date is still missing
    if not issuance_date:
        issuance_date = date.today()
        logger.warning(f"Using today's date for EO {eo_id} due to missing signing/publication date")
    
    # Create result dictionary matching our model
    result = {
        'id': eo_id,
        'title': document.get('title', ''),
        'issuance_date': issuance_date,
        'president': document.get('president', 'Unknown'),
        'federal_register_citation': document.get('citation', ''),
        'url': document.get('html_url', ''),
        'plain_language_summary': None  # Will be added in a future phase
    }
    
    return result

def transform_federal_register_response(response):
    """
    Transform an entire Federal Register API response to a list of model-compatible dictionaries.
    
    Args:
        response (dict): Response from Federal Register API
        
    Returns:
        list: List of dictionaries with fields matching the ExecutiveOrder model
    """
    results = []
    
    if not response or 'results' not in response:
        logger.warning("Empty or invalid response from Federal Register API")
        return results
    
    for document in response.get('results', []):
        try:
            transformed = transform_federal_register_document_to_model(document)
            if transformed and transformed.get('id'):
                results.append(transformed)
            else:
                logger.warning(f"Skipping document with missing ID: {document.get('document_number', 'Unknown')}")
        except Exception as e:
            logger.error(f"Error transforming document {document.get('document_number', 'Unknown')}: {str(e)}")
    
    return results