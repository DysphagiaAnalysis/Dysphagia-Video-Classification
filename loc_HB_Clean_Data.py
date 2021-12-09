import os
import glob
import util_read_excel
import pandas as pd
import math


class loc:
    def __init__(self, folder, df_excel, clip_name):
        self.c = util_read_excel.clip_info(df_excel, clip_name)
        self.clip_name = clip_name

        data_dir = os.path.join(os.path.abspath(os.getcwd()), folder, "*")
        data_file_names = glob.glob(data_dir)
        for loc_file_dir in data_file_names:
            if self.clip_name in loc_file_dir:
                self.loc_folder_path = loc_file_dir
                break

        self.df_hb = self.get_HB()
        
        self.ss, self.se = (
            int(self.c.df_clip["SS"].iloc[0]),
            int(self.c.df_clip["SE"].iloc[0]),
            )

        self.hbr, self.hbm, self.hbo = (
            int(self.c.df_clip["HBR"].iloc[0]),
            int(self.c.df_clip["HBM"].iloc[0]),
            int(self.c.df_clip["HBOS"].iloc[0]),
        )

    # DONE
    def get_HB(self):
        HB_CSV = os.path.join(self.loc_folder_path, "HB.csv")
        return pd.read_csv(HB_CSV, header=0)

if __name__ == "__main__":

    folder = "HB_Anno_E/"     # change A, D, E when necessary
    excel_name = "info_summary/E.xlsx"  # change A, D, E when necessary
    data_list = "info_summary/HB_list_E.txt"  # change A, D, E when necessary

    r = util_read_excel.r_excel(excel_name)
    df = r.df_excel

    clip_names = []
    with open(data_list) as file:
        clip_names = file.readlines()
        clip_names = [clip.rstrip() for clip in clip_names]
        
    need_clean = []
    can_use = []
    
    # create new folder for the clean data
    current_directory = os.getcwd()
    final_dir = os.path.join(current_directory, r'HB_Anno_E_Clean_Data') # change A, D, E when necessary
    if not os.path.exists(final_dir):
        os.makedirs(final_dir)        
        
    # write clean data to csv files
    for clip_name in clip_names:
        l = loc(folder, df, clip_name)
        if not l.df_hb[l.df_hb['frame'] == l.ss].empty and not l.df_hb[l.df_hb['frame'] == l.se].empty:
            can_use.append(l.clip_name)
            name = "HB_"+l.clip_name + "_clean_data"
            filename = "%s.csv" % name
            full_name = os.path.join(final_dir,filename)
            l.df_hb[l.df_hb.index[l.df_hb['frame'] == l.ss].tolist()[0]:l.df_hb.index[l.df_hb['frame'] == l.se].tolist()[0]+1].to_csv(full_name)
        else:
            need_clean.append(l.clip_name)

    textfile = open("HB_list_E_new.txt", "w")  #change A, D, E when necessary
    for element in can_use:
        textfile.write(element + "\n")
    textfile.close()
    
    textfile = open("HB_list_E_need_clean.txt", "w") #change A, D, E when necessary
    for element in need_clean:
        textfile.write(element + "\n")
    textfile.close()





