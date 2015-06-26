# -*- coding:utf-8 -*-
import sys
import numpy as np
import my_text_processing as tp
import weiboplot as wpl
import pickle
reload(sys)
sys.setdefaultencoding('utf-8')
############################################################################################
# 1. Load dictionary and dataset
# Load sentiment dictionary
posdict = tp.get_txt_data("positive and negative dictionary/posdict.txt", "lines")
negdict = tp.get_txt_data("positive and negative dictionary/negdict.txt", "lines")

# Load adverbs of degree dictionary
mostdict = tp.get_txt_data('adverbs of degree dictionary/most.txt', 'lines')
verydict = tp.get_txt_data('adverbs of degree dictionary/very.txt', 'lines')
moredict = tp.get_txt_data('adverbs of degree dictionary/more.txt', 'lines')
ishdict = tp.get_txt_data('adverbs of degree dictionary/ish.txt', 'lines')
insufficientdict = tp.get_txt_data('adverbs of degree dictionary/insufficiently.txt', 'lines')
inversedict = tp.get_txt_data('adverbs of degree dictionary/inverse.txt', 'lines')

# Load dataset
weibo = u'纯吐槽…大学班里有一男生，走路我打招呼都不正眼瞧我，前段时间突然加我微信，开口就让我帮买iphone。。我抢了几次未果就没帮他买。刚才无聊搞了个微信测试，发现这人早把我删了。。我就想说好歹四年的同学，人与人之间起码的尊重呢。你丫这样我真是一辈子都不想再有任何联系。。[位置]香港中西区'

# 2.0 Sentiment dictionary analysis basic function
# Function of mathcing adverbs of degree and set weights
def match(word, sentiment_value):
	if word in mostdict: #太，极其，惊人的
		sentiment_value *= 2.0
	elif word in verydict: #很是，颇为，实在
		sentiment_value *= 1.5
	elif word in moredict: #大不了，愈发，进一步
		sentiment_value *= 1.25
	elif word in ishdict: #或多或少，稍微，未免
		sentiment_value *= 0.5
	elif word in insufficientdict: #半点，丁点，丝毫
		sentiment_value *= 0.25
	elif word in inversedict: #不，没有，此时会否定掉前面的肯定意义
		sentiment_value *= -1
	return sentiment_value

# Function of transforming negative score to positive score
# Example: [5, -2] -> [7, 0]; [-4, 8] -> [0, 12]
def transform_to_positive_num(poscount, negcount, upvotes=0, forwards=0, reviews=0):
	pos_count = 0
	neg_count = 0
	if poscount < 0 and negcount >= 0:
		neg_count += negcount - poscount
		pos_count = 0
	elif negcount < 0 and poscount >= 0:
		pos_count = poscount - negcount
		negcount = 0
	elif poscount < 0 and negcount < 0:
		neg_count = -poscount
		pos_count = -negcount
	else:
		pos_count = poscount
		neg_count = negcount
	if upvotes != 0 or forwards != 0 or reviews != 0:
		pos_count *= 1.25
		neg_count *= 1.25
		#print 'haha
	return [pos_count, neg_count]

# 3.1 Single weibo's positive and negative score
# Function of calculating weibo's every sentence sentiment score
def sumup_sentence_sentiment_score(score_list):
	score_array = np.array(score_list) #将list转换成数组供np计算使用
	Pos = np.sum(score_array[:,0]) # Compute positive score
	Neg = np.sum(score_array[:,1])
	AvgPos = np.mean(score_array[:,0]) # Compute weibo positive average score, average score = score/sentence number
	AvgNeg = np.mean(score_array[:,1])
	StdPos = np.std(score_array[:,0]) # Compute weibo positive standard deviation score(标准差)
	StdNeg = np.std(score_array[:,1])
	return [Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg]

def single_weibo_sentiment_score(weibo):
	single_weibo_senti_score = []
	cuted_weibo = tp.cut_sentences_2(weibo) # 切分成一个个小句子的list

	for sent in cuted_weibo:
		print '', sent
		seg_sent = tp.segmentation(sent, 'list') # 分词，返回单词列表
		i = 0 # word position counter
		s = 0 # sentiment word position
		poscount = 0 # count a positive word
		negcount = 0 # count a negative word

		for word in seg_sent:
			print '', word
			if word in posdict:
				poscount += 1
				for w in seg_sent[s:i]:
					poscount = match(w, poscount)
				a = i + 1
			elif word in negdict:
				negcount += 1
				for w in seg_sent[s:i]:
					negcount = match(w, negcount)
				a = i + 1
			# Match "！" in the weibo, every "！" has a weight of +2
			elif word == "!".decode('utf-8') or word == "！".decode('utf-8'):
				for w2 in seg_sent[::-1]:
					if w2 in posdict:
						poscount += 2
						break
					elif w2 in negdict:
						negcount += 2
						break
			i += 1
		print 'positive and negative',poscount, negcount
		single_weibo_senti_score.append(transform_to_positive_num(poscount, negcount))
		weibo_sentiment_score = sumup_sentence_sentiment_score(single_weibo_senti_score)
	for i in single_weibo_senti_score:
		print i
	return weibo_sentiment_score

