from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
# PHOTO UPLOAD
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'static/uploads/')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = '12345'
from flask_migrate import Migrate
from flask_login import LoginManager
migrate = Migrate(app, db,  render_as_batch=True)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
from pavshop.controlers import *