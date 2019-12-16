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


function absent(){
    let info = document.getElementById("absent_info").value;
    let date = document.getElementById("absent_date").value;
    let rdate = document.getElementById("reach_date").value;
    $.ajax( {
        url:"/upload_api",
        type: "POST",
        data: {"api":"absent","info":info,"date":date,"rdate":rdate},
        dataType: "json",
        //processData:false,
        //contentType: false,

        success: function(data){
            if (data.status == "1"){
                alert("申请成功!");
                window.location.href="/";
            }else if(data.status == "-1"){
                alert("请输入理由和日期!");
            }else if(data.status == "-2"){
                alert("请假日期小于今天!");
            }else if(data.status == "-3"){
                alert("返回日期小于请假日期!");
            }
        },
        error: function(){
            alert("网络错误，请重试!");
        }
    });
    }

    function sign_show(){
        getMedia("video_sign")
        document.getElementById("modal-937647").click()
    }
    function sign(){
takePhoto("video_sign")
let canvas = document.getElementById("canvas");
//var username = document.getElementById("username").value;
//var password = document.getElementById("password").value;
var dataURL = canvas.toDataURL("image/jpeg");
dataURL = dataURL.replace("data:image/jpeg;base64,", "");
$.ajax( {
url:"/upload_api",
type: "POST",
data: {"faceid":dataURL,"api":"flag"},
dataType: "json",
//processData:false,
//contentType: false,

success: function(data){
    if (data.status == "1"){
        alert("签到成功!");
        window.location.href="/";
    }else if(data.status == "-1"){
        alert("请打开摄像头并将脸放于视频中间！");
    }else if(data.status == "-2"){
        alert("你今天已经签过到了!");
        window.location.href="/";
    }
},
error: function(){
    alert("网络错误，请重试!");
}
});
}

function show_sign_table(){
document.getElementById("modal-37746").click()
}

function show_week_table(){
document.getElementById("modal-213589").click()
}
function submit_week_report(){
    let did = document.getElementById("did").value;
    let trouble = document.getElementById("trouble").value;
    let want = document.getElementById("want").value;
    $.ajax( {
        url:"/upload_api",
        type: "POST",
        data: {"api":"week_report","did":did,"trouble":trouble,"want":want},
        dataType: "json",
        //processData:false,
        //contentType: false,

        success: function(data){
            if (data.status == "1"){
                alert("提交成功!");
                window.location.href="/";
            }else if(data.status == "-1"){
                alert("请输入完整！");
            }else if(data.status == "-2"){
                alert("本周已经提交过了！");
            }
        },
        error: function(){
            alert("网络错误，请重试!");
        }
    });
    }

    var dom = document.getElementById("one_info");
    var myChart = echarts.init(dom);
    var app = {};
    var get_data = {};
    $.ajax( {
        url:"/upload_api",
        type: "POST",
        data: {"api":"one_info"},
        dataType: "json",
        //async: false,
        //processData:false,
        //contentType: false,
    
        success: function(data){
            show_data(data.data)
        },
        error: function(){
            alert("获取个人数据失败！");
        }
    });
    
    function show_data(get_data){
    option = null;
    app.title = '环形图';
    
    option = {
    tooltip: {
        trigger: 'item',
        formatter: "{a} <br/>{b}: {c} ({d}%)"
    },
    legend: {
        orient: 'vertical',
        x: 'left',
        data:get_data.keys,
    },
    series: [
        {
            name:'签到情况',
            type:'pie',
            radius: ['50%', '70%'],
            avoidLabelOverlap: false,
            label: {
                normal: {
                    show: false,
                    position: 'center'
                },
                emphasis: {
                    show: true,
                    textStyle: {
                        fontSize: '30',
                        fontWeight: 'bold'
                    }
                }
            },
            labelLine: {
                normal: {
                    show: false
                }
            },
            data:get_data.values
        }
    ]
    };
    if (option && typeof option === "object") {
    myChart.setOption(option, true);
    window.onresize = function() {  
    myChart.resize();  
    };
    }
    }