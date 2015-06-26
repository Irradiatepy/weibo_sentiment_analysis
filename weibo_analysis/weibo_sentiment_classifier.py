#! /usr/bin/env python2.7
#coding=utf-8

import textprocessing as tp
import pickle
import itertools
from random import shuffle

import nltk
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures
from nltk.probability import FreqDist, ConditionalFreqDist

import sklearn
from sklearn.svm import SVC, LinearSVC, NuSVC
from sklearn.naive_bayes import GaussianNB, MultinomialNB, BernoulliNB
from sklearn.linear_model import LogisticRegression
from nltk.classify.scikitlearn import SklearnClassifier
from sklearn.metrics import accuracy_score


# 1. Load positive and negative review data
# posdata是list类型，长度1084，表中每个元素都是一个list，如元素：[u'\u7535\u6c60', u'\u4e0d\u7ed9\u529b', u'\u90fd']，
# 是每条评论的分词,如[电池 不给力 都 很 好 老婆 买 带 16G 卡 一张]
'''
posdata = pickle.load(open("seg_pos_result.pkl",'r'))
negdata = pickle.load(open("seg_neg_result.pkl",'r'))
objdata = pickle.load(open("obj_seg_new_weibo.pkl", 'r'))
'''
posdata = pickle.load(open("pos_weibo.pkl",'r'))
negdata = pickle.load(open("neg_weibo.pkl",'r'))
objdata = pickle.load(open("obj_new_weibo.pkl", 'r'))

pos = posdata
neg = negdata
obj = objdata
# 2. Feature extraction function
# 2.1 Use all words as features
def bag_of_words(words):
    return dict([(word, True) for word in words])


