# -*- coding:utf-8 -*-
import sys
from Tkinter import *
import Tkinter
from pylab import *
#import pylab as plt
import matplotlib.pyplot as plt
import numpy as np

import os
import random
import pickle
import numpy as np

import jieba
import jieba.analyse
import jieba.posseg
from getconnect import GetConnect
reload(sys)
sys.setdefaultencoding('utf-8')
############################################################################################
'''
运行顺序：
	1. getWordFrequency() 运行五个学校的，得到五个学校的所有用词school_worddict.pkl文件
	2. getHighFrequencyWordPickle() 得到五个学校的高频用词school_highwordlist.pkl文件
	3. convey_Idf_To_Pickle() 将idf文档转化成字典，并保存在idf.pkl中
	4. diffSchoolWord() 显示两个学校的用词差异，并调用cos函数显示值
'''

############################################################################################	
"""
input:
	schoolname
output:
	返回该学校用词频率文本或者pickle文件。
"""
def getWordFrequency(schoolname):
	get_keyword_sql = 'select keywords from %s where is_meaningful = 1' % (schoolname+'_wordsegment')
	myconnect = GetConnect()
	results = myconnect.getData(get_keyword_sql)
	worddict = {} # 单词字典，记录所有出现的单词以及出现的次数
	print len(results)
	index = 0
	for r in results:
		for w in r[0].split():
			index += 1
			if worddict.has_key(w) == False:
				worddict[w] = 1
			else:
				worddict[w] += 1
	print index, 'index' # 这是单词出现的总数 dlut有27万词
	print len(worddict) # 这是存储到字典中的单词总数，dlut有6.5万词
	pickle.dump(worddict, open('weibo word contrast\\%s_worddict.pkl' % schoolname, 'w'))
############################################################################################
"""
input:
	schoolname
output:
	返回该学校用词高频率文本或者pickle文件。
"""	
def getHighFrequencyWordPickle(schoolname):
	pkl_file = open('weibo word contrast\\%s_worddict.pkl' % schoolname, 'r')
	loaded_word_dict = pickle.load(pkl_file)
	pkl_file.close()
	highworddict = {}
	for word in loaded_word_dict:
		if loaded_word_dict[word] > 10:
			highworddict[word] = loaded_word_dict[word]
	print len(highworddict), 'highworddict'
	output = open('weibo word contrast\\%s_highwordlist.pkl' % (schoolname), 'w')
	pickle.dump(highworddict, output)
	output.close()
###########################################################################################
"""
description:
	将idf文档转化成字典，并保存在idf.pkl文件中
input:
output:
"""
def convey_Idf_To_Pickle():
	idfdict = {}
	index = 0
	if os.path.exists('weibo word contrast\\idfdict.pkl') == False:
		# 从txt文本中提取到字典中
		for line in open('weibo word contrast\\idf.txt', 'r'):
			idfdict[line.split()[0]] = float(line.split()[1])
		print len(idfdict)
		# 保存到pkl文件中
		output = open('weibo word contrast\\idfdict.pkl', 'w')
		pickle.dump(idfdict, output)
		output.close()
	else:
		print 'idfdict has already existscmd'
