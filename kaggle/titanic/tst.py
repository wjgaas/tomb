#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import numpy as np
import scipy as sp

# http://www.kaggle.com/c/titanic-gettingStarted

def read_in(s, test = False):
    s = s.strip()
    s = s.replace(', ', '. ')
    ss = s.split(',')
    if not test:
        (pid, y, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked) = ss
    else:
        (pid, pclass, name, sex, age, sibsp, parch, ticket, fare, cabin, embarked) = ss
    pid = int(pid)
    pclass = int(pclass)
    if sex == 'male': gender = 1
    else: assert(sex == 'female'); gender = 0

    if not age: age = 28
    else: age = float(age)

    # 0,1,2,3,4,5,8
    sibsp = int(sibsp)
    # 0,1,2,3,4,5,6
    parch = int(parch)

    # 根据class估计中值费用
    median_fare = [60.28, 14.25, 8.05]
    if not fare: fare = median_fare[pclass - 1]
    fare = float(fare)

    # #. of null = 687.
    if cabin: cabin = cabin[0]
    cs = {'':0, 'A':1, 'B':2, 'C':3, 'D':4,'E':5,'F':6,'G':7,'T':8}
    c = cs[cabin]

    if embarked == 'C': port = 0
    elif embarked == 'Q': port = 1
    elif embarked == 'S': port = 2
    else: port = 2 # 测试数据集合没有为空情况
    # 训练数据只有2个cases, 所以可以分配一个相对比较多的类别.

    #       0         1   2    3        4   5      6   7
    x = [pclass, gender, age, sibsp, parch, fare, c, port]
    # 根据random forest计算出的特征重要性
    #   pclass        gender      age           sibsp       parch      fare      cabin         port
    # [ 0.08164458  0.29202753  0.20687465  0.04891756  0.03969756  0.22704767  0.07028126  0.03350917]
    if not test: return (x, int(y))
    return (x, pid)

# 再变换
def tp(xs, f): return np.array(map(lambda x: np.array(f(x)), xs))
def read_train():
    f = open('train.csv')
    xs = []
    ys = []
    for s in f:
        if s.startswith('PassengerId'): continue
        (x, y) = read_in(s)
        xs.append(np.array(x))
        ys.append(y)
    f.close()
    xs = np.array(xs)
    ys = np.array(ys)
    return (xs, ys)

def read_test():
    f = open('test.csv')
    xs = []
    pids = []
    for s in f:
        if s.startswith('PassengerId'): continue
        (x, pid) = read_in(s, True)
        xs.append(np.array(x))
        pids.append(pid)
    f.close()
    xs = np.array(xs)
    return (xs, pids)

from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import cross_val_score, KFold, StratifiedKFold
from sklearn.grid_search import GridSearchCV
from sklearn.svm import SVC
from sklearn.metrics import f1_score, precision_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.ensemble import GradientBoostingClassifier

def print_best_estimator(clf):
    print("Best parameters set found on development set:")
    print(clf.best_estimator_)
    print("Grid scores on development set:")
    for params, mean_score, scores in clf.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r" % (mean_score, 2 * scores.std(), params))

def select_rf(tr):
    (X, Y) = tr
    fields = (0,1,2,3,4,5,6,7)
    X = X[:,fields]
    n = 100
    tuning = 0
    rf = RandomForestClassifier(n_estimators = n, min_samples_split = 6, random_state = 0)

    # Probability Calibration
    cutoff_value = 0.5
    def cutoff_f1(clf, X, y):
        y_pred = (clf.predict_proba(X)[:,1] > cutoff_value).astype(int)
        y_pred2 = clf.predict(X)
        s1 = f1_score(y, y_pred)
        s2 = f1_score(y, y_pred2)
        # print 'f1 = %.4f, %.4f' % (s1, s2)
        return s1

    if not tuning:
        class Clf:
            def __init__(self):pass
            def fit(self, xs, ys):
                rf.fit(xs[:,fields], ys)
            def predict(self, xs):
                # y_pred = (rf.predict_proba(xs[:,fields])[:,1] > cutoff_value).astype(int)
                y_pred = rf.predict(xs[:,fields]).astype(int)
                return y_pred
            def ftimp(self):
                return rf.feature_importances_
        return Clf()

    tuned_parameters = [{'min_samples_split': [5,6,7]}]
    clf = GridSearchCV(rf, tuned_parameters, scoring = 'f1', cv = KFold(X.shape[0], 10, shuffle = True, random_state = 0) , verbose = 2)
    clf.fit(X, Y)
    print_best_estimator(clf)
    print 'feature importances = ', clf.best_estimator_.feature_importances_

