#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import sys
import os
sys.path.append(os.path.join(os.environ['HOME'], 'repo/caffe/python'))
import caffe
import numpy as np
from sklearn.cross_validation import train_test_split
from common import *

# no = 42000.
(data, labels) = read_train(-1)
data = data.reshape((-1, 1, 28, 28)) * 0.00390625
labels = labels.reshape((-1, 1, 1, 1))

# train size = 42000 * 0.96
# test size = 42000 * 0.04
# test size / 420(batch size) = 4, that's why test_iter in solver.prototxt is 4.
(tr_x, tt_x, tr_y, tt_y) = train_test_split(data, labels, test_size = 0.04, random_state = 0)
solver = caffe.get_solver('caffe-conf/solver.prototxt')
# solver.restore('uv_iter_5000.solverstate')
solver.net.set_input_arrays(tr_x, tr_y)
solver.test_nets[0].set_input_arrays(tt_x, tt_y)
solver.solve()
