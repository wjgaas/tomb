#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import os
import sys
sys.path.append(os.path.join(os.environ['HOME'], 'repo/caffe/python'))
import caffe

caffe.set_mode_cpu()
net = caffe.Net('caffe-conf/test.prototxt',
                'uv_iter_2000.caffemodel',
                caffe.TEST)

from common import *
data = read_test(10)
start_timer()
data = data.reshape((-1, 1, 28, 28))
out = net.forward_all(**{'data': data})
blobs = net._blobs
for name in net._layer_names: print name

import pylab as plt
import matplotlib.cm as cm

def simple_plot(data, r0, c0):
    fig, axs = plt.subplots(r0, c0)
    for r in range(0, r0):
        for c in range(0, c0):
            ax = axs[r][c]
            ax.axes.get_xaxis().set_visible(False)
            ax.axes.get_yaxis().set_visible(False)
            im = data[r * c0 + c]
            ax.imshow(im, cmap = cm.Greys_r)
    plt.show()

data = blobs[1].data[2] # conv1, 3th instance.
simple_plot(data, 4, 8)

data = blobs[3].data[2] # conv2, 3th instance.
simple_plot(data, 8, 8)
