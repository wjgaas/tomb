#!/usr/bin/env python
#coding:utf-8
#Copyright (C) dirlt

import pandas as pd
from sklearn.cross_validation import train_test_split
from nolearn.lasagne import NeuralNet, BatchIterator
from lasagne import layers
from lasagne.nonlinearities import softmax
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


#train_data, valid_data, train_label, valid_label = train_test_split(train_data, train_label, test_size = 0.2, random_state = 21)

fc_1hidden = NeuralNet(
    layers = [  # three layers: one hidden layer
        ('input', layers.InputLayer),
        ('hidden', layers.DenseLayer),
        ('dropout', layers.DropoutLayer),
        ('output', layers.DenseLayer),
        ],
    # layer parameters:
    input_shape = (None, 784),  # 28x28 input pixels per batch
    hidden_num_units = 100,  # number of units in hidden layer
    dropout_p = 0.25, # dropout probability
    output_nonlinearity = softmax,  # output layer uses softmax function
    output_num_units = 10,  # 10 labels

    # optimization method:
    #update = nesterov_momentum,
    update = sgd,
    update_learning_rate = 0.001,
    #update_momentum = 0.9,

    eval_size = 0.1,

    # batch_iterator_train = BatchIterator(batch_size = 20),
    # batch_iterator_test = BatchIterator(batch_size = 20),

    max_epochs = 100,  # we want to train this many epochs
    verbose = 1,
    )

fc_1hidden.fit(train_data, train_label)
plot_loss(fc_1hidden)

pred = fc_1hidden.predict(test_data)
output = pd.DataFrame(data = {'ImageId': range(1, 28001), "Label": pred})
# LB score = 0.93314
output.to_csv('./fc_1hidden_predict.csv', index = False)

