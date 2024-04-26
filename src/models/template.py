from database import db
from enum import Enum

class TemplateStatus(Enum):
    PENDING = 0
    APPROVED = 1
    REJECTED = 2
    

class Template(db.Model):
    __tablename__ = "templates"
    
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), unique=False, nullable=False)
    message=db.Column(db.Text, nullable=False)
    status=db.Column(db.SmallInteger, nullable=False, default=TemplateStatus.PENDING.value)
    language=db.Column(db.String(6), nullable=False, default="en_us")
    organization_id = db.Column(db.BigInteger, db.ForeignKey('organizations.id'), nullable=False)
    
    
    def __init__(self, organization_id, title, message, language="en_US", status=TemplateStatus.PENDING.value):
        self.organization_id = organization_id
        self.title = title
        self.message = message
        self.language = language
        self.status = status
        
    
    
    def to_dict(self):
        return {
            "id":self.id,
            "organization_id": self.organization_id,
            "title":self.title,
            "message":self.message,
            "status":self.status,
            "language":self.language
        }
    
    