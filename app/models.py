from app import db,login_manger
from app import bcrypt
from flask_login import UserMixin

@login_manger.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model,UserMixin):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(length=30),nullable=False,unique=True)
    email = db.Column(db.String(length=50),nullable=False,unique=True)
    password_hash = db.Column(db.String(length=50),nullable=False)
    is_admin = db.Column(db.Boolean(),default=False)

    @property
    def password(self):
        raise AttributeError("password is not there")
    
    @password.setter
    def password(self,plain_pass):
        self.password_hash = bcrypt.generate_password_hash(plain_pass).decode('utf-8')

    def verify_password(self,entered_password):
        return bcrypt.check_password_hash(self.password_hash,entered_password)