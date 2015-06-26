# -*- coding:utf-8 -*-
#从学校（如：tsinghua）表中找到关注列表，并存储到proflie表中
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
from profile import Profile
from profile_db import Profile_Db
#数据库访问锁
mylock = threading.RLock()

reload(sys)
sys.setdefaultencoding('utf-8')
############################################################################################
class GetAllUserList(threading.Thread):
	#访问数据库对象，作为静态对象，加锁访问
	profile_d = Profile_Db()
	def __init__(self, cookdic=None, weiboid=None):
		#初始化线程
		threading.Thread.__init__(self)
		self.homepage = 'http://weibo.cn/'
		self.urlsuffix = '/follow?page='
		self.weiboid = weiboid
		self.cookdic = cookdic
		#默认只有一页
		self.pagenum = 1
	def run(self):
		self.getPageNum()
		mylock.acquire()
		print '%s thread locked' % self.weiboid
		self.getAllUser()
		mylock.release()
		print '%s thread released' % self.weiboid

	def getPage(self, page=1):
		'获取给定页数的页面并返回'
		#url = 'http://weibo.cn/1828021***/follow?page=1'
		url = self.homepage + self.weiboid + self.urlsuffix + str(page)
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
		#print soup
		return soup

	def getPageNum(self):
		'确定该微博用户一共有多少页关注列表'
		soup = self.getPage(1)
		body = soup.body
		page = body.find(id='pagelist')
		#如果有分页的话
		if page:
			pl_regex = u'/(\d+)页'
			pagenum = re.search(pl_regex, page.text).group(1)
			self.pagenum = int(pagenum)
			#print pagenum

	def getAllUser(self):
		'获取该微博用户所有的关注用户'
		for curpage in xrange(self.pagenum):
			print 'This is ' + str(curpage + 1) + ' page'
			print '-' * 100
			soup = self.getPage(curpage + 1)
			if soup:
				self.getList(soup)
			else:
				print 'soup is None!'
			#延迟3秒后再爬取数据，防止被禁
			time.sleep(random.randrange(2, 4))
			
	def getList(self, soup):
		'获取每一页中的所有用户'
		body = soup.body
		userlist = body.find_all('table')
		#print userlist.__len__()
		weiboid_regex = ur'http://weibo.cn/attention/.*?uid=(\d+)'
		for u in userlist:
			p = Profile()
			p.nickname = u.text.strip().replace('\n','').split(' ')[0]
			if re.search(weiboid_regex, str(u)):
				p.weiboid = re.search(weiboid_regex, str(u)).group(1)
				GetAllUserList.profile_d.insertIntoDB(p)
				print '',p
			else:
				print "can't find"

def initParams():
	'从配置文件中初始化参数变量'
	cf = ConfigParser.ConfigParser()
	cf.read('config.ini')
	cookie = cf.get('cookie', 'cookie')
	cookdic = dict(Cookie=cookie)
	return cookdic

# 获取所有账户表中未下载过关注列表的用户帐号
def getWeiboIds(schooltable):
	weiboids = []
	myconnect = GetConnect()
	sql = 'select weiboid from %s where is_profile = -1' % schooltable
	results = myconnect.getData(sql)
	if results:
		for r in results:
			weiboids.append(r[0])
	return weiboids

# 更新weiboids里面的微博账户信息
def updateSchools(weiboids, schooltable):
	myconnect = GetConnect()
	for w in weiboids:
		sql = "update %s set is_profile = 1 where weiboid = '%s'" % (schooltable, str(w))
		#print sql
		myconnect.executeDB(sql)

######################################################################################################
def main():
	# 设置两个线程
	threadnum = 2
	# 本次下载的数据为ecupsl表中的
	schooltable = 'ecupsl'
	# 从ecupsl表中获取未下载过关注列表的用户微博帐号
	weiboids = getWeiboIds(schooltable)
	# 随机获取两个微博帐号
	if weiboids.__len__() > threadnum:
		weiboids = random.sample(weiboids, threadnum)
	# 从配置文件中获取cookie值
	cookdic = initParams()
	#  启动两个线程
	threadnums = weiboids.__len__()
	threads = []
	nloops = xrange(threadnums)
	for i in nloops:
		t = GetAllUserList(cookdic, weiboids[i])
		threads.append(t)

	for i in nloops:
		threads[i].start()

	for i in nloops:
		threads[i].join()
	# 将下载过关注列表的两个微博帐号进行标记以不重复下载
	updateSchools(weiboids, schooltable)

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
			time.sleep(480)
			looptimes = 0
		time.sleep(random.randrange(75, 140))
	print "It's all end"
