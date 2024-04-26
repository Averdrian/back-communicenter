from database import db



class FastMessage(db.Model):
    __tablename__ = "fast_messages"
    #TODO:
    id = db.Column(db.BigInteger, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    language=db.Column(db.String(6), nullable=False, default="en_us")
    organization_id = db.Column(db.BigInteger, db.ForeignKey('organizations.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    
    
    def __init__(self):
        #TODO:
        pass
    
    
    def to_dict(self):
        #TODO:
        pass
    
    