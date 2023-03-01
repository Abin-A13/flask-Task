from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdb.db'
app.config['SECRET_KEY'] ='efgsysejsfkryir5767yu7'
db = SQLAlchemy(app)
migrate = Migrate(app,db)
bcrypt =  Bcrypt(app)
login_manger = LoginManager(app)

from app import routers