from app.models.executive_order import ExecutiveOrder
from datetime import date, datetime

def test_executive_order_creation(session):
    """Test executive order model creation."""
    eo = ExecutiveOrder(
        id="EO-14001",
        title="Test Executive Order",
        issuance_date=date(2023, 6, 15),
        president="Test President",
        federal_register_citation="88 FR 1234",
        url="https://example.com/eo/14001",
        plain_language_summary="This is a test executive order."
    )
    
    session.add(eo)
    session.commit()
    
    # Query the database for the executive order
    saved_eo = session.query(ExecutiveOrder).get("EO-14001")
    
    assert saved_eo is not None
    assert saved_eo.id == "EO-14001"
    assert saved_eo.title == "Test Executive Order"
    assert saved_eo.issuance_date == date(2023, 6, 15)
    assert saved_eo.president == "Test President"
    assert saved_eo.federal_register_citation == "88 FR 1234"
    assert saved_eo.url == "https://example.com/eo/14001"
    assert saved_eo.plain_language_summary == "This is a test executive order."
    assert isinstance(saved_eo.created_at, datetime)
    assert isinstance(saved_eo.updated_at, datetime)

def test_executive_order_repr(session):
    """Test executive order string representation."""
    eo = ExecutiveOrder(
        id="EO-14002",
        title="Another Test Executive Order",
        issuance_date=date(2023, 6, 16),
        president="Test President"
    )
    
    session.add(eo)
    session.commit()
    
    assert repr(eo) == "<ExecutiveOrder EO-14002: Another Test Executive Order>"

def test_executive_order_to_dict(session):
    """Test executive order to_dict serialization."""
    eo = ExecutiveOrder(
        id="EO-14003",
        title="Dict Test Executive Order",
        issuance_date=date(2023, 6, 17),
        president="Test President",
        federal_register_citation="88 FR 5678",
        url="https://example.com/eo/14003",
        plain_language_summary="This is a test for dictionary serialization."
    )
    
    session.add(eo)
    session.commit()
    
    eo_dict = eo.to_dict()
    
    assert eo_dict["id"] == "EO-14003"
    assert eo_dict["title"] == "Dict Test Executive Order"
    assert eo_dict["issuance_date"] == "2023-06-17"
    assert eo_dict["president"] == "Test President"
    assert eo_dict["federal_register_citation"] == "88 FR 5678"
    assert eo_dict["url"] == "https://example.com/eo/14003"
    assert eo_dict["plain_language_summary"] == "This is a test for dictionary serialization."
    assert "created_at" in eo_dict
    assert "updated_at" in eo_dict

def test_executive_order_nullable_fields(session):
    """Test executive order with nullable fields."""
    eo = ExecutiveOrder(
        id="EO-14004",
        title="Nullable Fields Test",
        issuance_date=date(2023, 6, 18),
        president="Test President"
    )
    
    session.add(eo)
    session.commit()
    
    saved_eo = session.query(ExecutiveOrder).get("EO-14004")
    
    assert saved_eo.federal_register_citation is None
    assert saved_eo.url is None
    assert saved_eo.plain_language_summary is None

def test_executive_order_dates_serialization(session):
    """Test executive order date serialization."""
    eo = ExecutiveOrder(
        id="EO-14005",
        title="Dates Test",
        issuance_date=date(2023, 6, 19),
        president="Test President"
    )
    
    session.add(eo)
    session.commit()
    
    eo_dict = eo.to_dict()
    
    assert eo_dict["issuance_date"] == "2023-06-19"
    assert isinstance(eo_dict["created_at"], str)
    assert isinstance(eo_dict["updated_at"], str)