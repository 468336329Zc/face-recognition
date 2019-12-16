from ..models import *
import flask_login
import uuid
import json
import numpy as np
import time
import datetime
from sqlalchemy import and_


from ..Library.face_recognition import distance


DISTANCE_LIMIT = 0.69
MOVE_DISTANCE_LIMIT = 0.72


def index_search():
    today = datetime.date.today() 
    oneday = datetime.timedelta(days=1) 
    get_date = today-oneday 

    sign_list = list()
    absent_list = list()
    get_user = flask_login.current_user
    get_come = Come.query.filter_by(user_id = get_user.id).order_by(Come.ComeTime.desc()).limit(5).all()
    yesterday_count = Come.query.filter(Come.ComeTime.like("%s%%"%(get_date))).count()
    for i in get_come:
        one = dict()
        one['time'] = i.ComeTime
        one['face'] = i.Img2Base64
        sign_list.append(one)
    get_absent = Absent.query.filter_by(user_id = get_user.id).order_by(Absent.applyTime.desc()).limit(10).all()
    for i in get_absent:
        one = {
            'id':i.id,
            'info':i.info,
            'abtime':i.absentTime,
            'retime':i.reachTime,
            'apptime':i.applyTime,
            'status':i.status,
        }
        absent_list.append(one)
    result = {
        'sign':sign_list,
        'absent':absent_list,
        'count':yesterday_count,
    }
    return result


def admin_search(get_date):
    if get_date == '0':
        today = int(time.time())
        today = time.localtime(today)
        now = time.strftime("%Y-%m-%d %H:%M:%S", today)
        get_date = now.split(" ")[0]
    get_come = Come.query.filter(Come.ComeTime.like("%s%%"%(get_date))).order_by(Come.ComeTime.desc()).all()
    get_absent = Absent.query.filter(and_(and_(Absent.absentTime <= get_date,Absent.reachTime >= get_date),Absent.status == "通过")).order_by(Absent.applyTime.desc()).all()
    #get_absent = get_absent.query.filter(Absent.status == "通过").all()
    inspect_absent = Absent.query.filter(Absent.status == "待审核").order_by(Absent.applyTime.asc()).all()
    result = dict()
    come_list = list()
    absent_list = list()
    inspect_list = list()
    for i in get_come:
        one = dict()
        get_user = User.query.filter_by(id = i.user_id).first()
        one['name'] = get_user.username
        one['time'] = i.ComeTime
        one['face'] = i.Img2Base64
        come_list.append(one)
    for i in get_absent:
        one = dict()
        get_user = User.query.filter_by(id = i.user_id).first()
        one['name'] = get_user.username
        one['face'] = get_user.Img2Base64
        one['info'] = i.info
        one['retime'] = i.reachTime
        absent_list.append(one)
    for i in inspect_absent:
        one = dict()
        get_user = User.query.filter_by(id = i.user_id).first()
        one['id'] = i.id
        one['name'] = get_user.username
        one['face'] = get_user.Img2Base64
        one['info'] = i.info
        one['abtime'] = i.absentTime
        one['retime'] = i.reachTime
        inspect_list.append(one)

    result['sign'] = come_list
    result['absent'] = absent_list
    result['inspect'] = inspect_list
    return result

def admin_stream_search(get_date,page):
    result = {
        'count':0,
        'info':list(),
    }
    page_size = 10
    if get_date == '0':
        today = int(time.time())
        today = time.localtime(today)
        now = time.strftime("%Y-%m-%d %H:%M:%S", today)
        get_date = now.split(" ")[0]

    get_stream = Welcome.query.filter(Welcome.time.like("%s%%"%(get_date))).order_by(Welcome.time.desc()).limit(page_size).offset((page-1)*page_size)
    today_count = Welcome.query.filter(Welcome.time.like("%s%%"%(get_date))).count()
    for i in get_stream:
        if i.user_id:
            get_user = User.query.filter_by(id = i.user_id).first()
            one = {
                'face64':i.Img2Base64,
                'time':i.time,
                'name':get_user.username
            }
        else:
            one = {
                'face64':i.Img2Base64,
                'time':i.time,
                'name':'new'
            }
        result['info'].append(one)
    result['count'] = today_count
    result['page'] = page
    result['date'] = get_date
    result['max_page'] = int(today_count/page_size)+1
    return result

def admin_cluster_search_face(get_date):
    if get_date == '0':
        today = int(time.time())
        today = time.localtime(today)
        now = time.strftime("%Y-%m-%d %H:%M:%S", today)
        get_date = now.split(" ")[0]

    get_stream = Welcome.query.filter(Welcome.time.like("%s%%"%(get_date))).all()
    face_in_database = dict()
    for i in get_stream:
        face_in_database[i.id] = np.array(json.loads(i.faceid))
  
    return face_in_database


