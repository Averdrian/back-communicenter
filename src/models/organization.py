from database import db


class Organization(db.Model):
    __tablename__ = "organizations"
    
    id = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    wa_phone_id = db.Column(db.BigInteger, unique=True, nullable=True)
    wb_account_id = db.Column(db.BigInteger, unique=True, nullable=True)
    wa_api_key = db.Column(db.String(300), nullable=True)
    wa_verify_token = db.Column(db.String(50), nullable=True)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    users = db.relationship('User', back_populates='organization', lazy='joined')
    chats = db.relationship('Chat', backref='organization', lazy='joined')
    templates = db.relationship('Template', backref='organization', lazy='joined')

    def __init__(self, organization_data):
        self.name = organization_data['name']
        self.wa_phone_id = organization_data['wa_phone_id'] if 'wa_phone_id' in organization_data else None
        self.wb_account_id = organization_data['wb_account_id'] if 'wb_account_id' in organization_data else None
        self.wa_verify_token = organization_data['wa_verify_token'] if 'wa_verify_token' in organization_data else None
        self.wa_api_key = organization_data['wa_api_key'] if 'wa_api_key' in organization_data else None
        
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'wa_phone_id': self.wa_phone_id,
            'wb_account_id': self.wb_account_id,
            'wa_api_key': self.wa_api_key,
            'wa_verify_token': self.wa_verify_token
        }