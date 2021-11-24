import os
import glob
import util_read_excel
import pandas as pd
import math


class loc:
    def __init__(self, df_excel, clip_name):
        self.c = util_read_excel.clip_info(df_excel, clip_name)
        self.clip_name = clip_name

        data_dir = os.path.join(os.path.abspath(os.getcwd()), "HB_Anno", "*")
        data_file_names = glob.glob(data_dir)
        for loc_file_dir in data_file_names:
            if self.clip_name in loc_file_dir:
                self.loc_folder_path = loc_file_dir
                break

        self.df_hb = self.get_HB()
        self.df_mandible = self.get_Mandible()

        self.hbr, self.hbm = (
            int(self.c.df_clip["HBR"].iloc[0]),
            int(self.c.df_clip["HBM"].iloc[0]),
        )

    # DONE
    def get_HB(self):
        HB_CSV = os.path.join(self.loc_folder_path, "HB.csv")
        return pd.read_csv(HB_CSV, header=None)

    # DONE
    def get_Mandible(self):
        all_files = os.path.join(self.loc_folder_path, "*")
        names_for_check = glob.glob(all_files)
        if "M.csv" not in names_for_check:
            return None
        else:
            M_CSV = os.path.join(self.loc_folder_path, "M.csv")
            return pd.read_csv(M_CSV, header=None)

    # DONE
    # 500 pixels -> 10 cm; 50 pixels-> 1cm
    def cal_max_displacement(self):
        onset_x, onset_y = self.df_hb.iloc[self.hbr]
        maximum_x, maximum_y = self.df_hb.iloc[self.hbm]
        return math.sqrt((onset_x - maximum_x) ** 2 + (onset_y - maximum_y) ** 2) / 50

    # DONE
    def cal_relative_loc(self, timestamp="hbr"):
        if not self.df_mandible:
            return None
        if timestamp == "hbr":
            x, y = self.df_hb.iloc[self.hbr]
            ref_x, ref_y = self.df_mandible.iloc[self.hbr]
        elif timestamp == "hbm":
            x, y = self.df_hb.iloc[self.hbm]
            ref_x, ref_y = self.df_mandible.iloc[self.hbm]
        return math.sqrt((x - ref_x) ** 2 + (y - ref_y) ** 2) / 50

    # DONE
    def cal_delta_percentage(self, axis="x"):  # in x or y axis
        if not self.df_mandible:
            return None
        x_hbr, y_hbr = self.df_hb.iloc[self.hbr]
        x_hbm, y_hbm = self.df_hb.iloc[self.hbm]
        x_hbr_ref, y_hbr_ref = self.df_mandible.iloc[self.hbr]
        x_hbm_ref, y_hbm_ref = self.df_mandible.iloc[self.hbm]
        if axis == "x":
            hbr_relative, hbm_relative = x_hbr - x_hbr_ref, x_hbm - x_hbm_ref
        elif axis == "y":
            hbr_relative, hbm_relative = y_hbr - y_hbr_ref, y_hbm - y_hbm_ref
        return (hbr_relative - hbm_relative) / hbr_relative

    # DONE
    # theta(HBM - M) - theta(M - HBR)
    def cal_angle_in_degree(self):
        if not self.df_mandible:
            return None
        x_hbr, y_hbr = self.df_hb.iloc[self.hbr]
        x_hbm, y_hbm = self.df_hb.iloc[self.hbm]
        x_hbr_ref, y_hbr_ref = self.df_mandible.iloc[self.hbr]
        x_hbm_ref, y_hbm_ref = self.df_mandible.iloc[self.hbm]
        theta1 = math.atan((y_hbm - y_hbm_ref) / (x_hbm - x_hbm_ref)) * 180 / math.pi
        theta2 = math.atan((y_hbr - y_hbr_ref) / (x_hbr - x_hbr_ref)) * 180 / math.pi
        return theta1 - theta2


if __name__ == "__main__":

    excel_name = "D.xlsx"
    r = util_read_excel.r_excel(excel_name)
    df = r.df_excel

    clip_names = []
    data_list = "GH_E_list.txt"
    with open(data_list) as file:
        clip_names = file.readlines()
        clip_names = [clip.rstrip() for clip in clip_names]

    clip = []
    onset2max = []
    max2offset = []

    for i in range(len(names)):
        name = names[i]
        c = read_excel.clip_info(df, name)
        h_onset, h_maximum, h_offset = c.hyoid_info()
        print(name, h_onset, h_maximum, h_offset)
        file_dir = os.path.join(os.path.abspath(os.getcwd()), folder, name + ".csv")
        clip_df = pd.read_csv(file_dir, header=None)
        onset_x, onset_y = clip_df.iloc[h_onset]
        maximum_x, maximum_y = clip_df.iloc[h_maximum]
        offset_x, offset_y = clip_df.iloc[h_offset]

        dis1 = (
            math.sqrt((onset_x - maximum_x) ** 2 + (onset_y - maximum_y) ** 2) / 30.78
        )
        dis2 = (
            math.sqrt((offset_x - maximum_x) ** 2 + (offset_y - maximum_y) ** 2) / 30.78
        )
        clip.append(name)
        onset2max.append(dis1)
        max2offset.append(dis2)

    dis_df = pd.DataFrame(
        list(zip(clip, onset2max, max2offset)),
        columns=["clip", "onset2max", "max2offset"],
    )
    dis_df.to_csv("displacement.csv", index=False)

