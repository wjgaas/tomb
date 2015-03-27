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

print 'read data'
train_df = pd.read_csv('./train.csv')
test_df = pd.read_csv('./test.csv')

train_label = train_df.values[:, 0]
train_data = train_df.values[:, 1:]
print "train:", train_data.shape, train_label.shape

test_data = test_df.values
print "test:", test_data.shape

train_data = train_data.astype(np.float)
train_label = train_label.astype(np.int32)
train_data, train_label = shuffle(train_data, train_label, random_state = 21)


train_data = train_data.reshape(-1, 1, 28, 28)
test_data = test_data.reshape(-1, 1, 28, 28)

CUDA_CONVNET = False
if CUDA_CONVNET:
    from lasagne.layers.cuda_convnet import Conv2DCCLayer, MaxPool2DCCLayer
    Conv2DLayer = Conv2DCCLayer
    MaxPool2DLayer = MaxPool2DCCLayer
else:
    Conv2DLayer = layers.Conv2DLayer
    MaxPool2DLayer = layers.MaxPool2DLayer

cnn = NeuralNet(
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
    #update = adagrad,
    update = rmsprop,
    update_learning_rate = 0.0001,
    #update_learning_rate = 0.01,

    eval_size = 0.1,

    max_epochs = 200,  # we want to train this many epochs
    verbose = 1,
    )

cnn.fit(train_data, train_label)
plot_loss(cnn)

pred = cnn.predict(test_data)

output = pd.DataFrame(data = {"ImageId": range(1, 28001), "Label": pred})
output.to_csv("./fc_2hidden_predict.csv", index = False, quoting = 3)

