# -*- coding:utf-8 -*-
import sys
import weibo_senti_analysis
import weiboplot
import weibo_word_contrast
from pylab import *
import matplotlib.pyplot as plt
import numpy as np
import my_text_processing as tp
import pickle


reload(sys)
sys.setdefaultencoding('utf-8')
##########################################################

##########################################################

##########################################################
class Intermediate(object):
	def __init__(self):
		pass
	def show_school_meaning_contrast(self, school):
		'显示一个学校有意义微博和无意义微博的饼状图对比'
		print school,'school'
		weiboplot.schoolWeiboMeaningPieChart(school)

	def show_person_meaning_contrast(self, school,weiboid):
		'显示一个学校的某个用户的有意义和无意义微博的饼状图对比'
		# 此处最后应该从full_user_weibo表中取数据
		print school, 'person'
		weiboplot.weiboMeaningPieChart(schoolname=school,weiboid=weiboid)

	def show_school_word_contrast(self,a, b):
		'显示两个学校用词之间的差异'
		print a,b
		school_dict = {1:'dlut', 2:'tsinghua', 3:'peking', 4:'nanking', 5:'ecupsl'}
		weibo_word_contrast.diffSchoolWord(school_dict[a], school_dict[b])

	def show_school_dict_analysis(self, schoolname):
		'字典分析显示一个学校的微博'
		print schoolname
		weiboplot.school_dict_analysis(schoolname)

	def show_person_dict_analysis(self, schoolname, weiboid):
		'字典分析一个用户的微博'
		print schoolname
		weiboid = 1523342215
		weibo_senti_analysis.show_ones_weibo(schoolname=schoolname,weiboid=weiboid)

	def show_school_machine_analysis(self, schoolname):
		'机器学习分析一个学校的微博'
		weiboplot.school_machine_analysis(schoolname)
##########################################################

##########################################################

def main():
	pass
if __name__ == '__main__':
	main()

'''
		# 0项表示积极的微博数目，1项表示消极的微博数目，2项代表无意义的微博数目
		dict_analyis_result = pickle.load(open('dict weibo data\\%s_end_results.pkl' % (schoolname), 'r'))
		labels = 'Positive:%s' % dict_analyis_result[0], 'Negative:%s' % dict_analyis_result[1], 'Objective:%s' % dict_analyis_result[2]
		colors = ('#9999ff','#ff9999', '#CC0000')
		explode = (0, 0.05, 0.05)
		pietitle = "%s's dict analyis" % schoolname
		self.weiboPieChart(pielist=dict_analyis_result, labels=labels, explode=explode, colors=colors, pietitle=pietitle)

	def weiboPieChart(self, pielist, labels, explode, colors, pietitle):
		# make a square figure and axes
		figure(1, figsize=(8.1,7.5)) # 图形的size，这里图形指的是边界
		ax = axes([0.1, 0.1, 0.8, 0.8]) # 图形的size，指的是里面的内容
		# pielist :# 每一块占得比例，总和为100
		pie(pielist, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, colors=colors)
		title(pietitle)
		show()		'''