import numpy as np
import util_read_excel
import loc
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
    inv = np.linalg.inv(np.dot(PHI.transpose(), PHI))
    theta = np.matmul(inv, PHI.transpose())
    theta = np.matmul(theta, Y_observe)
    return theta


import classfier 
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
    order = 2
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

    # shuffle 
    index = [i for i in range(length)]
    random.shuffle(index)
    y = np.concatenate((np.zeros((NUM[0], 1)), np.ones((NUM[1], 1)), np.zeros((NUM[2], 1))), axis=0)
    y = np.array(y).astype('int32')
    
    x = PARAM[index, :]
    y = y[index, :]

    # Start GMM-EM
    result = classfier.gmm_cluster(x, y, length)
    print(result)
    # end GMM-EM

    # Start SVR
    # b = np.zeros((y.shape[1], 1 + 1))
    # b[np.arange(y.shape[1]), y] = 1
    # y = b

    acc = classfier.svm(x, y, length)

    print('---')
    print(acc)







    # version 1
    # DATA1 = DATA[0]
    #
    #
    # folder_path = 'E:/PhD/Lectures/SSP/Project/data_test/'
    # order = 5
    # num = len(os.listdir(folder_path))
    # PARAM = np.zeros((num, 2*order))
    # j = 0
    #
    # for i in os.listdir(folder_path):
    #     HB_CSV = folder_path + i
    #     data = pd.read_csv(HB_CSV, header=0)
    #     data1 = np.array(data)[:,1:]
    #     theta_x = claculate_arma_param(data1, order, 0)
    #     theta_y = claculate_arma_param(data1, order, 1)
    #     theta = np.concatenate((theta_x, theta_y),axis=0).transpose()
    #     PARAM[j:j+1,:] = theta
    #     j = j + 1
