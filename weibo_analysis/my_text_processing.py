# -*- coding:utf-8 -*-
import sys
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
"""
input :
	parameter_1: A txt file with many lines
	parameter_2: A txt file with only one line of data
output:
	parameter_1: Every line is a value of the txt_data list.
	parameter_2: Txt data is a string. (str)
"""
def get_txt_data(filepath, para):
	if para == 'lines':
		txt_file1 = open(filepath, 'r')
		txt_tmp1 = txt_file1.readlines()
		txt_tmp2 = ''.join(txt_tmp1)
		txt_data1 = txt_tmp2.decode('utf-8').split('\n')
		txt_file1.close()
		return txt_data1
	elif para == 'line':
		txt_file2 = open(filepath, 'r')
		txt_tmp = txt_file2.readline()
		txt_data2 = txt_tmp.decode('utf-8')
		txt_file2.close()
		return txt_data2
############################################################################################
"""
description:
	得到一个人的微博数据，如果给定微博id就返回该微博id的微博，如果没给就随机返回该学校一个用户的微博
input:

"""
def get_one_weibo_data(schoolname, weiboid=None):
	myconnect = GetConnect()
	if weiboid is None:
		get_weibo_id_sql = "select weiboid from %s where is_wb_ori_no_pic = 1 order by rand() limit 1;" % schoolname
		results = myconnect.getData(get_weibo_id_sql)
		if results:
			weiboid = results[0][0]
		else:
			print "get weiboid wrong"
			weiboid = '2591961830'

	if schoolname == 'dlut':
		school_weibo_table = 'wb_ori_no_pic'
	else:
		school_weibo_table = schoolname + '_wb_ori_no_pic'

	get_weibo_content_sql = "select content, upvotes, forwards, reviews, weiboid from %s where weiboid = %s" % (school_weibo_table, weiboid)
	weibo_content_results = myconnect.getData(get_weibo_content_sql)
	if weibo_content_results:
		return weibo_content_results
	else:
		return None
############################################################################################
"""
description:
	得到一个学校全部的微博
input:
	schoolname

"""
def get_school_weibo(schoolname):
	myconnect = GetConnect()
	school_weibo_table = schoolname + '_wordsegment'
	school_weibo = 'select segments, is_meaningful from %s' % school_weibo_table
	weibo_content_results = myconnect.getData(school_weibo)
	print len(weibo_content_results)
	for i in xrange(100):
		print weibo_content_results[i][0],weibo_content_results[i][1]

	pickle.dump(weibo_content_results, open('dict weibo data\\%s_seg_weibo.pkl' % (schoolname), 'w'))
def get_school_weibo_2(schoolname):
	weibo_content_results = pickle.load(open('dict weibo data\\%s_seg_weibo.pkl' % (schoolname), 'r'))
	weibo_content_new = []
	a_cell = []
	for cell in xrange(len(weibo_content_results)):
		a_cell.append(weibo_content_results[cell][0].replace(' ',''))
		a_cell.append(weibo_content_results[cell][1])
		weibo_content_new.append(a_cell)
		a_cell = []
	pickle.dump(weibo_content_new, open('dict weibo data\\%s_seg_weibo_new.pkl' % (schoolname), 'w'))
############################################################################################
"""
description:
	给定一个学校名，返回该学校的有意义微博和无意义微博数量
input:
	schoolname：学校名
output:
	返回一个数组countMeaning，countMeaning[0]代表有意义微博总数，countMeaning[1]代表无意义微博总数
"""
def getSchooWeiboMeaning(schoolname):
	schoolname = schoolname + '_wordsegment'
	countMeaning = []
	myconnect = GetConnect()
	get_school_weibo_meaning_num = 'select count(*) as meaningcount,is_meaningful from %s group by is_meaningful;' % schoolname
	meaning_num_results = myconnect.getData(get_school_weibo_meaning_num)
	if meaning_num_results:
		countMeaning.append(int(meaning_num_results[1][0]))
		countMeaning.append(int(meaning_num_results[0][0]))
	return countMeaning

