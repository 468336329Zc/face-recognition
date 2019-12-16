import numpy as np
import math
from flask import jsonify
import flask_login
import time
import random

from .Library.face_recognition import face2vec
from .Library.face_recognition import faceAlign
from .Library.face_recognition import clustering
from .Library.pic_opreation import *
from .Library.sql import *

from .models import *

align_model = faceAlign.faceAlign()
face_model = face2vec.face2vec()



def regist_upload(request):
    return_data = {"api":'regist'}
    faceid=request.form.get("faceid")
    get_user = request.form.get("username")
    get_pwd = request.form.get("password")

    if not 6 <= len(get_user) <= 14 or not 6 <= len(get_pwd) <= 14:
        return_data["status"] = '-3'
        return return_data

    if "@" not in get_user:
        return_data["status"] = '-4'
        return return_data

    face_encoding = list()
    face_ids = list()
    face_encoding.append(np.asarray(base2Img(faceid)))
    face_encoding,rface_encoding = align_model.align_start(face_encoding)
    faceBase64 = list()
    if len(rface_encoding) < 1:
        return_data["status"] = '-1'
        return return_data
    
    for i in rface_encoding:
        faceBase64.append(image_to_base64(i))
    for i in range(len(face_encoding)):
        face_ids.append(i)
    
    nrof_images = len(face_encoding)
    nrof_batches = int(math.ceil(1.0*nrof_images / 100))
    emb_array = np.zeros((nrof_images, face_model.embedding_size))
    facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
    return_data["status"] = regist_insert(get_user,get_pwd,facial_encodings,faceBase64)
    return return_data


def login_upload(request):
    return_data = {"api":'login'}
    faceid=request.form.get("faceid")
    face_encoding = list()
    face_ids = list()
    face_encoding.append(np.asarray(base2Img(faceid)))
    face_encoding,rface_encoding = align_model.align_start(face_encoding)
    faceBase64 = list()
    if len(rface_encoding) < 1:
        return_data["status"] = '-1'
        return return_data
    
    for i in rface_encoding:
        faceBase64.append(image_to_base64(i))
    for i in range(len(face_encoding)):
        face_ids.append(i)
    
    nrof_images = len(face_encoding)
    nrof_batches = int(math.ceil(1.0*nrof_images / 100))
    emb_array = np.zeros((nrof_images, face_model.embedding_size))
    facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
    return_data["status"] = login_insert(facial_encodings,faceBase64)
    return return_data


def login2_upload(request):
    return_data = {"api":'login2'}
    faceid=request.form.get("faceid")
    get_user = request.form.get("username")
    get_pwd = request.form.get("password")

    face_encoding = list()
    face_ids = list()
    face_encoding.append(np.asarray(base2Img(faceid)))
    face_encoding,rface_encoding = align_model.align_start(face_encoding)
    faceBase64 = list()
    if len(rface_encoding) < 1:
        return_data["status"] = '-1'
        return return_data
    
    for i in rface_encoding:
        faceBase64.append(image_to_base64(i))
    for i in range(len(face_encoding)):
        face_ids.append(i)

    nrof_images = len(face_encoding)
    nrof_batches = int(math.ceil(1.0*nrof_images / 100))
    emb_array = np.zeros((nrof_images, face_model.embedding_size))
    facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
    return_data["status"] = login2_insert(get_user,get_pwd,facial_encodings,faceBase64)
    return return_data



def loginNoface_upload(request):
    return_data = {"api":'loginNoface'}
    get_user = request.form.get("username")
    get_pwd = request.form.get("password")

    return_data["status"] = loginNoface_insert(get_user,get_pwd)
    return return_data


def flag_upload(request):
    return_data = {"api":'flag'}
    faceid=request.form.get("faceid")
    face_encoding = list()
    face_ids = list()
    face_encoding.append(np.asarray(base2Img(faceid)))
    face_encoding,rface_encoding = align_model.align_start(face_encoding)
    faceBase64 = list()
    if len(rface_encoding) < 1:
        return_data["status"] = '-1'
        return return_data
    
    for i in rface_encoding:
        faceBase64.append(image_to_base64(i))
    for i in range(len(face_encoding)):
        face_ids.append(i)
    
    nrof_images = len(face_encoding)
    nrof_batches = int(math.ceil(1.0*nrof_images / 100))
    emb_array = np.zeros((nrof_images, face_model.embedding_size))
    facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
    return_data["status"] = flag_insert(facial_encodings,faceBase64)
    return return_data

