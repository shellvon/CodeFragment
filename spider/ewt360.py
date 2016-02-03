# encoding=utf8
# author:shellvon

"""抓取study.ewt360.com中的高中视频教育资源

由于版权原因没有下载地址，故分析其网页源代码得知使用了rtmp协议传输视频
步骤：
1.登录 function => login
2.通过科目关键字抓取该科目的URL => getTypeUrlByKeyword(keyword)
3.通过科目URL获取课程URL => getLessonsByType
4.通过课程URL抓取对应课程的视屏URL => getLessionDetailsByUrl(sub_url)
5.通过视屏URL获取该视屏对应的rtmp协议的地址，利用rtmpdump下载（mplayer --dump也可以）

文件保存路径：
科目/章节/课程/课程名_老师.flv (为了防歧义,空格也被替换未下划线)


遇见的问题：
1.登录一会儿就过期了 所以需要每个科目都去login一次。或者使用心跳包～
2.同时启用多个rtmpdump的时候，视屏会下载失败。所以group为5个一组。
3.有时候网络差会下载失败，所以加入了重试3次。
4.防止重复下载，所以只有文件存在就认为是下载过的（实际上可能没有下载完成）

结果：
下载使用了8小时52分钟31秒，下载视屏931个。

➜  Downloads  du -sh 数学  物理 语文 化学
 25G	数学
 6.6G	物理
 14G	语文
 13G	化学

格式转化：
使用ffmpeg转化

flv_lst=`find 物理 化学 语文 数学 -name "*.flv"`
for file in $flv_lst
do
    out=${file%.flv}.mp4;
    echo $out;
    ffmpeg -i "$file" -codec copy $out
done

"""
import os
import re
import sys
import time
import requests
import subprocess

host = 'http://study.ewt360.com/'
keyword = ['语文', '数学', '物理', '化学']
session = requests.Session()

headers = {'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.97 Safari/537.36'}
def login():
	login_url = 'http://passport.ewt360.com/login/prelogin'
	login_data = {
		'username':'username',
		'password':'password',
		'code':'',
		'isremember':1,
		'fromurl':'http://study.ewt360.com/'
	}
	req = session.post(login_url, data=login_data)
	return req

def getTypeUrlByKeyword(keyword):
	regex = '<li><a href="(/KeCheng/Lists\?parentId=\d+)"\s+>({0})</a></li>'.format('|'.join(keyword))
	data = session.get(host, headers=headers).content
	return { k:host + v for v,k in re.findall(regex, data)}

def getLessonsByType(type_url):
	sub_regx = '<a title="([^\"]+)" href="(/Knowledge/Index\?parentId=\d+&pointId=(\d+)&childId=\d+)">'
	grp_regx = '<h3 class="mrgL15 parentId" v="(\d+)" title="([^\"]+)">'
	data = session.get(type_url, headers=headers).content
	sub_lst = re.findall(sub_regx, data)
	grp_dict = dict(re.findall(grp_regx, data))
	sys.stdout.write('find %d group and %d subitem\n'%(len(grp_dict), len(sub_lst)))
	return [(sub_name, host+path, grp_dict[grp_id]) for sub_name, path, grp_id in sub_lst]

def getLessionDetailsByUrl(sub_url):
	regex = '<h4><a href="(/Lesson\?LessonId=\d+)">([^<]+)</a></h4>\s+\n\s+<p class="speaker"><b>主讲老师：</b>([^<]+)</p>'
	data = session.get(sub_url, headers = headers).content
	result = [(host+path, title, teacher) for path,title,teacher in re.findall(regex, data)]
	sys.stdout.write('\033[0;36;49mFind %d lessons..\033[0m\n' % len(result))
	return result

def getFilePath(detail_url):
	regex = '<input type="hidden" ID="FilePath" name="FilePath" value="([^\"]+)" />'
	data = session.get(detail_url).content
	result = re.findall(regex, data)
	if result:
		return result[0]

def getFullName(subject, subitem, subname, title, teacher):
	directory = os.sep.join([subject.strip().replace(' ', '_'), subitem.strip().replace(' ', '_'), subname.strip().replace(' ', '_')])
	if not os.path.exists(directory):
		sys.stdout.write('\033[0;34;49mmkdir => %s\033[0m\n'%directory)
		os.makedirs(directory)
	fname = '%s_%s.flv'%(title.strip().replace(' ', '_'), teacher.strip().replace(' ', '_'))
	fullname = os.sep.join([directory, fname])
	return fullname

