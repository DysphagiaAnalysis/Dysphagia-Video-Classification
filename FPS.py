import numpy as np
import os
import glob
import pandas as pd

def load_text_numpy(path, delimiter, dtype):
    if isinstance(delimiter, (tuple, list)):
        for d in delimiter:
            try:
                ground_truth_rect = np.loadtxt(path, delimiter=d, dtype=dtype)
                return ground_truth_rect
            except:
                pass

        raise Exception('Could not read file {}'.format(path))
    else:
        ground_truth_rect = np.loadtxt(path, delimiter=delimiter, dtype=dtype)
        return ground_truth_rect

def load_text(path, delimiter=' ', dtype=np.float32, backend='numpy'):
    if backend == 'numpy':
        return load_text_numpy(path, delimiter, dtype)


folder = "Dump Annotations Test"
file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, "*.zip")
names = glob.glob(file_dir)
names_anno = [name.split('/')[-1].split('.')[0] for name in names]
names_excel = ['_'.join(name.split('_')[1:-1]) for name in names_anno]
names_excel.sort()
names_pred = names_excel


tracker = 'ATOM18'

from scipy import stats
items = []

for i in range(len(names_pred)):
    item = []
    item.append(names_pred[i])
    file_name = names_pred[i] + '_time.txt'
    results_path = os.path.join(os.path.abspath(os.getcwd()), tracker, file_name) 

    times = load_text(str(results_path), delimiter=('\t', ','), dtype=np.float64)
    tot_time = np.sum(times)
    frame = len(times)
    FPS = frame/tot_time
    item.append(FPS)
    items.append(item)

df = pd.DataFrame(items, columns =['name', 'FPS'])

name = 'FPS' + tracker
df.to_excel(name + '.xlsx')