function getMedia(get_id) {
    let constraints = {
            video: {width: 500, height: 500},
            audio: false
    };
    //获得video摄像头区域
    let video = document.getElementById(get_id);
    //这里介绍新的方法，返回一个 Promise对象
    // 这个Promise对象返回成功后的回调函数带一个 MediaStream 对象作为其参数
    // then()是Promise对象里的方法
    // then()方法是异步执行，当then()前的方法执行完后再执行then()内部的程序
    // 避免数据没有获取到
    let promise = navigator.mediaDevices.getUserMedia(constraints);
    promise.then(function (MediaStream) {
            video.srcObject = MediaStream;
            video.play();
    });
}

function takePhoto(get_id) {
    //获得Canvas对象
    let video = document.getElementById(get_id);
    let canvas = document.getElementById("canvas");
    let ctx = canvas.getContext('2d');
    ctx.drawImage(video, 0, 0, 500, 500);
}

function login_show(){
    getMedia("video_login")
    document.getElementById("modal-213298").click()
}

function login(){
    takePhoto("video_login")
    let canvas = document.getElementById("canvas");
    //var username = document.getElementById("username").value;
    //var password = document.getElementById("password").value;
    var dataURL = canvas.toDataURL("image/jpeg");
    dataURL = dataURL.replace("data:image/jpeg;base64,", "");
    $.ajax( {
        url:"/upload_api",
        type: "POST",
        data: {"faceid":dataURL,"api":"login"},
        dataType: "json",
        //processData:false,
        //contentType: false,

        success: function(data){
                if (data.status == "1"){
                        window.location.href="/";
                }else if(data.status == "-1"){
                        alert("请打开摄像头并将脸放于视频中间！");
                }else if(data.status == "0"){
                        document.getElementById("modal-312795").click()
                }
        },
        error: function(){
            alert("服务器连接失败！");
        }
    });
}

function register_show(){
    getMedia("video_regist")
    document.getElementById("modal-581631").click()
}

function register(){
    takePhoto("video_regist")
    let canvas = document.getElementById("canvas");
    var username = document.getElementById("r_username").value;
    var password = document.getElementById("r_password").value;
    var dataURL = canvas.toDataURL("image/jpeg");
    dataURL = dataURL.replace("data:image/jpeg;base64,", "");
    $.ajax( {
    url:"/upload_api",
    type: "POST",
    data: {"username":username,"password":password,"faceid":dataURL,"api":"regist"},
    dataType: "json",
    //processData:false,
    //contentType: false,

    success: function(data){
        if (data.status == "1"){
            window.location.href="/";
        }else if(data.status == "-1"){
            alert("请打开摄像头并将脸放于视频中间！");
        }else if(data.status == "-2"){
            alert("该用户名已注册！");
        }else if(data.status == "-3"){
            alert("请保证用户和密码在6到18位之间！");
        }else if(data.status == "-4"){
            alert("用户名格式有误！");
        }
    },
    error: function(){
            alert("服务器连接失败！");
        }
    });
}

function login2(){
    let canvas = document.getElementById("canvas");
    var username = document.getElementById("l2_username").value;
    var password = document.getElementById("l2_password").value;
    var dataURL = canvas.toDataURL("image/jpeg");
    dataURL = dataURL.replace("data:image/jpeg;base64,", "");
    $.ajax( {
    url:"/upload_api",
    type: "POST",
    data: {"username":username,"password":password,"faceid":dataURL,"api":"login2"},
    dataType: "json",
    //processData:false,
    //contentType: false,

    success: function(data){
        if (data.status == "1"){
            window.location.href="/";
        }else if(data.status == "-1"){
            alert("请打开摄像头并将脸放于视频中间！");
        }else if(data.status == "-2"){
            alert("用户或密码错误！");
        }
    },
    error: function(){
            alert("服务器连接失败！");
        }
    });
}

function loginNoface(){
    var username = document.getElementById("l_username").value;
    var password = document.getElementById("l_password").value;
    $.ajax( {
    url:"/upload_api",
    type: "POST",
    data: {"username":username,"password":password,"api":"loginNoface"},
    dataType: "json",
    //processData:false,
    //contentType: false,

    success: function(data){
    if (data.status == "1"){
    window.location.href="/";
    }
    else if(data.status == "-2"){
    alert("用户或密码错误！");
    }
    },
    error: function(){
        alert("服务器连接失败！");
        }
    });
}