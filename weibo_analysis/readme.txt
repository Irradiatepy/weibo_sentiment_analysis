文件夹：
adverbs of degree dictionary:
	里面存放程度副词词典txt。

dict weibo data:
	pickle文件，保存的是五个学校微博分词结果，文件较大，只给出一个学校的。

machine learning data:
	pickle文件，保存机器学习使用到的数据文件。

positive and negative dictionary:
	里面存放积极和消极的情感词典txt。

screenshot：
	里面存放程序运行的相关截图。

segment data:
	里面存放的是微博分词的代码。
	主要通过 weibo_word_segment.py运行,该模块是用来对所有的微博进行分词，并提取出微博关键字，判断出有意义的微博，最终存储在对应的school_wordsegment表中
	
stop word：
	里面存放的为停止词词典txt，用户词典。
	停止词可以用于处理微博数据，用户词典可以添加到结巴分词中。

weibo word contrast:
	里面存放idf.txt文档，存放学校的用词词典，高频用词词典，基向量，学校用词向量等pickle文件。
		
文件：
config.ini
	配置信息文件，提供了数据库配置参数，cookie值，入口微博账户。
	每次只要更新cookie为有效的cookie即可访问微博。

getconnect.py:
	提供数据库连接，相关数据库操作方法

intermediate.py:
	是连接weibo_main.py文件与其他模块的中间层，封装所有的接口调用，
	使得gui程序直接调用intermediate程序就行，而不必考虑其他实现的细节问题

my_text_processing.py:
	文本数据处理模块，具体有分句，分词，
	依赖：getconnect模块

weibo_dict_senti_analysis.py:
	该模块为字典分析微博情感模块
	依赖文件：积极和消极字典文本，程度副词文本，weiboplot模块，my_text_processing模块

weibo_main.py:
	是gui入口程序，最终用来显示整个项目最终成绩的模块。
	使用pygame和pgu模块编写，pgu不支持中文。

weibo_ml_senti_analysis.py:
	该模块为机器学习方式进行微博情感分析，给出微博的情感倾向概率。
	其中涉及到的分类器是由weibo_sentiment_classifier.py模块提供的。

weibo_plot.py:
	提供图形化接口绘制相关的信息
	具体有：
	1. 饼状图绘制一个学校的某个用户的有意义微博和无意义微博的对比（weiboMeaningPieChart）
	2. 饼状图绘制一个学校的有意义微博和无意义微博的对比（schoolWeiboMeaningPieChart）
	3. 折线图描述字典分析后的积极和消极情感的
		总和，均值，方差（singleWeiboAnalysisLineChart）
	依赖：my_text_processing模块

weibo_sentiment_classifier.py:
	生成分类器并存储模块。

weibo_word_contrast.py:
	该模块主要为比较两个学校的常用词的差异，即相似度比较模块。