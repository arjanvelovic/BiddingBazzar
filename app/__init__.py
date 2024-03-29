from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
from flask_cors import CORS
    
db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.signin'
login_manager.login_message_category = 'info'
mail = Mail()


app = Flask(__name__)
CORS(app)
app.config.from_object(Config)

db.init_app(app)
bcrypt.init_app(app)
login_manager.init_app(app)
mail.init_app(app)

from app.users.routes import users
from app.items.routes import items
from app.main.routes import main
from app.errors.handlers import errors
app.register_blueprint(users)
app.register_blueprint(items)
app.register_blueprint(main)
app.register_blueprint(errors)

