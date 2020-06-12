from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
csrf = CSRFProtect(app)
app.config['SECRET_KEY'] = 'ba62b3b78e5f8cd53c51a50e20fe32a6'
bcrypt=Bcrypt(app)
#app.config.from_object('config.settings')
csrf.init_app(app)

login_manager=LoginManager(app)
login_manager.login_view='login'

from flaskblog import routes