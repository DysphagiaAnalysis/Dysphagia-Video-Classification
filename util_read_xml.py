import read_excel 

import os 
from xml.etree import ElementTree
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D

file_name = 'annotations.xml'
full_file = os.path.abspath(file_name)
mytree = ElementTree.parse(file_name)
myroot = mytree.getroot()
first_point = myroot[2][0].attrib['points'].split(',')
first_x, first_y = float(first_point[0]), float(first_point[1])
frame_tot = len(myroot[2])
pts_x_lst = []
pts_y_lst = []
frames_lst = []
count = 0
for i in myroot[2]:
    frame = float(i.attrib['frame'])
    point = i.attrib['points'].split(',')
    x = float(point[0]) - first_x
    y = float(point[1]) - first_y
    pts_x_lst.append(x)
    pts_y_lst.append(y)
    frames_lst.append(frame)

    pts_x = np.array(pts_x_lst)
    pts_y = np.array(pts_y_lst)
    frames = np.array(frames_lst)
    
    fig = plt.figure()    
    ax = fig.add_subplot(111,projection = '3d')

    ax.set_xlim(-50,20)
    ax.set_ylim(0,frame_tot)
    ax.set_zlim(30, -30)
    ax.set_xlabel('X')
    ax.set_ylabel('frames')
    ax.set_zlabel('Y')
    ax.view_init(elev=10, azim=270)

    ax.scatter(pts_x, frames, pts_y)
    plt.savefig('plot%d'% count)
    count += 1



    
'''
print(myroot.tag)
print(myroot[2].tag)
print(myroot[2].attrib)
for x in myroot[2]:
    print( x.attrib['frame'], x.attrib['points'])
'''



if __name__ == '__main__':

    import os 
    import glob
    import read_excel
    import pandas as pd
    import math

    excel_name = 'Swallowing Coordination Data_raw (for trimming).xlsx'
    r = read_excel.r_excel(excel_name)
    df = r.df_excel

    folder = "anno_csv"
    file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, "*.csv")
    names = glob.glob(file_dir)
    names = [name.split('/')[-1].split('.')[0] for name in names]
    print(names)
    clip = []
    onset2max = []
    max2offset = []

    for i in range(len(names)):
        name = names[i]
        c = read_excel.clip_info(df, name)
        h_onset, h_maximum, h_offset = c.hyoid_info()
        print(name, h_onset, h_maximum, h_offset)
        file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, name + '.csv')
        clip_df = pd.read_csv(file_dir, header = None)
        onset_x, onset_y = clip_df.iloc[h_onset]
        maximum_x, maximum_y = clip_df.iloc[h_maximum]
        offset_x, offset_y = clip_df.iloc[h_offset]

        dis1 = math.sqrt((onset_x - maximum_x)**2 + (onset_y - maximum_y)**2) / 30.78
        dis2 = math.sqrt((offset_x - maximum_x)**2 + (offset_y - maximum_y)**2) / 30.78
        clip.append(name)
        onset2max.append(dis1)
        max2offset.append(dis2)

    dis_df = pd.DataFrame(list(zip(clip, onset2max, max2offset)), columns =['clip', 'onset2max', 'max2offset']) 
    dis_df.to_csv('displacement.csv', index=False)