def generateCmd(**kwargs):
	cmd = ['rtmpdump',
			'-r',
			'rtmp://video.ewt360.com/vod',
			'-y', 'mp4:/ewt360%s' % kwargs['file_path'],
			'-o', '%s' % kwargs['output']]
	return cmd

def getDownloadInfo():
	login()
	url_dict = getTypeUrlByKeyword(keyword)
	url_dict_size = len(url_dict)
	download_lst = []
	for idx, el in enumerate(url_dict, 1):
		sys.stdout.write('parse [%d/%d]: %s\n' % (idx, url_dict_size, el))
		sub_url_lst = getLessonsByType(url_dict[el])
		login()
		for sub_name, url, grp_name in sub_url_lst:
			info = getLessionDetailsByUrl(url)
			for url,title,teacher in info:
				fp = getFilePath(url)
				if not fp:
					sys.stdout.write('\033[0;31;49mError\033[0m: Could not get file path:%s\n' % sub_name)
				fname = getFullName(el, grp_name, sub_name, title, teacher)
				bsname = os.path.basename(fname)
				if os.path.isfile(fname):
					sys.stdout.write('file exists, skipped it:[\033[0;32;49m%s\033[0m]\n'%bsname)
					continue
				sys.stdout.write('generate download info for [\033[0;32;49m%s\033[0m]\n'%bsname)
				download_lst.append(generateCmd(file_path = fp, output = fname))
	return download_lst

def downloadByGroup(groups):
	sys.stdout.write('\033[0;33;49mJob Count: %d\033[0m\n' % len(groups))
	process = [(cmd, subprocess.Popen(cmd, stdout=subprocess.PIPE)) for cmd in groups]
	retry_dict = {}
	max_retry_cnt = 3
	success_cnt = 0
	error_cnt = 0
	while process:
		for cmd, p in process[:]:
			fname = cmd[-1]
			bsname = os.path.basename(fname)
			sys.stdout.write('downloading => [\033[0;32;49m%s\033[0m]\n' % bsname)
			sys.stdout.flush()
			p.wait()
			process.remove((cmd, p))
			if p.returncode == 0:
				sys.stdout.write('file download ok:[\033[0;32;49m%s\033[0m]\n' % bsname)
				success_cnt += 1
			else:
				sys.stdout.write('\033[0;31;49mERROR\033[0m: download failed, delete file:[\033[0;31;49m%s\033[0m]\n' % bsname)
				try:
					os.remove(fname)
				except:
					pass
				retry_dict[fname] =  retry_dict.setdefault(fname, 0) + 1
				if retry_dict[fname] > max_retry_cnt:
					sys.stdout.write('\033[0;31;49mERROR\033[0m: max try failed ,remove this job\n')
					with open('error_record.txt', 'wa') as f:
						f.write('%s => %s\n'%(fname, cmd))
					error_cnt += 1
				else:
					sys.stdout.write('\033[0;36;49mRetry it later..\033[0m\n')
					process.append((cmd, subprocess.Popen(cmd, stdout=subprocess.PIPE)))
	sys.stdout.write('success cnt:%d\n' % success_cnt)
	sys.stdout.write('failed  cnt:%d\n' % error_cnt)

def download():
	download_info_lst = getDownloadInfo()
	max_process_cnt = 5
	group_n = lambda lst, n: zip(*([iter(lst)] * n))
	groups_info = group_n(download_info_lst, max_process_cnt)
	group_size = len(groups_info)
	sys.stdout.write('\033[0;36;49mGet %d file to download, split %d groups\033[0m\n' % (len(download_info_lst), group_size))
	for idx, groups in enumerate(groups_info, 1):
		sys.stdout.write('\033[0;36;49m downloading group:[%d/%d]\033[0m\n' % (idx, group_size))
		downloadByGroup(groups)

def main():
	begin_time  = time.time()
	download()
	sys.stdout.write('use time :%.2f seconds\n' % (time.time() - begin_time))

if __name__ == '__main__':
	main()