############################################################################################
"""
input: 这款手机大小合适。
output:
	parameter_1: 这 款 手机 大小 合适 。(unicode)
    parameter_2: [u'\u8fd9', u'\u6b3e', u'\u624b\u673a', u'\u5927\u5c0f', u'\u5408\u9002', u'\uff0c']
"""
def segmentation(sentence, para):
	if para == 'str':
		seg_list = jieba.cut(sentence)
		seg_result = ''.join(seg_list)
		return seg_result
	elif para == 'list':
		seg_list2 = jieba.cut(sentence)
		seg_result2 = []
		for w in seg_list2:
			seg_result2.append(w)
		return seg_result2
############################################################################################
"""
input: A review like this
	'这款手机大小合适，配置也还可以，很好用，只是屏幕有点小。。。总之，戴妃+是一款值得购买的只能手机。'
output: A multidimentional list
	[u'\u8fd9\u6b3e\u624b\u673a\u5927\u5c0f\u5408\u9002\uff0c',
    u'\u914d\u7f6e\u4e5f\u8fd8\u53ef\u4ee5\uff0c', u'\u5f88\u597d\u7528\uff0c',
    u'\u53ea\u662f\u5c4f\u5e55\u6709\u70b9\u5c0f\u3002', u'\u603b\u4e4b\uff0c',
    u'\u6234\u5983+\u662f\u4e00\u6b3e\u503c\u5f97\u8d2d\u4e70\u7684\u667a\u80fd\u624b\u673a\u3002']	
"""
'''Maybe this algorithm will have bugs in it'''
def cut_sentences_1(words):
	#words = (words).decode('utf-8')
	start = 0
	i = 0 #i is the position of words
	sents = []
	token = 'meaningless'
	punt_lists = ',.!?;~，。！？：；～… '.decode('utf8')
	for word in words:
		if word in punt_lists and token not in punt_lists:
			sents.append(words[start:i+1])#每次将句子中的一段放入sents中去
			start = i + 1
			i += 1
		else:
			i += 1
			token = list(words[start:i+2]).pop()
	#if there is no punctuations(标点符号) in the end of a sentence, it can still be cuted
	if start < len(words):
		sents.append(words[start:])
	return sents
############################################################################################
""" Sentence cutting algorithm without bug, but a little difficult to explain why"""
def cut_sentences_2(words):
	#words = (words).decode('utf-8')
	start = 0
	i = 0 # i is the position of words
	token = "meaningless"
	sents = []
	punt_lists = ',.!?;~，。！？：；～… '.decode('utf8')
	for word in words:
		if word not in punt_lists:
			i += 1
			token = list(words[start:i+2]).pop()
		elif word in punt_lists and token in punt_lists:
			i += 1
			token = list(words[start:i+2]).pop()
		else:
			sents.append(words[start:i+1])
			start = i+1
			i += 1
	if start < len(words):
		sents.append(words[start:])
	return sents

############################################################################################	
"""
input: '这款手机大小合适。'
output:
    parameter_1: 这 r 款 m 手机 n 大小 b 合适 a 。 x
    parameter_2: [(u'\u8fd9', ['r']), (u'\u6b3e', ['m']),
    (u'\u624b\u673a', ['n']), (u'\u5927\u5c0f', ['b']),
    (u'\u5408\u9002', ['a']), (u'\u3002', ['x'])]
"""
def postagger(sentence, para):
	if para == 'list':
		pos_data1 = jieba.posseg.cut(sentence)
		pos_list = []
		for w in pos_data1:
			#make every word and tag as a tuple and add them to a list
			pos_list.append((w.word, w.flag))
		return pos_list
	elif para == 'str':
		pos_data2 = jieba.posseg.cut(sentence)
		pos_list2 = []
		for w2 in pos_data2:
			pos_list2.extend([w2.word.encode('utf-8'), w2.flag])
		pos_str = ' '.join(pos_list2)
		return pos_str
