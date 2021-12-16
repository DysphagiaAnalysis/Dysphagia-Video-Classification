import numpy as np
import os
import pandas as pd
from sklearn import preprocessing
import random

from sklearn.preprocessing import OneHotEncoder as onehot

def claculate_arma_param(data, order,dimension):

    # start calculating variance
    # order_selection = 10
    # length = data.shape[0]
    # t = length//2
    # data_part_order = data[t-order_selection:t, :]
    # mean = np.mean(data_part_order, axis=1).reshape(order_selection,1)
    # std = np.std(data_part_order, axis=1).reshape(order_selection,1)
    # data_part_order_normalize = preprocessing.normalize(data_part_order)
    # cov = np.cov(data_part_order_normalize)
    # end

    data_part = data[:, dimension:(dimension+1)] # choose x or y
    Y_observe = data_part[order:]
    PHI = np.zeros((Y_observe.shape[0], order))
    for i in range(Y_observe.shape[0]):
        PHI_row = data_part[(i):(i+order), :]
        arr = PHI_row[::-1].transpose()
        PHI[i,:] = arr
    inv = np.linalg.pinv(np.dot(PHI.transpose(), PHI))
    theta = np.matmul(inv, PHI.transpose())
    theta = np.matmul(theta, Y_observe)
    return theta


import classifier 
if __name__ == "__main__":

    root =  os.path.join(os.getcwd(), 'data/');
    DATA = []
    NUM = []
    for j in os.listdir(root):
        if j == '.DS_Store':
            continue
        sub_sub = root +j + '/'
        num = 0
        for k in os.listdir(sub_sub):
            if k == '.DS_Store':
                continue
            num = num + 1
            sub_sub_sub = sub_sub + k 
            data = pd.read_csv(sub_sub_sub, header=0)
            data1 = np.array(data)[:, 1:]
            DATA.append(data1)
        NUM.append(num)

    length = len(DATA)
    order = 3
    PARAM = np.zeros((length, 2*order))
    j = 0
    for i in range (length):
        current_data = DATA[i]
        length_1 = current_data.shape[0]
        theta_x = claculate_arma_param(current_data, order, 0)
        theta_y = claculate_arma_param(current_data, order, 1)
        theta = np.concatenate((theta_x, theta_y), axis=0).transpose()
        PARAM[j:j+1,:] = theta
        j = j + 1

    # TODO: split data based on subject instead of clip
    # shuffle 
    index = [i for i in range(length)]
    random.shuffle(index)

    y = np.concatenate((np.zeros((NUM[0], 1)), np.ones((NUM[1], 1)), np.zeros((NUM[2], 1))), axis=0)
    y = np.array(y).astype('int32')
    
    x = PARAM[index, :]
    y = y[index, :]
    y = np.squeeze(y)

    result = classifier.gmm_cluster(x, y, length)
    print('gmm')
    print(result)

    acc = classifier.svm(x, y, length)
    print('svm')
    print(acc)

    acc_logistic = classifier.logistic(x, y, length)
    print('logistic')
    print(acc_logistic)

    acc_knn = classifier.knn(x, y, length)
    print('knn')
    print(acc_knn)

# looks like predictions tend to be 0 with arma features 