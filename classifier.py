# class classifier:
#     def __init__(self):
#         pass

#     def gmm(self):
#         pass

#     def knn(self):
#         pass

#     def svm(self):
#         pass

#     def logistic(self):
#         pass

from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVR
import numpy as np
from sklearn.mixture import GaussianMixture as gmm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier

 # TODO: split data based on subject instead of clip
 # TODO: ROC and confusion matrix

def gmm_cluster(x, y, length, cluster=2):
    
    model = gmm(n_components=2, max_iter=500, n_init=1).fit(x)
    cluster_mean = model.means_
    result = model.predict(x)

    accuracy1 = sum(y == result) / length
    return accuracy1

# label might be wrong, 0/1?
def svm(x, y, length, train_percentage = 0.6):
    num1 = int(length*train_percentage)
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1]
    test_y = y[num1:]

    svm = make_pipeline(StandardScaler(), SVR(kernel='linear', C=0.0001, epsilon=0.02))
    svm.fit(train_x, train_y)
    y_hat = svm.predict(test_x)
    y_predict = np.round(y_hat)
    acc =  np.sum(test_y == y_predict)/test_y.shape[0]
    return acc

def logistic(x, y, length, train_percentage=0.6):
    num1 = int(length*train_percentage)
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1]
    test_y = y[num1:]
    lr = LogisticRegression(solver='newton-cg')
    lr.fit(train_x, train_y)
    y_hat = lr.predict(test_x)
    y_predict = np.round(y_hat)
    acc = np.sum(test_y == y_predict)/test_y.shape[0]
    return acc

def knn(x, y, length, train_percentage=0.6):
    num1 = int(length*train_percentage)
    train_x = x[0:num1, :]
    test_x = x[num1:, :]
    train_y = y[0:num1]
    test_y = y[num1:]
    knn = KNeighborsClassifier(n_neighbors=4)
    knn.fit(train_x, train_y)
    y_hat = knn.predict(test_x)
    y_predict = np.round(y_hat)
    acc = np.sum(test_y == y_predict)/test_y.shape[0]
    return acc