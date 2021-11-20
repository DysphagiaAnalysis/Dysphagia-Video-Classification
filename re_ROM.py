
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
import glob


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


class pattern:
    
    def __init__(self, tracker, name):
        self.name = name 
        csv_file = name + '.csv'
        csv_dir_anno = os.path.join(os.path.abspath(os.getcwd()), 'anno_csv', csv_file)
        self.df_anno = pd.read_csv(csv_dir_anno, header = None)  

        file_name = name + '.txt'
        results_path = os.path.join(os.path.abspath(os.getcwd()), tracker, file_name) 
        pred_bb = load_text(str(results_path), delimiter=('\t', ','), dtype=np.float64)
        pred_center = pred_bb[:, :2] + 0.5 * (pred_bb[:, 2:] - 1.0)
        self.df_pred = pd.DataFrame(pred_center)  

        self.num_frames = len(self.df_anno.index)
        self.X_anno = self.df_anno.iloc[:,0].to_numpy()
        self.Y_anno = self.df_anno.iloc[:,1].to_numpy()
        self.X_pred = self.df_pred.iloc[:,0].to_numpy()
        self.Y_pred = self.df_pred.iloc[:,1].to_numpy()


    def ROMs(self, onset, maximum, offset):
        X_start_anno = self.X_anno[onset]
        Y_start_anno = self.Y_anno[onset]
        X_start_pred = self.X_pred[onset]
        Y_start_pred = self.Y_pred[onset]
        Xs_end_anno = self.X_anno[maximum: offset + 1]
        Ys_end_anno = self.Y_anno[maximum: offset + 1]
        distances = np.sqrt((Xs_end_anno - X_start_anno)**2 + (Ys_end_anno - Y_start_anno)**2)
        delta_frame = np.argmax(distances)
        ROM = np.max(distances)
        
        
        X_end_pred = self.X_pred[maximum+delta_frame]
        Y_end_pred = self.Y_pred[maximum+delta_frame]
        ROM_pred = np.sqrt((X_end_pred - X_start_pred)**2 + (Y_end_pred - Y_start_pred)**2)
        re_2d = abs(ROM_pred - ROM)/ROM

        ROM_X_anno = abs(self.X_anno[maximum+delta_frame] - X_start_anno)
        ROM_X_pred = abs(X_end_pred - X_start_pred)
        re_X = abs(ROM_X_anno - ROM_X_pred)/ROM_X_anno

        ROM_Y_anno = abs(self.Y_anno[maximum+delta_frame] - Y_start_anno)
        ROM_Y_pred = abs(Y_end_pred - Y_start_pred)
        re_Y = abs(ROM_Y_anno - ROM_Y_pred)/ROM_Y_anno
        

        return ROM, re_2d, re_X, re_Y

    def ROM_on2max(self, onset, maximum):
        X_on, Y_on  = self.X[onset], self.Y[onset]
        X_max, Y_max = self.X[maximum], self.Y[maximum]
        dis = np.sqrt((X_max - X_on)**2 + (Y_max - Y_on)**2)
        return dis
    
    def ROM_ss2max(self, ss, maximum):
        X_ss, Y_ss  = self.X[ss], self.Y[ss]
        X_max, Y_max = self.X[maximum], self.Y[maximum]
        dis = np.sqrt((X_max - X_ss)**2 + (Y_max - Y_ss)**2)
        return dis

if __name__ == "__main__":
    import os 
    import glob
    import read_excel


    excel_name = 'Swallowing Coordination Data_raw (for trimming).xlsx'
    r = read_excel.r_excel(excel_name)
    df = r.df_excel

    folder = "Dump Annotations Test"
    file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, "*.zip")
    names = glob.glob(file_dir)
    names_anno = [name.split('/')[-1].split('.')[0] for name in names]
    names_excel = ['_'.join(name.split('_')[1:-1]) for name in names_anno]
    #names_excel = [name[0].upper() + name[1:] for name in names_excel]
    print(names_excel)
    names_excel.sort()
    print(names_excel)
    names_anno = names_excel


    tracker = 'SiamFC22'
    lst = []

    for i in range(len(names_anno)):
        item = []
        c = read_excel.clip_info(df, names_excel[i])
        ss, se = c.swallow_info()
        h_onset, h_max, h_offset = c.hyoid_info()
        h_onset -= 1

        p = pattern(tracker, names_anno[i])
        item.append(names_anno[i])
        ROM, re_2d, re_X, re_Y = p.ROMs(h_onset,h_max,h_offset)
        item.append(ROM)
        item.append(re_2d)
        item.append(re_X)
        item.append(re_Y)

        lst.append(item)

    df = pd.DataFrame(lst, columns = ['clip', 'ROM', 're_2d', 're_X', 're_Y'])
    df.to_excel(tracker+'re2_ROM' +'.xlsx')