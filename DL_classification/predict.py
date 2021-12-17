
import os
from keras.models import load_model
import numpy as np
from PIL import Image
import sys

model = load_model('model_frame50_size256.hdf5')  # frame_50 79%  size(128,128)
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
            Y_true.append([0, 1])
        else:
            Y_true.append([1, 0])

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
                im_crop = im_crop.resize((256, 256), Image.BILINEAR)
                im_array = np.asarray(im_crop)
                images.append(im_array)
                frame_num = frame_num + 1

    images = np.array(images)[np.newaxis,:,:,:,:]

    y_predict = model.predict(images)
    y_predict = y_predict.reshape((1,2))
    predict_label = np.where(y_predict == np.max(y_predict))[1]
    Y_predict.append(predict_label)

Y_predict = np.array(Y_predict).reshape((len(X_train_list),1))
Y_true = np.where(Y_true==1)[1].reshape((len(X_train_list),1))
num = len(np.where(Y_predict == Y_true)[0])
acc = num/len(X_train_list)*100
print(acc)



