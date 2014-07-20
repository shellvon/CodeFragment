  function apiController ($scope) {
        $scope.apis = [
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
                        'example':'shellvon',
                        'needed':true
                    },
                ]
            },
            {
                'name':"Stock/StockSync",
                'parameters':[
                    {
                        'value':'upc_code',
                        'example':'shellvon',
                        'needed':true
                    }
                ]
            }
            ];
        $scope.params=[
            {
                'text':'origin',
                'placeholder':"http://www.openapi.com/",
                'val':"http://www.openapi.com"
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
        $scope.postdata=[]

        $scope.getApi = function(apiname){
            var api;
            for (var i = $scope.apis.length - 1; i >= 0; i--) {
                if($scope.apis[i].name==apiname){
                    api = $scope.apis[i];
                    break;
                }
            };
            $scope.postdata = api.parameters;
            var keys = [],arr = api.parameters;
            for(i in arr){
                v = arr[i].value;
                keys.push(v);   
            }
            keys.push('client_id');
            keys.push('client_key');
            $scope.parameterList=keys;
            var origin  = jQuery("input[name=origin]").val();
            $scope.url = origin+"/"+api.name;
        }
        jQuery("#send").click(
            function() {
                var url = jQuery(this).attr('name');
                if(url==''){
                    alert("url empty!!");
                }
                console.log(url);
                var parameter = JSON.parse(jQuery('#parameter').val());
                var data = {}
                for( i in parameter){
                    v = jQuery("input[name="+parameter[i]+']"').val();
                    if(v!=''){
                        data[parameter[i]] = v;
                    }
                }
                console.log(data);
                var auth = jQuery("input[name=origin]").val()+"/Base1";
                console.log(auth);
                $.ajax({url:auth,data:data})
                    .done(
                        function(req){
                            data['sign'] = req;
                            $.ajax({url:url,data:data})
                                .done(
                                    function(req){
                                        $("#result").text(JSON.stringify(req));
                                        console.log(req);
                                    }
                                );
                        }
                    );
            });
    }
