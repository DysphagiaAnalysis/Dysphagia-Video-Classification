class classifier:
    def __init__(self):
        pass

    def gmm(self):
        pass

    def knn(self):
        pass

    def svm(self):
        pass

    def logistic(self):
        pass

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
import numpy as np
from sklearn.mixture import GaussianMixture as gmm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier

 # TODO: split data based on subject instead of clip

def gmm_cluster(x, y, length, cluster=2):
    
    model = gmm(n_components=2, max_iter=500, n_init=1).fit(x)
    cluster_mean = model.means_
    classification_result = model.predict(x)
    result = classification_result.reshape(length, 1)

    t = sum(y == result)
    accuracy1 = t[0] / length
    return accuracy1

def svm(x, y, length, train_percentage = 0.6):
    num1 = int(length*train_percentage)
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
    return acc

def logistic(x, y, length, train_percentage=0.6):
    num1 = int(length*train_percentage)
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1, :]
    test_y = y[num1:, :]
    model = LogisticRegression(C=1e6)
    model.fit(train_x, train_y)
    y_hat = model.predict(test_x)
    y_predict = np.round(y_hat).reshape(length-num1,1)
    num = np.sum(test_y == y_predict)
    acc = num/test_y.shape[0]
    return acc

def knn(x, y, length, train_percentage=0.6):
    num1 = int(length*train_percentage)
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1, :]
    test_y = y[num1:, :]
    knn = KNeighborsClassifier(n_neighbors=4)
    knn.fit(train_x, train_y)
    y_hat = knn.predict(test_x)
    y_predict = np.round(y_hat).reshape(length-num1,1)
    num = np.sum(test_y == y_predict)
    acc = num/test_y.shape[0]
    return acc