STATS = """
  DenseLayer            (None, 10)              produces      10 outputs
  DropoutLayer          (None, 500)             produces     500 outputs
  DenseLayer            (None, 500)             produces     500 outputs
  DropoutLayer          (None, 64, 6, 6)        produces    2304 outputs
  MaxPool2DLayer        (None, 64, 6, 6)        produces    2304 outputs
  Conv2DLayer           (None, 64, 12, 12)      produces    9216 outputs
  DropoutLayer          (None, 32, 13, 13)      produces    5408 outputs
  MaxPool2DLayer        (None, 32, 13, 13)      produces    5408 outputs
  Conv2DLayer           (None, 32, 26, 26)      produces   21632 outputs
  InputLayer            (None, 1, 28, 28)       produces     784 outputs

 Epoch  |  Train loss  |  Valid loss  |  Train / Val  |  Valid acc  |  Dur
--------|--------------|--------------|---------------|-------------|-------
     1  |   14.416470  |    1.666978  |     8.648266  |     62.20%  |  287.7s
     2  |    1.802640  |    1.132366  |     1.591923  |     78.01%  |  297.7s
     3  |    1.255777  |    0.692776  |     1.812674  |     86.62%  |  287.6s
     4  |    0.964767  |    0.477968  |     2.018474  |     90.04%  |  286.9s
     5  |    0.758623  |    0.363507  |     2.086954  |     91.97%  |  291.2s
     6  |    0.611553  |    0.283635  |     2.156128  |     93.48%  |  290.6s
     7  |    0.521000  |    0.234883  |     2.218119  |     94.37%  |  288.5s
     8  |    0.440474  |    0.194418  |     2.265605  |     95.21%  |  285.1s
     9  |    0.387755  |    0.177030  |     2.190336  |     95.57%  |  283.5s
    10  |    0.350900  |    0.158439  |     2.214730  |     96.18%  |  281.8s
    11  |    0.313523  |    0.139903  |     2.241000  |     96.45%  |  293.7s
    12  |    0.284224  |    0.129096  |     2.201651  |     96.80%  |  298.9s
    13  |    0.262049  |    0.116024  |     2.258568  |     97.04%  |  293.2s
    14  |    0.241110  |    0.107925  |     2.234048  |     97.06%  |  288.8s
    15  |    0.223143  |    0.102133  |     2.184824  |     97.37%  |  286.8s
    16  |    0.210686  |    0.092122  |     2.287030  |     97.68%  |  287.4s
    17  |    0.203142  |    0.092073  |     2.206309  |     97.44%  |  287.0s
    18  |    0.192345  |    0.085359  |     2.253378  |     97.75%  |  287.7s
    19  |    0.176012  |    0.079875  |     2.203583  |     97.87%  |  287.4s
    20  |    0.174205  |    0.077618  |     2.244383  |     97.84%  |  286.6s
    21  |    0.167510  |    0.073895  |     2.266863  |     98.03%  |  283.9s
    22  |    0.159487  |    0.069773  |     2.285798  |     98.01%  |  284.1s
    23  |    0.158129  |    0.069067  |     2.289505  |     98.15%  |  284.2s
    24  |    0.146698  |    0.064718  |     2.266730  |     98.20%  |  283.1s
    25  |    0.141212  |    0.062704  |     2.252029  |     98.22%  |  284.5s
    26  |    0.144435  |    0.061956  |     2.331259  |     98.32%  |  287.7s
    27  |    0.132885  |    0.058747  |     2.261976  |     98.51%  |  291.9s
    28  |    0.131090  |    0.057594  |     2.276100  |     98.37%  |  291.5s
    29  |    0.125631  |    0.055523  |     2.262673  |     98.48%  |  291.1s
    30  |    0.126093  |    0.054051  |     2.332865  |     98.46%  |  291.8s
    31  |    0.115732  |    0.051219  |     2.259551  |     98.53%  |  291.8s
    32  |    0.121142  |    0.053559  |     2.261847  |     98.46%  |  289.9s
    33  |    0.113494  |    0.052109  |     2.178013  |     98.46%  |  290.2s
    34  |    0.110854  |    0.050048  |     2.214927  |     98.72%  |  290.1s
    35  |    0.110299  |    0.049365  |     2.234363  |     98.60%  |  290.9s
    36  |    0.102664  |    0.048228  |     2.128697  |     98.63%  |  290.1s
    37  |    0.103729  |    0.047463  |     2.185475  |     98.72%  |  290.4s
    38  |    0.106937  |    0.046837  |     2.283164  |     98.70%  |  289.7s
    39  |    0.103809  |    0.045627  |     2.275184  |     98.77%  |  290.5s
    40  |    0.099379  |    0.044838  |     2.216389  |     98.77%  |  290.5s
    41  |    0.096352  |    0.044725  |     2.154327  |     98.72%  |  289.9s
    42  |    0.097233  |    0.043342  |     2.243387  |     98.75%  |  291.6s
    43  |    0.094956  |    0.043072  |     2.204585  |     98.70%  |  291.9s
    44  |    0.096651  |    0.042846  |     2.255754  |     98.77%  |  291.8s
    45  |    0.091428  |    0.042101  |     2.171637  |     98.89%  |  290.1s
    46  |    0.090178  |    0.042237  |     2.135026  |     98.72%  |  290.1s
    47  |    0.087478  |    0.040886  |     2.139552  |     98.86%  |  292.3s
    48  |    0.086173  |    0.039959  |     2.156554  |     98.89%  |  292.1s
    49  |    0.088399  |    0.041067  |     2.152524  |     98.84%  |  291.7s
    50  |    0.084482  |    0.039052  |     2.163339  |     98.89%  |  291.9s
    51  |    0.083990  |    0.038955  |     2.156072  |     98.89%  |  292.1s
    52  |    0.081185  |    0.038036  |     2.134393  |     98.91%  |  292.2s
    53  |    0.081602  |    0.038933  |     2.095943  |     98.91%  |  291.6s
    54  |    0.080312  |    0.036918  |     2.175414  |     98.89%  |  291.8s
    55  |    0.081115  |    0.037688  |     2.152259  |     98.93%  |  291.9s
    56  |    0.079434  |    0.036597  |     2.170524  |     99.03%  |  291.5s
    57  |    0.077640  |    0.036795  |     2.110078  |     99.03%  |  292.2s
    58  |    0.075087  |    0.038234  |     1.963878  |     98.96%  |  292.6s
    59  |    0.074584  |    0.036076  |     2.067392  |     98.91%  |  292.0s
    60  |    0.075520  |    0.037152  |     2.032718  |     98.89%  |  292.2s
    61  |    0.075690  |    0.036419  |     2.078329  |     99.01%  |  292.3s
    62  |    0.072492  |    0.035568  |     2.038123  |     98.98%  |  292.2s
    63  |    0.072299  |    0.034742  |     2.081017  |     98.96%  |  292.3s
    64  |    0.073198  |    0.035847  |     2.041932  |     98.98%  |  292.2s
    65  |    0.069272  |    0.034728  |     1.994694  |     99.03%  |  290.7s
    66  |    0.072396  |    0.035853  |     2.019221  |     98.96%  |  289.8s
    67  |    0.067927  |    0.034439  |     1.972395  |     98.98%  |  290.2s
    68  |    0.066257  |    0.034245  |     1.934761  |     98.96%  |  290.6s
    69  |    0.066819  |    0.034246  |     1.951163  |     98.98%  |  291.8s
    70  |    0.066128  |    0.033491  |     1.974488  |     99.01%  |  292.0s
    71  |    0.064783  |    0.034193  |     1.894615  |     98.98%  |  292.1s
    72  |    0.064451  |    0.034638  |     1.860694  |     98.93%  |  291.7s
    73  |    0.064081  |    0.033837  |     1.893801  |     99.08%  |  290.7s
    74  |    0.062924  |    0.033623  |     1.871468  |     99.01%  |  289.7s
    75  |    0.061323  |    0.032831  |     1.867818  |     99.05%  |  289.9s
    76  |    0.062112  |    0.031973  |     1.942615  |     99.08%  |  289.5s
    77  |    0.062464  |    0.033231  |     1.879688  |     98.96%  |  289.8s
    78  |    0.062559  |    0.032591  |     1.919521  |     98.96%  |  290.6s
    79  |    0.060402  |    0.032825  |     1.840114  |     99.01%  |  291.9s
    80  |    0.059497  |    0.034030  |     1.748353  |     98.96%  |  292.0s
    81  |    0.061148  |    0.033033  |     1.851100  |     98.91%  |  292.1s
    82  |    0.058462  |    0.031610  |     1.849444  |     98.98%  |  291.3s
    83  |    0.056136  |    0.031403  |     1.787637  |     99.12%  |  290.0s
    84  |    0.057371  |    0.031889  |     1.799103  |     99.03%  |  290.3s
    85  |    0.057550  |    0.031905  |     1.803822  |     98.98%  |  290.4s
    86  |    0.058050  |    0.031413  |     1.847956  |     99.08%  |  290.9s
    87  |    0.059540  |    0.031625  |     1.882722  |     99.08%  |  291.7s
    88  |    0.055702  |    0.030957  |     1.799364  |     99.20%  |  292.0s
"""
