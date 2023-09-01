import numpy as np
import pandas as pd
from matplotlib import pyplot as plt

def data_initialization():
    test_data = pd.read_csv(r'C:\Users\Edmund Hogan\Coding_Projects\Python_Neural_Network\mnist_test.csv')
    test_data = (np.array(test_data)).T
    training_data = pd.read_csv(r'C:\Users\Edmund Hogan\Coding_Projects\Python_Neural_Network\mnist_train.csv')
    training_data = (np.array(training_data)).T
    rows, pixels = training_data.shape()
    y_train = training_data[0]
    x_train = training_data[1:]
    # Could Package this but would most likely just end up unpackagaing once I have returned it
    return test_data, training_data, rows, pixels, y_train, x_train

def parameter_initialization():
    w1 = np.random.randn(10, 784)
    b1 = np.random.randn(10, 1)
    w2 = np.random.randn(10, 150)
    b2 = np.random.randn(10, 1)
    w3 = np.random.randn(10, 10)
    b3 = np.random.randn(10, 1)
    return w1, b1, w2, b2

def activation_function(z):
    """
    Sigmoid Function
    """
    return 1/(1 + np.exp(-x))

def softmax(z):
    return exp(Z) / np.sum(exp(2))

def forward_prop(w1, b1, w2, b2, input_layer):
    unactivated1 = w1.dot(input_layer) + b1
    hidden1 = activation_function(unactivated1)
    unactivated2 = w2.dot(hidden1) + b2
    hidden2 = activation_function(unactivated2)
    unactivated3 = w3.dot(hidden2) + b3
    output_layer = softmax(unactivated3)
    return unactivated1, hidden1, unactivated2, hidden2, unactivated3, hidden3