############################################################################################	
"""
input:
	weibo content
output:
	return True if the weibo is meaningful else return False
	如果微博有意义则返回True
"""
def is_meaningful(weibocontent):
	malwords = [u'红包', u'领取', u'点击', u'专享', u'加号', u'交友', u'http']
	tags = jieba.analyse.extract_tags(weibocontent, 8, False)
	myset = set(malwords) & set(tags)
	meaningful = True if myset.__len__() == 0 else False
	return meaningful
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
	output = open('%s_worddict.pkl' % schoolname, 'w')
	pickle.dump(worddict, output)
	output.close()
############################################################################################	
"""
input:
	schoolname
output:
	返回该学校用词高频率文本或者pickle文件。
"""	
def getHighFrequencyWordPickle(schoolname):
	pkl_file = open('%s_worddict.pkl' % schoolname, 'r')
	loaded_word_dict = pickle.load(pkl_file)
	pkl_file.close()
	highworddict = {}
	for word in loaded_word_dict:
		if loaded_word_dict[word] > 10:
			highworddict[word] = loaded_word_dict[word]
	print len(highworddict), 'highworddict'
	output = open('%s_highwordlist.pkl' % (schoolname), 'w')
	pickle.dump(highworddict, output)
	output.close()
############################################################################################	
"""
input:
	schoolname
output:
	返回该学校用词频率文本或者pickle文件。
"""
def diffSchoolWord(schoolname1, schoolname2):
	pkl_file1 = open('%s_highwordlist.pkl' % schoolname1, 'r')
	loaded_word_dict1 = pickle.load(pkl_file1)
	pkl_file1.close()
	pkl_file2 = open('%s_highwordlist.pkl' % schoolname2, 'r')
	loaded_word_dict2 = pickle.load(pkl_file2)
	pkl_file2.close()
	########
	"""构建临时的比较文本，等最后所有学校的数据齐了后使用最终文本"""
	baseworddict = {}
	print len(loaded_word_dict1)
	print len(loaded_word_dict2)
	if os.path.exists('%s_wordlist.pkl' % (schoolname1+schoolname2)) == False:
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

		output = open('%s_wordlist.pkl' % (schoolname1+schoolname2), 'w')
		pickle.dump(basewordlist, output)
		output.close()
		print len(basewordlist)
	else:
		base_pkl_file = open('%s_wordlist.pkl' % (schoolname1+schoolname2), 'r')
		basewordlist = pickle.load(base_pkl_file)
		pkl_file1.close()
		print len(basewordlist),'2schoolname1+2'
	########
	school1_list = []
	school2_list = []
	# 保证school1_list的长度与basewordlist长度相同
	for i in basewordlist:
		# 所有出现在loaded_word_dict1中的单词全部添加到学校1的列表中，所有没出现的，列表中添加1
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
	idf_pkl = open('idfdict.pkl', 'r')
	idfdict = pickle.load(idf_pkl)
	idf_pkl.close()
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
	print 'considersing tf-idf:', getCos(school1_list, school2_list)
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
"""
description:
	将idf文档转化成字典，并保存在idf.pkl文件中
input:
output:
"""
def convey_Idf_To_Pickle():
	idfdict = {}
	index = 0
	if os.path.exists('idfdict.pkl') == False:
		# 从txt文本中提取到字典中
		for line in open('idf.txt', 'r'):
			idfdict[line.split()[0]] = float(line.split()[1])
		print len(idfdict)
		# 保存到pkl文件中
		output = open('idfdict.pkl', 'w')
		pickle.dump(idfdict, output)
		output.close()
	else:
		print 'idfdict has already existscmd'
