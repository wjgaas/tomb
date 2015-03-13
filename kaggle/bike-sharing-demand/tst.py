#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import numpy as np
import pickle
from sklearn.externals import joblib
import datetime

# binning.
atemp_range = range(0, 46 + 2, 2)
temp_range = range(0, 41 + 2, 2)
humidity_range = range(0, 100 + 2, 2)
windspd_range =  range(0, 56 + 2, 2)

def bsidx(v, r):
    s = 0
    e = len(r) - 1
    if v > r[e]: return e + 1
    while s <= e:
        m = (s + e) / 2
        if v <= r[m]:
            e = m - 1
        else:
            s = m + 1
    return s

def read_in(s, test = False):
    ss = s.split(',')
    (dt, tm) = ss[0].split(' ')
    (year, month, day) = map(lambda x:int(x), dt.split('-'))
    dt2 = datetime.datetime(year, month, day)
    # http://shubhamtomar.me/2015/02/25/Bike-Sharing-Demand/
    # 把weekday考虑进去
    weekday = dt2.weekday()
    hour = int(tm.split(':')[0]) # 0-23
    season = int(ss[1]) # 1-4
    holiday = int(ss[2]) # 0,1
    wkday = int(ss[3]) # 0,1
    weather = int(ss[4]) # 1-4
    # temp = bsidx(float(ss[5]), temp_range) # 0.380696399388 0.0838957548628
    temp = float(ss[5])
    atemp = float(ss[6])
    humidity = float(ss[7])
    windspd = float(ss[8])
    #    0         1       2          3        4        5    6         7     8       9       10
    p = [weekday, hour, year - 2011, season, holiday, wkday, weather, temp, atemp, humidity, windspd]
    if not test: return (p, int(ss[9]), int(ss[10]))
    else: return (p, ss[0])

# 对ts按照(mn,mx,step)做直方图统计
# 使用binning
def histogram(ts, mn, mx, step):
    ss = np.arange(mn, mx, step)
    ss2 = zip(ss[:-1], ss[1:])
    return (ss[1:], np.array([ts[np.logical_and(ts >= l, ts < h)].shape[0] for (l,h) in ss2]))
# 不使用binning
def histogram2(ts):
    d = {}
    for t in ts:
        if not t in d: d[t] = 1
        else: d[t] += 1
    return d

def read_train():
    f = open('train.csv')
    xs = []
    ys = []
    for r in f:
        if r.startswith('date'): continue
        (x, y, y2) = read_in(r, False)
        xs.append(x)
        ys.append((y,y2))
    xs = np.array(xs)
    ys = np.array(ys)
    return (xs, ys)

def read_test():
    f = open('test.csv')
    xs = []
    dts = []
    for r in f:
        if r.startswith('date'): continue
        (x, dt) = read_in(r, True)
        xs.append(x)
        dts.append(dt)
    xs = np.array(xs)
    return (xs, dts)

from sklearn.cross_validation import cross_val_score, KFold
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import explained_variance_score, mean_squared_error, make_scorer
from sklearn.grid_search import GridSearchCV

def cross_val(reg, tr, cv = 10):
    print 'cross validation...'
    (X, Y) = tr
    scores = []
    kf = KFold(X.shape[0], cv)
    for train, test in kf:
        (tr_x, tt_x, tr_y, tt_y) = (X[train], X[test], Y[train], Y[test])
        reg.fit(tr_x, tr_y)
        y = reg.predict(tt_x)
        score = mean_squared_error(np.log(y + 1), np.log(tt_y[:,0] + tt_y[:,1] + 1)) ** 0.5
        print 'score = ', score
        scores.append(score)
    return np.array(scores)

def print_best_estimator(reg):
    print("Best parameters set found on development set:")
    print(reg.best_estimator_)
    print("Grid scores on development set:")
    for params, mean_score, scores in reg.grid_scores_:
        print("%0.3f (+/-%0.03f) for %r" % (mean_score, scores.std(), params))

class Reg:
    def __init__(self, r0, r1):
        self.r0 = r0
        self.r1 = r1
        self.select = (0,1,2,3,5,6,7,8,9,10)
    def fit(self, xs, ys):
        self.r0.fit(xs, ys[:,0])
        self.r1.fit(xs[:,self.select], np.log(ys[:,1] + 1))
    def predict(self, xs):
        ys0 = self.r0.predict(xs)
        ys1 = np.exp(self.r1.predict(xs[:,self.select])) - 1
        ys = np.intp(np.around(ys0 + ys1))
        ys[ys < 0] = 0
        return ys

