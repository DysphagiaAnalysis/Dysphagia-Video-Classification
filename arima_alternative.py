import pyodbc 
import matplotlib.pyplot as plt
import numpy as np 
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.seasonal import seasonal_decompose
from statsmodels.tsa.arima_process import arma_generate_sample
import os 
from classifier import classifier 
import random


root =  os.path.join(os.getcwd(), 'data/');
DATA = []
NUM = []
PARAM = []
length = 0
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
        theta_x = ARIMA((data['x'] - data['x'][0])/ (max(data['x']) - min(data['x'])), order=(3, 1, 2)).fit(method_kwargs={"warn_convergence": False})
        theta_y = ARIMA((data['y'] - data['y'][0])/ (max(data['y']) - min(data['y'])), order=(3, 1, 2)).fit(method_kwargs={"warn_convergence": False})
        theta = np.concatenate((theta_x.arparams, theta_x.maparams, theta_y.arparams, theta_y.maparams), axis=0).transpose()
        PARAM.append(theta)
    length += num
    NUM.append(num)

index = [i for i in range(length)]
random.shuffle(index)

y = np.concatenate((np.zeros((NUM[0], 1)), np.ones((NUM[1], 1)), np.zeros((NUM[2], 1))), axis=0)
y = np.array(y).astype('int32')

PARAM = np.array(PARAM)
x = PARAM[index, :]
y = y[index, :]
y = np.squeeze(y)

c = classifier(x, y, length, 'arima312')

result = c.gmm_cluster()
print('gmm')
print(result)

acc = c.svm()
print('svm')
print(acc)

acc_logistic = c.logistic()
print('logistic')
print(acc_logistic)

acc_knn = c.knn()
print('knn')
print(acc_knn)