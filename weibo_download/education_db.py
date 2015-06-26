# -*- coding:utf-8 -*-
import sys
import MySQLdb
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

class Education_Db(object):
	def __init__(self):
		self.host = None
		self.user = None
		self.passwd = None
		self.port = None
		self.db = None
		self.charset = None
		self.use_unicode = None
		self.table = 'education'
		self.initParams()
		self.conn = None
		self.cur = None
		self.initDb()

	def initParams(self):
		'从配置文件中初始化参数变量'
		cf = ConfigParser.ConfigParser()
		cf.read('config.ini')
		self.host = cf.get('db', 'host')
		self.port = int(cf.get('db', 'port'))
		self.user = cf.get('db', 'user')
		self.passwd = cf.get('db', 'passwd')
		self.db = cf.get('db', 'db')
		self.charset = cf.get('db', 'charset')
		self.use_unicode = cf.get('db', 'use_unicode')

	def initDb(self):
		try:
			self.conn = MySQLdb.connect(host=self.host, port=self.port, user=self.user, \
							passwd=self.passwd, db=self.db, charset=self.charset, use_unicode=self.use_unicode)
			self.cursor = self.conn.cursor()
		except MySQLdb.Error, e:
			print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
			print 'Failed to connect to database! Please check your config file and confirm your database is open'
			sys.exit(-1)
		print 'Success connect database'

	def findExists(self, weiboid):
		'判断'
		pass
	def insertIntoDB(self, obj):
		'''将给定的Profile对象插入到数据库中，注意，不能增加原先已经含有的记录
		使用replace into语句，能够做到不插入重复的行'''
		self.cursor.execute('replace into education(wmd5, weiboid, school, enrolltime) values(%s, %s, %s, %s)', \
			(obj.wmd5, obj.weiboid, obj.school, obj.enrolltime))
		self.conn.commit()

	def describeRows(self, weiboid=None):
		if weiboid:
			clause = 'select * from %s where weiboid = %s;' % (self.table, weiboid)
		else:
			clause = 'select * from %s;' % self.table;

		count = self.cursor.execute(clause)
		print 'There has %d rows record' % count
		return count

	def describeProfile(self, weiboid=None):
		'查看给定微博用户的所有微博'
		count = self.describeRows(weiboid=weiboid)
		if count != 0:
			results = self.cursor.fetchall()
			for r in results:
				print r[0], r[1]

	def closeResource(self):
		if self.cur:
			self.cur.close()
		if self.conn:
			self.conn.close()


def main():
	p_d = Education_Db()
	p_d.describeRows()
	p_d.describeProfile()
	p_d.closeResource()
if __name__ == '__main__':
	main()