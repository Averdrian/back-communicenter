from database import db
from phone_iso3166.country import phone_country
from datetime import datetime

#TODO: Enumerado para los status (MIRAR CONSTRUCTOR QUE USA 0 DE BASE)

class Chat(db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    phone = db.Column(db.BigInteger, unique=True, nullable=False)
    whatsapp_name = db.Column(db.String(60), unique=False, nullable=True)
    organization_id = db.Column(db.BigInteger, db.ForeignKey('organization.id'), nullable=True)
    status = db.Column(db.SmallInteger, unique=False, nullable=False)
    last_message_at = db.Column(db.DateTime, unique=False, nullable=True)
    expires_at = db.Column(db.DateTime, unique=False, nullable=True)
    country = db.Column(db.String(5), unique=False, nullable=True)
    messages = db.relationship('Message', backref='chat', cascade='all, delete-orphan')
    
    def __init__(self, phone, status = 0, whatsapp_name = None, organization_id = None):
        self.phone = phone
        self.status = status
        self.whatsapp_name = whatsapp_name
        self.organization_id = organization_id
        self.country = phone_country(phone)


    def to_dict(self):
        return {
            'id':self.id,
            'phone':self.phone,
            'whatsapp_name':self.whatsapp_name,
            'organization_id':self.organization_id,
            'status':self.status, #TODO: Esto cambiara y devolvera el nombre del status en su debido momento
            'last_message_at': self.last_message_at.strftime("%d/%m/%Y %H:%M"),
            'expires_at': self.expires_at.strftime("%d/%m/%Y %H:%M"),
            'country' : self.country
        }