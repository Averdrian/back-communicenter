from database import db

class Template(db.Model):
    __tablename__ = "templates"
    
    id=db.Column(db.Integer, primary_key=True)
    title=db.Column(db.String(100), unique=False, nullable=False)
    message=db.Column(db.Text, nullable=False)
    status=db.Column(db.SmallInteger, nullable=False, default=0)
    language=db.Column(db.String(6), nullable=False)