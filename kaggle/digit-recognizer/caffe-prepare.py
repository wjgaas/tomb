#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

from common import *
import h5py
from skimage.transform import rotate

if True:
    start_timer()
    (data, labels) = read_train(-1)
    print_timer("read train")
    f = h5py.File('train.hdf5','w')
    max_n = 42000 * 9
    ds = f.create_dataset('data', (max_n, 1, 28, 28), compression = 'lzf', dtype = np.float32)
    ll = f.create_dataset('label', (max_n, 1, 1, 1), compression = 'lzf', dtype = np.float32)

    labels = labels.reshape((-1, 1, 1, 1))
    
    # augment data by rotating.
    start_timer()    
    idx = 0
    ds[idx:idx + data.shape[0]] = data.reshape((-1, 1, 28, 28))
    ll[idx:idx + data.shape[0]] = labels
    idx += data.shape[0]
    print_timer("store original")

    data = data.reshape((-1, 28, 28))
    for angle in (-20, -16, -8, -4, 4,  8, 16, 20):
        start_timer()
        d = np.array(map(lambda x: rotate(x, angle), data)).astype(np.float32).reshape((-1, 1, 28, 28))
        print_timer("rotate %d" % (angle))
        ds[idx:idx + d.shape[0]] = d
        ll[idx:idx + d.shape[0]] = labels
        print_timer("store rotate %d" % (angle))
        assert(d.shape[0] == data.shape[0])
        idx += d.shape[0]
    f.close()
