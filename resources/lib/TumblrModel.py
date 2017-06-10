# -*- coding: utf-8 -*-
#--------------------------------------
# Author: moedje
# Date: 2017-05-29
# Git: http://github.com/moedje/tumblrv
# Initial Author:waitig.com
# Initial Date:2016-04-01
#--------------------------------------
import sys, getopt
import time,re,os,requests,urllib2

class TumblrClass:
	def __init__(self):
		self.clear_video=0
		self.clear_img=0
		self.img_path=''
		self.video_path=''
		self.index_url=''
		self.curPage=1
		self.video_url_file=''
		self.img_url_file=''
		self.headers = {
		'Host':self.index_url.replace('http://',''),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': self.index_url,
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0'
		}
		self.se = requests.Session()
	def set_headers(self,reUrl):
		self.headers = {
		'Host':self.index_url.replace('http://','').strip('/'),
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:44.0) Gecko/20100101 Firefox/44.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'X-Requested-With':'XMLHttpRequest',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate',
		'Referer': reUrl,
		'Connection': 'keep-alive',
		'Cache-Control': 'max-age=0'
		}	
	
	def get_blogs_in_file(self,fileName):
		blogList=[]
		inFile=open(fileName,'r')
		for line in inFile:
			blogList.append(line)
		return blogList
	def get_img_urls(self,text):
		img_urls=[]
		return img_urls
	def get_video_urls(self,text):
		video_urls=re.findall('(?P<video_urls>https://www.tumblr.com/video/[^/]*?/\d+/\d+/)',text)
		return video_urls
	def get_video_files(self,url):
		url=url.strip('/')
		print 'Start to deal video url : '+url
		#-----------------------------------------------------------
		self.set_headers(url)
		self.headers={
		'Host': 'www.tumblr.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive'
		}
		Reslut=self.se.get(url,headers=self.headers)
		sourceUrl=''
		sourceUrls=re.findall('src=\"(?P<video_urls>https://www.tumblr.com/video_file/\d+/[^\"]*?)\"',Reslut.text)
		if(sourceUrls!=[]):
			sourceUrl=sourceUrls[0]
		print 'Source url : '+sourceUrl
		SourceType=''
		SourceTypes=re.findall('type=\"video/(?P<vide_type>[^\"]*?)\"',Reslut.text)
		if(SourceTypes!=[]):
			SourceType=SourceTypes[0]
		sourceUrl=re.sub('https://www.tumblr.com/video_file/\d+/','',sourceUrl)
		sourceUrl=sourceUrl.replace('/','_')
		sourceUrl='https://vt.tumblr.com/'+sourceUrl
		trueUrl=sourceUrl+'.'+SourceType
		return trueUrl
	def save_video_file(self,url,path):
		url=self.get_video_files(url)
		print 'Start to download video file : '+url
		self.video_url_file.write(url+'\n')
		self.video_url_file.flush()
		fileName=url.replace('https://vt.tumblr.com/','')
		tmp_fileName='_'+fileName
		if(os.path.exists(path)==False):
			os.makedirs(path)
		if(os.path.exists(path+fileName) and self.clear_video==0):
			print 'The video file : ['+fileName+'] exists! skipped!'
			return
		self.headers={
		'Host': 'vt.tumblr.com',
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:45.0) Gecko/20100101 Firefox/45.0',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
		'Accept-Encoding': 'gzip, deflate, br',
		'Connection': 'keep-alive'
		}
		#---------wget-----------------------
		if(self.isSave=='1'):
			#print 'Downloadding... method=wget'
			#result = wget.download(url,out=path+tmp_fileName)
		
		#---------urllib2--------------------
			print 'Downloadding... method=urllib2'
			request = urllib2.Request(url, headers=self.headers)
			times=1
			while True:
				try:
					response = urllib2.urlopen(request,timeout=30)
				except:
					if(times>5):
						print 'Connect Error,exit!'
						return
					print 'Connect error , try agin!'
					times+=1
			file_size = int(response.headers['content-length'])
			print 'File size : '+str(file_size)
			with open(path+tmp_fileName,"wb") as videos:
				received = 0
				while True:
					buffer = response.read(1024*256)
					if not buffer:
						break
					received += len(buffer)
					videos.write(buffer)
					self.update_display(received,file_size)
		#---------request---------------------