############################################################################################
def seg_fil_senti_excel(filepath, sheetnum, colnum):
    # Read product review data from excel file and segment every review
    review_data = []
    for cell in get_excel_data(filepath, sheetnum, colnum, 'data')[0:get_excel_data(filepath, sheetnum, colnum, 'rownum')]:
        review_data.append(segmentation(cell, 'list')) # Seg every reivew
    
    # Read txt file contain sentiment stopwords
    sentiment_stopwords = get_txt_data('sentiment_stopword.txt', 'lines')
 
    # Filter stopwords from reviews
    seg_fil_senti_result = []
    for review in review_data:
        fil = [word for word in review if word not in sentiment_stopwords and word != ' ']
        seg_fil_senti_result.append(fil)
        fil = []

    output = open('%s.pkl' % filepath[:-5], 'w')
    pickle.dump(seg_fil_senti_result, output)
    output.close()
    # Return filtered segment reviews
    return seg_fil_senti_result
############################################################################################
"""
description:
	从数据中获取标记过的微博数据
input:
output:
"""
def getMarkedWeibo():
	marked_weibo_data = []
	pos_weibo = [] # 表达积极情绪的微博
	neg_weibo = [] # 表达消极情绪的微博
	act_weibo = [] # 代表参与一个活动随手转发的微博，一般都是广告，含有链接
	obj_weibo = [] # 客观的微博，即不包含任何感情的微博
	# Read txt file contain sentiment stopwords
	sentiment_stopwords = get_txt_data('sentiment_stopword.txt', 'lines')

	# 获取已经标注过的微博数据，-1代表未知，1代表积极，2代表消极，
	# 3代表活动（有链接，一般是广告），4是客观（没有表达任何情绪）
	get_mark_weibo_sql = "select content, mark from markedweibo;"
	myconnect = GetConnect()
	results = myconnect.getData(get_mark_weibo_sql)
	for weibo in results:
		if weibo[1] == 1:
			pos_weibo.append(weibo[0])
		elif weibo[1] == 2:
			neg_weibo.append(weibo[0])
		elif weibo[1] == 3:
			act_weibo.append(weibo[0])
		elif weibo[1] == 4:
			obj_weibo.append(weibo[0])
	# Filter stopwords from reviews
	seg_pos_result = []
	seg_neg_result = []
	seg_act_result = []
	seg_obj_result = []
	for weibo in pos_weibo:
		fil = [word for word in weibo if word not in sentiment_stopwords and word != ' ']
		seg_pos_result.append(fil)
		fil = []
	for weibo in neg_weibo:
		fil = [word for word in weibo if word not in sentiment_stopwords and word != ' ']
		seg_neg_result.append(fil)
		fil = []
	for weibo in act_weibo:
		fil = [word for word in weibo if word not in sentiment_stopwords and word != ' ']
		seg_act_result.append(fil)
		fil = []
	for weibo in obj_weibo:
		fil = [word for word in weibo if word not in sentiment_stopwords and word != ' ']
		seg_obj_result.append(fil)
		fil = []
	# 将这些数据存储成pickle
	pickle.dump(pos_weibo, open("maked weibo\\seg_pos_result.pkl", 'w'))
	pickle.dump(neg_weibo, open("maked weibo\\seg_neg_result.pkl", 'w'))
	pickle.dump(act_weibo, open("maked weibo\\seg_act_result.pkl", 'w'))
	pickle.dump(obj_weibo, open("maked weibo\\seg_obj_result.pkl", 'w'))
