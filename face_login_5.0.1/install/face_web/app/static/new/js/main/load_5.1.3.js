function change(number,title){
	var inp=document.getElementById("load_%"); 
	var inp2=document.getElementById("title_%"); 
	inp.setAttribute("style","width:"+number+"%");
	inp2.innerHTML = title
}

function load_apply(number,status){
    console.log(number)
    $.ajax( {
        url:"/upload_api_new",
        type: "POST",
        data: {"api":"load",'status':status,'process':number},
        dataType: "json",
        //processData:false,
        //contentType: false,
    
        success: function(data){
            if (data.status == "loading" || data.status == "reload"){
                change(data.process,data.info);
                load_apply(data.process,data.status);
            }else if (data.status == "unlogin"){
                change(15,"你都没登录，加载个锤子。。。。。。");
            }else if (data.status == "loaded"){
                window.location.href="/";
            }else{
                change(data.process,"参数错误！");
            }
        },
        error: function(){
                var inp2=document.getElementById("title_%"); 
	            inp2.innerHTML = "登录失败，请刷新重试！"
            }
        });
}

load_apply(0,'loading')