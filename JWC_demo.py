#!encoding=utf-8
#! /usr/bin/env python

"""废品!!!"""

import requests
import re

class JWC(object):
	"""docstring for JWC"""

	def __init__(self, session,data):
		super(JWC, self).__init__()
		self.login_url = 'http://www.cuit.edu.cn/PassPort/Login.asp'
		self.jwc_url   = 'http://jwc.cuit.edu.cn/Jxgl/GetWindow.asp'
		self.main_url  = 'http://jwc.cuit.edu.cn/JXGL/Xs/MainMenu.asp'
		self.jwc_post_data  = {
			'WinW':1920,
			'WinH':1056,
			'RetAddr':'/Jxgl/UserPub/Login.asp?UTp=Xs',
			'Func':'Post',
		}
		self.user_info=None
		self.session = session
		self._init(data)
		
	def _init(self,post_data):
		self.session.post(self.jwc_url,self.jwc_post_data)
		content = self.get_page_content(self.main_url)
		try:
			self.session.get(re.findall('URL=([^"]+)',content)[0])
			req =  self.session.post(self.login_url,data=post_data)
			content = req.content.decode('gbk').encode('utf8')
			self.user_info 	= ','.join(re.findall(r'用户标识：<b>(\d+)</b>\(([^)]+)',content)[0])
		except:
			print 'Login Error'
	def get_session(self):
		return self.session

	def get_page_content(self,url):
		return self.session.get(url).content.decode('gbk').encode('utf8')
	
	def get_user_info(self):
		return self.user_info

	def save_picture(self,name):
		with open(name,'w') as f:
			f.write(obj.get_page_content('http://www.cuit.edu.cn/PassPort/GetZpPic.asp'))

	def get_score_with_html(self):
		pass

	def get_score_with_json(self):
		#parse the html data.
		pass
	def get_all_classes(self):
		pass
		
if __name__ == '__main__':
	username = ''
	userpass = ''
	post_data = {
		'Login':'Check',
		'txtId':username,
		'txtMM':userpass,
		'WinW':1920,
		'WinH':1056,
		'x':42,
		'y':16
	}
	obj = JWC(requests.Session(),post_data)
	#get user_info.
	#print obj.get_user_info()
	#print obj.get_page_content('http://jwc.cuit.edu.cn/JXGL/UserPub/GetCjByXh.asp?UTp=Xs')#score url.