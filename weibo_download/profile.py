# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class Profile(object):
	def __init__(self, weiboid=None, nickname=None):
		#微博帐号id
		self.weiboid = weiboid;
		#微博昵称
		self.nickname = nickname;
		#是否下载过教育信息，1代表有，-1代表无
		self.is_education = -1

	def __str__(self):
		'重载__str__()函数，便于输出显示'
		self.weiboid = self.weiboid if self.weiboid else '未知'
		self.nickname = self.nickname if self.nickname else '无'
		if self.is_education == 1:
			str_is_education = '有'
		else:
			str_is_education = '无'
		return '微博号：' + self.weiboid + '\t昵称：' + self.nickname \
		 + '\t是否下载过教育信息：' + str_is_education
		
def main():
	p = Profile('1254634657','wumeng')#我在“不在” 你在不在？'
	print p

if __name__ == '__main__':
	main()