def absent_upload(request):
    return_data = {"api":'absent'}
    info = request.form.get('info')
    date = request.form.get('date')
    rdate = request.form.get('rdate')
    if not info or not date:
        return_data["status"] = '-1'
        return return_data
    if not rdate:
        rdate = date
    return_data["status"] = absent_insert(info,date,rdate)
    return return_data


def absent_inspect(request):
    return_data = {"api":'absent_inspect'}
    get_user = flask_login.current_user
    if get_user.isAdmin != '1':
        return_data['status'] = '-1'
        return return_data
    abid = request.form.get('abid')
    op = request.form.get('op')
    return_data['status'] = absent_update(abid,op)
    return return_data


def welcome(request):
    return_data = {'api':'welcome'}
    video_pic = request.form.get('video_pic')
    face_encoding = list()
    face_ids = list()
    face_encoding.append(np.asarray(base2Img(video_pic)))
    face_encoding,rface_encoding = align_model.align_start(face_encoding)
    faceBase64 = list()
    if len(rface_encoding) < 1:
        return_data["status"] = '-1'
        return return_data
    
    for i in rface_encoding:
        faceBase64.append(image_to_base64(i))
    for i in range(len(face_encoding)):
        face_ids.append(i)
    
    nrof_images = len(face_encoding)
    nrof_batches = int(math.ceil(1.0*nrof_images / 100))
    emb_array = np.zeros((nrof_images, face_model.embedding_size))
    facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
    return_data['status'],return_data['account'],return_data['min_d'],return_data['known_person'] = welcome_insert(facial_encodings,faceBase64)
    return return_data

def index_view(request):
    return index_search()

def admin_view(request):
    get_date = request.args.get("date")
    if not get_date:
        get_date = '0'
    return admin_search(get_date)


def admin_stream_view(request):
    get_date = request.args.get("date")
    if not get_date:
        get_date = '0'
    try:
        get_page = int(request.args.get("page"))
        if not get_page or get_page < 1:
            get_page = 1
    except:
        get_page = 1
    return admin_stream_search(get_date,get_page)

def admin_cluster_view(request):
    get_date = request.args.get("date")
    if not get_date:
        today = int(time.time())
        today = time.localtime(today)
        now = time.strftime("%Y-%m-%d %H:%M:%S", today)
        get_date = now.split(" ")[0]
    
    faceids = admin_cluster_search_face(get_date)
    cluster_result = clustering.cluster_facial_encodings(faceids)
    result = {
        'count':0,
        'info':list(),
        'date':get_date
    }
    for i in cluster_result:
        result['info'].append(
            admin_cluster_search_one(i)
        )
    result['count'] = len(result['info'])
    return result

def download_enroll_info(request):
    return_data = {'api':'download_enroll_info'}
    get_start = request.args.get("start")
    get_end = request.args.get('end')
    if not get_start or not get_end:
        return_data['status'] = '没有输入正确的日期'
        return_data['data'] = {'title':[],'info':{}}
        return return_data
    return_data['status'] = '成功'
    return_data['data'] = download_enroll_search(get_start,get_end)
    return return_data


def status_view(request):
    return status_search()

def one_info(request):
    return_data = {'api':'one_info'}
    get_id = request.args.get("id")
    return_data['data'] = one_info_search(get_id)
    return return_data

def winner_view(request):
    return winner_search()

def index_week_report_view(request):
    return index_week_report_search()

def week_report_view(request):
    get_id = request.args.get("id")
    return week_report_search(get_id)

def week_report_upload(request):
    return_data = {'api':'week_report'}
    get_did = request.form.get("did")
    get_trouble = request.form.get("trouble")
    get_want = request.form.get("want")

    if not get_did or not get_trouble or not get_want:
        return_data['status'] = "-1"
        return return_data
    return_data['status'] = week_report_insert(get_did,get_trouble,get_want)
    return return_data

