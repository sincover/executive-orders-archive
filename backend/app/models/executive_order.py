from app.models import Base
from sqlalchemy import Column, String, Date, Text, DateTime
from datetime import datetime

class ExecutiveOrder(Base):
    """
    Executive Order database model.
    
    Represents a presidential executive order stored in the database.
    """
    __tablename__ = 'executive_orders'
    
    id = Column(String(20), primary_key=True)
    title = Column(String(255), nullable=False)
    issuance_date = Column(Date, nullable=False)
    president = Column(String(100), nullable=False)
    federal_register_citation = Column(String(50), nullable=True)
    url = Column(String(255), nullable=True)
    plain_language_summary = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        """String representation of the Executive Order."""
        return f"<ExecutiveOrder(id='{self.id}', title='{self.title[:30]}...', president='{self.president}')>"
    
    def to_dict(self):
        """
        Convert the model instance to a dictionary.
        
        Returns:
            dict: Dictionary representation of the executive order
        """
        return {
            'id': self.id,
            'title': self.title,
            'issuance_date': self.issuance_date.isoformat() if self.issuance_date else None,
            'president': self.president,
            'federal_register_citation': self.federal_register_citation,
            'url': self.url,
            'plain_language_summary': self.plain_language_summary,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }