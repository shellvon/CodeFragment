//
//初始化2个默认的json数据
//
var default_params=[
        {
            'text':'origin',
            'placeholder':"please enter the origin",
            'val':"http://openapi.ext.jumei.com"
        },
        {
            'text':"client_id",
            'placeholder':"please enter the client_id",
            'val':72
        },
        {
            'text':'client_key',
            'placeholder':'please enter the client_key',
            'val':'2ffd7cbdbe876867c987373f3d367f0f'
        }
    ];
var default_apis = [
        {
            'name':"Order/GetOrder",
            'parameters':[
                {
                    'value':'start_date',
                    'example':'2012-12-12 20:39:30',
                    'needed':false
                },
                {
                    'value':'end_date',
                    'example':'2012-12-12 20:39:30',
                    'needed':false
                },
                {
                    'value':'page',
                    'example':1,
                    'needed':true
                },
                {
                    'value':'page_size',
                    'example':1,
                    'needed':true
                }
            ]
        },
        {
            'name':"Order/GetOrderById",
            'parameters':[
                {
                    'value':'order_id',
                    'example':1,
                    'needed':true
                }
            ]
        },
        {
            'name':"Order/GetLogistics",
            'parameters':[

            ]
        },
        {
            'name':"Order/SetOrderStock",
            'parameters':[
                {
                    'value':'order_ids',
                    'example':'1,2,3,4',
                    'needed':true
                }
            ]
        },
        {
            'name':"Order/SetShipping",
            'parameters':[
                {
                    'value':'order_id',
                    'example':'1234',
                    'needed':true
                },
                {
                    'value':'logistic_id',
                    'example':'1234',
                    'needed':true
                },
                {
                    'value':'logistic_track_id',
                    'example':'a_string',
                    'needed':true
                },
            ]
        },
        {
            'name':"Stock/StockSync",
            'parameters':[
                {
                    'value':'upc_code',
                    'example':'a_string',
                    'needed':true
                },
                {
                    'value':'enable_num',
                    'example':'1234',
                    'needed':true
                }
            ]
        }
        ];
var Parameters = {}
Parameters.params = {
    'default_params':JSON.stringify(default_params),
    'default_apis':  JSON.stringify(default_apis)
    };

//更具指定的key载入制定的json数据，key只能为Parameters.params中定义的key.
//否者就是默认是要取基本信息，而不是api的参数信息
Parameters.loadParameter = function (key) {
    if(!(key in Parameters.params)){
        // 给定的key有问题。
        console.log('error key when loadParameter,set to default_params');
        key = 'default_params';
    }
    if(window.localStorage){
        if(localStorage.getItem(key)==null){
            localStorage.setItem(key,Parameters.params[key]);
        }
        return JSON.parse(localStorage.getItem(key));
    }
    return Parameters.params[key];
}

//更新默认的基本信息的json。传入的json
//中含有的信息包括client_key,client_id和对应的url.
Parameters.updateDefaultParamsJson = function(json){
    var oldjson = Parameters.loadParameter('default_params');
    for (var i = oldjson.length - 1; i >= 0; i--) {
        oldjson[i].val = json[oldjson[i].text];
    };
    return Parameters.updateParameter('default_params',oldjson);
}
//跟新api的参数信息，就目前而言
//暂时不用做。所以是空。
Parameters.updateDefaultApisJson = function(apiname,json){
    //pass
}

//更根据指定的key去更新指定的json数据。
Parameters.updateParameter = function(key,parameters){
    if(window.localStorage){
        localStorage.setItem(key,JSON.stringify(parameters));
        return true;
    }
    return false;
}