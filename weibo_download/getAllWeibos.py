# -*- coding:utf-8 -*-
import sys
import requests
import threading
import ConfigParser
from bs4 import BeautifulSoup
import time
import re
import MySQLdb
import random
from getconnect import GetConnect
from wb_ori_no_pic import Wb_Ori_No_Pic
from wb_ori_no_pic_db import Wb_Ori_No_Pic_Db
reload(sys)
sys.setdefaultencoding('utf-8')
###########################################################################################################
class GetWeiboDetail(object):
	def __init__(self, weiboid, weibotablename):
	#http://weibo.cn/103092****/profile?hasori=1&haspic=2&endtime=20150425&advancedfilter=1&page=2
		self.homepage = 'http://weibo.cn/'
		self.urlmid = '/profile?hasori=1&haspic=2&endtime='
		self.urlsuffix = '&advancedfilter=1&page='
		self.weiboid = weiboid
		self.endtime = '20150426'
		self.cookdic = None
		#默认只有一页
		self.pagenum = 1
		self.initParams()
		#访问数据库对象
		self.wb_o_n_p_d = Wb_Ori_No_Pic_Db(weibotablename)

	def initParams(self):
		'从配置文件中初始化参数变量'
		cf = ConfigParser.ConfigParser()
		cf.read('config.ini')
		cookie = cf.get('cookie', 'cookie')
		self.cookdic = dict(Cookie=cookie)

	def getPage(self, page=1):
		'获取给定页数的页面并返回'
		#url = http://weibo.cn/187350****/profile?hasori=1&haspic=2&starttime=20150100&endtime=20150420&advancedfilter=1&page=6
		url = self.homepage + self.weiboid + self.urlmid + self.endtime + self.urlsuffix + str(page)
		try:
			req = requests.get(url, cookies=self.cookdic, timeout=100)
		except Exception, e:
			print 'Something wroing'
			return None
		if req.status_code != requests.codes.ok:
			print "haven't get 200,  status_code is: " + req.status_code
			return None
		soup = BeautifulSoup(req.text)
		soup = BeautifulSoup(soup.prettify())
		return soup

	def getPageNum(self):
		'确定该微博用户一共有多少页微博'
		soup = self.getPage(0)
		body = soup.body
		page = body.find(id='pagelist')
		#如果有分页的话
		if page:
			pl_regex = u'/(\d+)页'
			pagenum = re.search(pl_regex, page.text).group(1)
			self.pagenum = int(pagenum)
			mynum = 10
			if self.pagenum > mynum:
				self.pagenum = mynum
			print '%s 有 %s 页微博' %(self.weiboid, self.pagenum)

	def getAllWeibo(self):
		'获取该微博用户所有的微博'
		for curpage in xrange(self.pagenum):
			print 'This is ' + str(curpage + 1) + ' page'
			print '-' * 100
			soup = self.getPage(curpage + 1)
			if soup:
				self.getPageContent(soup)
			#延迟3秒后再爬取数据，防止被禁
			time.sleep(random.randrange(2, 4))

	#获取每一页的微博内容
	def getPageContent(self, soup):
		body = soup.body
		weibolist = body.find_all(attrs={'class':'c'})
		wdlist = []
		for weibo in weibolist:
			#如果这个div中包含原文内容的话
			if weibo.find(attrs={'class':'ctt'}):
				#使用Wb_Ori_No_Pic对象来存储获取的微博数据
				wd = Wb_Ori_No_Pic()
				#赋予其weiboid号
				wd.weiboid = self.weiboid
				#获取微博原文内容
				wd.content = weibo.find(attrs={'class':'ctt'}).text.strip().replace('\n','').replace(' ','')
				#获取转发时间
				ct = weibo.find(attrs={'class':'ct'})
				wd.ftime = ct.text.strip().replace('\n','').replace(' ','')
				#获取赞数目
				upvote_regex = ur'赞\[(\d+)\]'
				result = re.search(upvote_regex, weibo.text)
				wd.upvotes = int(result.group(1))
				#获取转发数目
				forward_regex = ur'转发\[(\d+)\]'
				result = re.search(forward_regex, weibo.text)
				wd.forwards = int(result.group(1))
				#获取评论数目
				review_regex = ur'评论\[(\d+)\]'
				result = re.search(review_regex, weibo.text)
				wd.reviews = int(result.group(1))
				#设置该微博md5值
				wd.setWmd5()
				print wd
				try:
					self.wb_o_n_p_d.insertIntoDB(wd)
					#pass
				except Exception, e:
					pass
					print 'Something wrong'
					print '*' * 100
					sys.exit(-1)

def getWeiboIds(schoolname=None):
	'获取schoolname表中没有下载原创无图微博的用户'
	weiboids = []
	sql = "select weiboid from %s order by rand() limit 20" % schoolname
	myconnect = GetConnect() 
	results = myconnect.getData(sql)
	if results:
		for r in results:
			weiboids.append(r[0])
			#print r[0]
	return weiboids

# 将已经下载微博的用户进行标识，以免重复下载
def updateSchoolers(weiboids, schoolname=None):
	myconnect = GetConnect()
	for w in weiboids:
		sql = "update %s set is_wb_ori_no_pic = 1 where weiboid = '%s'" % (schoolname, str(w))
		print sql
		myconnect.executeDB(sql)

###################################################################################################
def main():
	schoolname = 'dlut'
	# 获取未下载微博的用户列表
	weiboids = getWeiboIds(schoolname)
	weibotablename = 'full_user_weibo'
	# 八个线程进行下载
	threadnum = 8
	# 随机选择8个用户
	if weiboids.__len__() > threadnum:
		#weiboids = weiboids[0:threadnum]
		weiboids = random.sample(weiboids, threadnum)

	for r in weiboids:
		print r
		gd = GetWeiboDetail(r, weibotablename)
		gd.getPageNum()
		gd.getAllWeibo()

	# 更新已经用户列表，标识那些已经下载过微博的用户
	updateSchoolers(weiboids, schoolname)

	localtime = time.asctime(time.localtime(time.time()))
	print "Local current time :", localtime

if __name__ == '__main__':
	# 为了长时间下载而采取的一些措施
	looptimes = 0
	while True:
		print 'This is %s times loop' % looptimes
		main()
		looptimes = looptimes + 1
		if looptimes == 3:
			#break
			time.sleep(480)
			looptimes = 0
		time.sleep(random.randrange(75, 140))
	print "It's all end"