#			print 'Downloadding... method=request'
#			Result=self.se.get(url,headers=self.headers)
#			print 'File size : '+Result.headers['Content-Length']
#			with open(path+tmp_fileName,"wb") as videos:
#				videos.write(Result.content)
		#----------------------------------------
			os.rename(path+tmp_fileName,path+fileName)
			print 'Video file downloaded in '+path+fileName
	def save_img_file(self,url,path):
		print 'Start to download image file : '+url
		fileName=''
		tmp_fileName='_'+fileName
		if(os.path.exists(path)==False):
			os.makedirs(path)
		if(os.path.exists(path+fileName) and self.clear_img==0):
			print 'The Image file : ['+fileName+'] exists! skipped!'
			return
		os.rename(path+tmp_fileName,path+fileName)
		print 'Image file downloaded in '+path+fileName
	def deal_blogs_page(self,url):
		print 'Start to deal url : '+url
		self.set_headers(url)
		Result=self.se.get(url,headers=self.headers)
		text=Result.text
		img_urls=self.get_img_urls(text)
		video_urls=self.get_video_urls(text)
		for img in img_urls:
			self.save_img_file(img,self.img_path)
		for videoUrl in video_urls:
			self.save_video_file(videoUrl,self.video_path)
		nextUrls=re.findall('href=\"/page/(?P<next>\d+)\"',text)
		if(nextUrls!=[]):
			nextPage=str(self.curPage+1)
			if(nextPage in nextUrls):
				nextUrl=self.index_url+'page/'+nextPage
				self.curPage+=1
				self.deal_blogs_page(nextUrl)
		else:
			return
	def deal_save_path(self):
		userNames=re.findall('http://(?P<PATH>[^\.]*?)\.tumblr\.com/',self.index_url)
		if(userNames!=[]):
			userName=userNames[0]
		self.img_path=userName+'/img/'
		self.video_path=userName+'/videos/'
		if(os.path.exists(self.video_path)==False):
			os.makedirs(self.video_path)
		self.video_url_file=open(self.video_path+'video_url','w')
	
	def display_progress(width, percent):
		percent=int(percent)  
		print "%s %d%%\r" % (('%%-%ds' % width) % (width * percent / 100 * '='), percent),  
		if percent >= 100:  
			print  
			sys.stdout.flush()  
	
	def update_display(self,received,file_size):
		percent = received*100.0/file_size
		if percent > 100:
			percent = 100.0
		self.display_progress(100,percent)
	
	def main(self,type,value,isSave):
		self.isSave=isSave
		if(type=='b'):
			if(re.match('^[http://]',value)==False):
				self.index_url='http://'+value.strip('/')+'/'
			else:
				self.index_url=value.strip('/')+'/'
			self.set_headers(self.index_url)
			self.deal_save_path()
			self.deal_blogs_page(self.index_url)
		elif(type=='f'):
			urlList=self.get_blogs_in_file(value)
			for url in urlList:
				if(re.match('^[http://]',url)==False):
					self.index_url='http://'+url.strip('/')+'/'
				else:
					self.index_url=url.strip('/')+'/'
				self.deal_save_path()
				self.deal_blogs_page(self.index_url)
	def __del__(self):
		self.video_url_file.close()

if __name__ == '__main__':
	tc=TumblrClass()
	type=''
	values=''
	isSave=0
	if(len(sys.argv)!=3):
		print 'Input number Error!'
		print 'python '+sys.argv[0]+' -u[url] or -f[fileName] [0/1]'
		exit()
	opts, args = getopt.getopt(sys.argv[1:], "hu:f:h:s:")
	for op, value in opts:
		if(op=='-u'):
			type='b'
			values=value
		elif(op=='-f'):
			type = 'f'
			values=value
		else:
			print 'python '+sys.argv[0]+' -u[url] or -f[fileName]  [0/1]'
			exit()
	isSave=sys.argv[2]
	#print isSave
	tc.main(type,values,isSave)