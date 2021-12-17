import os
import numpy as np

f = open('filename.txt')
line = f.readlines()
k = 0
NUM_frame = []
for i in line:
    new = i.split("\n")[0]
    num_frame = new.split('--')[2]
    num_frame = np.int(num_frame)
    NUM_frame.append(num_frame)

num = np.array(NUM_frame)
min = np.max(num)
print(min)

a = 'frame_000444'
b = a.split('_')[1]
print(np.int(b))