from app import app
from app import views
from app import models

'''
from flask_login import LoginManager
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
'''

app.run(host='0.0.0.0',port=8080,threaded=True)
