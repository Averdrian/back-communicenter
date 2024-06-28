from database import db
from settings import login_manager
from flask_login import UserMixin
from enum import Enum

class UserRole(Enum):
    CHIEF = 0
    EMPLOYEE = 1

class User(UserMixin, db.Model):
    __tablename__ = "users"
    
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(72), unique=False, nullable=False)
    organization_id = db.Column(db.BigInteger, db.ForeignKey("organizations.id", ondelete='CASCADE'))
    role = db.Column(db.SmallInteger, nullable=False, default=UserRole.EMPLOYEE.value)
    organization = db.relationship('Organization', back_populates='users', lazy='joined')


    def __init__(self, username, email, password, organization_id, role = UserRole.EMPLOYEE.value):
        self.username = username
        self.email = email
        self.password = password
        self.organization_id = organization_id
        self.role = role

    def get_id(self):
        return str(self.id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()
    
    
    def to_dict(self):
        return {
            'id' : self.id,
            'username' : self.username,
            'email' : self.email,
            'organization_id' : self.organization_id,
            'organization': self.organization.name,
            'role' : self.role
        }