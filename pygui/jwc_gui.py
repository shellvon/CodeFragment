# -*- coding:utf-8 -*- 
#! /usr/bin/env python
#
# GUI版本.
# 为了淡定更改一下main()即可切换为止使用JWC~这个类
# 用于选课或许更简单
"""
	To All:
		让加的UI已经加入。

	唉。代码很烂，这为了演示post数据这个简单的流程而已。
	大多数功能可以在后期加入，主要是文本的处理。比如获取课表/成绩等
	处理为json/html/txt的格式
	html处理的时候考虑过使用bs4[以前安装了].但是这学校的html太烂了。所以放弃。
	pyquery也考虑过。后来直接选择了regex.愿意写的请自己尝试。


	！！能命令行用就命令行啊！这UI有问题。。
	关于网络：
		请注意：一定要在内网。一定要在网络不拥挤的情况下使用
		如果要使用外网。可以在JWC.py里面，使用代理。
		代理的使用方式参考requests的文档。代理服务器在实验室的孩子
		可能可以为你提供。需要的话可以联系我。不会写代理的也可以找我。
		
	关于提前选课：
		a.因为当正在选课的时候。我曾使用while True 来一直登录最后post.但是这
		似乎是Dos攻击了。严重的是学校服务器在大量访问下会挂，所以我的抢课也是废物
		故而舍弃了之前的想法
		b.考虑过使用线程池。我没写。但是觉得服务器还是会挂。没意思。所以我想到了第三点
		提前选课
		即在学校公布选课的时候我们已经可以知道有哪些课可以提交，并更具以往经验来自己组装一个
		数据来提前post给服务器。因学校服务器关闭。测试需要在明年选课前的时候测试。

	关于界面：
		Tkinter 不是很会。不好撸ui啊。考虑过使用PyQt.但是因为不想使用太多第三方库放弃而放弃
"""
import Tkinter,ttk
import re
import requests
import urllib
import tkMessageBox
import thread
import threading
import webbrowser

