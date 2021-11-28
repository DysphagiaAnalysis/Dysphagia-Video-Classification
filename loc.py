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
        self.df_mandible = self.get_Mandible()

        self.hbr, self.hbm = (
            int(self.c.df_clip["HBR"].iloc[0]),
            int(self.c.df_clip["HBM"].iloc[0]),
        )

    # DONE
    def get_HB(self):
        HB_CSV = os.path.join(self.loc_folder_path, "HB.csv")
        return pd.read_csv(HB_CSV, header=0)

    # DONE
    def get_Mandible(self):
        all_files = os.path.join(self.loc_folder_path, "*")
        names_for_check = glob.glob(all_files)
        for name_check in names_for_check:
            if "M.csv" in name_check:
                return pd.read_csv(name_check, header=0)
        return None

    # DONE
    # 500 pixels -> 10 cm; 50 pixels-> 1cm
    def cal_max_displacement(self):
        onset = self.df_hb.loc[self.df_hb["frame"] == self.hbr]
        onset_x, onset_y = float(onset["x"]), float(onset["y"])
        maximum = self.df_hb.loc[self.df_hb["frame"] == self.hbm]
        maximum_x, maximum_y = float(maximum["x"]), float(maximum["y"])
        return math.sqrt((onset_x - maximum_x) ** 2 + (onset_y - maximum_y) ** 2) / 50

    # DONE
    def cal_relative_loc(self, timestamp="hbr"):
        if self.df_mandible is None:
            return None
        if timestamp == "hbr":
            loc = self.df_hb.loc[self.df_hb["frame"] == self.hbr]
            ref_loc = self.df_mandible.loc[self.df_mandible["frame"] == self.hbr]
        elif timestamp == "hbm":
            loc = self.df_hb.loc[self.df_hb["frame"] == self.hbm]
            ref_loc = self.df_mandible.loc[self.df_mandible["frame"] == self.hbm]
        x, y = float(loc["x"]), float(loc["y"])
        ref_x, ref_y = float(ref_loc["x"]), float(ref_loc["y"])
        return math.sqrt((x - ref_x) ** 2 + (y - ref_y) ** 2) / 50

    # DONE
    def cal_delta_percentage(self, axis="x"):  # in x or y axis
        if self.df_mandible is None:
            return None
        loc_hbr = self.df_hb.loc[self.df_hb["frame"] == self.hbr]
        x_hbr, y_hbr = float(loc_hbr["x"]), float(loc_hbr["y"])
        loc_hbm = self.df_hb.loc[self.df_hb["frame"] == self.hbm]
        x_hbm, y_hbm = float(loc_hbm["x"]), float(loc_hbm["y"])
        loc_ref_hbr = self.df_mandible.loc[self.df_mandible["frame"] == self.hbr]
        x_hbr_ref, y_hbr_ref = float(loc_ref_hbr["x"]), float(loc_ref_hbr["y"])
        loc_ref_hbm = self.df_mandible.loc[self.df_mandible["frame"] == self.hbm]
        x_hbm_ref, y_hbm_ref = float(loc_ref_hbm["x"]), float(loc_ref_hbm["y"])
        if axis == "x":
            hbr_relative, hbm_relative = x_hbr - x_hbr_ref, x_hbm - x_hbm_ref
        elif axis == "y":
            hbr_relative, hbm_relative = y_hbr_ref - y_hbr, y_hbm_ref - y_hbm
        return (hbr_relative - hbm_relative) / hbr_relative

    # DONE
    # theta(HBM - M) - theta(M - HBR)
    def cal_angle_in_degree(self):
        if self.df_mandible is None:
            return None
        loc_hbr = self.df_hb.loc[self.df_hb["frame"] == self.hbr]
        x_hbr, y_hbr = float(loc_hbr["x"]), float(loc_hbr["y"])
        loc_hbm = self.df_hb.loc[self.df_hb["frame"] == self.hbm]
        x_hbm, y_hbm = float(loc_hbm["x"]), float(loc_hbm["y"])
        loc_ref_hbr = self.df_mandible.loc[self.df_mandible["frame"] == self.hbr]
        x_hbr_ref, y_hbr_ref = float(loc_ref_hbr["x"]), float(loc_ref_hbr["y"])
        loc_ref_hbm = self.df_mandible.loc[self.df_mandible["frame"] == self.hbm]
        x_hbm_ref, y_hbm_ref = float(loc_ref_hbm["x"]), float(loc_ref_hbm["y"])
        theta1 = math.atan((y_hbm_ref - y_hbm) / (x_hbm - x_hbm_ref)) * 180 / math.pi
        theta2 = math.atan((y_hbr_ref - y_hbr) / (x_hbr - x_hbr_ref)) * 180 / math.pi
        return theta1 - theta2


if __name__ == "__main__":

    folder = "HB_Anno_E/"
    excel_name = "info_summary/E.xlsx"
    data_list = "info_summary/HB_list_E.txt"

    r = util_read_excel.r_excel(folder, excel_name)
    df = r.df_excel

    clip_names = []
    with open(data_list) as file:
        clip_names = file.readlines()
        clip_names = [clip.rstrip() for clip in clip_names]

    clip = []
    max_displacement = []
    relative_loc_hbr = []
    relative_loc_hbm = []
    percentage_x = []
    percentage_y = []
    theta_in_degree = []

    for clip_name in clip_names:
        l = loc(folder, df, clip_name)

        clip.append(clip_name)
        max_displacement.append(l.cal_max_displacement())
        relative_loc_hbr.append(l.cal_relative_loc())
        relative_loc_hbm.append(l.cal_relative_loc(timestamp="hbm"))
        percentage_x.append(l.cal_delta_percentage())
        percentage_y.append(l.cal_delta_percentage(axis="y"))
        theta_in_degree.append(l.cal_angle_in_degree())

    df_loc = pd.DataFrame(
        list(
            zip(
                clip,
                max_displacement,
                relative_loc_hbr,
                relative_loc_hbm,
                percentage_x,
                percentage_y,
                theta_in_degree,
            )
        ),
        columns=[
            "clip",
            "max_displacement_in_cm",
            "relative_loc_hbr_in_cm",
            "relative_loc_hbm_in_cm",
            "percentage_x",
            "percentage_y",
            "theta_in_degree",
        ],
    )
    df_loc.to_csv("measurements.csv", index=False)

