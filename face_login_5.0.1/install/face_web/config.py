import datetime


class index():
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:Hanabi2020@172.17.0.1:3306/face_login?charset=utf8mb4'
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    PERMANENT_SESSION_LIFETIME = datetime.timedelta(minutes=30)
    #PERMANENT_SESSION_LIFETIME = datetime.timedelta(seconds=10)
    SEND_FILE_MAX_AGE_DEFAULT = datetime.timedelta(days=7)
    DEBUG = False

