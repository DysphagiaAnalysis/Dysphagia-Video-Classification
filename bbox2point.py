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

if __name__ == '__main__':
    folder = "Dump Annotations Test"
    file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, "*.zip")
    names = glob.glob(file_dir)
    names_anno = [name.split('/')[-1].split('.')[0] for name in names]
    names_excel = ['_'.join(name.split('_')[1:-1]) for name in names_anno]
    names_excel.sort()
    names_pred = names_excel

    for i in range(len(names_pred)):
        file_name = names_pred[i] + '.txt'
        results_path = os.path.join(os.path.abspath(os.getcwd()), 'SiamFC22', file_name) 
        pred_bb = load_text(str(results_path), delimiter=('\t', ','), dtype=np.float64)
        pred_center = pred_bb[:, :2] + 0.5 * (pred_bb[:, 2:] - 1.0)
        df = pd.DataFrame(pred_center)
        df.to_excel(names_pred[i] + '.xlsx', header = 0, index = 0)