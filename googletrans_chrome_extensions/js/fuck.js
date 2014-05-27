/**...not work in chrome://(Not support this scheme..fuck...it's bug for me.)**/
window.onmouseup = function(){
	/*console.log('select sth');*/
    var selection = window.getSelection();
    if(selection.anchorOffset != selection.extentOffset){
        chrome.runtime.sendMessage(selection.toString().trim());
    }
}