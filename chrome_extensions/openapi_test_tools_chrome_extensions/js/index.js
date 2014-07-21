
// 改编自:http://stackoverflow.com/questions/4810841/how-can-i-pretty-print-json-using-javascript
function highlightJson(json) {
    json = json.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
    return json.replace(/("(\\u[a-zA-Z0-9]{4}|\\[^u]|[^\\"])*"(\s*:)?|\b(true|false|null)\b|-?\d+(?:\.\d*)?(?:[eE][+\-]?\d+)?)|[{},\[\]]/g, function (match) {
        var cls = 'number';
        if (/^"/.test(match)) {
            if (/:$/.test(match)) {
                match = match.slice(0, - 1) + '<span class="brace">:</span>';//如果是key,去掉冒号，然后让冒号也高亮
                cls = 'key';
            } else {
                cls = 'string';
            }
        } else if (/true|false/.test(match)) {
            cls = 'boolean';
        } else if (/null/.test(match)) {
            cls = 'null';
        }
        else{
            cls = 'brace';//比如 {}[]：，之类的。
        }
        return '<span class="' + cls + '">' + match + '</span>';
    });
}

var stk = [];//放递归生成的html,id等
//构建HTML tables.
function buildHtmlTable(json) {
   mktable(json,'panel-260100');
   for (var i = stk.length - 1; i >= 0; i--) {
       var html = stk[i].html;
       var id  = stk[i].id;
       $('#'+id).html(html);
   };
}
//生成tables.此函数为递归函数，构建出来放入stack中。
function mktable(json,id)
{
    var html ="";
    var th = "";
    var td = "";
    var cls = [
        'success',
        'danger',
        'warning',
        'info',
        ''
    ];
    var index = 4;
    $.each(json, function(key,val) {
        th +="<th>"+key+"</th>";
        if(key=='error'||key=='code'){
            switch(parseInt(val)){
                case 403:
                    index=1;//error
                break;
                case 0:
                    index=0;
                break;
                case 1:
                    index=1;
                break;
                case 2:
                    index =  2;
                break;
                default:
                    index = Math.floor(Math.random()*10)%4;
                break;
            }
        }
        if($.type(val)=='object'){
            mid = guid();
            td+="<td id='"+mid+"'></td>"
            mktable(val,mid);
        }
        else if(val instanceof Array){
        	for (var i = val.length - 1; i >= 0; i--) {
        		mid = guid();
            	td+="<td id='"+mid+"'></td>"
        		mktable(val[i],mid);
        	};
        }
        else
            td +="<td>"+val+"</td>"
    });
    html = '<thead><tr>'+th+"</tr><thead>";
    html += '<tbody><tr class="'+cls[index]+'">'+td+"</tr><tbody>";
    html ='<table id="'+id+'" class="table table-bordered table-hover table-condensed" border="1">'+html+'</table>';
    stk.push({'id':id,'html':html});
}
//http://stackoverflow.com/questions/105034/how-to-create-a-guid-uuid-in-javascript
var guid = (function() {
  function s4() {
    return Math.floor((1 + Math.random()) * 0x10000)
               .toString(16)
               .substring(1);
  }
  return function() {
    return s4() + s4() + '-' + s4() + '-' + s4() + '-' +
           s4() + '-' + s4() + s4() + s4();
  };
})();
//展示提示信息
function displayInfo (msg) {
        jQuery('#showinfo').text(msg).fadeIn(1000);
        function delay(){
            jQuery("#showinfo").fadeOut(1000);
        }
        window.setTimeout(delay,2000);
}

//根据api的名字更新api的参数信息，parameters应该为参数信息
//TODO暂未实现。
function updateDefaultApis(apiname,parameters){
    Parameters.updateDefaultApisJson(apiname,parameters);
}

//更新默认的参数信息，默认信息指 client_key,client_id,origin。
function updateDefaultParamers(parameters){
    var key_set = ['client_key','client_id','origin']
    var params = {}
    for (var i = key_set.length - 1; i >= 0; i--) {
        params[key_set[i]] = parameters[key_set[i]];
    };
    var ret = Parameters.updateDefaultParamsJson(params);
    if(ret){
        //displayInfo("已经帮你把参数更新到localStorage了. ^_^");
    }
    else{
        //因为第一次已经提示过了。就不再提示。
    }
}


//
//angluar.js中的controller定义
//
function apiController($scope) {
    
    $scope.apis = Parameters.loadParameter('default_apis');
    $scope.params = Parameters.loadParameter('default_params');
    if(!window.localStorage){
       displayInfo('Sorry,您的浏览器不支持localStorage.');
    }
    $scope.api = "";
    $scope.getApi = function(api){
        $scope.postdata=[]
        if(api==null){
            $scope.apiname="";
            return;
        }
        $scope.postdata = api.parameters;
        var keys = [],arr = api.parameters;
        for(i in arr){
            v = arr[i].value;
            keys.push(v);   
        }
        keys.push('client_id');
        keys.push('client_key');
        $scope.parameterList=keys;
        $scope.apiname = api.name;
    }
}


jQuery(function(){
    //按钮点击事件
    $("#send").click(
        function() {
            var that = this;
            $(that).addClass('disabled');
            var origin  = jQuery("input[name=origin]").val();
            var apiname = jQuery(this).attr('name');
            if(origin==''||apiname==''){//用户应该知道要做什么。所以都不判断算了。。
                alert("please choose api and enter the origin");
                $(that).removeClass('disabled');
                return;
            }
            var url = origin+"/"+apiname;
            var parameter = JSON.parse(jQuery('#parameter').val());
            var data = {};
            for( i in parameter){
                v = jQuery("input[name="+parameter[i]+']"').val();
                if(v!=''){
                    data[parameter[i]] = v;
                }
            }
            var tmpdata =data;
            tmpdata['origin'] = origin;
            updateDefaultParamers(tmpdata);//更新默认参数值

            var auth = origin+"/Base1";
            console.log('Auth URL:'+auth);//获取验证url.
            $.ajax({url:auth,data:data})
                .done(
                    function(res){
                        data['sign'] = res;
                        console.log('request url:'+url);
                        $.ajax({url:url,data:data})
                            .done(
                                function(res){
                                    //返回值可能不一定是json，所以我先try try...
                                    $(that).removeClass('disabled');
                                    console.log('response data:',res); 
                                    if($.type(res)!='object'){
                                        //清空上次的结果
                                        info = '<p class="text-center alert alert-info">错误返回，参见console.</p>'
                                        $("#panel-260100").html(info);
                                        $('#panel-74802').html(info);
                                        return;
                                    }
                                    //buildHtmlTable(res);
                                    $("#panel-260100").html('<p class="text-center alert alert-info">对不起,暂停该功能^_^.</p>')
                                    var json = JSON.stringify(res,null,'\t');
                                    html = '<pre id="result" class="col-md-12">'+highlightJson(json)+'</pre>';
                                    $("#panel-74802").html(html);
                                }
                            ).fail(function(){
                                $(that).removeClass('disabled');
                                alert("Sorry,Ajax excute errors");
                            });
                    }
                ).fail(function(){
                    $(that).removeClass('disabled');
                    alert("Sorry,Ajax excute errors.");
                });
        });
});
