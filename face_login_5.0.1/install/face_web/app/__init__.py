from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_login import LoginManager

app = Flask(__name__)
app.config.from_object('config.index')
db = SQLAlchemy(app)

from app.models import User
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
login_manager.login_message = 'Access denied.'
login_manager.init_app(app)
app.config['SECRET_KEY']='face_login'


@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(id = user_id).first()