def admin_cluster_search_one(get_ids):
    flag = 0
    result = {}
    for get_id in get_ids:
        if flag == 1:
            return result
        get_one = Welcome.query.filter_by(id = get_id).first()
        if get_one.user_id:
            get_user = User.query.filter_by(id = get_one.user_id).first()
            result = {
                'face64':get_one.Img2Base64,
                'time':get_one.time,
                'name':get_user.username,
            }
            flag = 1
        else:
            result = {
                'face64':get_one.Img2Base64,
                'time':get_one.time,
                'name':'new',
            }
    return result
    

def regist_insert(gwt_user, get_pwd, face_encodings,base64s):
    check_user = User.query.filter_by(username = gwt_user).first()
    if check_user:
        return "-2"
    
    hasUser = User.query.first()
    if not hasUser:
        get_id = "".join(str(uuid.uuid1()).split('-'))
        newUser= User(
            get_id,
            gwt_user,
            get_pwd,
            base64s[0],
            str(face_encodings[0].tolist()),
            '1'
        )
        flask_login.login_user(newUser)
        db.session.add(newUser)
        db.session.commit()
        return "1"
    else:
        get_id = "".join(str(uuid.uuid1()).split('-'))
        newUser= User(
            get_id,
            gwt_user,
            get_pwd,
            base64s[0],
            str(face_encodings[0].tolist()),
            '0'
        )
        flask_login.login_user(newUser)
        db.session.add(newUser)
        db.session.commit()
        return "1"



def login_insert(face_encodings,base64s):
    face_in_database = list()
    database = User.query.all()
    for i in database:
        face_in_database.append(json.loads(i.faceid))
    face_in_database = np.array(face_in_database)
    for j in range(len(face_encodings)):
        try:
            result = distance.face_distance_cos(face_encodings[j],face_in_database)
        except:
            result = list()
        flag = list()
        for k in range(len(result)):
            if result[k] < DISTANCE_LIMIT:
                flag.append(int(k))
        
        if len(flag) == 1:
            get_user = database[flag[0]]
            get_user.Img2Base64 = base64s[j]
            get_user.faceid = str(face_encodings[j].tolist())
            flask_login.login_user(get_user)
            db.session.add(get_user)
            db.session.commit()
            return '1'
        else:
            return "0"

def login2_insert(gwt_user, get_pwd, face_encodings,base64s):
    check_user = User.query.filter_by(username = gwt_user).first()
    if not check_user:
        return "-2"
    if check_user.password != get_pwd:
        return "-2"
    
    for j in range(len(face_encodings)):
        get_user = check_user
        get_user.Img2Base64 = base64s[j]
        get_user.faceid = str(face_encodings[j].tolist())
        flask_login.login_user(get_user)
        db.session.add(get_user)
        db.session.commit()
        return '1'


def loginNoface_insert(get_user,get_pwd):
    check_user = User.query.filter_by(username = get_user).first()
    if not check_user:
        return "-2"
    if check_user.password != get_pwd:
        return "-2"
    
    flask_login.login_user(check_user)
    return "1"


def flag_insert(face_encodings,base64s):
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = now.split(" ")[0]
    for j in range(len(face_encodings)):
        get_user = flask_login.current_user
        get_come = Come.query.filter_by(user_id = get_user.id).order_by(Come.ComeTime.desc()).first()
        if get_come:
            get_time = get_come.ComeTime.split(" ")[0]
        else:
            get_time = '0'
        if today == get_time:
            return "-2"
        else:
            newCome = Come(
                "".join(str(uuid.uuid1()).split('-')),
                get_user.id,
                now,
                base64s[j],
                str(face_encodings[j].tolist())
            )
            db.session.add(newCome)
            db.session.commit()
            return '1'


def absent_insert(info,date,rdate):
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = now.split(" ")[0]

    c_today = int("".join(today.split("-")))
    c_date = int("".join(date.split("-")))
    c_rdate = int("".join(rdate.split("-")))
    if c_rdate < c_date:
        return "-3"
    if c_today > c_date:
        return "-2"
    get_user = flask_login.current_user
    creat_absent = Absent(
        "".join(str(uuid.uuid1()).split('-')),
        get_user.id,
        info,
        date,
        rdate,
        now,
        "待审核",
    )
    db.session.add(creat_absent)
    db.session.commit()
    return '1'


def absent_update(abid,op):
    get_absent = Absent.query.filter(Absent.id == abid).first()
    if op == '1':
        get_absent.status = '通过'
    if op == '-1':
        get_absent.status = '拒绝'
    db.session.add(get_absent)
    db.session.commit()
    return '1'


