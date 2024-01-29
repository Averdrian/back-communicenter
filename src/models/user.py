from database import db
from settings import login_manager
from flask_login import UserMixin


class User(UserMixin, db.Model):
    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String(80), unique=False, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(72), unique=False, nullable=False)
    organization_id = db.Column(db.BigInteger, db.ForeignKey("organization.id", ondelete='CASCADE'))

    def __init__(self, username, email, password, organization_id):
        self.username = username
        self.email = email
        self.password = password
        self.organization_id = organization_id

    def get_id(self):
        return str(self.id)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter_by(id=user_id).first()