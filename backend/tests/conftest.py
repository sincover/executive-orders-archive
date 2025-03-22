import pytest
import os
from app import create_app
from app.database import db as _db
from app.models.executive_order import ExecutiveOrder
from datetime import date

@pytest.fixture(scope='session')
def app():
    """Create and configure a Flask app for testing."""
    app = create_app('testing')
    
    # Create a test client using the Flask application
    with app.app_context():
        yield app

@pytest.fixture(scope='session')
def db(app):
    """Create and configure a database for testing."""
    with app.app_context():
        _db.create_all()
        yield _db
        _db.drop_all()

@pytest.fixture(scope='function')
def session(db):
    """Create a new database session for each test."""
    connection = db.engine.connect()
    transaction = connection.begin()
    
    session = db.session
    
    yield session
    
    # Roll back the transaction
    transaction.rollback()
    connection.close()
    session.remove()

@pytest.fixture
def client(app):
    """Create a test client for the app."""
    return app.test_client()

@pytest.fixture
def sample_executive_orders(session):
    """Create sample executive orders for testing."""
    eos = [
        ExecutiveOrder(
            id="EO-13985",
            title="Advancing Racial Equity and Support for Underserved Communities Through the Federal Government",
            issuance_date=date(2021, 1, 20),
            president="Joseph R. Biden Jr.",
            federal_register_citation="86 FR 7009",
            url="https://www.federalregister.gov/documents/2021/01/25/2021-01753/advancing-racial-equity-and-support-for-underserved-communities-through-the-federal-government",
            plain_language_summary=None
        ),
        ExecutiveOrder(
            id="EO-13986",
            title="Ensuring a Lawful and Accurate Enumeration and Apportionment Pursuant to the Decennial Census",
            issuance_date=date(2021, 1, 20),
            president="Joseph R. Biden Jr.",
            federal_register_citation="86 FR 7015",
            url="https://www.federalregister.gov/documents/2021/01/25/2021-01755/ensuring-a-lawful-and-accurate-enumeration-and-apportionment-pursuant-to-the-decennial-census",
            plain_language_summary=None
        ),
        ExecutiveOrder(
            id="EO-13990",
            title="Protecting Public Health and the Environment and Restoring Science To Tackle the Climate Crisis",
            issuance_date=date(2021, 1, 20),
            president="Joseph R. Biden Jr.",
            federal_register_citation="86 FR 7037",
            url="https://www.federalregister.gov/documents/2021/01/25/2021-01765/protecting-public-health-and-the-environment-and-restoring-science-to-tackle-the-climate-crisis",
            plain_language_summary=None
        ),
        ExecutiveOrder(
            id="EO-13984",
            title="Taking Additional Steps to Address the National Emergency with Respect to Significant Malicious Cyber-Enabled Activities",
            issuance_date=date(2021, 1, 19),
            president="Donald J. Trump",
            federal_register_citation="86 FR 6837",
            url="https://www.federalregister.gov/documents/2021/01/25/2021-01714/taking-additional-steps-to-address-the-national-emergency-with-respect-to-significant-malicious",
            plain_language_summary=None
        ),
        ExecutiveOrder(
            id="EO-13983",
            title="Ensuring Democratic Accountability in Agency Rulemaking",
            issuance_date=date(2021, 1, 18),
            president="Donald J. Trump",
            federal_register_citation="86 FR 6823",
            url="https://www.federalregister.gov/documents/2021/01/22/2021-01635/ensuring-democratic-accountability-in-agency-rulemaking",
            plain_language_summary=None
        )
    ]
    
    for eo in eos:
        session.add(eo)
    
    session.commit()
    
    return eos