def welcome_insert(face_encodings,base64s):
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)

    face_in_database = list()
    database = User.query.all()
    for i in database:
        face_in_database.append(json.loads(i.faceid))
    face_in_database = np.array(face_in_database)
    min_distance_list = list()
    known_person = list()
    for j in range(len(face_encodings)):
        try:
            result = distance.face_distance_cos(face_encodings[j],face_in_database)
        except:
            result = list()
        if result.any():
            result = np.array(result)
            min_distance_list.append(result.min())
            if result.min() < MOVE_DISTANCE_LIMIT:
                flag = np.argwhere(result == result.min())[0][0]
            else:
                flag = -1
        else:
            flag = -1
        
        if flag != -1:
            new_one = Welcome(
                "".join(str(uuid.uuid1()).split('-')),
                now,
                base64s[j],
                str(face_encodings[j].tolist())
            )
            get_user = database[flag]
            new_one.user_id = get_user.id 
            db.session.add(new_one)
            db.session.commit()
            known_person.append(get_user.username)
        else:
            new_one = Welcome(
                "".join(str(uuid.uuid1()).split('-')),
                now,
                base64s[j],
                str(face_encodings[j].tolist())
            )
            db.session.add(new_one)
            db.session.commit()
    return '1',str(len(base64s)),min_distance_list,known_person



