import numpy as np
import util_read_excel
import loc
import os
import pandas as pd
from sklearn import preprocessing
from sklearn.mixture import GaussianMixture as gmm
import random
from sklearn.svm import SVR
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
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


def gmm_cluster(data, cluster=2):

    model = gmm(n_components=2, max_iter=500, n_init=1).fit(data)
    cluster_mean = model.means_
    classification_result = model.predict(data)
    return classification_result



if __name__ == "__main__":

    root = 'E:/PhD/Lectures/SSP/Project/data_position/'
    DATA = []
    NUM = []
    for i in os.listdir(root):
        sub = root + i +'/'
        for j in os.listdir(sub):
            sub_sub = sub +j + '/'
            num = 0
            for k in os.listdir(sub_sub):
                num = num + 1
                sub_sub_sub = sub_sub + k +'/'
                HB_CSV = sub_sub_sub + 'HB.csv'
                data = pd.read_csv(HB_CSV, header=0)
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


    # Start GMM-EM
    result = gmm_cluster(PARAM, cluster=2)
    result = result.reshape(1,length)

    p1 = np.zeros((1, NUM[0]+NUM[1]))
    p2 = np.ones((1,NUM[2]))
    p = np.concatenate((p1,p2),axis=1)

    t = np.where(p == result)
    mm = len(t[1])
    accuracy1 = mm / length

    print(result)
    print(accuracy1)
    print(1-accuracy1)
    # end GMM-EM



    # Start SVR
    index = [i for i in range(length)]
    random.shuffle(index)
    y = np.concatenate((np.zeros((1, NUM[0]+NUM[1])), np.ones((1,NUM[2]))), axis=1)
    y = np.array(y).astype('int32')
    y = y.transpose()
    # b = np.zeros((y.shape[1], 1 + 1))
    # b[np.arange(y.shape[1]), y] = 1
    # y = b
    x = PARAM[index, :]
    y = y[index, :]
    num1 = 60
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1, :]
    test_y = y[num1:, :]

    regr = make_pipeline(StandardScaler(), SVR(kernel='linear', C=0.0001, epsilon=0.02))
    regr.fit(train_x, train_y)
    y_hat = regr.predict(test_x)
    y_predict = np.round(y_hat).reshape(length-num1,1)
    num = np.sum(test_y == y_predict)
    acc = num/test_y.shape[0]
    print(acc)

    # End SVR








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
