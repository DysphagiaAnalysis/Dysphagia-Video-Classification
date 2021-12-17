
import os
from keras.models import load_model
import numpy as np
from PIL import Image
import sys
from sklearn.metrics import confusion_matrix, ConfusionMatrixDisplay, roc_curve, auc, RocCurveDisplay
import matplotlib.pyplot as plt


def metric(y_test, y_hat):
    y_test_1 = np.where(y_test == 1)[0]
    y_yest_0 = np.where(y_test == 0)[0]
    y_hat_1 = np.where(y_hat == 1)[0]
    y_hat_0 = np.where(y_hat == 0)[0]

    tp = len([p for p in y_hat_1 if p in y_test_1])
    tn = len([p for p in y_hat_0 if p in y_yest_0])
    fp = len([p for p in y_hat_1 if p in y_yest_0])
    fn = len([p for p in y_hat_0 if p in y_test_1])

    accuracy = (tp + tn) / (tp + tn + fp + fn) * 100
    recall = tp / (tp + fn) * 100
    precision = tp / (tp + fp) * 100
    return [accuracy, precision, recall]

def roc(y_test, y_hat, name):
    fpr, tpr, thresholds = roc_curve(y_test, y_hat)
    roc_auc = auc(fpr, tpr)
    display = RocCurveDisplay(fpr=fpr, tpr=tpr, roc_auc=roc_auc, estimator_name=name)
    display.plot()
    plt.savefig( ('plots_roc' + name + '.png'))
    return roc_auc


def cm_plot(y_test, y_hat, name):
    cm = confusion_matrix(y_test, y_hat)
    disp = ConfusionMatrixDisplay(confusion_matrix=cm)
    disp.plot()
    plt.savefig(('plots_confusion' + name + '.png'))



model = load_model('E:/PhD/Lectures/SSP/Project/checkpoint/model_frame50_size128_depth2.hdf5')  # frame_50 79%  size(128,128)
selected_frame_num = 50
video_list = [1, 5, 7, 10, 13, 16]


f = open('filename.txt')
line = f.readlines()
file_name_list = []
for i in line:
    new = i.split("\n")[0]
    file_name_list.append(new)


sample1 = ['a01', 'a05', 'a07', 'a20', 'a21', 'a23', 'a25']
sample1_y = ['0', '0', '0', '0', '0', '0', '0']
sample2 = ['e01', 'e03', 'e06', 'e08', 'e09']
sample2_y = ['0', '0', '0', '0', '0']
sample3 = ['d01', 'd02', 'd06', 'd07', 'd08']
sample3_y = ['1', '1', '1', '1', '1']
sample = sample1 + sample2 + sample3
sample_y = sample1_y + sample2_y + sample3_y


X_train_list=[]

ID = []
for i in range(len(file_name_list)):
    Id = file_name_list[i].split('--')[-1]
    ID.append(Id)


Y_true = []
for i in video_list:
    NO_tester = sample[i]  # the id of selected tester
    tester_label = sample_y[i]
    ind = [p for p in range(len(file_name_list)) if ID[p] == NO_tester]
    t = [file_name_list[i] for i in ind]
    for j in t:
        X_train_list.append(j)

    num_video_of_tester = len(ind)
    for k in range(num_video_of_tester):

        if tester_label == '1':  # unhealthy
            Y_true.append([1])
        else:
            Y_true.append([0])

Y_true = np.array(Y_true)


Y_predict = []
for i in range(len(X_train_list)):

    current1 = X_train_list[i]
    current = current1.split('--')[0]
    start = np.int(current1.split('--')[1])
    end = np.int(current1.split('--')[2])
    category = current1.split('--')[4]


    images = []

    total_frame_num = selected_frame_num
    frame_num = 0
    for j in os.listdir(current):
        idx = j.split('_')[1]
        idx = idx.split('.')[0]
        idx = np.int(idx)

        if frame_num < selected_frame_num:
            if idx >= start:
                absolute_path = current + '/' + j
                im = Image.open(absolute_path)
                left = 400; right = 750; top = 500; bottom = 750
                im_crop = im.crop((left, top, right, bottom))
                im_crop = im_crop.resize((128, 128), Image.BILINEAR)
                im_array = np.asarray(im_crop)
                images.append(im_array)
                frame_num = frame_num + 1

    images = np.array(images)[np.newaxis,:,:,:,:]

    y_predict = model.predict(images)
    y_predict[y_predict >= 0.5] = 1
    y_predict[y_predict < 0.5] = 0
    y_predict = y_predict.reshape((1,1))
    Y_predict.append(y_predict)
    # y_predict = y_predict.reshape((1,2))
    # predict_label = np.where(y_predict == np.max(y_predict))[1]
    # Y_predict.append(predict_label)

Y_predict = np.array(Y_predict).reshape((len(X_train_list),1))


# evaluate metric
name = 'BCU_2'
metrics = metric(Y_true,Y_predict)
roc_auc = roc(Y_true, Y_predict, name)
cm_plot(Y_true, Y_predict, name)
#
print(metrics)
print(roc_auc)
