# -*- coding:utf-8 -*-
import sys
import ConfigParser
reload(sys)
sys.setdefaultencoding('utf-8')


class MyConfig(object):
	'从配置文件中初始化参数变量'
	def __init__(self):
		self.cf = ConfigParser.ConfigParser()
		self.cf.read('config/config.ini')

	def getStartWeiboIds(self):
		startWeiboIds = []
		for i in xrange(6):
			startWeiboIds.append(self.cf.get('weibo', 'weiboid%d' % i))
		return startWeiboIds

	def getCookdic(self):
		cookie = self.cf.get('cookie', 'cookie')
		cookdic = dict(Cookie=cookie)
		return cookdic
def main():
	myconfig = MyConfig()
	cookdic = myconfig.getCookdic()
	print cookdic

if __name__ == '__main__':
	main()