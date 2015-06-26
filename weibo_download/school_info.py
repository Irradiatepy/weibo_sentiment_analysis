# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class School_Info(object):
	def __init__(self, weiboid=None):
		#微博帐号id
		self.weiboid = weiboid;
		#是否下载过该微博id的关注列表
		self.is_profile = -1
		#是否下载过该微博id的原创无图微博，1代表有，-1代表无
		self.is_wb_ori_no_pic = -1

	def __str__(self):
		'重载__str__()函数，便于输出显示'
		self.weiboid = self.weiboid if self.weiboid else '未知'
		if self.is_profile == 1:
			str_is_profile = '有'
		else:
			str_is_profile = '无'

		if self.is_wb_ori_no_pic == 1:
			str_is_wb_ori_no_pic = '有'
		else:
			str_is_wb_ori_no_pic = '无'

		return '微博号：' + self.weiboid \
		 + '\t是否下载过关注列表：' + str_is_profile + '\t是否下载过原创无图微博：' + str_is_wb_ori_no_pic
		
def main():
	p = School_Info('1254634657')#我在“不在” 你在不在？'
	print p
if __name__ == '__main__':
	main()