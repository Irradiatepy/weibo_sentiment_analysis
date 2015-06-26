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
from profile import Profile
from detailprofile import DetailProfile
from education import Education

from profile_db import Profile_Db
from detailprofile_db import DetailProfile_Db
from education_db import Education_Db

import reutil
#数据库访问锁
mylock = threading.RLock()
reload(sys)
sys.setdefaultencoding('utf-8')
############################################################################################
class GetAllProfileList(threading.Thread):
	#访问数据库对象，作为静态对象，加锁访问
	dprofile_d = DetailProfile_Db()
	education_d = Education_Db()
	def __init__(self, cookdic=None, weiboid=None):
		#初始化线程
		threading.Thread.__init__(self)
		self.homepage = 'http://weibo.cn/'
		self.pageSuffix = '/info'
		self.weiboid = weiboid
		self.cookdic = cookdic
	def run(self):
		global dblock
		#爬取该微博id的页面
		print '下载当前profile表中所有用户的详细信息'
		soup = self.getPage(self.weiboid)
		mylock.acquire()
		#分析该微博id的页面并写入数据库
		self.getPersonInfo(soup, self.weiboid)
		mylock.release()
		print '%s thread released, access to database' % self.weiboid
		time.sleep(1)


	def getPage(self, weiboid):
		'获取给定页面并返回'
		#url = 'http://weibo.cn/2111502322/info'
		url = self.homepage + weiboid + self.pageSuffix
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

	def getPersonInfo(self, soup, weiboid):
		body = soup
		#DetailProfile
		dp= DetailProfile()
		dp.weiboid = weiboid
		dp.gender, dp.description, dp.address, dp.birthday, dp.blog, dp.status,\
		dp.sexuality, dp.bloodtype, dp.fashion = reutil.detailprofile_re(body.text)
		print '',dp
		try:
			GetAllProfileList.dprofile_d.insertIntoDB(dp)
		except Exception, e:
			pass
		
		#education
		schoollist = reutil.education_re(body.text)
		if schoollist:
			sname, stime = schoollist
			einfolist = []
			if sname.__len__() == stime.__len__():
				for i in range(sname.__len__()):
					einfo = Education(weiboid, sname[i], stime[i])
					einfo.setWmd5()
					print 'Why'
					print '',einfo
					try:
						GetAllProfileList.education_d.insertIntoDB(einfo)
					except Exception, e:
						pass
					time.sleep(0.3)
		else:
			print '该用户没有学校信息'

# 获取未下载教育信息的微博帐号
def getWeiboIds():
	weiboids = []
	myconnect = GetConnect()
	sql = 'select weiboid from profile where is_education = -1'
	results = myconnect.getData(sql)
	if results:
		for r in results:
			weiboids.append(r[0])
	return weiboids

# 更新已经下载过教育信息的微博账户
def updateProfiles(weiboids):
	myconnect = GetConnect()
	for w in weiboids:
		sql = "update profile set is_education = 1 where weiboid = '%s'" % str(w)
		print sql
		myconnect.executeDB(sql)

def initParams():
	'从配置文件中初始化参数变量'
	cf = ConfigParser.ConfigParser()
	cf.read('config.ini')
	cookie = cf.get('cookie', 'cookie')
	cookdic = dict(Cookie=cookie)
	return cookdic

############################################################################################
def main():

	idnum = 50

	# 获取未下载教育信息的帐号列表
	weiboids = getWeiboIds()
	# 随机获取50个微博帐号
	if weiboids.__len__() > idnum:
		weiboids = random.sample(weiboids, idnum)

	# 从配置文件中获取cookie值
	cookdic = initParams()

	#  启动50个线程
	threadnums = weiboids.__len__()
	threads = []
	nloops = xrange(threadnums)
	for i in nloops:
		t = GetAllProfileList(cookdic, weiboids[i])
		threads.append(t)

	for i in nloops:
		threads[i].start()

	for i in nloops:
		threads[i].join()

	# 将下载过教育信息的微博帐号进行标记以不重复下载
	updateProfiles(weiboids)

	localtime = time.asctime(time.localtime(time.time()))
	print "Local current time :", localtime


if __name__ == '__main__':
	# 为了长时间下载而采取的一些措施
	looptimes = 0
	index = 0
	while True:
		print 'This is %s times loop' % looptimes
		main()
		looptimes = looptimes + 1
		if looptimes == 3:
			#break
			time.sleep(480)
			looptimes = 0
		time.sleep(random.randrange(90, 160))
	print "It's all end"
