from app import db


class Chat(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    phone = db.Column(db.BigInteger, unique=True, nullable=False)
    whatsapp_name = db.Column(db.String(60), unique=False, nullable=True)
    last_message_at = db.Column(db.DateTime, unique=False, nullable=True)
    organization_id = db.Column(db.BigInteger, db.ForeignKey('organization.id'), nullable=True)
    status = db.Column(db.SmallInteger, unique=False, nullable=False)
    
    
    def __init__(self, phone, status):
        self.phone = phone
        self.status = status
