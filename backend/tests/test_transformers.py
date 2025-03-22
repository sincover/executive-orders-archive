from app.utils.data_transformers import transform_federal_register_document_to_model, transform_federal_register_response
from datetime import date

def test_transform_document_with_complete_data():
    """Test transforming a document with complete data."""
    document = {
        "executive_order_number": "13985",
        "title": "Advancing Racial Equity",
        "signing_date": "2021-01-20",
        "president": "Joseph R. Biden Jr.",
        "citation": "86 FR 7009",
        "html_url": "https://www.federalregister.gov/documents/2021/01/25/2021-01753/advancing-racial-equity"
    }
    
    result = transform_federal_register_document_to_model(document)
    
    assert result["id"] == "EO-13985"
    assert result["title"] == "Advancing Racial Equity"
    assert result["issuance_date"] == date(2021, 1, 20)
    assert result["president"] == "Joseph R. Biden Jr."
    assert result["federal_register_citation"] == "86 FR 7009"
    assert result["url"] == "https://www.federalregister.gov/documents/2021/01/25/2021-01753/advancing-racial-equity"
    assert result["plain_language_summary"] is None

def test_transform_document_with_minimal_data():
    """Test transforming a document with minimal required data."""
    document = {
        "document_number": "2021-01753",  # No executive_order_number
        "title": "Minimal Data Test",
        "publication_date": "2021-01-25",  # No signing_date
        "president": "Joseph R. Biden Jr."
    }
    
    result = transform_federal_register_document_to_model(document)
    
    assert result["id"] == "2021-01753"
    assert result["title"] == "Minimal Data Test"
    assert result["issuance_date"] == date(2021, 1, 25)
    assert result["president"] == "Joseph R. Biden Jr."
    assert result["federal_register_citation"] == ""
    assert result["url"] == ""

def test_transform_document_with_executive_order_notes():
    """Test transforming a document with EO number in notes."""
    document = {
        "document_number": "2021-01753",
        "title": "Executive Order Notes Test",
        "signing_date": "2021-01-20",
        "president": "Joseph R. Biden Jr.",
        "executive_order_notes": "Executive Order 13985"
    }
    
    result = transform_federal_register_document_to_model(document)
    
    assert result["id"] == "EO-13985"

def test_transform_document_with_invalid_dates():
    """Test transforming a document with invalid dates."""
    document = {
        "executive_order_number": "13990",
        "title": "Invalid Date Test",
        "signing_date": "invalid-date",
        "publication_date": "also-invalid",
        "president": "Joseph R. Biden Jr."
    }
    
    result = transform_federal_register_document_to_model(document)
    
    assert result["id"] == "EO-13990"
    assert result["title"] == "Invalid Date Test"
    # Should use today's date when both dates are invalid
    assert isinstance(result["issuance_date"], date)

def test_transform_response_with_multiple_documents():
    """Test transforming a response with multiple documents."""
    response = {
        "count": 2,
        "total_pages": 1,
        "results": [
            {
                "executive_order_number": "13985",
                "title": "First Document",
                "signing_date": "2021-01-20",
                "president": "Joseph R. Biden Jr."
            },
            {
                "executive_order_number": "13986",
                "title": "Second Document",
                "signing_date": "2021-01-20",
                "president": "Joseph R. Biden Jr."
            }
        ]
    }
    
    results = transform_federal_register_response(response)
    
    assert len(results) == 2
    assert results[0]["id"] == "EO-13985"
    assert results[1]["id"] == "EO-13986"

def test_transform_empty_response():
    """Test transforming an empty response."""
    # Empty response
    results = transform_federal_register_response(None)
    assert len(results) == 0
    
    # Response with no results
    results = transform_federal_register_response({"count": 0})
    assert len(results) == 0