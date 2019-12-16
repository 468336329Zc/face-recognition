from app import app
from flask import url_for, request, redirect, render_template,jsonify,current_app,make_response
import flask_login
from . import apis




@app.route('/favicon.ico')
def favicon():
    return current_app.send_static_file('favicon.ico')



@app.route('/')
@flask_login.login_required
def index(): 
    if not ifload():
        return redirect(url_for("load"))
    show_result = apis.index_view(request)
    show_result['winnerData'] = apis.winner_view(request)
    show_result['week_report'] = apis.index_week_report_view(request)
    resp = make_response(render_template('index.html',myData = show_result))
    resp.set_cookie('next','reload')
    return resp


@app.route('/load')
def load():
    return render_template('load.html')


def admin_no():
    result = {
        "main":"爪巴",
        "title":"滚出克！",
        "content":"给👴爪巴",
        'url':url_for('index'),
        'butten':"我自己滚",
    }
    return render_template('model.html',myData=result)


def ifload():
    get_p = request.cookies.get('next')
    if get_p == 'loaded':
        return True
    else:
        False


@app.route('/admin')
@flask_login.login_required
def admin(): 
    get_user = flask_login.current_user
    if get_user.isAdmin != '1':
        return admin_no()

    show_result = apis.admin_view(request)
    show_result['week_report'] = apis.admin_week_report_view(request) 
    return render_template('admin.html',myData = show_result)


@app.route('/admin/stream')
@flask_login.login_required
def admin_stream():
    get_user = flask_login.current_user
    if get_user.isAdmin != '1':
        return admin_no()
    show_result = apis.admin_stream_view(request)
    return render_template('admin_stream.html',myData = show_result)

@app.route('/admin/cluster')
@flask_login.login_required
def admin_cluster():
    get_user = flask_login.current_user
    if get_user.isAdmin != '1':
        return admin_no()
    show_result = apis.admin_cluster_view(request)
    return render_template('admin_cluster.html',myData = show_result)

@app.route('/download/id/1')
@flask_login.login_required
def enroll_form():
    show_result = apis.download_enroll_info(request)
    return render_template('form.html',myData = show_result)



@app.route('/login')
def login():
    lang = request.args.get('lang')
    if lang == "jp":
        resp = make_response(render_template('login_jp.html'))
        resp.delete_cookie('next')
        return resp
    resp = make_response(render_template('login.html'))
    resp.delete_cookie('next')
    return resp



@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    result = {
        "main":"登出",
        "title":"登出成功！",
        "content":"点击下面的按钮回到登录界面",
        'url':url_for('index'),
        'butten':"我手滑了，让我重新登录~",
    }
    return render_template('model.html',myData=result)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route("/weekReort")
def week_report_view():
    show_result = apis.week_report_view(request)
    return render_template("week_report.html", myData = show_result)


@app.route('/status')
def status(): 
    show_result = apis.status_view(request)
    return render_template('status.html',myData = show_result)


@app.route('/upload_api',methods=['POST'])
def api():
    get_user = flask_login.current_user
    if get_user:
        if request.form.get('api'):
            callback = route_api.get(request.form.get('api'))
            return jsonify(
                callback(request)
            )
        else:
            if request.form.get('api'):
                callback = route_api_no_login.get(request.form.get('api'))
                return jsonify(
                    callback(request)
                )


route_api_no_login = {
    'login':apis.login_upload,
    'login2':apis.login2_upload,
    'loginNoface':apis.loginNoface_upload,
    'welcome':apis.welcome,
}


route_api = {
    'regist':apis.regist_upload,
    'login':apis.login_upload,
    'login2':apis.login2_upload,
    'loginNoface':apis.loginNoface_upload,
    'flag':apis.flag_upload,
    'absent':apis.absent_upload,
    'absent_inspect':apis.absent_inspect,
    'welcome':apis.welcome,
    'one_info':apis.one_info,
    'week_report':apis.week_report_upload,
    'week_report_change':apis.week_report_change,
}


@app.route('/upload_api_new',methods=['POST'])
def api_new():
    get_user = flask_login.current_user
    if get_user:
        if request.form.get('api'):
            callback = route_api_new.get(request.form.get('api'))
            return callback(request)
        else:
            if request.form.get('api'):
                callback = route_api_no_login_new.get(request.form.get('api'))
                return callback(request)


route_api_no_login_new = {

}


route_api_new = {
    'load':apis.load_data,
    'info_index':apis.info_index_view,
}


@app.route('/test')
def test():
    #apis.test()
    return "少女祈祷中..."
