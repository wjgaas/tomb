#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import sys
import os
sys.path.append(os.path.join(os.environ['HOME'], 'repo/caffe/python'))
import caffe
import numpy as np
from sklearn.utils import shuffle
from sklearn.cross_validation import train_test_split
from common import *
import h5py

f = h5py.File('train.hdf5')
data = f['data']
labels = f['label']

solver = caffe.get_solver('caffe-conf/solver.prototxt')
# solver.restore('uv_iter_5000.solverstate')

start_timer()
tr_x, tt_x, tr_y, tt_y = train_test_split(data, labels, test_size = 0.1, random_state = 40)
print_timer('split')

start_timer()
solver.net.set_input_arrays(tr_x, tr_y)
solver.test_nets[0].set_input_arrays(tt_x, tt_y)
solver.solve()
print_timer("solve")
