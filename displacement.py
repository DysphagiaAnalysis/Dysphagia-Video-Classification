import read_excel 


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