class Average:
    def __init__(self, regs):
        self.regs = regs
    def fit(self, xs, ys):
        for r in self.regs:
            r.fit(xs, ys)
    # def predict(self, xs):
    #     ys0 = np.zeros(xs.shape[0])
    #     ys1 = np.zeros(xs.shape[0])
    #     for r in self.regs:
    #         r0 = r.r0
    #         r1 = r.r1
    #         ys0 += r0.predict(xs)
    #         ys1 += np.exp(r1.predict(xs)) - 1
    #     ys = np.intp(np.around((ys0 + ys1) * 1.0 / len(self.regs)))
    #     ys[ys < 0] = 0
    #     return ys

    def predict(self, xs):
        ys = np.zeros(xs.shape[0])
        for r in self.regs:
            ys += r.predict(xs)
        ys *= 1.0 / len(self.regs)
        ys = np.intp(np.around(ys))
        ys[ys < 0] = 0
        return ys

def select_rf(tr):
    (X, Y) = tr
    n = 1000
    print '----- RF -----'
    # if we tune parameters.
    tuning = 0

    if not tuning:
        reg0 = RandomForestRegressor(n_estimators = n, random_state = 0, min_samples_split = 5, oob_score = False, n_jobs = -1)
        reg1 = RandomForestRegressor(n_estimators = n, random_state = 0, min_samples_split = 5, oob_score = False, n_jobs = -1)
        reg = Reg(reg0, reg1)
        return reg

    min_samples_split = [2,3,4,5,6,7]
    info = {}
    for mss in min_samples_split:
        print 'min_samples_split = ', mss
        reg0 = RandomForestRegressor(n_estimators = n, random_state = 0, min_samples_split = mss, oob_score = False, n_jobs = -1)
        reg1 = RandomForestRegressor(n_estimators = n, random_state = 0, min_samples_split = mss, oob_score = False, n_jobs = -1)
        reg = Reg(reg0, reg1)
        scores = cross_val(reg, tr, 10)
        info[mss] = scores
    for mss in info:
        scores = info[mss]
        print('min_samples_split = %d, socre = %.5f(%.5f)' % (mss, scores.mean(), scores.std()))

# RF n = 1000 ms = 5 0.38550 (ms = 6, 0.38673)
# [ 0.54101887  0.4893499   0.28546896  0.33875963  0.40013234  0.41900714
#   0.38498317  0.27187354  0.29676393  0.38401737]
# 0.381137484692 0.0831239063825

# RF n = 2000 ms = 5 0.38554 (ms = 6, 0.38570)
# [ 0.54112786  0.48912899  0.28554728  0.33843558  0.40124313  0.42025452
#   0.38408297  0.27181023  0.29658713  0.38474727]
# 0.381296497687 0.0832328473713

# RF + GBDT n = 1000 ms = 5 md = 8 0.38921 (n = 2000, 0.39028) 对总和做平均
# [ 0.49909659  0.48631     0.28507903  0.33743276  0.38145931  0.38117835
#   0.38991038  0.28009474  0.29850571  0.34665952] # RMSLE
# 0.368572639285 0.072689498321 # 均值，方差
# 对各项平均然后求和 0.39047
# [ 0.50625495  0.48698589  0.28601487  0.33635841  0.38214079  0.38632692
#   0.3930925   0.27970706  0.29734006  0.34870254]
# 0.370292399797 0.0743428577902

def select_gbdt(tr):
    (X, Y) = tr
    n = 1000
    print '----- GBDT -----'
    # if we tune parameters
    tuning = 0

    if not tuning:
        reg0 = GradientBoostingRegressor(n_estimators = n, min_samples_split = 5, max_depth = 8, random_state = 0)
        reg1 = GradientBoostingRegressor(n_estimators = n, min_samples_split = 5, max_depth = 8, random_state = 0)
        reg = Reg(reg0, reg1)
        return reg

    max_depth = [5,6,7,8,9]
    info = {}
    for md in max_depth:
        print 'max_depth = ', md
        reg0 = GradientBoostingRegressor(n_estimators = n, min_samples_split = 5, max_depth = md, random_state = 0)
        reg1 = GradientBoostingRegressor(n_estimators = n, min_samples_split = 5, max_depth = md, random_state = 0)
        reg = Reg(reg0, reg1)
        scores = cross_val(reg, tr, 10)
        info[md] = scores
    for md in info:
        scores = info[md]
        print('max_depth = %d, socre = %.5f(%.5f)' % (md, scores.mean(), scores.std()))

def select():
    print('loading training set ...')
    tr = read_train()
    print('training ...')
    reg_rf = select_rf(tr)
    reg = reg_rf
    reg_gbdt = select_gbdt(tr)
    reg = reg_gbdt
    reg = Average([reg_rf, reg_gbdt])
    cv = 1
    if cv:
        scores = cross_val(reg, tr, 10)
        print scores
        print scores.mean(), scores.std()
    return (reg, tr)

def run(reg, tr):
    if not reg: return
    (xs, ys) = tr
    print('training ...')
    reg.fit(xs, ys)
    print('loading test set ...')
    (xs, dts) = read_test()
    print('testing ...')
    ys = reg.predict(xs)
    f = open('submission.csv','w')
    f.write('datetime,count\n')
    n = len(dts)
    for i in xrange(0, n):
        f.write('%s,%d\n' % (dts[i], ys[i]))
    f.close()

if __name__ == '__main__':
    (reg, tr) = select()
    run(reg, tr)
