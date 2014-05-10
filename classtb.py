 #encoding: utf-8
 #!/usr/bin/env python
 #Author shellvon
 #


import	urllib2
import	urllib
import cookielib
import re
from bs4 import BeautifulSoup
class SpiderToGetClassTable(object):
 	"""docstring for SpiderToGetClassTable"""
 	def __init__(self, arg={}):
 		super(SpiderToGetClassTable, self).__init__()
 		self.arg = arg
 		self.cookie = urllib2.HTTPCookieProcessor(cookielib.CookieJar())
 		self.opener = urllib2.build_opener(self.cookie)
 		urllib2.install_opener(self.opener)
 		self.stream = None
 		self.html = None
 		self.url = None
 		self.title = None
 		self.plain_data=None
 	def login(self,usr_data={}):
 		url = 'http://pkxt.cuit.edu.cn/showfunction.asp'
 		post_data = urllib.urlencode(usr_data)
 		req = urllib2.Request(url,post_data)
 		res = urllib2.urlopen(req)
 		body = res.read().decode('gb2312').encode('utf8')
 		if body.find('into')>-1:#login ok
 			post_data = urllib.urlencode(self.arg)
 			url = r'http://pkxt.cuit.edu.cn/showclasstb.asp'
 			req = urllib2.Request(url,post_data)
 			self.stream = urllib2.urlopen(req).read().decode('gb2312').encode('utf8')
 			print 'login ok'
 		else:
 			print 'login error'
 		return self

 	def parse(self):
 		url_set = re.findall('href=\"(.*?)\"',self.stream)
 		self.url = "http://pkxt.cuit.edu.cn/%s"%url_set[0]
 		#print url
 		self.stream = urllib2.urlopen(self.url).read().decode('gb2312').encode('utf8')
 		self.title = re.findall('<font[^>]+>(.*)<',self.stream,re.M)[0]
 		
 		table_tag = re.findall('<table[^>]+>.*?</table>',self.stream,re.M|re.I|re.S)#dot match all
 		soup = BeautifulSoup(table_tag[1],from_encoding="uft8")
		self.html = soup.prettify().encode('utf-8')
		rows=[]
		for row in soup.find_all('tr'):
			rows.append([val.text.encode('utf8') for val in row.find_all('td')])
		self.plain_data=rows
 		return self

 	def pprint_class_table(self):
 		pass

 	def get_title(self):
		return self.title

	def get_class_table(self):
		return self.html
	
	def get_plain_text(self):
		return self.plain_data
	def make_table(self,data):
		pass

	def make_json(self,data):
		pass

	def make_html(self,name):
		with open(name,'w') as f:
			f.write('<strong>%s</strong>\n'%self.title)
			f.write(self.html)
		print 'save file name with:%s in current workspace'%name
if __name__ == '__main__':
	#what the fuck
	class_info_to_post = {
					#'Area':u"本部".encode('gbk'),
					'mode':2,#the easy way
					'depart':u'软件工程学院'.encode('gbk'),
					'pro':u'软件工程本科'.encode('gbk'),
					'grade':u'2012级'.encode('gbk'),
					'class':u'03班'.encode('gbk'),
					'Submit':u'查  询'.encode('gbk'),
					}
	usr_data_to_post = {'user':'guest','passwd':'guest'};

	obj = SpiderToGetClassTable(class_info_to_post).login(usr_data_to_post).parse()
	obj.make_html(name="test.html")