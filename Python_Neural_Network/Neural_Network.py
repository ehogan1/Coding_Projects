import numpy as np
import pandas as pd

def data_initialization():
    test_data = pd.read_csv(r'C:\Users\Edmund Hogan\Coding_Projects\Python_Neural_Network\mnist_test.csv')
    test_data = (np.array(test_data)).T
    training_data = pd.read_csv(r'C:\Users\Edmund Hogan\Coding_Projects\Python_Neural_Network\mnist_train.csv')
    training_data = (np.array(training_data)).T
    y_train = training_data[0]
    x_train = training_data[1:]
    # Could Package this but would most likely just end up unpackagaing once I have returned it
    return test_data, training_data, y_train, x_train

def parameter_initialization():
    w1 = np.random.rand(10, 784) - 0.5
    b1 = np.random.rand(10, 1) - 0.5
    w2 = np.random.rand(10, 10) - 0.5
    b2 = np.random.rand(10, 1) - 0.5
    return w1, b1, w2, b2

def activation_function(z):
    """
    Sigmoid Function
    """
    return 1/(1 + np.exp(-z))

def deriv_activ_func(z):
    """
    Sigmoid Derivative Function
    """
    return activation_function(z) * (1 - activation_function(z))

def softmax(z):
    return np.exp(z) / sum(np.exp(z))

def forward_prop(w1, b1, w2, b2, input_layer):
    unactivated1 = w1.dot(input_layer) + b1
    hidden1 = activation_function(unactivated1)
    unactivated2 = w2.dot(hidden1) + b2
    output_layer = softmax(unactivated2)
    return unactivated1, hidden1, unactivated2, output_layer

def one_hot(y):
    one_hot_y = np.zeros((y.size, y.max() + 1))
    one_hot_y[np.arange(y.size), y] = 1
    one_hot_y = one_hot_y.T
    return one_hot_y

def back_prop(unactivated1, hidden1, unactivated2, output_layer, w2, x, y):
    one_hot_y = one_hot(y)
    m = y.size
    dz2 = output_layer - one_hot_y
    dw2 = 1 / m * dz2.dot(hidden1.T)
    db2 = 1 / m * np.sum(dz2)
    dz1 = w2.T.dot(dz2) * deriv_activ_func(unactivated1)
    dw1 = 1 / m * dz1.dot(x.T)
    db1 = 1 / m * np.sum(dz1)
    return dw1, db1, dw2, db2

def update_parameters(w1, b1, w2, b2, dw1, db1, dw2, db2, alpha):
    w1 = w1 - alpha * dw1
    b1 = b1 - alpha * db1
    w2 = w2 - alpha * dw2
    b2 = b2 - alpha * db2
    return w1, b1, w2, b2

def get_predictions(output_layer):
    return np.argmax(output_layer, 0)

def get_accuracy(predictions, y):
    print(predictions, y)
    return np.sum(predictions == y) / y.size

def gradient_decent(x, y, iterations, alpha):
    w1, b1, w2, b2 = parameter_initialization()
    for i in range(iterations):
        unactivated1, hidden1, unactiavted2, output_layer = forward_prop(w1, b1, w2, b2, x)
        dw1, db1, dw2, db2 = back_prop(unactivated1, hidden1, unactiavted2, output_layer, w2, x, y)
        w1, b1, w2, b2 = update_parameters(w1, b1, w2, b2, dw1, db1, dw2, db2, alpha)
        if (i % 50 == 0):
            print('Iteration: ', i)
            print('Accuracy: ', get_accuracy(get_predictions(output_layer), y)) 
    return w1, b1, w2, b2

test_data, training_data, y_train, x_train = data_initialization()
w1, b1, w2, b2 = gradient_decent(x_train, y_train, 1500, .5)