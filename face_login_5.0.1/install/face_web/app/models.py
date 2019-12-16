from app import db
from flask_login import UserMixin

class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(40), primary_key=True)
    username = db.Column(db.String(30))
    password = db.Column(db.String(30))
    Img2Base64 = db.Column(db.Text)
    faceid = db.Column(db.Text)
    isAdmin = db.Column(db.String(5))

    def __init__(self, get_id, username, password, base64, faceid,admin_status):
        self.id = get_id
        self.username = username
        self.password = password
        self.Img2Base64 = base64
        self.faceid = faceid
        self.isAdmin = admin_status

    def __repr__(self):
        return '<User %s>' % self.id


class Come(db.Model):
    __tablename__ = 'comes'
    id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), nullable=False)
    ComeTime = db.Column(db.String(50), nullable=False)
    Img2Base64 = db.Column(db.Text)
    faceid = db.Column(db.Text)


    def __init__(self,get_id,user_id,ComeTime,face64,faceid):
        self.id = get_id
        self.user_id = user_id
        self.ComeTime = ComeTime
        self.Img2Base64 = face64
        self.faceid = faceid


    def __repr__(self):
        return '<Come %s>' % self.user_id


class Absent(db.Model):
    __tablename__ = 'absents'
    id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), nullable=False)
    info = db.Column(db.Text, nullable=False)
    absentTime = db.Column(db.String(50), nullable=False)
    reachTime = db.Column(db.String(50), nullable=False)
    applyTime = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(20), nullable=False)


    def __init__(self,get_id,user_id,info,abtime,retime,apptime,status):
        self.id = get_id
        self.user_id = user_id
        self.info = info
        self.absentTime = abtime
        self.reachTime = retime
        self.applyTime = apptime
        self.status = status


    def __repr__(self):
        return '<Absent %s>' % self.user_id


class Welcome(db.Model):
    __tablename__ = 'welcomes'
    id = db.Column(db.String(40), primary_key=True)
    time = db.Column(db.String(50), nullable=False)
    Img2Base64 = db.Column(db.Text)
    faceid = db.Column(db.Text)
    user_id = db.Column(db.String(40), nullable=True)

    def __init__(self,get_id,get_time,get_face64,get_faceid):
        self.id = get_id
        self.time = get_time
        self.Img2Base64 = get_face64
        self.faceid = get_faceid

    def __repr__(self):
        return '<Absent %s>' % self.id

class weekReport(db.Model):
    __tablename__ = 'weekReports'
    id = db.Column(db.String(40), primary_key=True)
    user_id = db.Column(db.String(40), nullable=False)
    week = db.Column(db.String(50), nullable=False)
    submit_time = db.Column(db.String(50), nullable=False)
    did = db.Column(db.Text)
    trouble = db.Column(db.Text)
    want = db.Column(db.Text)

    def __init__(self, get_id, user_id, get_week, get_subtime, get_did, get_trouble, get_want):
        self.id = get_id
        self.user_id = user_id
        self.week = get_week
        self.submit_time = get_subtime
        self.did = get_did
        self.trouble = get_trouble
        self.want = get_want

    def __repr__(self):
        return '<weekReport %s>' % self.id


class info(db.Model):
    __tablename__ = 'infos'
    id = db.Column(db.String(40), primary_key=True)
    info = db.Column(db.Text)
    location = db.Column(db.String(40))

    def __init__(self,get_id,get_info, get_loc):
        self.id = get_id
        self.info = info
        self.location = get_loc

    def __repr__(self):
        return '<info %s>' % self.id