def select_gbdt(tr):
    (X, Y) = tr
    fields = (0,1,2,3,4,5,6,7)
    X = X[:,fields]
    n = 100
    tuning = 0
    gbdt = GradientBoostingClassifier(n_estimators = n, max_depth = 4, random_state = 0)

    if not tuning:
        class Clf:
            def __init__(self):pass
            def fit(self, xs, ys):
                gbdt.fit(xs[:,fields], ys)
            def predict(self, xs):
                return gbdt.predict(xs[:,fields])
        return Clf()

    tuned_parameters = [{'max_depth':[3,4,5]}]
    clf = GridSearchCV(gbdt, tuned_parameters, scoring = 'f1', cv = KFold(X.shape[0], 10, shuffle = True, random_state = 0), verbose = 2)
    clf.fit(X, Y)
    print_best_estimator(clf)

def tf_svm(x):
    (pclass, gender, age, sibsp, parch, fare, c, port) = x
    nx = []
    v = [0] * 3
    v[int(pclass)-1] = 1
    nx.extend(v)
    nx.append(gender)

    if age < 7: nx.append(1)
    else: nx.append(0)
    if age > 30: nx.append(1)
    else: nx.append(0)
    if age < 7 or age > 30: r = 0.0
    else: r = (age - 7) / (30 - 7)
    nx.append(r)

    nx.append(sibsp * 1.0 / 8)
    nx.append(parch * 1.0 / 6)

    if fare > 200: fare = 165.0
    nx.append(fare * 1.0 / 166)

    v = [0] * 9
    v[int(c)] = 1
    nx.extend(v)

    v = [0] * 3
    v[int(port)] = 1
    nx.extend(v)
    return nx

def select_svm(tr):
    (X, Y) = tr

    X = tp(X, tf_svm)
    tuning = 1
    clf = SVC(C = 1, kernel = 'rbf', gamma = 1e-1, random_state = 0)
    if not tuning:
        class Clf:
            def __init__(self): pass
            def fit(self, xs, ys):
                clf.fit(tp(xs, tf_svm), ys)
            def predict(self, xs):
                return clf.predict(tp(xs, tf_svm))
        return Clf()

    tuned_parameters = [{'kernel':['rbf'], 'C': [1, 2, 5], 'gamma':[1e-2, 1e-1, 1, 2]}]
    clf = GridSearchCV(clf, tuned_parameters, scoring = 'f1', cv = KFold(X.shape[0], 10, shuffle = True, random_state = 0), verbose = 2)
    clf.fit(X, Y)
    print_best_estimator(clf)

def run():
    print 'loading train set...'
    tr = read_train()
    print 'load test set...'
    tt = read_test()

    clf0 = select_rf(tr)
    clf1 = select_gbdt(tr)
    # clf2 = select_svm(tr)
    if clf0 and clf1:
        class Clf:
            def __init__(self): pass
            def fit(self, xs, ys):
                clf0.fit(xs, ys)
                clf1.fit(xs, ys)
            def predict(self, xs):
                y = clf0.predict(xs)
                y += clf1.predict(xs)
                y = np.around(y / 2.0)
                return y
        clf = Clf()
    clf = clf1
    if not clf: return

    print 'evaluating...'
    (X, Y) = tr
    kf = KFold(X.shape[0], 10)
    scores = []
    for tr_idx, tt_idx in kf:
        clf.fit(X[tr_idx], Y[tr_idx])
        y_pred = clf.predict(X[tt_idx])
        s = f1_score(Y[tt_idx], y_pred)
        scores.append(s)
    scores = np.array(scores)
    print 'score = %.4f(+-%.4f)' % (scores.mean(), 2 * scores.std())

    print 'learning ...'
    (X, Y) = tr
    clf.fit(X, Y)
    print 'predicting...'
    ys = clf.predict(tt[0])
    f = open('submission.csv','w')
    f.write('PassengerId,Survived\n')
    pids = tt[1]
    sz = len(ys)
    for i in range(0, sz):
        f.write('%s,%d\n'% (pids[i], ys[i]))
    f.close()

if __name__ == '__main__':
    run()