# 2.2 Use bigrams as features (use chi square chose top 200 bigrams)
def bigrams(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(bigrams)


# 2.3 Use words and bigrams as features (use chi square chose top 200 bigrams)
def bigram_words(words, score_fn=BigramAssocMeasures.chi_sq, n=200):
    bigram_finder = BigramCollocationFinder.from_words(words)
    bigrams = bigram_finder.nbest(score_fn, n)
    return bag_of_words(words + bigrams)


# 2.4 Use chi_sq to find most informative features of the review
# 2.4.1 First we should compute words or bigrams information score
def create_word_scores():
    # posdata是list类型，长度1084，表中每个元素都是一个list，如元素：[u'\u7535\u6c60', u'\u4e0d\u7ed9\u529b', u'\u90fd']，
    # 是每条评论的分词,如[电池 不给力 都 很 好 老婆 买 带 16G 卡 一张]
    
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))
    objWords = list(itertools.chain(*objdata))

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()

    for word in posWords:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in negWords:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1
    for word in objWords:
        word_fd[word] += 1
        cond_word_fd['obj'][word] += 1

    pos_word_count = cond_word_fd['pos'].N() # N()计算出现过的次数总和，可以理解为所有pos类型的词出现的次数总和
    neg_word_count = cond_word_fd['neg'].N()
    obj_word_count = cond_word_fd['obj'].N()
    total_word_count = pos_word_count + neg_word_count + obj_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        obj_score = BigramAssocMeasures.chi_sq(cond_word_fd['obj'][word], (freq, obj_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score + obj_score

    return word_scores

def create_bigram_scores():
    
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))
    objWords = list(itertools.chain(*objdata))

    bigram_finder = BigramCollocationFinder.from_words(posWords)
    bigram_finder = BigramCollocationFinder.from_words(negWords)
    bigram_finder = BigramCollocationFinder.from_words(objWords)
    posBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 8000)
    negBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 8000)
    
    objBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 8000)

    pos = posBigrams
    neg = negBigrams
   
    obj = objBigrams
    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()
    for word in pos:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in neg:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1
    for word in objWords:
        word_fd[word] += 1
        cond_word_fd['obj'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    
    obj_word_count = cond_word_fd['obj'].N()
    total_word_count = pos_word_count + neg_word_count + obj_word_count
    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
        
        obj_score = BigramAssocMeasures.chi_sq(cond_word_fd['obj'][word], (freq, obj_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score  + obj_score
    return word_scores

# Combine words and bigrams and compute words and bigrams information scores
def create_word_bigram_scores():
    posWords = list(itertools.chain(*posdata))
    negWords = list(itertools.chain(*negdata))
    
    objWords = list(itertools.chain(*objdata))

    bigram_finder = BigramCollocationFinder.from_words(posWords)
    bigram_finder = BigramCollocationFinder.from_words(negWords)
    
    bigram_finder = BigramCollocationFinder.from_words(objWords)
    posBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)
    negBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)
    
    objBigrams = bigram_finder.nbest(BigramAssocMeasures.chi_sq, 5000)


    pos = posWords + posBigrams
    neg = negWords + negBigrams
    
    obj = objWords + objBigrams

    word_fd = FreqDist()
    cond_word_fd = ConditionalFreqDist()
    for word in pos:
        word_fd[word] += 1
        cond_word_fd['pos'][word] += 1
    for word in neg:
        word_fd[word] += 1
        cond_word_fd['neg'][word] += 1
    for word in objWords:
        word_fd[word] += 1
        cond_word_fd['obj'][word] += 1

    pos_word_count = cond_word_fd['pos'].N()
    neg_word_count = cond_word_fd['neg'].N()
    
    obj_word_count = cond_word_fd['obj'].N()
    total_word_count = pos_word_count + neg_word_count + obj_word_count

    word_scores = {}
    for word, freq in word_fd.iteritems():
        pos_score = BigramAssocMeasures.chi_sq(cond_word_fd['pos'][word], (freq, pos_word_count), total_word_count)
        neg_score = BigramAssocMeasures.chi_sq(cond_word_fd['neg'][word], (freq, neg_word_count), total_word_count)
       
        obj_score = BigramAssocMeasures.chi_sq(cond_word_fd['obj'][word], (freq, obj_word_count), total_word_count)
        word_scores[word] = pos_score + neg_score + obj_score

    return word_scores

# Choose word_scores extaction methods
# word_scores是一个字典，如：划开 5.16503343808，每个词，对应一个频率
word_scores = create_word_scores()
#word_scores = create_bigram_scores()
#word_scores = create_word_bigram_scores()

# 2.4.2 Second we should extact the most informative words or bigrams based on the information score
def find_best_words(word_scores, number):
    best_vals = sorted(word_scores.iteritems(), key=lambda (w, s): s, reverse=True)[:number]
    best_words = set([w for w, s in best_vals])
    return best_words

# Set dimension and initiallize most informative words
# 集合，长度1500,如：差手，退，出来，重启
best_words = find_best_words(word_scores,1250) 
#pickle.dump(best_words, open("best_wordsv3.pkl", 'w'))

# 2.4.3 Third we could use the most informative words and bigrams as machine learning features
# Use chi_sq to find most informative words of the review
def best_word_features(words):
    return dict([(word, True) for word in words if word in best_words])


# 3. Transform review to features by setting labels to words in review
def pos_features(feature_extraction_method):
    posFeatures = []
    for i in pos:
        posWords = [feature_extraction_method(i),'pos']
        posFeatures.append(posWords)
    return posFeatures

def neg_features(feature_extraction_method):
    negFeatures = []
    for j in neg:
        negWords = [feature_extraction_method(j),'neg']
        negFeatures.append(negWords)
    return negFeatures

def act_features(feature_extraction_method):
    actFeatures = []
    for j in act:
        actWords = [feature_extraction_method(j),'act']
        actFeatures.append(actWords)
    return actFeatures

def obj_features(feature_extraction_method):
    objFeatures = []
    for j in obj:
        objWords = [feature_extraction_method(j),'obj']
        objFeatures.append(objWords)
    return objFeatures
# 把选出的这些词作为特征
# （这就是选择了信息量丰富的特征）
# 这里长度为1084，类型为list,
# 如：[[{'哎':True,'觉得':True},'pos'],...]
posFeatures = pos_features(best_word_features)
negFeatures = neg_features(best_word_features)

objFeatures = obj_features(best_word_features)

# 4. Train classifier and examing classify accuracy
# Make the feature set ramdon
# 打乱顺序
shuffle(posFeatures)
shuffle(negFeatures)

shuffle(objFeatures)


# 75% of features used as training set (in fact, it have a better way by using cross validation function)
size_pos = int(len(posdata) * 0.75)
size_neg = int(len(negdata) * 0.75)

size_obj = int(len(objdata) * 0.75)

# 划分出训练集和测试集，取75%为训练集，剩下的25%为测试集
train_set = posFeatures[:size_pos] + negFeatures[:size_neg] + objFeatures[:size_obj]
test_set = posFeatures[size_pos:] + negFeatures[size_neg:] + objFeatures[size_obj:]

test, tag_test = zip(*test_set)
'''
def nltk_naivebayes_clf_score(classifier):
    classifier.train(train_set)
    return nltk.classify.accuracy(classifier, test_set)
def clf_score(classifier):
    classifier = SklearnClassifier(classifier)
    classifier.train(train_set)

    predict = classifier.batch_classify(test)
    return accuracy_score(tag_test, predict)

print 'BernoulliNB`s accuracy is %f' %clf_score(BernoulliNB())
print 'GaussianNB`s accuracy is %f' %clf_score(GaussianNB())
print 'MultinomiaNB`s accuracy is %f' %clf_score(MultinomialNB())
print 'LogisticRegression`s accuracy is %f' %clf_score(LogisticRegression())
print 'SVC`s accuracy is %f' %clf_score(SVC(gamma=0.001, C=100., kernel='linear'))
print 'LinearSVC`s accuracy is %f' %clf_score(LinearSVC())
print 'NuSVC`s accuracy is %f' %clf_score(NuSVC())
'''
classifier = nltk.NaiveBayesClassifier.train(train_set)
# 载入文本数据
moto = pickle.load(open("weibos.pkl", 'r'))

def extract_features(data):
    feat = []
    for i in data:
        feat.append(best_word_features(i))
    return feat

moto_features = extract_features(moto)
'''
for i in moto_features:
    for j in i:
        print '', j.encode('utf-8')
    print classifier.classify(i)'''
#print classifier.classify(moto_features[3])
naive_bayes_accuracy = nltk.classify.accuracy(classifier, test_set)
print naive_bayes_accuracy
'''
if naive_bayes_accuracy > 0.694:
    pickle.dump(classifier, open("navieBayesv3.pkl", 'w'))
    print "done"
else:
    print "undone" '''
print 
print 
for i in moto_features:
    print classifier.prob_classify(i).prob('neg'),classifier.prob_classify(i).prob('pos'),classifier.prob_classify(i).prob('obj')
    #print len(classifier.prob_classify(i))
#for i in classifier.most_informative_features(50):
#   print i[0].encode('utf-8')
#print "nltk's NaiveBayes accuracy is %f" % nltk_naivebayes_clf_score(classifier)
