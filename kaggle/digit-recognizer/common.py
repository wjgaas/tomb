#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

# http://www.kaggle.com/c/digit-recognizer

import numpy as np
import time

def read_in(s, test = False):
    s = s.strip()
    ss = map(lambda x: int(x), s.split(','))
    if not test: return (ss[1:], ss[0])
    else: return ss

def read_train(n):
    f = open('train.csv')
    xs = []
    ys = []
    for s in f:
        if s.startswith('label'): continue
        n -= 1
        if not n: break        
        (x, y) = read_in(s)
        xs.append(np.array(x))
        ys.append(y)
    return (np.array(xs), np.array(ys))

def read_test(n):
    f = open('test.csv')
    xs = []
    for s in f:        
        if s.startswith('pixel'): continue
        n -= 1
        if not n: break
        x = read_in(s, True)
        xs.append(np.array(x))
    return np.array(xs)

def write_result(ys, fname):
    f = open(fname, 'w')
    f.write('ImageId,Label\n')
    for i in xrange(0, len(ys)):
        y = ys[i]
        f.write('%d,%d\n' % (i+1, y))
    f.close()

_ts = 0
def start_timer():
    global _ts
    _ts = time.time()
def print_timer(msg):
    global _ts
    _now = time.time()
    print('%s: %.2f seconds' % (msg, _now - _ts))
    _ts = _now
