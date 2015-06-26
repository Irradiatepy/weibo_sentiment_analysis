# -*- coding:utf-8 -*-
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class DetailProfile(object):
	def __init__(self, weiboid=None, gender=-1, description=None, address=None, \
				birthday=None, blog=None, relation=None, sexuality=-1, bloodtype=None, fashion=None):
		#微博帐号id
		self.weiboid = weiboid;
		#性别，1代表男，0代表女，-1代表未知
		self.gender = gender
		#个人简介
		self.description = description
		#个人地址，格式：省+市
		self.address = address;
		#生日，格式：年+月+日
		self.birthday = birthday;
		#博客地址，如http://blog.csdn.net/whiterbear
		self.blog = blog;
		#感情状况，如单身，暗恋中，求交往等
		self.relation = relation
		#性取向，1代表男，0代表女，-1代表未知，默认未知
		self.sexuality = sexuality
		#血型，A，B，AB或O
		self.bloodtype = bloodtype
		#达人类型，如电影 旅游 音乐等
		self.fashion = fashion

	def __str__(self):
		'重载__str__()函数，便于输出显示'
		self.weiboid = self.weiboid if self.weiboid else '未知'
		self.gender = self.gender if self.gender else '未知'
		self.description = self.description if self.description else '未知'
		self.address = self.address if self.address else '未知'
		self.birthday = self.birthday if self.birthday else '未知'
		self.blog = self.blog if self.blog else '未知'
		self.relation = self.relation if self.relation else '未知'
		self.bloodtype = self.bloodtype if self.bloodtype else '未知'
		self.fashion = self.fashion if self.fashion else '未知'
		
		if self.gender == -1:
			strgender = '未知'
		elif self.gender == 0:
			strgender = '女'
		else:
			strgender = '男'

		if self.sexuality == -1:
			strsexuality = '未知'
		elif self.sexuality == 0:
			strsexuality = u'女'
		else:
			strsexuality = u'男'

		return '微博号：' + self.weiboid + '\t性别：' + strgender + '\t个人简介：' + self.description+ \
			'\n\t地址：' + self.address + '\t生日：' + self.birthday + \
		 	'\n\t博客：' + self.blog + '\t感情状况：' + self.relation + 'description\t性取向：' + strsexuality + \
		 	'\t血型：' + self.bloodtype + '\t达人：' + self.fashion
		
def main():
	p = DetailProfile()#'1254634***','wumeng', -1, '我在“不在” 你在不在？'
	p.weiboid = '1254634***'
	p.relation = '暧昧中'
	p.blog = 'disdji'
	print '',p

if __name__ == '__main__':
	main()