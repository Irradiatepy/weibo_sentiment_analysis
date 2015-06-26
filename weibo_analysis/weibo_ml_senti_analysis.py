#! /usr/bin/env python2.7
#coding=utf-8

import os.path
#import textprocessing as tp
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


# Use chi_sq to find most informative words of the review
def best_word_features(words):
    return dict([(word, True) for word in words if word in best_words])

def extract_features(data):
    feat = []
    for i in data:
        feat.append(best_word_features(i))
    return feat

###################################################################
def save_features(schoolname):
    # 载入文本数据
    moto = pickle.load(open("machine learning data\\%s_weibo.pkl" % schoolname, 'r'))
    moto_features = extract_features(moto)
    pickle.dump(moto_features, open("machine learning data\\%s_moto_features.pkl" % schoolname, 'w'))

###################################################################
def show_machine_analysis(schoolname):
    # 载入分类器
    classifier = pickle.load(open("machine learning data\\navieBayesv3.pkl", 'r'))

    # 载入best_words
    best_words = pickle.load(open("machine learning data\\best_wordsv3.pkl", 'r'))

    moto_features = pickle.load(open("machine learning data\\%s_moto_features.pkl" % schoolname, 'r'))
    pos_count = 0
    neg_count = 0
    obj_count = 0
    pos_value = 0.0
    neg_value = 0.0
    obj_value = 0.0
    index = 0
    for i in moto_features:
        neg_value = classifier.prob_classify(i).prob('neg')
        pos_value = classifier.prob_classify(i).prob('pos')
        obj_value = classifier.prob_classify(i).prob('obj')
        if neg_value > pos_value and neg_value > obj_value:
            #print 'neg',neg_value
            neg_count += 1
        elif pos_value > neg_value and pos_value > obj_value:
            #print 'pos', pos_value
            pos_count += 1
        else:
            #print 'obj',obj_value
            obj_count += 1
    end_results = [pos_count, neg_count, obj_count]
    pickle.dump(end_results, open('machine learning data\\%s_end_results.pkl' % schoolname, 'w'))
    print end_results

###################################################################
def main():
    schools = ['dlut', 'nanking', 'peking', 'tsinghua', 'ecupsl']
    #save_features(schools[4])
    show_machine_analysis(schools[4])
##########################################################
if __name__ == '__main__':
    main()
