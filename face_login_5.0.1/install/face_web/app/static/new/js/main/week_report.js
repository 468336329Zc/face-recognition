function show_week_table(){
	document.getElementById("modal-852840").click()
}

function submit_week_report(get_id){
		let did = document.getElementById("did").value;
		let trouble = document.getElementById("trouble").value;
		let want = document.getElementById("want").value;
		$.ajax( {
			url:"/upload_api",
			type: "POST",
			data: {"api":"week_report_change","id":get_id ,"did":did,"trouble":trouble,"want":want},
			dataType: "json",
			//processData:false,
			//contentType: false,
	
			success: function(data){
				if (data.status == "1"){
					alert("提交成功!");
					location.reload();
				}else if(data.status == "-1"){
					alert("请输入完整！");
				}else if(data.status == "-2"){
					alert("非法修改！");
				}
			},
			error: function(){
				alert("网络错误，请重试!");
			}
		});
		}