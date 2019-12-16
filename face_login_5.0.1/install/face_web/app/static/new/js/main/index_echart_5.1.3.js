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
