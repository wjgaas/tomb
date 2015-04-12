#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import pandas as pd
from sklearn.cross_validation import train_test_split
from nolearn.lasagne import NeuralNet, BatchIterator
from lasagne import layers
from lasagne.nonlinearities import softmax, rectify, tanh
from lasagne.updates import momentum, nesterov_momentum, sgd, rmsprop
import numpy as np
from matplotlib import pyplot
from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
import h5py

def plot_loss(net):
    """
    Plot the training loss and validation loss versus epoch iterations with respect to
    a trained neural network.
    """
    train_loss = np.array([i["train_loss"] for i in net.train_history_])
    valid_loss = np.array([i["valid_loss"] for i in net.train_history_])
    pyplot.plot(train_loss, linewidth = 3, label = "train")
    pyplot.plot(valid_loss, linewidth = 3, label = "valid")
    pyplot.grid()
    pyplot.legend()
    pyplot.xlabel("epoch")
    pyplot.ylabel("loss")
    #pyplot.ylim(1e-3, 1e-2)
    pyplot.yscale("log")
    pyplot.show()

def read_train():
    train_df = pd.read_csv('./train.csv')
    train_label = train_df.values[:, 0]
    train_data = train_df.values[:, 1:] * 1.0 / 256
    (X, y) = (train_data.astype(np.float32), train_label.astype(np.int32))
    (X, y) = shuffle(X, y, random_state = 42)
    return (X, y)

def read_train2():
    # see caffe-prepare.py
    f = h5py.File('train.hdf5')
    data = f['data'].value.astype(np.float32)
    labels = f['label'].value.astype(np.int32)
    (X, y) = shuffle(data, labels, random_state = 42)
    return (X, y)

def read_test():
    test_df = pd.read_csv('./test.csv')
    return test_df.values.astype(np.float32) * 1.0 / 256

CUDA_CONVNET = False
if CUDA_CONVNET:
    from lasagne.layers.cuda_convnet import Conv2DCCLayer, MaxPool2DCCLayer
    Conv2DLayer = Conv2DCCLayer
    MaxPool2DLayer = MaxPool2DCCLayer
else:
    Conv2DLayer = layers.Conv2DLayer
    MaxPool2DLayer = layers.MaxPool2DLayer

def create_ann():
    nn = NeuralNet(
    layers = [  # three layers: one hidden layer
        ('input', layers.InputLayer),
        ('h1', layers.DenseLayer),
        ('d1', layers.DropoutLayer),
        ('h2', layers.DenseLayer),
        ('d2', layers.DropoutLayer),
        ('output', layers.DenseLayer),
        ],
    # layer parameters:
    input_shape = (None, 784),  # 28x28 input pixels per batch
    h1_num_units = 400,  # number of units in hidden layer
    h1_nonlinearity = tanh,
    d1_p = 0.25,
    h2_num_units = 100,
    h2_nonlinearity = rectify,
    d2_p = 0.25,
    output_nonlinearity = softmax,  # output layer uses softmax function
    output_num_units = 10,  # 10 labels

    # optimization method:
    update = nesterov_momentum,
    update_learning_rate = 0.01,
    update_momentum = 0.9,

    eval_size = 0.1,
    max_epochs = 100,
    verbose = 1,
    )
    return nn

def create_cnn():
    nn = NeuralNet(
    layers = [  # three layers: one hidden layer
        ('input', layers.InputLayer),

        ('conv1', Conv2DLayer),
        ('pool1', MaxPool2DLayer),
        ('dropout1', layers.DropoutLayer),

        ('conv2', Conv2DLayer),
        ('pool2', MaxPool2DLayer),
        ('dropout2', layers.DropoutLayer),

        # ('conv3', Conv2DLayer),
        # ('pool3', MaxPool2DLayer),
        # ('dropout3', layers.DropoutLayer),

        ('hidden4', layers.DenseLayer),
        ('dropout4', layers.DropoutLayer),

        ('output', layers.DenseLayer),
        ],
    # layer parameters:
    input_shape = (None, 1, 28, 28),  # 28x28 input pixels per batch

    conv1_num_filters = 32, conv1_filter_size = (3, 3), pool1_ds = (2, 2), dropout1_p = 0.5,
    conv2_num_filters = 64, conv2_filter_size=(2, 2), pool2_ds=(2, 2), dropout2_p = 0.5,
    # conv3_num_filters = 128, conv3_filter_size = (2, 2), pool3_ds = (2, 2), dropout3_p = 0.5,

    hidden4_num_units = 500, dropout4_p = 0.5,

    output_num_units = 10,  # 10 labels

    conv1_nonlinearity = rectify, conv2_nonlinearity = rectify, conv3_nonlinearity = rectify,
    hidden4_nonlinearity = rectify,
    # hidden4_nonlinearity = tanh,
    output_nonlinearity = softmax,  # output layer uses softmax function

    # optimization method:
    update = nesterov_momentum,
    update_learning_rate = 0.01,
    update_momentum = 0.9,

    eval_size = 0.1,

    max_epochs = 200,  # we want to train this many epochs
    verbose = 1,
    )
    return nn

def write_test(pred):
    output = pd.DataFrame(data = {"ImageId": range(1, 28001), "Label": pred})
    output.to_csv("./cnn.csv", index = False, quoting = 3)
