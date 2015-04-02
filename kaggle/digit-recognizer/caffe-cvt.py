#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from common import *
import h5py

(data, labels) = read_train(-1)
with h5py.File('train.hdf5','w') as f:
    f['data'] = data.reshape((-1, 1, 28, 28)) * 1.0 / 256
    f['label'] = labels.reshape((-1, 1, 1, 1))