STATS = """
  DenseLayer            (None, 10)              produces      10 outputs
  DropoutLayer          (None, 100)             produces     100 outputs
  DenseLayer            (None, 100)             produces     100 outputs
  InputLayer            (None, 784)             produces     784 outputs

 Epoch  |  Train loss  |  Valid loss  |  Train / Val  |  Valid acc  |  Dur
--------|--------------|--------------|---------------|-------------|-------
     1  |    5.138614  |    1.349365  |     3.808173  |     64.88%  |  1.8s
     2  |    1.381726  |    1.086093  |     1.272198  |     73.61%  |  1.8s
     3  |    1.174405  |    0.967675  |     1.213636  |     77.65%  |  1.9s
     4  |    1.049514  |    0.881361  |     1.190788  |     79.88%  |  1.8s
     5  |    0.970446  |    0.792536  |     1.224483  |     81.31%  |  1.8s
     6  |    0.882359  |    0.724309  |     1.218208  |     82.48%  |  1.8s
     7  |    0.817977  |    0.677200  |     1.207880  |     83.01%  |  1.8s
     8  |    0.762020  |    0.630181  |     1.209208  |     84.37%  |  1.8s
     9  |    0.721199  |    0.604975  |     1.192114  |     84.70%  |  1.8s
    10  |    0.691728  |    0.581347  |     1.189872  |     85.22%  |  1.8s
    11  |    0.654013  |    0.562929  |     1.161804  |     86.32%  |  1.8s
    12  |    0.634585  |    0.560292  |     1.132597  |     86.34%  |  1.8s
    13  |    0.609580  |    0.530465  |     1.149143  |     88.31%  |  1.8s
    14  |    0.597475  |    0.525589  |     1.136771  |     88.66%  |  1.9s
    15  |    0.579766  |    0.506285  |     1.145139  |     88.95%  |  1.8s
    16  |    0.566739  |    0.501745  |     1.129537  |     88.17%  |  1.8s
    17  |    0.553238  |    0.487394  |     1.135093  |     89.50%  |  1.9s
    18  |    0.544719  |    0.477523  |     1.140718  |     89.50%  |  1.9s
    19  |    0.526860  |    0.480100  |     1.097397  |     90.05%  |  1.8s
    20  |    0.509766  |    0.467831  |     1.089636  |     89.91%  |  1.8s
    21  |    0.502412  |    0.457630  |     1.097855  |     90.35%  |  1.8s
    22  |    0.496067  |    0.451124  |     1.099623  |     90.31%  |  1.9s
    23  |    0.483748  |    0.450609  |     1.073543  |     90.54%  |  1.8s
    24  |    0.471942  |    0.443484  |     1.064169  |     90.52%  |  1.8s
    25  |    0.466477  |    0.437877  |     1.065315  |     90.42%  |  1.8s
    26  |    0.457745  |    0.443899  |     1.031191  |     90.85%  |  1.8s
    27  |    0.453557  |    0.439215  |     1.032654  |     90.80%  |  1.9s
    28  |    0.441931  |    0.437528  |     1.010064  |     90.95%  |  1.8s
    29  |    0.432837  |    0.423731  |     1.021490  |     91.35%  |  1.8s
    30  |    0.426860  |    0.423571  |     1.007764  |     91.37%  |  1.9s
    31  |    0.426353  |    0.419268  |     1.016896  |     91.34%  |  1.9s
    32  |    0.418201  |    0.422113  |     0.990730  |     91.42%  |  1.8s
    33  |    0.417873  |    0.411208  |     1.016208  |     91.68%  |  1.8s
    34  |    0.404239  |    0.416240  |     0.971170  |     91.44%  |  1.8s
    35  |    0.396009  |    0.413110  |     0.958605  |     91.61%  |  1.9s
    36  |    0.398703  |    0.412656  |     0.966187  |     91.65%  |  1.9s
    37  |    0.392182  |    0.410873  |     0.954508  |     91.74%  |  1.8s
    38  |    0.392474  |    0.398031  |     0.986038  |     92.03%  |  1.8s
    39  |    0.379077  |    0.406352  |     0.932878  |     91.82%  |  1.8s
    40  |    0.379507  |    0.403871  |     0.939676  |     91.98%  |  1.8s
    41  |    0.375868  |    0.399934  |     0.939826  |     91.86%  |  1.8s
    42  |    0.373658  |    0.396857  |     0.941543  |     91.86%  |  1.8s
    43  |    0.372461  |    0.408016  |     0.912860  |     91.94%  |  1.8s
    44  |    0.372687  |    0.408089  |     0.913251  |     91.77%  |  1.8s
    45  |    0.357152  |    0.401343  |     0.889890  |     91.77%  |  1.8s
    46  |    0.359734  |    0.397292  |     0.905466  |     92.11%  |  1.8s
    47  |    0.356419  |    0.390482  |     0.912766  |     92.27%  |  1.8s
    48  |    0.349704  |    0.384013  |     0.910657  |     92.36%  |  1.8s
    49  |    0.352005  |    0.387553  |     0.908276  |     92.46%  |  1.8s
    50  |    0.343493  |    0.392054  |     0.876138  |     92.25%  |  1.8s
    51  |    0.342784  |    0.389796  |     0.879394  |     92.17%  |  1.8s
    52  |    0.340761  |    0.388637  |     0.876812  |     92.34%  |  1.8s
    53  |    0.335264  |    0.379837  |     0.882651  |     92.57%  |  1.8s
    54  |    0.333189  |    0.381870  |     0.872520  |     92.19%  |  1.8s
    55  |    0.332337  |    0.386562  |     0.859725  |     92.12%  |  1.8s
    56  |    0.325761  |    0.390068  |     0.835140  |     92.24%  |  1.8s
    57  |    0.324918  |    0.388791  |     0.835714  |     92.46%  |  1.8s
    58  |    0.322188  |    0.381789  |     0.843890  |     92.38%  |  1.8s
    59  |    0.321890  |    0.378994  |     0.849327  |     92.60%  |  1.8s
    60  |    0.319708  |    0.380760  |     0.839657  |     92.48%  |  1.8s
    61  |    0.312900  |    0.387853  |     0.806749  |     92.42%  |  1.8s
    62  |    0.312779  |    0.379676  |     0.823805  |     92.70%  |  1.8s
    63  |    0.305468  |    0.377193  |     0.809843  |     92.65%  |  1.8s
    64  |    0.305270  |    0.387330  |     0.788138  |     92.70%  |  1.8s
    65  |    0.305775  |    0.381999  |     0.800461  |     92.74%  |  1.8s
    66  |    0.306230  |    0.375630  |     0.815244  |     92.65%  |  1.8s
    67  |    0.299941  |    0.381265  |     0.786699  |     93.01%  |  1.8s
    68  |    0.301109  |    0.385017  |     0.782066  |     92.82%  |  1.8s
    69  |    0.297304  |    0.378341  |     0.785809  |     92.96%  |  1.8s
    70  |    0.292032  |    0.375714  |     0.777273  |     92.75%  |  1.8s
    71  |    0.284810  |    0.373701  |     0.762133  |     93.11%  |  1.8s
    72  |    0.286912  |    0.375600  |     0.763878  |     93.15%  |  1.8s
    73  |    0.279730  |    0.374808  |     0.746328  |     92.98%  |  1.9s
    74  |    0.282244  |    0.370911  |     0.760949  |     93.13%  |  1.8s
    75  |    0.287752  |    0.372999  |     0.771454  |     92.82%  |  1.8s
    76  |    0.285880  |    0.373128  |     0.766172  |     92.84%  |  1.8s
    77  |    0.273829  |    0.366970  |     0.746191  |     93.10%  |  1.9s
    78  |    0.282160  |    0.368835  |     0.765004  |     92.83%  |  1.8s
    79  |    0.274136  |    0.362118  |     0.757034  |     92.98%  |  1.8s
    80  |    0.269810  |    0.363612  |     0.742027  |     93.03%  |  1.8s
    81  |    0.274290  |    0.366623  |     0.748153  |     93.27%  |  1.8s
    82  |    0.268247  |    0.359812  |     0.745521  |     93.22%  |  1.8s
    83  |    0.268180  |    0.362015  |     0.740796  |     92.91%  |  1.9s
    84  |    0.266617  |    0.359707  |     0.741205  |     93.11%  |  1.8s
    85  |    0.270260  |    0.363031  |     0.744455  |     93.15%  |  1.8s
    86  |    0.263069  |    0.365769  |     0.719220  |     93.24%  |  1.8s
    87  |    0.258731  |    0.368136  |     0.702814  |     92.91%  |  1.9s
    88  |    0.259111  |    0.355898  |     0.728049  |     93.53%  |  1.8s
    89  |    0.263481  |    0.358250  |     0.735467  |     93.15%  |  1.8s
    90  |    0.261059  |    0.363092  |     0.718990  |     93.12%  |  1.8s
    91  |    0.257732  |    0.370690  |     0.695276  |     93.15%  |  1.9s
    92  |    0.257370  |    0.371288  |     0.693182  |     92.98%  |  1.8s
    93  |    0.253283  |    0.363292  |     0.697189  |     93.24%  |  1.8s
    94  |    0.256367  |    0.356234  |     0.719660  |     93.24%  |  1.8s
    95  |    0.254607  |    0.367652  |     0.692520  |     93.18%  |  1.8s
    96  |    0.253532  |    0.358700  |     0.706807  |     93.08%  |  1.8s
    97  |    0.250925  |    0.363233  |     0.690810  |     93.33%  |  1.8s
    98  |    0.248032  |    0.360176  |     0.688640  |     93.53%  |  1.8s
    99  |    0.249762  |    0.362043  |     0.689869  |     93.27%  |  1.9s
   100  |    0.249313  |    0.363034  |     0.686748  |     93.24%  |  1.8s
"""
