from app.database import db
from datetime import datetime

class ExecutiveOrder(db.Model):
    __tablename__ = 'executive_orders'
    
    id = db.Column(db.String(20), primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    issuance_date = db.Column(db.Date, nullable=False)
    president = db.Column(db.String(100), nullable=False)
    federal_register_citation = db.Column(db.String(50), nullable=True)
    url = db.Column(db.String(255), nullable=True)
    plain_language_summary = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f"<ExecutiveOrder {self.id}: {self.title}>"
    
    def to_dict(self):
        """Convert the model instance to a dictionary."""
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