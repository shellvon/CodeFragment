chrome.contextMenus.create({
    type: 'normal',
    title: '使用google翻译...',
    contexts: ['selection'],
    id:'shellvon',
    onclick:translate
});

/**https://developer.chrome.com/extensions/contextMenus*/
function translate (info,tab) {
	var url = 'http://translate.google.com.hk/#auto/zh-CN/'+info.selectionText;
	window.open(url,'_blank');
}


chrome.runtime.onMessage.addListener(function(message, sender, sendResponse){
    chrome.contextMenus.update('shellvon',{
        'title':'使用Google翻译“'+message+'”'
    });
});

