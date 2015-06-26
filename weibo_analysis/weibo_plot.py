# -*- coding:utf-8 -*-
import sys
from pylab import *

import matplotlib.pyplot as plt
import numpy as np
import my_text_processing as tp
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')
########################################################################
"""
input:
	True and False list, 列表中True的总数代表该微博用户的有意义的微博数目
	weiboid: 用户微博id
output:
	显示饼状图，饼状图表示一个人微博的有意义和无意义微博数量对比
"""
def weiboMeaningPieChart(schoolname, weiboid=None):
	weibo_content_results = tp.get_one_weibo_data(schoolname=schoolname, weiboid=weiboid)
	if weibo_content_results is None:
		print "There is no data about %s yet." % schoolname
	else:
		meaningful = [0,0]
		weiboid = None
		for w in weibo_content_results:
			weiboid = w[4]
			if tp.is_meaningful(w[0]) == True:
				meaningful[0] += 1
			else:
				meaningful[1] += 1

		meaningful[0] = math.floor((meaningful[0]*1.0/(meaningful[0]+meaningful[1]))*100)
		meaningful[1] = 100.0 - meaningful[0]
		labels = 'Meaningful','Meaningless' # 对应每一块的标志
		explode = (0, 0.05) # 离开整体的距离，看效果
		colors = ('#9999ff','#ff9999')
		pietitle = "%s's %s's meaningful analysis" % (schoolname, weiboid)
		weiboPieChart(pielist=meaningful, labels=labels, explode=explode, colors=colors, pietitle=pietitle)
########################################################################
"""
input:
	schoolname: 学校名称
output:
	饼状图，反映该学校的有意义微博和无意义微博数量对比
"""
def schoolWeiboMeaningPieChart(schoolname):
	#countMeaning[0]代表有意义微博总数，countMeaning[1]代表无意义微博总数
	countMeaning = tp.getSchooWeiboMeaning(schoolname)
	labels = 'Meaningful:%s' % countMeaning[0],'Meaningless:%s' % countMeaning[1] # 对应每一块的标志
	colors = ('#9999ff','#ff9999')
	explode = (0, 0.05) # 离开整体的距离，看效果
	pietitle = "%s's meaningful analysis" % schoolname
	if len(countMeaning) != 0:
		countMeaning[0] = math.floor((countMeaning[0]*1.0/(countMeaning[0]+countMeaning[1]))*100)
		countMeaning[1] = 100.0 - countMeaning[0]
		weiboPieChart(pielist=countMeaning, labels=labels, explode=explode, colors=colors, pietitle=pietitle)
	else:
		print 'There is no data to show %s meaningful pie chart'
########################################################################
"""
input:
	schoolname: 学校名称
output:
	饼状图，反映该学校的积极和消极和客观的微博对比图
"""
def school_dict_analysis(schoolname):
	# 0项表示积极的微博数目，1项表示消极的微博数目，2项代表客观的微博数目
	dict_analyis_result = pickle.load(open('dict weibo data\\%s_end_results.pkl' % (schoolname), 'r'))
	labels = 'Positive:%s' % dict_analyis_result[0], 'Negative:%s' % dict_analyis_result[1], 'Objective:%s' % dict_analyis_result[2]
	colors = ('#9999ff','#ff9999', '#CC0000')
	explode = (0, 0.05, 0.05)
	pietitle = "%s's dict analyis" % schoolname
	weiboPieChart(pielist=dict_analyis_result, labels=labels, explode=explode, colors=colors, pietitle=pietitle)
########################################################################
def school_machine_analysis(schoolname):
	# 0项表示积极的微博数目，1项表示消极的微博数目，2项代表客观的微博数目
	dict_analyis_result = pickle.load(open('machine learning data\\%s_end_results.pkl' % (schoolname), 'r'))
	labels = 'Positive:%s' % dict_analyis_result[0], 'Negative:%s' % dict_analyis_result[1], 'Objective:%s' % dict_analyis_result[2]
	colors = ('#9999ff','#ff9999', '#CC0000')
	explode = (0, 0.05, 0.05)
	pietitle = "%s's machine learning analyis" % schoolname
	weiboPieChart(pielist=dict_analyis_result, labels=labels, explode=explode, colors=colors, pietitle=pietitle)
########################################################################
"""
descriptions:
	该函数通过给定的参数描述一个饼状图
input:
	
output:
	饼状图
"""
#指定图形的字体  
font = {'family' : 'serif',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 24,  
        }  
def weiboPieChart(pielist, labels, explode, colors, pietitle):
	# make a square figure and axes
	figure(1, figsize=(8.1,7.5)) # 图形的size，这里图形指的是边界
	ax = axes([0.1, 0.1, 0.8, 0.8]) # 图形的size，指的是里面的内容
	# pielist :# 每一块占得比例，总和为100
	pie(pielist, explode=explode, labels=labels, autopct='%1.1f%%', shadow=True, colors=colors)
	title(pietitle,fontdict=font)
	show()
########################################################################
"""
descriptions:
	该函数通过给定的参数描述一个折线图
input:
	
output:
	折线图
"""
def singleWeiboAnalysisLineChart(schoolname, weiboid, all_weibo_count):
	score = []
	Poslist = []
	Neglist = []
	AvgPoslist = []
	AvgNeglist = []
	StdPoslist = []
	StdNeglist = []
	for weibo in all_weibo_count:
		score_array = np.array(weibo)
		Pos = np.sum(score_array[:,0])
		Poslist.append(Pos)
		Neg = np.sum(score_array[:,1])
		Neglist.append(Neg)
		AvgPos = np.mean(score_array[:,0])
		AvgPoslist.append(AvgPos)
		AvgNeg = np.mean(score_array[:,1])
		AvgNeglist.append(AvgNeg)
		StdPos = np.std(score_array[:,0])
		StdPoslist.append(StdPos)
		StdNeg = np.std(score_array[:,1])
		StdNeglist.append(StdNeg)
		score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
	plt.figure(1)
	ax1 = plt.subplot(3, 1, 1) # 三行，一列，子图名：1
	ax2 = plt.subplot(3, 1, 2)
	ax3 = plt.subplot(3, 1, 3)
	plt.sca(ax1)
	plt.rcParams['font.sans-serif'] = ['SimHei']
	plt.title(u"%s schools %s's weibo Sentiment analysis" % (schoolname, weiboid),fontdict=font)
	#plt.text(1000,60,u"积极消极分值",color='black',size=18,horizontalalignment='right',verticalalignment='top')
	#plt.xlabel(u'微博数目')
	plt.plot(Poslist,'r') # 红色代表积极的情感
	plt.plot(Neglist, 'g--') # 绿色代表消极的情感
	plt.sca(ax2)
	plt.title("Sentiment AvgNum",fontdict=font)
	plt.plot(AvgPoslist,'r')
	plt.plot(AvgNeglist, 'g--')
	plt.sca(ax3)
	plt.title("Sentiment Variance",fontdict=font)
	plt.plot(StdPoslist,'r')
	plt.plot(StdNeglist, 'g--')
	
	plt.show()

########################################################################
def main():
	schools = ['dlut', 'nanking', 'peking', 'tsinghua', 'ecupsl']
	#schoolWeiboMeaningPieChart('dlut')
	#weiboMeaningPieChart('dlut')
	school_dict_analysis(schools[4])
##########################################################
if __name__ == '__main__':
	main()
