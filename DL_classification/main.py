import numpy as np
from DL_classification.extractor import Extractor
from DL_classification.models import ResearchModels
from DL_classification.generator import data_generator
from keras.callbacks import TensorBoard, ModelCheckpoint, EarlyStopping, ReduceLROnPlateau
import random


def train(model_name,
          selected_frame_num,
          num_videos,
          batch_size,
          file_name_list,
          train_video_list,
          val_video_list,
          Y_train,
          Y_val):

    root = 'E:/PhD/Lectures/SSP/Project/checkpoint/'
    checkpointer = ModelCheckpoint(filepath='model_frame50_size256.hdf5',
                                   monitor='loss',
                                   verbose=1,
                                   save_best_only=True)
    early_stopper = EarlyStopping(patience=10,monitor='loss')

    learningrate_strategy = ReduceLROnPlateau(factor=0.5,
                                     patience=30,
                                     monitor='loss',
                                     verbose=1)

    # detection-{epoch:02d}-{loss:.2f}.hdf5


    # generate train & val generator

    train_generator = data_generator(batch_size=batch_size,
                                     selected_frame_num=selected_frame_num,
                                     file_name_list=file_name_list,
                                     video_list=train_video_list,
                                     Y_label=Y_train)

    val_generator = data_generator(batch_size=1,
                                   selected_frame_num=selected_frame_num,
                                   file_name_list=file_name_list,
                                   video_list=val_video_list,
                                   Y_label=Y_val)

    train_steps_per_epoch = np.int(len(train_video_list)//batch_size)
    val_steps_per_epoch = np.int(len(val_video_list)//1)
    model = ResearchModels(2, model_name,selected_frame_num)

    history = model.model.fit_generator(generator=train_generator,
                    steps_per_epoch=train_steps_per_epoch,
                    epochs=30,
                    verbose=1,
                    callbacks=[checkpointer, early_stopper, learningrate_strategy])



def main():

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

    length = len(sample)  # 17 tester
    # li = list(range(0, length))
    # random.shuffle(li)
    #
    # train_sample_num = np.int(0.6*length)
    # train_sample_list = li[0:train_sample_num]
    # val_sample_list = li[train_sample_num:length]

    train_sample_list = [0, 2, 3, 4, 6, 8, 9, 11, 12, 14, 15]
    val_sample_list = [1, 5, 7, 10, 13, 16]


    ID = []
    for i in range(len(file_name_list)):
        Id = file_name_list[i].split('--')[-1]
        ID.append(Id)

    # train_sample_video_clip_name
    X_train_list = []
    Y_train = []
    for i in train_sample_list:
        NO_tester = sample[i]  # the id of selected tester
        tester_label = sample_y[i]
        ind = [p for p in range(len(file_name_list)) if ID[p] == NO_tester]
        t = [file_name_list[i] for i in ind]
        for j in t:
            X_train_list.append(j)

        num_video_of_tester = len(ind)
        for k in range(num_video_of_tester):

            if tester_label == '1':  # unhealthy
                Y_train.append([0, 1])
            else:
                Y_train.append([1, 0])

    Y_train = np.array(Y_train)
    del num_video_of_tester
    del t

    # val_sample_video_clip_name
    X_val_list = []
    Y_val = []

    for i in val_sample_list:  #
        NO_tester = sample[i]  # the id of selected tester, e.g. 'a01'
        tester_label = sample_y[i]
        ind = [p for p in range(len(file_name_list)) if ID[p] == NO_tester]
        t = [file_name_list[i] for i in ind]
        for j in t:
            X_val_list.append(j)

        num_video_of_tester = len(ind)
        for k in range(num_video_of_tester):

            if tester_label == '1':  # unhealthy
                Y_val.append([0, 1])
            else:
                Y_val.append([1, 0])
    Y_val = np.array(Y_val)



    # list1 = []
    # list2 = []
    # list3 = []
    #
    # for i in range(len(file_name_list)):
    #     t = file_name_list[i].split('--')[-1]
    #     pos = sample.index(t)
    #     if pos <= 6:
    #         list1.append(file_name_list[i])
    #     elif pos <=11:
    #         list2.append(file_name_list[i])
    #     else:
    #         list3.append(file_name_list[i])

    # THE ORIGINAL SELECTION METHOD!
    # total_videos_num = len(file_name_list)
    # train_videos_num = np.int(0.7 * total_videos_num)
    # # val_videos_num = total_videos_num - train_videos_num
    # li = list(range(0,total_videos_num))
    # random.shuffle(li)
    # train_videos_list = li[0:train_videos_num]
    # val_videos_list = li[train_videos_num:total_videos_num]
    #
    # healthy = np.array([[0,1]]); y1 = np.repeat(healthy,195, axis=0)
    # unhealthy = np.array([[1,0]]); y2 = np.repeat(unhealthy, 39, axis=0)
    # Y_label = np.concatenate([y1,y2],axis=0)
    #
    # Y_train = [Y_label[i,:] for i in train_videos_list]
    # Y_train = np.array(Y_train)
    # Y_val = [Y_label[i,:] for i in val_videos_list]
    # Y_val = np.array(Y_val)

    total_videos_num = len(file_name_list)
    selected_frame_num = 50
    model_name = 'lrcn'
    batch_size = 2



    train(model_name=model_name,
          selected_frame_num=selected_frame_num,
          num_videos=total_videos_num,
          batch_size=batch_size,
          file_name_list=file_name_list,
          train_video_list=X_train_list,
          val_video_list=X_val_list,
          Y_train=Y_train,
          Y_val=Y_val)



if __name__ == '__main__':
    main()






















#   extract features
# extractor = Extractor()
# root = 'E:/PhD/Lectures/SSP/Project/data/'
# file_path = root + 'task_a01_5ml-l0-5-2021_07_09_11_16_54-segmentation mask 1/SegmentationClass/'
#
#
# Features = []
# for frames in os.listdir(file_path):
#
#     features = extractor.extract(file_path+frames)
#     Features.append(features)