def download_enroll_search(start,end):
    result = dict()
    info = dict()
    datestart=datetime.datetime.strptime(start,'%Y-%m-%d')
    dateend=datetime.datetime.strptime(end,'%Y-%m-%d')
    date_list = []
    date_list.append(datestart.strftime('%Y-%m-%d'))
    while datestart<dateend:
        datestart+=datetime.timedelta(days=+1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    
    get_user = flask_login.current_user
    if get_user.isAdmin != '1':
        get_user = User.query.filter(User.id == get_user.id).all()
    else:
        get_user = User.query.all()
    for i in get_user:
        info[i.username] = list()
        for j in date_list:
            get_come = Come.query.filter(and_(Come.ComeTime.like("%s%%"%(j)),Come.user_id==i.id)).first()
            if not get_come:
                get_absent = Absent.query.filter(and_(and_(Absent.absentTime <= j,Absent.reachTime >= j),Absent.user_id == i.id)).first()
                if get_absent:
                    if get_absent.status == "通过":
                        info[i.username].append(
                            {
                                'date':j,
                                'status':"请假通过",
                                'time':''
                            }
                        )
                    else:
                        info[i.username].append(
                            {
                                'date':j,
                                'status':"请假拒绝",
                                'time':''
                            }
                        )
                else:
                    info[i.username].append(
                            {
                                'date':j,
                                'status':"无故缺席",
                                'time':''
                            }
                        )
            else:
                info[i.username].append(
                            {
                                'date':j,
                                'status':"已签到",
                                'time':get_come.ComeTime.split(' ')[1]
                            }
                        )
    result['title'] = date_list
    result['info'] = info
    return result

def status_search():
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = now.split(" ")[0]

    datestart=datetime.datetime.strptime(today,'%Y-%m-%d')
    date_list = []
    for _ in range(7):
        datestart+=datetime.timedelta(days=-1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    date_list = date_list[::-1]
    
    count_list = list()
    for i in date_list:
        count_list.append(
            Come.query.filter(Come.ComeTime.like("%s%%"%(i))).count()
        )
    
    return {
        'title':date_list,
        'count':count_list
    }


def one_info_search(get_id):
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = now.split(" ")[0]

    datestart=datetime.datetime.strptime(today,'%Y-%m-%d')
    date_list = []
    for _ in range(30):
        datestart+=datetime.timedelta(days=-1)
        date_list.append(datestart.strftime('%Y-%m-%d'))
    date_list = date_list[::-1]

    result = {
        'keys':['出勤','请假','缺席'],
    }
    result['values'] = [
        {'name':result['keys'][0],'value':0},
        {'name':result['keys'][1],'value':0},
        {'name':result['keys'][2],'value':0},
    ]

    get_user = flask_login.current_user
    get_user = User.query.filter(User.id == get_user.id).all()
    for i in get_user:
        for j in date_list:
            get_come = Come.query.filter(and_(Come.ComeTime.like("%s%%"%(j)),Come.user_id==i.id)).first()
            if not get_come:
                get_absent = Absent.query.filter(and_(and_(Absent.absentTime <= j,Absent.reachTime >= j),Absent.user_id == i.id)).first()
                if get_absent:
                    if get_absent.status == "通过":
                        result['values'][1]['value'] += 1
                    else:
                        result['values'][2]['value'] += 1
                else:
                    result['values'][2]['value'] += 1
            else:
                result['values'][0]['value'] += 1
    return result

def winner_search():
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = now.split(" ")[0]

    datestart=datetime.datetime.strptime(today,'%Y-%m-%d')
    datestart+=datetime.timedelta(days=-1)
    get_date = datestart.strftime('%Y-%m-%d')
    get_come = Come.query.filter(Come.ComeTime.like("%s%%"%(get_date))).order_by(Come.ComeTime.desc()).all()
    result = dict()
    come_list = list()

    flag = 0
    win = ["冠军","亚军","季军"]
    for i in get_come:
        one = dict()
        get_user = User.query.filter_by(id = i.user_id).first()
        one['name'] = get_user.username
        one['time'] = i.ComeTime
        one['win'] = win[flag]
        come_list.append(one)
        flag += 1
        if flag >= 3:
            break

    result['sign'] = come_list
    return result

def index_week_report_search():
    get_user = flask_login.current_user
    get_report = weekReport.query.filter_by(user_id = get_user.id).order_by(weekReport.week.desc()).limit(5).all()
    result = list()
    for i in get_report:
        result.append(
            {
                'id':i.id,
                'subtime':i.submit_time,
                'week':i.week
            }
        )
    return result

def week_report_search(get_id):
    get_user = flask_login.current_user
    get_user = flask_login.current_user
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = "".join(now.split(" ")[0].split('-'))
    get_week = "%s-%s"%(today[:4],datetime.datetime.strptime(today,"%Y%m%d").strftime("%W"))

    get_report = weekReport.query.filter(and_(weekReport.id==get_id,weekReport.user_id==get_user.id)).first()
    if get_report:
        return {
            'id' : get_report.id,
            'did' : get_report.did,
            'trouble' : get_report.trouble,
            'want' : get_report.want,
            'week': get_report.week,
            'this_week':get_week,
        }
    else:
        return {
            'id' : "非法访问！",
            'did' : "非法访问！",
            'trouble' : "非法访问！",
            'want' : "非法访问！",
            'week': "非法访问！",
            'this_week':get_week,
        }

def week_report_insert(get_did, get_trouble, get_want):
    get_user = flask_login.current_user
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = "".join(now.split(" ")[0].split('-'))
    get_week = "%s-%s"%(today[:4],datetime.datetime.strptime(today,"%Y%m%d").strftime("%W"))

    get_report = weekReport.query.filter(and_(weekReport.week==get_week,weekReport.user_id==get_user.id)).first()
    if get_report:
        return '-2'
    
    new_report = weekReport(
        "".join(str(uuid.uuid1()).split('-')),
        get_user.id,
        get_week,
        now,
        get_did,
        get_trouble,
        get_want
    )
    db.session.add(new_report)
    db.session.commit()
    return '1'

def week_report_update(get_id, get_did, get_trouble, get_want):
    get_user = flask_login.current_user
    today = int(time.time())
    today = time.localtime(today)
    now = time.strftime("%Y-%m-%d %H:%M:%S", today)
    today = "".join(now.split(" ")[0].split('-'))
    get_week = "%s-%s"%(today[:4],datetime.datetime.strptime(today,"%Y%m%d").strftime("%W"))

    get_user = flask_login.current_user
    get_report = weekReport.query.filter(and_(weekReport.id==get_id,weekReport.user_id==get_user.id)).first()
    if get_report.week == get_week:
        get_report.did = get_did
        get_report.trouble = get_trouble
        get_report.want = get_want
        db.session.add(get_report)
        db.session.commit()
        return "1"
    else:
        return "-2"

def admin_week_report_search(get_date):
    if not get_date:
        today = int(time.time())
        today = time.localtime(today)
        get_date = time.strftime("%Y-%m-%d %H:%M:%S", today)

    today = "".join(get_date.split(" ")[0].split('-'))
    get_week = "%s-%s"%(today[:4],datetime.datetime.strptime(today,"%Y%m%d").strftime("%W"))

    get_report = weekReport.query.filter_by(week = get_week).all()
    result = list()
    for i in get_report:
        get_user = User.query.filter_by(id = i.user_id).first()
        result.append(
            {
                'name':get_user.username,
                'subtime':i.submit_time,
                'week':i.week,
                'did' : i.did,
                'trouble' :i.trouble,
                'want' : i.want,
            }
        )
    return {
        'info':result,
        'week':get_week,
    }

def info_index_search():
    get_info = info.query.filter_by(location = "index").first()
    if get_info:
        return {
            'info':get_info.info,
            'status':'1'
        }
    else:
        return {
            'info':"",
            'status':'0'
        }
