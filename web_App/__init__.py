from datetime import datetime
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
#from pylint_flask_sqlalchemy import SQLAlchemy

#from models import User , Post

app = Flask(__name__)
app.config['SECRET_KEY'] = '0547be8d60dfeb9a4f9c82d5e7c2b001'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
db = SQLAlchemy(app)
bcrypt = Bcrypt()
login_manager=LoginManager(app)
login_manager.login_view='login'
#login_manager.login_view='login'


from web_App.route import *

