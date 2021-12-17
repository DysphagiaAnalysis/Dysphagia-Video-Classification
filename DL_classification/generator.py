import os
from PIL import Image
import numpy as np
from util_read_excel import r_excel, clip_info



def data_generator(batch_size, selected_frame_num, file_name_list, video_list,Y_label):


    # X_train_list = [file_name_list[i] for i in video_list]

    #
    X_train_list = video_list


    while True:

        X, Y = [], []
        list_length = len(X_train_list)

        while len(X_train_list)> 0:

            for i in range (list_length):
                # Loop from here!
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



                images = np.array(images) # all frames of one video  shape(180, 80, 80, 3)
                y = Y_label[i,:]
                X.append(images)
                Y.append(y)

                if len(X) == batch_size or (len(X_train_list)==0 and len(X) >0):
                    X = np.array(X)
                    Y = np.array(Y)

                    yield X, Y
                    X, Y = [], []
