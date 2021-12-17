# Use the eigenvalue and variance calculated from HM + EM
# as the input of features for prediction
import os 
import pandas as pd
import numpy as np
import random
from classifier import classifier 

root =  os.path.join(os.getcwd(), 'Eigenvalue_Calc/');
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
        data = np.array(pd.read_csv(sub_sub_sub, header=None))
        DATA.append(data)
    NUM.append(num)

length = len(DATA)
index = [i for i in range(length)]
random.shuffle(index)
y = np.concatenate((np.zeros(NUM[0]), np.ones(NUM[1]), np.zeros(NUM[2])), axis=0)
y = np.array(y).astype('int32')

x = np.array(DATA).reshape(length, -1)[index, :]
y = y[index]

c = classifier(x, y, length, 'hmm')

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