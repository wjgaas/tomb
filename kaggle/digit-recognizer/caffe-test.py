#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import os
import sys
sys.path.append(os.path.join(os.environ['HOME'], 'repo/caffe/python'))
import caffe

caffe.set_mode_cpu()
clf = caffe.Classifier('caffe-conf/test.prototxt',
                       'uv_iter_5000.caffemodel')

from common import *
data = read_test(-1)
# classifier要求数据数据是H * W * K
data = data.reshape((-1, 28, 28, 1)) * 1.0 / 256
rs = clf.predict(data)
ys = map(lambda x: find_max_idx(x), rs)
write_result(ys, 'caffe.csv')