############################################################################################
"""
input:
	schoolname
output:
	返回该学校用词频率文本或者pickle文件。
"""
def diffSchoolWord(schoolname1, schoolname2):
	loaded_word_dict1 = pickle.load(open('weibo word contrast\\%s_highwordlist.pkl' % schoolname1, 'r'))
	loaded_word_dict2 = pickle.load(open('weibo word contrast\\%s_highwordlist.pkl' % schoolname2, 'r'))
	########
	"""构建临时的比较文本，等最后所有学校的数据齐了后使用最终文本"""
	baseworddict = {}
	print len(loaded_word_dict1)
	print len(loaded_word_dict2)
	if os.path.exists('weibo word contrast\\%s_wordlist.pkl' % (schoolname1+schoolname2)) == False:
		# 添加第一个学校的词典
		for word in loaded_word_dict1:
			if loaded_word_dict1[word] > 10:
				if baseworddict.has_key(word) == False:
					baseworddict[word] = 1
		print len(baseworddict),'schoolname1'
		# 添加第二个学校的词典
		for word in loaded_word_dict2:
			if loaded_word_dict2[word] > 10:
				if baseworddict.has_key(word) == False:
					baseworddict[word] = 1
		print len(baseworddict),'schoolname1+2'
		# 将dict再转成list保存起来，这样每个词在数组中的位置就固定起来了
		basewordlist = []
		for bd in baseworddict:
			basewordlist.append(bd)

		pickle.dump(basewordlist, open('weibo word contrast\\%s_wordlist.pkl' % (schoolname1+schoolname2), 'w'))
		print len(basewordlist)
	else:
		basewordlist = pickle.load(open('weibo word contrast\\%s_wordlist.pkl' % (schoolname1+schoolname2), 'r'))
		print len(basewordlist),'2schoolname1+2'
	########
	school1_list = []
	school2_list = []
	#保证school1_list的长度与basewordlist长度相同
	for i in basewordlist:
		#所有出现在loaded_word_dict1中的单词全部添加到学校1的列表中，所有没出现的，列表中添加1
		if loaded_word_dict1.has_key(i) == True:
			school1_list.append(loaded_word_dict1[i])
		else:
			school1_list.append(1)
	print len(school1_list), 'school1_list'
	for i in basewordlist:
		if loaded_word_dict2.has_key(i) == True:
			school2_list.append(loaded_word_dict2[i])
		else:
			school2_list.append(1)
	print len(school2_list), 'school2_list'
	# 此处还需要把上面的两个list转换成double类型的数组，存储出现的概率，还要结合idf
	sum_school_1 = sum(school1_list)
	sum_school_2 = sum(school2_list)
	# 得到学校常用词的tf频率列表
	for i, value in enumerate(school1_list):
		school1_list[i] =  school1_list[i]*1.0/sum_school_1 * 1
	for i, value in enumerate(school2_list):
		school2_list[i] =  school2_list[i]*1.0/sum_school_2 * 1
	# 计算两个学校的余弦值(在不考虑idf的情况下的相似度)
	print 'without considersing idf, just tf:', getCos(school1_list, school2_list)
	# 考虑idf的情况
	idfdict = pickle.load(open('weibo word contrast\\idfdict.pkl', 'r'))
	# 生成自己的idf列表
	for i, value in enumerate(basewordlist):
		if idfdict.has_key(value.encode('utf-8')) == True:
			basewordlist[i] = idfdict[value.encode('utf-8')]
		else:
			basewordlist[i] = 3
	# 得到学校常用词的tf*idf列表
	for i, value in enumerate(school1_list):
		school1_list[i] =  school1_list[i] * basewordlist[i]
	for i, value in enumerate(school2_list):
		school2_list[i] =  school2_list[i] * basewordlist[i]
	# 计算两个学校的余弦值(在考虑idf的情况下的相似度)
	arc = getCos(school1_list, school2_list)
	print 'considersing tf-idf:', arc
	draw_picture(schoolname1=schoolname1,schoolname2=schoolname2, s_arc=arc, worddiff=(len(loaded_word_dict1)-len(loaded_word_dict2)))
############################################################################################	
"""
给定两个向量，计算并返回两个向量之间的夹角
"""
def getCos(list_1,list_2,para=None):
	# 第一步转化为numpy数组
	array_1 = np.array(list_1)
	array_2 = np.array(list_2)
	# 第二步计算两个向量的长度
	len_1 = np.sqrt(array_1.dot(array_1))
	len_2 = np.sqrt(array_2.dot(array_2))
	# 第三步计算夹角的cos值
	cos_angle = array_1.dot(array_2)/(len_1*len_2)
	# 第四步，弧度制夹角
	angle = np.arccos(cos_angle)
	# 第五步，转换为角度值
	angle2 = angle*360/2/np.pi
	# 根据参数的不同返回弧度或者角度
	if para == None or para == 'angle':
		return angle2
	elif para == 'arc':
		return angle
############################################################################################
#指定图形的字体  
font = {'family' : 'serif',  
        'color'  : 'black',  
        'weight' : 'normal',  
        'size'   : 24,  
        }  
def draw_picture(s_arc, schoolname1, schoolname2, worddiff):
	top = Tkinter.Tk()

	C = Tkinter.Canvas(top, bg="white", height=250, width=400)

	coord = 10, 50, 300, 250
	arc = C.create_arc(coord, start=0, extent=s_arc, fill="steelblue")
	label1 = Label(top, text="%s,%s word diff:%s" % (schoolname1,schoolname2,worddiff), width=30, height=3,font=80)
	label2 = Label(top, text="arc:%s" % s_arc, width=30, height=3,font=80)
	label1.pack()

	C.pack()
	label2.pack()

	top.mainloop()
############################################################################################	
def main():
	
	schools = ['dlut', 'nanking', 'peking', 'tsinghua', 'ecupsl']
	# 1. 得到五个学校的school_worddict.pkl文件
	'''
	for i in schools:
		getWordFrequency(i)
	'''
	# 2. 得到五个学校的高频用词school_highwordlist.pkl文件
	'''
	for i in schools:
		getHighFrequencyWordPickle(i)
	'''
	# 3. 将idf文档转化成字典，并保存在idf.pkl中
	'''
	convey_Idf_To_Pickle()
	'''
	# 4. 显示两个学校用词的差异
	diffSchoolWord(schools[0], schools[2])
##########################################################
if __name__ == '__main__':
	main()
