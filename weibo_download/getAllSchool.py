# -*- coding:utf-8 -*-
#将education表中教育信息为大学的转移到表中
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
from school_info import School_Info
from school_db import School_Db
##################################################################################################
def conveyToSchoolTable(schoolname, schooltable):
	'将education表中所有大学的微博用户添加到表中'
	global GetConnect
	sql = "select * from education where school = '%s'" % schoolname
	myconnect = GetConnect()
	results = myconnect.getData(sql)
	school_d = School_Db(schooltable)
	if results:
		for r in results:
			schoolers = School_Info(r[1])
			school_d.insertIntoDB(schoolers)
			#print r[1]
		countsql = "select * from %s" % schooltable
		count = myconnect.getCount(countsql)
		return count
##################################################################################################
def main():
	schoolname = u'华东政法大学'
	schoolIdCount = conveyToSchoolTable(schoolname, 'ecupsl')
	print 'There are %s number of ecupsl students now' % schoolIdCount

if __name__ == '__main__':
	main()
