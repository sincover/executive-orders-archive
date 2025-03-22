import json
from datetime import date

def test_get_executive_orders_empty(client, session):
    """Test getting executive orders from an empty database."""
    response = client.get("/api/v1/executive-orders")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["items"] == []
    assert data["pagination"]["total_items"] == 0
    assert data["pagination"]["page"] == 1

def test_get_executive_orders(client, sample_executive_orders):
    """Test getting all executive orders."""
    response = client.get("/api/v1/executive-orders")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 5
    assert data["pagination"]["total_items"] == 5
    assert data["pagination"]["page"] == 1

def test_get_executive_orders_with_pagination(client, sample_executive_orders):
    """Test getting executive orders with pagination."""
    # First page, 2 items per page
    response = client.get("/api/v1/executive-orders?page=1&per_page=2")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 2
    assert data["pagination"]["total_items"] == 5
    assert data["pagination"]["page"] == 1
    assert data["pagination"]["per_page"] == 2
    assert data["pagination"]["total_pages"] == 3
    assert data["pagination"]["has_next"] == True
    assert data["pagination"]["has_prev"] == False
    
    # Second page, 2 items per page
    response = client.get("/api/v1/executive-orders?page=2&per_page=2")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 2
    assert data["pagination"]["page"] == 2
    assert data["pagination"]["has_next"] == True
    assert data["pagination"]["has_prev"] == True
    
    # Third page, 2 items per page (only 1 item on this page)
    response = client.get("/api/v1/executive-orders?page=3&per_page=2")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 1
    assert data["pagination"]["page"] == 3
    assert data["pagination"]["has_next"] == False
    assert data["pagination"]["has_prev"] == True

def test_get_executive_orders_with_filtering(client, sample_executive_orders):
    """Test getting executive orders with filtering."""
    # Filter by president
    response = client.get("/api/v1/executive-orders?president=Donald J. Trump")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 2
    for item in data["items"]:
        assert item["president"] == "Donald J. Trump"
    
    # Filter by year
    response = client.get("/api/v1/executive-orders?year=2021")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert len(data["items"]) == 5
    for item in data["items"]:
        assert item["issuance_date"].startswith("2021")

def test_get_executive_orders_with_sorting(client, sample_executive_orders):
    """Test getting executive orders with sorting."""
    # Sort by president, ascending
    response = client.get("/api/v1/executive-orders?sort=president&order=asc")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["items"][0]["president"] == "Donald J. Trump"
    assert data["items"][-1]["president"] == "Joseph R. Biden Jr."
    
    # Sort by issuance_date, descending (default)
    response = client.get("/api/v1/executive-orders")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    # Should be most recent first
    assert data["items"][0]["issuance_date"] >= data["items"][-1]["issuance_date"]

def test_get_executive_order_by_id(client, sample_executive_orders):
    """Test getting a single executive order by ID."""
    # Get existing executive order
    response = client.get("/api/v1/executive-orders/EO-13985")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["success"] == True
    assert data["data"]["id"] == "EO-13985"
    assert data["data"]["title"] == "Advancing Racial Equity and Support for Underserved Communities Through the Federal Government"
    
    # Try to get non-existent executive order
    response = client.get("/api/v1/executive-orders/EO-99999")
    data = json.loads(response.data)
    
    assert response.status_code == 404
    assert data["error"] == True

def test_get_latest_executive_orders(client, sample_executive_orders):
    """Test getting the latest executive orders."""
    # Get latest 3 executive orders
    response = client.get("/api/v1/latest-executive-orders?limit=3")
    data = json.loads(response.data)
    
    assert response.status_code == 200
    assert data["success"] == True
    assert len(data["data"]) == 3
    
    # Verify they are ordered by issuance_date (newest first)
    for i in range(len(data["data"]) - 1):
        assert data["data"][i]["issuance_date"] >= data["data"][i+1]["issuance_date"]

def test_invalid_parameters(client, sample_executive_orders):
    """Test handling of invalid parameters."""
    # Invalid sort field
    response = client.get("/api/v1/executive-orders?sort=invalid_field")
    data = json.loads(response.data)
    
    assert response.status_code == 400
    assert data["error"] == True
    
    # Invalid page number (negative)
    response = client.get("/api/v1/executive-orders?page=-1")
    data = json.loads(response.data)
    
    assert response.status_code == 200  # Should correct to page 1
    assert data["pagination"]["page"] == 1
    
    # Invalid per_page (too large)
    response = client.get("/api/v1/executive-orders?per_page=1000")
    data = json.loads(response.data)
    
    assert response.status_code == 200  # Should correct to default
    assert data["pagination"]["per_page"] == 20