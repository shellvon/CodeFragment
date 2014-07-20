#coding:utf-8
"""
    下载豆瓣站点上的音乐~
"""
import urllib2
import threading
import re,time
import Queue

class PaserDouban(object):
    def __init__(self,url):
        self.re_name_pattern=r'(?:"name":"(.*?)")'
        self.re_url_list_pat=r'(?:"rawUrl":"(http:.*?\.mp3)")'
        self.data=self._get_data(url)
    def _get_data(self,url):
        if url.lower().find("site.douban.com")!=-1:
            try:
                data = urllib2.urlopen(url).read()
            except:
                print "url_不对！！！"
                pass
        else:
            print "不是豆瓣小站！！"
            data = None
        return data
    def get_name_list(self):
        name_list=re.findall(self.re_name_pattern,self.data)
        return name_list
    def get_url_list(self):
        url_list=re.findall(self.re_url_list_pat,self.data)
        if url_list:
            url_list=map(lambda x:''.join(x.split("\\")),url_list)
        return url_list

class MyThread(threading.Thread):
    def __init__(self,queue):
        threading.Thread.__init__(self)
        self.queue=queue
        self.start()
    def run(self):
        while True:
            try:
                print u"读取数据中...\n",
                func,args = self.queue.get(block=False)
                func(*args)
                self.queue.task_done()
            except:
                break
            
class DownloadManager(object):
    def __init__(self,thread_num,url_list,name_list):
        self.queue = Queue.Queue()
        self.threads=[]
        self.init_queue(url_list,name_list)
        self.init_pool(thread_num)
    def init_pool(self,thread_num):
        for i in range(thread_num):
            self.threads.append(MyThread(self.queue))
    def init_queue(self,url_list,name_list):
        for i,j in enumerate(url_list):
            self.queue.put((self.func,(j,name_list[i])))
    def func(self,url,name):
        try:
            print u"正在下载：%s\n"%name.decode('utf-8'),
            file = open(u"%s.mp3"%name.decode('utf-8'),"wb")
            data =urllib2.urlopen(url).read()
            file.write(data)
            file.close()
            print u"下载完成：%s\n"%name,
        except:
            print u"写入数据出错：%s!!!!\n"%name,
    def wait(self):
        for t in self.threads:
            if t.isAlive():
                t.join()

url_source = raw_input(u"请输入豆瓣小站的地址:")
test = PaserDouban(url_source)
print u"%s 首歌曲被搜索到，即将全部下载"%len(test.get_url_list())
print u"是否显示这些歌曲详细信息？(y/n):"
if raw_input().lower()=='y':
    list_1=test.get_url_list()
    list_2=test.get_name_list()
    for i,j in enumerate(list_1):
        print "="*80
        print "name:%s"%list_2[i].decode('utf-8')
        print "url:%s"%j
        print 
before = time.time()
download =DownloadManager(5,test.get_url_list(),test.get_name_list())
download.wait()
print u"全部下载完成，一共用时:%ss"%(time.time()-before)