def week_report_change(request):
    return_data = {'api':'week_report_update'}
    get_id = request.form.get("id")
    get_did = request.form.get("did")
    get_trouble = request.form.get("trouble")
    get_want = request.form.get("want")

    if not get_did or not get_trouble or not get_want:
        return_data['status'] = "-1"
        return return_data

    return_data['status'] = week_report_update(get_id,get_did,get_trouble,get_want)
    return return_data
    
def admin_week_report_view(request):
    get_id = request.args.get("date")
    return admin_week_report_search(get_id)


def load_data(request):
    get_user = flask_login.current_user
    try:
        aaa = get_user.username
    except:
        return_data = {'api':'load'}
        return_data['status'] = "unlogin"
        return_data['info'] = ""
        return_data['status'] = 100
        return jsonify(return_data)

    sentence = ["少女祈祷中......","土豆服务器正在重启......","多等等说不定就能进去呢~","NM$L"]
    info = ["读取信息:%s"%(get_user.username),'正在获取图表数据......','正在生成图表......','正在生成主页......','正在进行最后的处理......']

    return_data = {'api':'load'}
    get_status = request.form.get('status')
    get_process = request.form.get('process')
    try:
        get_process = int(get_process)
    except:
        get_status = "loading"
        get_process = 0
    
    if request.cookies.get('next') == "reload":
        if get_process == 0:
            return_data['process'] = 15
            return_data['info'] = info[0]
            return_data['status'] = 'reload'
        elif get_process == 15:
            return_data['info'] = "使用缓存"
            return_data['process'] = 100
            return_data['status'] = 'reload'
            time.sleep(random.uniform(0.15,0.3))
        elif get_process == 100:
            return_data['process'] = 101
            return_data['info'] = "冲冲冲！"
            return_data['status'] = 'loaded'
            time.sleep(random.uniform(0.21,0.3))

    elif get_status == "loading":
        if 74 < get_process < 99:
            return_data['info'] = random.choice(sentence)
            return_data['process'] = 99
            return_data['status'] = 'loading'
            time.sleep(random.uniform(0.15,0.3))
        elif get_process == 99:
            return_data['info'] = "正在跳转到主页......"
            return_data['process'] = 100
            return_data['status'] = 'loading'
            time.sleep(random.uniform(0.51,0.6))
        elif get_process == 100:
            return_data['process'] = 101
            return_data['info'] = "冲冲冲！"
            return_data['status'] = 'loaded'
        elif get_process == 0:
            return_data['process'] = 15
            return_data['info'] = info[0]
            return_data['status'] = 'loading'
        elif get_process == 15:
            return_data['info'] = info[int(get_process/15)]
            return_data['process'] = get_process+15
            return_data['status'] = 'loading'
            time.sleep(random.uniform(0.51,0.6))
        else:
            return_data['info'] = info[int(get_process/15)]
            return_data['process'] = get_process+15
            return_data['status'] = 'loading'
            time.sleep(random.uniform(0.15,0.3))
    
    resp = jsonify(return_data)
    resp.set_cookie("next","%s"%(return_data['status']))
    return resp
        

def info_index_view(request):
    return jsonify(info_index_search())










'''def test():
    import math

    get_da = User.query.all()
    for i in get_da:
        faceid = i.Img2Base64
        face_encoding = list()
        face_ids = list()
        face_encoding.append(np.asarray(base2Img(faceid)))
        face_encoding,rface_encoding = align_model.align_start(face_encoding)


        for j in range(len(face_encoding)):
            face_ids.append(j)

        nrof_images = len(face_encoding)
        nrof_batches = int(math.ceil(1.0*nrof_images / 100))
        emb_array = np.zeros((nrof_images, face_model.embedding_size))
        facial_encodings = face_model.compute_facial_encodings(nrof_images,nrof_batches,emb_array,100,face_encoding,face_ids)
        i.faceid = str(facial_encodings[0].tolist())
        db.session.add(i)
        db.session.commit()'''

