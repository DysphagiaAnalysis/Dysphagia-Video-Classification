from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
import numpy as np
from sklearn.mixture import GaussianMixture as gmm
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay
from sklearn.metrics import auc, roc_curve, RocCurveDisplay
from sklearn.metrics import PrecisionRecallDisplay
import matplotlib.pyplot as plt
import os

 # TODO: split data based on subject instead of clip

class classifier:
    def __init__(self, x, y, length, feature_extractor, train_percentage = 0.6):
        self.X = x
        self.y = y
        self.length = length
        self.feature_extrator = feature_extractor
        num1 = int(length*train_percentage)
        self.train_X = self.X[0:num1, :]
        self.test_X = self.X[num1:, :]
        self.train_y = self.y[0:num1]
        self.test_y = self.y[num1:]
        print(self.test_y)

    def gmm_cluster(self, cluster=2):
        
        model = gmm(n_components=2, max_iter=500, n_init=1).fit(self.X)
        cluster_mean = model.means_
        result = model.predict(self.X)

        acc = sum(self.y == result) / self.length
        #self.cm_plot(model, self.y, result, 'gmm')
        #self.roc(self.y, result, 'knn')
        return acc

    def knn(self):
        knn = KNeighborsClassifier(n_neighbors=4)
        knn.fit(self.train_X, self.train_y)
        y_hat = knn.predict(self.test_X)
        print(y_hat)
        acc = np.sum(self.test_y == y_hat)/self.test_y.shape[0]
        self.cm_plot(knn, self.test_y, y_hat, 'knn')
        self.roc(self.test_y, y_hat, 'knn')
        return acc

    # label might be wrong, 0/1?
    def svm(self):
        svm = make_pipeline(StandardScaler(), LinearSVC())
        svm.fit(self.train_X, self.train_y)
        y_hat = svm.predict(self.test_X)
        print(y_hat)
        acc =  np.sum(self.test_y == y_hat)/self.test_y.shape[0]
        self.cm_plot(svm, self.test_y, y_hat, 'svm')
        self.roc(self.test_y, y_hat, 'svm')
        return acc

    def logistic(self):
        lr = LogisticRegression(solver='newton-cg')
        lr.fit(self.train_X, self.train_y)
        y_hat = lr.predict(self.test_X)
        print(y_hat)
        acc = np.sum(self.test_y == y_hat)/self.test_y.shape[0]
        self.cm_plot(lr, self.test_y, y_hat, 'logistic')
        self.roc(self.test_y, y_hat, 'logistic')
        return acc

    def cm_plot(self, clf, y_test, y_hat, name):
        cm = confusion_matrix(y_test, y_hat, labels=clf.classes_)
        disp = ConfusionMatrixDisplay(confusion_matrix=cm, display_labels=clf.classes_)
        disp.plot()
        plt.savefig(os.path.join('plots', self.feature_extrator + '_cm_'+name + '.png'))
    
    def roc(self, y_test, y_hat, name):
        fpr, tpr, thresholds = roc_curve(y_test, y_hat)
        roc_auc = auc(fpr, tpr)
        display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name=name)
        display.plot()
        plt.savefig(os.path.join('plots', self.feature_extrator +'_roc_' + name + '.png'))