############################################################################################
"""
description:
	从数据中获取标记过的微博数据
input:
output:
"""
def visit_pickle_marked_weibo():
	pos_weibo = [] # 表达积极情绪的微博
	neg_weibo = [] # 表达消极情绪的微博
	act_weibo = [] # 代表参与一个活动随手转发的微博，一般都是广告，含有链接
	obj_weibo = [] # 客观的微博，即不包含任何感情的微博
	#pos_weibo_pkl = open("maked weibo\\pos_weibo.pkl", 'r')
	#neg_weibo_pkl = open("maked weibo\\pos_weibo.pkl", 'r')
	#act_weibo_pkl = open("maked weibo\\act_weibo.pkl", 'r')
	#obj_weibo_pkl = open("maked weibo\\obj_weibo.pkl", 'r')
	#act_weibo = pickle.load(act_weibo_pkl)
	#obj_weibo = pickle.load(obj_weibo_pkl)
	#print len(act_weibo),'#####',len(obj_weibo)
	seg_pos_result = pickle.load(open("maked weibo\\seg_pos_result.pkl", 'r'))
	seg_obj_result = pickle.load(open("maked weibo\\seg_obj_result.pkl", 'r'))
	#print len(seg_pos_result), '####', len(seg_obj_result)
	obj_weibo = seg_pos_result + seg_obj_result
	pickle.dump(obj_weibo, open("maked weibo\\obj_seg_new_weibo.pkl", 'w'))
	print len(obj_weibo)
	print
	
	for i in range(200):
		print obj_weibo[i]
############################################################################################
"""
description:
	从数据中获取一个学校所有的微博并保存成pickle模块
input:
output:
"""
def get_school_weibo_and_save(schoolname):
	if schoolname == 'dlut':
		schooltable = 'wb_ori_no_pic'
	else:
		schooltable = schoolname + '_wb_ori_no_pic'
	get_weibo_sql = "select content from %s;" % schooltable
	myconnect = GetConnect()
	results = myconnect.getData(get_weibo_sql)
	school_weibo = []
	index = 0
	for i in results:
		school_weibo.append(i[0])
		if index < 100:
			print i[0].encode('utf-8')
			index += 1
	pickle.dump(school_weibo, open("machine learning data\\%s_weibo.pkl" % schoolname,'w'))
############################################################################################
"""
description:
    给定一个字符串，返回分词已经去停用词后的词数组
input:
output: 

"""

def seg_weibo_senti(weibos):
    weibo_data = []
    for cell in weibos:
        weibo_data.append(segmentation(cell, 'list')) # Seg every reivew

    # Read txt file contain sentiment stopwords
    sentiment_stopwords = get_txt_data('sentiment_stopword.txt', 'lines')
 
    # Filter stopwords from reviews
    seg_weibo_senti_result = []
    for weibo in weibo_data:
        fil = [word for word in weibo if word not in sentiment_stopwords and word != ' ']
        seg_weibo_senti_result.append(fil)
        fil = []

    pickle.dump(seg_weibo_senti_result, open('weibos.pkl', 'w'))

    # Return filtered segment reviews
    return seg_weibo_senti_result
############################################################################################
def main():
	words = u'这款手机大小合适，配置也还可以，很好用，只是屏幕有点小。。。总之，戴妃+是一款值得购买的只能手机。'
	words2 = '好。'
	words3 = u'快毕业了，我可能要跟女朋友分手了，舍不得！！！'
	'''sents = cut_sentences_2(words3.decode('utf-8'))
	for s in sents:
		print '',s

	schoolname='dlut'
	weibo_content_results = get_one_weibo_data(schoolname)
	if weibo_content_results is None:
		print "There is no data about %s yet." % schoolname
	else:
		for w in weibo_content_results:
			print w[0], w[1], w[2], w[3], w[4]
			print isMeaningful(w[0])
	'''
	schools = ['dlut', 'nanking', 'peking', 'tsinghua', 'ecupsl']
	#getSchooWeiboMeaning('dlut')
	#getWordFrequency('tsinghua')
	#getHighFrequencyWordPickle('tsinghua')
	#diffSchoolWord('dlut', 'tsinghua')
	#getBaseWordText()
	#convey_Idf_To_Pickle()
	#getMarkedWeibo()
	#visit_pickle_marked_weibo()
	#get_school_weibo_and_save(schools[4])
	#get_school_weibo(schools[4])
	#get_school_weibo_2(schools[4])
			
if __name__ == '__main__':
	main()
