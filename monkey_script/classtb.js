// ==UserScript==
// @name       get class table
// @namespace  https://github.com/shellvon
// @version    0.1
// @description  For CUIT Student~
// @include http://pkxt.cuit.edu.cn/classtb.asp*
// @require http://ajax.googleapis.com/ajax/libs/jquery/1.6.0/jquery.js
// @copyright  2012+, You
// ==/UserScript==

oArray0=Array("全部专业"

,"函授大气科学本"

,"函授气象应用技术专"

);

oArray1=Array("全部专业"

,"大气科学本科"

,"应用气象学"

);

oArray2=Array("全部专业"

,"电信（雷电）"

,"电信(应电)本科"

,"电子工程本(大气)"

,"电子工程本科(信息)"

,"电子信息工程(航电)"

,"电子信息科技本科"

,"雷电防护与科学"

,"生物医学工程本科"

);

oArray3=Array("全部专业"

,"公选"

);

oArray4=Array("全部专业"

,"材料物理本科"

,"电子科学与技术本科"

,"光信息科学与技术本科"

,"应用物理学本科"

);

oArray5=Array("全部专业"

,"计算机科学本科(计工)"

,"计算机科学本科(应用)"

,"计算机科学与技术本科"

,"数字媒体技术本科"

);

oArray6=Array("全部专业"

,"测控技术与仪器本科"

,"电气工程与自动化本科"

,"自动化（机电）"

,"自动化本科"

,"自动化本科(工业)"

,"自动化本科（数控）"

);

oArray7=Array("全部专业"

,"软件工程本科"

);

oArray8=Array("全部专业"

,"信息与计算科学本科"

,"应用数学本科"

);

oArray9=Array("全部专业"

,"通信工程本科"

,"微电子学本科"

);

oArray10=Array("全部专业"

,"大学英语3选修"

,"大学英语4选修"

,"英语本科"

);

oArray11=Array("全部专业"

,"对外汉语本科"

,"汉语国际教育"

,"汉语言文学本科"

,"社会工作本科"

,"视觉传达设计"

,"艺术设计本科"

);

oArray12=Array("全部专业"

,"网络工程本科"

,"物联网工程本科"

,"信安实验本科"

,"信息安全本科"

,"信息对抗技术"

);

oArray13=Array("全部专业"

,"3S集成与气象应用"

,"大气"

,"大气科学"

,"电子微系统工程"

,"电子与通信工程"

,"管理"

,"管理科学与工程"

,"环境工程"

,"环境科学与工程"

,"基础数学"

,"计算机技术"

,"计算机科学与技术"

,"计算机应用技术"

,"农业信息化"

,"农业资源利用"

,"气象探测技术"

,"软件工程"

,"商"

,"通信"

,"通信与信息系统"

,"统计"

,"统计学"

,"物联网技术"

,"信号与信息处理"

,"信息安全"

,"信息与通信工程"

,"应用经济学"

,"应用数学"

,"在职农推"

);

oArray14=Array("全部专业"

,"测绘工程本科"

,"地理信息系统本科"

,"环境工程本科"

,"环境科学本科"

,"遥感科学与技术本科"

);

var arrary = Array(oArray0,oArray1,oArray2,oArray3,oArray4,oArray5,oArray6,
  oArray7,oArray8,oArray9,oArray10,oArray11,oArray12,oArray13,oArray14); 

//alert("检测到可以使用了~~");

$('select[name="depart"]').change(function(){
    //var  item = $('select[name="depart"] option[selected]')
      var index   = $(this)[0].selectedIndex-1;
      var element = $('select[name="pro"]').empty();
      $.each(arrary[index], function(index, value) {
         element.append($("<option></option>").attr("value", value).text(value));
      });
});