# 3.2 All weibo dataset's sentiment score
def all_weibo_sentence_sentiment_score(schoolname, weiboid=None):
	weibo_content_results = tp.get_one_weibo_data(schoolname, weiboid)
	cuted_weibo = []
	upvotes = []
	forwards = []
	reviews = []
	weiboid = None
	for cell in weibo_content_results:
		cuted_weibo.append(tp.cut_sentences_2(cell[0]))
		upvotes.append(int(cell[1]))
		forwards.append(int(cell[2]))
		reviews.append(int(cell[3]))
		weiboid = cell[4]
		'''
		print cell[0] #微博内容
		'''
		#print cell[1], #点赞数量
		#print cell[2] #转发数量
		#print cell[3] #评论数量
	
	single_weibo_count = []
	all_weibo_count = []
	for index,weibo in enumerate(cuted_weibo):
		for sent in weibo:
			seg_sent = tp.segmentation(sent, 'list')
			i = 0 # word position counter
			a = 0 # sentiment word position
			poscount = 0 # count a positive word
			negcount = 0 # count a negative word
			for word in seg_sent:
				if word in posdict:
					poscount += 1
					for w in seg_sent[a:i]:
						poscount = match(w, poscount)
					a = i + 1
				elif word in negdict:
					negcount += 1
					for w in seg_sent[a:i]:
						negcount = match(w, negcount)
					a = i + 1
				elif word == '!'.decode('utf-8') or word == '！'.decode('utf-8'):
					for w2 in seg_sent[::-1]:
						if w2 in posdict:
							poscount += 2
							break
						elif w2 in negdict:
							negcount += 2
							break
				i += 1
			single_weibo_count.append(transform_to_positive_num(poscount, negcount, upvotes[index], forwards[index], reviews[index])) #[[s1_score], [s2_score], ...]
		all_weibo_count.append(single_weibo_count) # [[[s11_score], [s12_score], ...], [[s21_score], [s22_score], ...], ...]
		single_weibo_count = []
	return all_weibo_count, weiboid
############################################################################################	
"""
description:
	通过给定学校名称，在有意义的微博里面判断积极的微博数和消极的微博数目
input:
	schoolname
output:
	返回一个数组，0项表示积极的微博数目，1项表示消极的微博数目，2项代表无意义的微博数目
"""
def school_weibo_dict_analysis(schoolname):
	weibo_content_results = pickle.load(open('dict weibo data\\%s_seg_weibo_new.pkl' % (schoolname), 'r'))
	cuted_weibo = []
	meaning_count = 0
	positive_count = 0
	negative_count = 0
	for cell in weibo_content_results:
		if cell[1] == 1:
			cuted_weibo.append(tp.cut_sentences_2(cell[0]))
			#pass
		else:
			meaning_count += 1
	single_weibo_count = []
	for index,weibo in enumerate(cuted_weibo):
		single_weibo_count = []
		for sent in weibo:
			seg_sent = tp.segmentation(sent, 'list')
			i = 0 # word position counter
			a = 0 # sentiment word position
			poscount = 0 # count a positive word
			negcount = 0 # count a negative word
			for word in seg_sent:
				if word in posdict:
					poscount += 1
					for w in seg_sent[a:i]:
						poscount = match(w, poscount)
					a = i + 1
				elif word in negdict:
					negcount += 1
					for w in seg_sent[a:i]:
						negcount = match(w, negcount)
					a = i + 1
				elif word == '!'.decode('utf-8') or word == '！'.decode('utf-8'):
					for w2 in seg_sent[::-1]:
						if w2 in posdict:
							poscount += 2
							break
						elif w2 in negdict:
							negcount += 2
							break
				i += 1
			single_weibo_count.append(transform_to_positive_num(poscount, negcount, 0, 0, 0))
		[pos_count, neg_count] = judge_weibo(single_weibo_count)
		#print index, pos_count, neg_count
		if pos_count > neg_count:
			positive_count += 1
		elif pos_count < neg_count:
			negative_count += 1
		else:
			meaning_count += 1
	end_results = [positive_count, negative_count, meaning_count]
	pickle.dump(end_results, open('dict weibo data\\%s_end_results.pkl' % schoolname, 'w'))
	print end_results
	return end_results
############################################################################################	
def judge_weibo(single_weibo_count):
	pos_count, neg_count = 0, 0
	for i in single_weibo_count:
		pos_count += i[0]
		neg_count += i[1]
	return pos_count, neg_count
############################################################################################	
# Computer all weibo's sentiment score
def all_weibo_sentiment_score(senti_score_list):
	score = []
	for weibo in senti_score_list:
		score_array = np.array(weibo)
		Pos = np.sum(score_array[:,0])
		Neg = np.sum(score_array[:,1])
		AvgPos = np.mean(score_array[:,0])
		AvgNeg = np.mean(score_array[:,1])
		StdPos = np.std(score_array[:,0])
		StdNeg = np.std(score_array[:,1])
		score.append([Pos, Neg, AvgPos, AvgNeg, StdPos, StdNeg])
	return score
############################################################################################
'''
	红色线表示积极的，绿色线表示消极的
'''
def show_ones_weibo(schoolname, weiboid=None):
	all_weibo_count, weiboid = all_weibo_sentence_sentiment_score(schoolname, weiboid)
	print all_weibo_count
	print weiboid
	for i in all_weibo_sentiment_score(all_weibo_count):
		print i
	wpl.singleWeiboAnalysisLineChart(schoolname=schoolname, weiboid=weiboid, all_weibo_count=all_weibo_count)

############################################################################################
def main():
	#print single_weibo_sentiment_score(weibo)
	schools = ['dlut', 'nanking', 'peking', 'tsinghua', 'ecupsl']
	show_ones_weibo(schools[0])
	#school_weibo_dict_analysis(schools[4])
	
if __name__ == '__main__':
	main()