class JWC_GUI_App(ttk.Frame):
	"""docstring for JWC_GUI_App"""
	def __init__(self,parent):
		ttk.Frame.__init__(self,parent)
		self.parent=parent
		self.parent.title('教务处评教GUI版')
		self.parent.geometry("300x200+400+400")
		self.style=ttk.Style()
		self.style.theme_use('default')
		self.username_entry = None
		self.password_entry = None 
		self.init_login_frame()
		self.pack(fill=Tkinter.BOTH,expand=True)
	def init_login_frame(self):
		global frame,login_btn,cancel_btn
		frame = ttk.Frame(self,relief=Tkinter.RAISED,borderwidth=1)
		frame.columnconfigure(0, pad=10)
		self.columnconfigure(1, pad=10)
		self.rowconfigure(0, pad=10)
		self.rowconfigure(1, pad=10)
		username_lb = Tkinter.Label(frame,text="用户名")
		password_lb = Tkinter.Label(frame,text="密  码")
		username_lb.grid(row=0, column=0)
		password_lb.grid(row=1,column=0)
		self.username_entry = Tkinter.Entry(frame)
		self.password_entry = Tkinter.Entry(frame,show='*')
		self.username_entry.focus_set()
		self.username_entry.grid(row=0,column=1)
		self.password_entry.grid(row=1,column=1)
		self.password_entry.bind('<Key-Return>',self.login_command)
		frame.pack(fill=Tkinter.BOTH,expand=True)
		login_btn=Tkinter.Button(self,text='登录',padx=5,pady=5,command=self.login_command)
		login_btn.pack(side=Tkinter.RIGHT)
		cancel_btn=Tkinter.Button(self,text='取消',padx=5,pady=5,command=self.cancel_command)
		cancel_btn.pack(side=Tkinter.RIGHT)
	def cancel_command(self):
		self.parent.destroy()
	def login_command(self,event=None):
		username = self.username_entry.get().strip()
		password = self.password_entry.get().strip()
		if not username or not password:
			tkMessageBox.showerror("Error", "密码和账号都得输入!")
			return
		post_data = {
			'Login':'Check',
			'txtId':username,
			'txtMM':password,
			'WinW':1920,
			'WinH':1056,
			'x':42,
			'y':16
		}
		def main_thread():
			global frame,login_btn,cancel_btn
			login_btn.config(state='disabled')
			obj = JWC(requests.Session(),post_data)#should be new thread.!Oh ..Shit.
			if obj.get_user_info():#remove old content and add a new content to display.
				frame.pack_forget()
				login_btn.pack_forget()
				cancel_btn.pack_forget()
				self.new_content(obj)
				self.parent.geometry("540x200")
			else:
				tkMessageBox.showerror('Error','登录失败，可能是服务器问题或者账户问题，请重试~')
			#thread.exit_thread()
			login_btn.config(state='normal')
		return main_thread()
		#return thread.start_new_thread(main_thread,())
		
	def pingjiao_command(self,obj,erea):#评教
		obj.pingjiao(erea)
	def help_command(self):
		tkMessageBox.showinfo("Info","建议使用命令行版的。此GUI功能太戳。单线程可能会死。所以在网络不拥挤等情况使用吧~")
	def link_command(self):
		webbrowser.open('https://github.com/shellvon/CodeFragment/blob/master/editer.py')
	def new_content(self,obj):

		frame = ttk.Frame(self,relief=Tkinter.RAISED,borderwidth=1)
		frame.columnconfigure(1, weight=1)
		frame.columnconfigure(3, pad=7)
		frame.rowconfigure(3, weight=1)
		frame.rowconfigure(5, pad=7)
		lbl = Tkinter.Label(frame, text="消息展示栏")
		lbl.grid(sticky=Tkinter.W, pady=4, padx=5)
		area = Tkinter.Text(frame,selectbackground='blue',selectforeground='gray')
		area.insert(1.0,"用户资料:%s\n"%obj.get_user_info())
		area.grid(row=1, column=0, columnspan=2, rowspan=4, padx=5, sticky=Tkinter.E+Tkinter.W+Tkinter.S+Tkinter.N)
		abtn = Tkinter.Button(frame, text="评教",command=lambda :self.pingjiao_command(obj,area))
		abtn.grid(row=1, column=4)
		hbtn = Tkinter.Button(frame, text="帮助",command=self.help_command)
		hbtn.grid(row=5, column=0, padx=5)
		sbtn = Tkinter.Button(frame, text="源码",command=self.link_command)
		sbtn.grid(row=2, column=4, padx=5)
		obtn = Tkinter.Button(frame, text="确定",command=self.cancel_command)
		obtn.grid(row=5, column=3)   

		photobtn = Tkinter.Button(frame, text="头像下载",command=obj.save_picture)
		photobtn.grid(row =1, column=3)

		score_download_btn= Tkinter.Button(frame,text="成绩下载",command=obj.get_score_with_html)
		score_download_btn.grid(row=2,column=3)

		choose_class_btn = Tkinter.Button(frame,text="提前选课",command=self.choose_classes_cmd)
		choose_class_btn.grid(row=3,columnspan=2,column=3)
		

		frame.pack(fill=Tkinter.BOTH,expand=True)
	def choose_classes_cmd(self):
		tkMessageBox.showinfo("info","请在正式选课之前查看好所压迫选择的课的课程代码等。然后使用命令行版本的jwc.py来完成。UI太尼玛难写了")

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
		#self._another_entry(data)

	def _another_entry(self,dic):
		url  = 'http://jwc.cuit.edu.cn/Jxgl/Login/xLogin/Login.asp'
		keyCode = re.findall("codeKey\s+=\s+'(\d+)'",self.session.get(url).content.decode('GBK').encode('utf8'))[0]
		verify_code_url='http://jwc.cuit.edu.cn/Jxgl/Login/xLogin/yzmDvCode.asp?k=%s&t=1403184545196'%keyCode
		#必须制定refer.不然该url不允许访问。
		req = self.session.get(verify_code_url,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36",'Referer':'http://jwc.cuit.edu.cn/Jxgl/Login/xLogin/Login.asp'})
		with open('fuck.png','a') as f:
			f.write(req.content)
		#可以使用pytester等OCR来验证这个验证码。这里人为识别我写起来就简单多了。哇哈哈
		vk = raw_input('ok,now you need to input your verify code:')
		dic['verifycode']=vk
		dic['keyCode']=keyCode
		req = self.session.post(url,dic)
		#print req.url.~。
		#判断是否为原始可以url.即可知道成功与否
		#如果这里登录成功后续一样。。

	def _init(self,post_data):
		req=self.session.post(self.jwc_url,self.jwc_post_data,headers={"User-Agent":"Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.114 Safari/537.36"})
		content = self.get_page_content(self.main_url)
		try:
			self.session.get(re.findall('URL=([^"]+)',content)[0])
			req =  self.session.post(self.login_url,data=post_data)
			content = req.content.decode('gbk','ignore').encode('utf8')
			self.user_info 	= ','.join(re.findall(r'用户标识：<b>(\d+)</b>\(([^)]+)',content)[0])
		except:
			self.user_info = None
	def get_session(self):
		return self.session

	def get_page_content(self,url):
		return self.session.get(url).content.decode('gbk','ignore').encode('utf8')
	
	def get_user_info(self):
		return self.user_info

	def save_picture(self,name="picture_photo"):
		with open(name,'w') as f:
			f.write(self.get_page_content('http://www.cuit.edu.cn/PassPort/GetZpPic.asp'))
		print 'ok~'
	def get_score_with_html(self):
		pass

	def get_score_with_json(self):
		#parse the html data.
		pass
	def get_all_classes(self,url):
		req = self.session.get(url)
		while req.status_code!=200:
			req = self.session.get(url)
			content = self.get_page_content(url)
		with open('hehe.html','a') as f:
			f.write(content)
		print 'save html in file.'
	def fuck_this_classes(self,url,data):
		#to post data to the url.
		req=self.session.post(url,data)
		while req.status_code!=200:#resp
			req=self.session.post(url,data)
		print req.content
	
	def choose_classes_(self,course_code=()):
		dic = self.make_xuanke_post_data()
		req = self.session.post(post_url,dic)
		print req.content.decode('GBK').encode('utf8')

	def make_xuanke_post_data(self):
		xuanke_url = 'http://jwc.cuit.edu.cn/Jxgl/Xs/kXk.asp?UTp=Xs'
		post_url = "http://jwc.cuit.edu.cn/Jxgl/Xs/kXkRs.asp"
		content = self.get_page_content(xuanke_url)
		#parse content to get classes_list,such as RsNum to make post data.
		#demo just for test
		dic={}
		dic['Xq'] = '20141'
		dic['DEL_87']='A'
		dic['RsNum']='89'
		dic['oldYc']=''
		dic['Kcdm_87']='2356'
		dic['Bjm_87']='软工111'.decode('utf8').encode('gbk')
		dic['Kcmc_87']='网络信息安全技术'.decode('utf8').encode('gbk')
		dic['Cxjs_87'] = '0'
		# print urllib.quote(dic['Bjm_87'])
		# print '%C8%ED%B9%A4111' #should be encode as this.
		return dic

	def pingjiao(self,eara=None):#不要这样写！太尼玛耦合了。
		pingjiao_url = "http://jwc.cuit.edu.cn/Jxgl/Xs/kXk.asp?Yc=Zs&UTp=Xs&Sp=pj"
		post_url = "http://jwc.cuit.edu.cn/Jxgl/Xs/XspjRs.asp"
		pre_fix_url="http://jwc.cuit.edu.cn/Jxgl/Xs/"
		re_url = '(xsPj.asp?[^>]+)'
		url_list = re.findall(re_url,self.get_page_content(pingjiao_url))
		err_lst=[]
		for i in url_list:
			url  = "%s%s"%(pre_fix_url,i)#获取到的url中get字符串有需要post的数据。所以需要在get_data中组成dict.
			dic	= self.get_data(self.get_page_content(url),i.split('?')[1])
			req = self.session.post(post_url,dic)
			course_name = urllib.unquote(dic['Kcmc']).decode('gbk','replace').encode('utf8')
			#判断当前url是否还是原始的url.因为Url后面的参数是无序的。所以我打算比较的是len
			#貌似有的部分url编码还是啥原因,比较url有点问题~所以。。。
			#所以假设状态码正常就评教正常算了
			if eara is None:
				continue
			eara.insert(Tkinter.END,"正在处理:%s\n"%course_name)
			if req.status_code!=200:
				eara.insert(Tkinter.END,"处理失败:%s"%course_name)
		if eara is not None:
			eara.insert(Tkinter.END,'为了确保评论成功。你最好自己上网看一看,状态是否为已评')
	def get_data(self,content,params):
		dic = {}
		dic['RsNum']=re.findall("RsNum.*?value=([^>]+)",content)[0]
		lst=params.split('&')
		for i in lst:
			k,v = i.split('=')
			dic[k]=urllib.unquote(v)
		for i in xrange(1,int(dic['RsNum'])+1):
			dic['Fz_%s'%i] = 'A'#全部评价为A
			dic['zw%s'%i]=''
		dic['canTj']=dic['Cxjs']=0
		dic['Yyjl'] = 'N'
		dic['Qtyj']=''
		return dic

if __name__ == '__main__':
	root = Tkinter.Tk()
	app = JWC_GUI_App(root)
	app.mainloop()