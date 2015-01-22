#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# http://inclass.kaggle.com/c/ml-course-internal-competition

import os
import numpy as np

def read_ft(fname):
    f = open(fname)
    xs = []
    for s in f:
        s = s.strip()
        xs.append(map(lambda x: int(x),s.split(' ')))
    f.close()
    # 选择特征非常重要:
    # 选择横竖以及正反对角线上1的分布作为feature.
    n = len(xs)
    xs2 = []
    for i in range(0, n):
        v = 0
        for j in range(0, n): v += xs[i][j]
        xs2.append(v)
    for j in range(0, n):
        v = 0
        for i in range(0, n): v += xs[i][j]
        xs2.append(v)
    tk = n
    for r in range(tk, -1, -1):
        v = 0
        c = 0
        while r < n:
            v += xs[r][c]
            c += 1; r += 1
        xs2.append(v)
    for c in range(0, tk):
        v = 0
        r = 0
        while c < n:
            v += xs[r][c]
            r += 1; c += 1
        xs2.append(v)
    for c in range(0, tk):
        v = 0
        r = 0
        while c >= 0:
            v += xs[r][c]
            r += 1; c -= 1
        xs2.append(v)
    for r in range(0, tk):
        v = 0
        c = 0
        while r < n:
            v += xs[r][c]
            r += 1; c -= 1
        xs2.append(v)
    xs3 = [0] * (n+1)
    for x in xs2:
        xs3[x] += 1
    return np.array(xs3)

# 训练数据
def load_tr():
    ys = []
    xs = []
    mp = (('1',1), ('2',3),('3',5))
    for p in mp:
        (tag, y) = p
        for f in os.listdir('tr/' + tag):
            ys.append(y)
            x = read_ft('tr/' + tag + '/' + f)
            xs.append(x)
    return (np.array(xs), np.array(ys))

# 测试数据
def load_tt():
    xs = []
    for f in range(1, 31):
        x = read_ft('tt/' + str(f) + '.txt')
        xs.append((f, x))
    return xs

from sklearn import svm
from sklearn.svm import SVC
from sklearn.cross_validation import train_test_split
from sklearn.grid_search import GridSearchCV
from sklearn.metrics import classification_report

def train(tr):
    print('------------------------------')
    (X, Y) = tr
    tr_x, tt_x, tr_y, tt_y = train_test_split(X, Y, test_size = 0.2, random_state = 0)
    print('train_size = %d, test_size = %d' % (tr_y.shape[0], tt_y.shape[0]))
    tuned_parameters = [{'kernel': ['rbf'], 'gamma': [ 1e-5, 1e-4, 1e-3, 1e-2], 'C': [1, 10, 100]}]
    clf = GridSearchCV(SVC(), tuned_parameters, cv = 6)
    clf.fit(tr_x, tr_y)
    print("Best parameters set found on development set:")
    print(clf.best_estimator_)
    print("Grid scores on development set:")
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r"
            % (mean_score, scores.std() / 2, params))
    print("Detailed classification report:")
    print("The model is trained on the full development set.")
    print("The scores are computed on the full evaluation set.")
    y_true, y_pred = tt_y, clf.predict(tt_x)
    print(classification_report(y_true, y_pred))
    print('------------------------------')
    return clf

def test(clf, tt):
    print('------------------------------')
    # 人工识别出来的
    y_true = [1,1,5,3,1,3,3,5,1,3,1,5,5,1,3,3,5,5,5,3,5,1,1,3,3,5,1,3,5,1]
    preds = clf.predict(map(lambda x: x[1], tt))
    print(classification_report(y_true, preds))
    print('------------------------------')

def main():
    print('loading training set ...')
    tr = load_tr()
    print('loading test set ...')
    tt = load_tt()
    print('training ...')
    clf = train(tr)
    print('testing ...')
    test(clf, tt)

if __name__ == '__main__':
    main()
