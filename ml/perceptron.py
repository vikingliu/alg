#coding=utf-8
import numpy as np

def original_perceptron_train(data, l=1):
    '''
    data = [x,y]
    '''
    n, m = data.shape
    x = data[:,0:m-1]
    y = data[:, -1]
    w = np.zeros(m - 1)
    b = 0
    while True:
        i = find_error_dot(x, y, w, b)
        if i < 0:
            break
        print 'x%s w=%s, b=%s' % (i + 1, w, b)
        w = w + l * y[i]*x[i]
        b = b + l * y[i]
    return w, b

def find_error_dot(x, y, w, b):
    for i in range(len(x)):
        if (y[i] * (np.dot(w, x[i]) + b) <= 0):
            return i
    return -1

def dual_perceptron_train(data, l=1):
    n, m = data.shape
    x = data[:,0:m-1]
    y = data[:, -1]
    a = np.zeros(n)
    b = 0
    G = np.dot(x, x.T)

    while True:
        i = dual_find_error_dot(G, y, a, b)
        if i < 0:
            break
        print 'x%s a=%s, b=%s' % (i + 1, a, b)
        a[i] = a[i] + l
        b = b + l * y[i]

    w = np.zeros(m - 1)
    for i in range(len(y)):
        w += a[i] * y[i] * x[i]
    return w, b

def dual_find_error_dot(G, y, a, b):
    for i in range(len(y)):
        sum = 0
        for j in range(len(y)):
            sum += a[j] * y[j] * G[j,i]
        if y[i] * (sum + b) <= 0:
            return i

if __name__ == '__main__':
    data = [[3,3,1], [4,3,1], [1,1,-1]]
    data = np.array(data)
    #print original_perceptron_train(data)
    print dual_perceptron_train(data)
