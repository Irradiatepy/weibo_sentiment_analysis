# -*- coding:utf-8 -*-
import sys
from md5util import md5
reload(sys)
sys.setdefaultencoding('utf-8')
#微博原创转发无图
class Wb_Ori_No_Pic(object):
	def __init__(self, weiboid=None, ftime=None, content=None, upvotes=0, forwards=0, reviews=0):
		#微博md5值，用来唯一标识该微博
		self.wmd5 = None
		#微博帐号id
		self.weiboid = weiboid;
		#该微博发布的时间
		self.ftime = ftime;
		#该微博的具体内容
		self.content = content;
		#收到的赞数目
		self.upvotes = upvotes;
		#该微博的转发数目
		self.forwards = forwards;
		#该微博的评论数
		self.reviews = reviews;

	def setWmd5(self):
		self.wmd5 = md5(str(self.weiboid) + str(self.content) + str(self.ftime) + str(self.upvotes) + str(self.forwards) + str(self.reviews))

	def __str__(self):
		'重载__str__()函数，便于输出显示'
		self.wmd5 = self.wmd5 if self.wmd5 else '未知'
		self.weiboid = self.weiboid if self.weiboid else '未知'
		self.ftime = self.ftime if self.ftime else '未知'
		self.content = self.content if self.content else '未知'

		return '微博号：' + self.weiboid + '\tmd5值：' + self.wmd5 + '\t时间：' + self.ftime + \
				'\n\t微博内容：' + self.content + '\n\t赞：' + str(self.upvotes) + '\t评论：' + str(self.reviews) + \
				'\t转发数：' + str(self.forwards)
		
def main():
	wd = Wb_Ori_No_Pic()
	wd.content = '今天天气真好'
	wd.reviews = 3
	print wd

if __name__ == '__main__':
	main()