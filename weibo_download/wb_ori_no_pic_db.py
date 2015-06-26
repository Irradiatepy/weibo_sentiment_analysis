# -*- coding:utf-8 -*-
import sys
import MySQLdb
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')

class Wb_Ori_No_Pic_Db(object):
	def __init__(self,table='full_user_weibo'):
		self.host = None
		self.user = None
		self.passwd = None
		self.port = None
		self.db = None
		self.charset = None
		self.use_unicode = None
		self.table = table
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
		clause = 'select * from %s where weiboid = %s;' % (self.table, weiboid)
		count = self.cursor.execute(clause)
		return count
	def insertIntoDB(self, obj):
		#将给定的wb_ori_no_pic对象插入到数据库中
		try:
			self.cursor.execute('replace into full_user_weibo(wmd5, weiboid, ftime, content, upvotes, forwards, reviews) values(%s, %s, %s, %s, %s, %s, %s)', \
				(obj.wmd5, obj.weiboid, obj.ftime, obj.content, obj.upvotes, obj.forwards, obj.reviews))
			self.conn.commit()
		except Exception, e:
			print 'Mysql Error %d: %s' % (e.args[0], e.args[1])
		

	def describeRows(self, weiboid=None):
		if weiboid:
			clause = 'select * from %s where weiboid = %s;' % (self.table, weiboid)
		else:
			clause = 'select * from %s;' % self.table;

		count = self.cursor.execute(clause)
		print 'There has %d rows record' % count
		return count

	def describeWeibo(self, weiboid=None):
		'查看给定微博用户的所有微博'
		count = self.describeRows(weiboid=weiboid)
		if count != 0:
			results = self.cur.fetchall()
			for r in results:
				print r

	def closeResource(self):
		if self.cur:
			self.cur.close()
		if self.conn:
			self.conn.close()


def main():
	wb_o_n_p_d = Wb_Ori_No_Pic_Db()
	wb_o_n_p_d.describeRows()
	wb_o_n_p_d.closeResource()
if __name__ == '__main__':
	main()