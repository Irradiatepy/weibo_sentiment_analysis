# -*- coding:utf-8 -*-
"""
注：Word Segment.py 能够将给定的原微博表里的微博转换到给定的目的表中，
这里的转换指的是分词和提取关键字和判断微博是否有意义
"""
import sys
import random
import jieba
import jieba.analyse
from getconnect import GetConnect

reload(sys)
sys.setdefaultencoding('utf-8')
############################################################################################
def getSegments(content):
	return " ".join(jieba.cut(content, cut_all=False))
########################################################################################
"""
input:
	weibo content
output:
	返回分词后的微博内容，和is_meaningful(1代表有意义，0代表无意义)
"""
def getKeywordsAndIs_Meaningful(content):
	malWords =[u'红包', u'领取', u'点击', u'专享', u'加号', u'交友', u'http']
	tags = jieba.analyse.extract_tags(content, 8, False)
	myset = set(malWords) & set(tags)
	is_meaningful = 1 if myset.__len__() == 0 else 0
	return str(" ".join(tags)), is_meaningful

############################################################################################
def main(sourcetable, destable):
	myconnect = GetConnect()
	sql = "select * from %s" % sourcetable
	numrows = myconnect.getCount(sql)
	myconnect2 = GetConnect()
	for r in xrange(numrows):
		row = myconnect.cursor.fetchone()
		wmd5, weiboid, wcontent = row[0], row[1], row[3]
		segments = str(getSegments(wcontent))
		keywords, is_meaningful = getKeywordsAndIs_Meaningful(wcontent)
		insert_sql = "replace into %s(wmd5, weiboid, segments, keywords, is_meaningful) values('%s', '%s', '%s', '%s', %s)" % (destable, wmd5, weiboid, segments, keywords, is_meaningful)
		try:
			myconnect2.executeDB(insert_sql)
		except Exception, e:
			print "Error %d: %s" % (e.args[0],e.args[1])
			
if __name__ == '__main__':
	main('ecupsl_wb_ori_no_pic','ecupsl_wordsegment')
