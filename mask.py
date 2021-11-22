from re import L
from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
from numpy.core.fromnumeric import clip
import read_excel
import glob
import os


class area:
    # DONE
    def __init__(self, df_excel, clip_name):
        self.c = read_excel.clip_info(df_excel, clip_name)
        # "data/task_a01_5ml-l0-5-2021_06_04_08_51_29-segmentation mask 1.1/SegmentationObject/"
        data_dir = os.path.join(os.path.abspath(os.getcwd()), "E_data", "*")
        data_file_names = glob.glob(data_dir)
        self.clip_name = clip_name
        for i in range(len(data_file_names)):
            if self.clip_name in data_file_names[i]:
                self.mask_folder_path = os.path.join(
                    data_file_names[i], "SegmentationObject", "*"
                )
                break
        self.mask_dir = glob.glob(self.mask_folder_path)  # nonono
        self.mask_dir.sort()
        self.start = self.c.zero_frame
        self.start_index = self.start - int(self.mask_dir[0].split(".")[-2][-3:])
        self.end = self.c.last_frame
        self.T = self.end - self.start + 1
        self.masks = self.get_masks()  # T*W*H
        self.all_frame_area_in_cm2 = self.get_all_frame_area()  # T*1

    # DONE
    def get_masks(self):
        W, H = Image.open(self.mask_dir[0]).size
        masks_gray = np.zeros((self.T, W, H))
        for i in range(self.T):
            image = Image.open(self.mask_dir[self.start_index + i])  # need to change
            data = np.transpose(np.asarray(image), (1, 0, 2))
            data_gray = 1 / 3 * (data[:, :, 0] + data[:, :, 1] + data[:, :, 2])
            masks_gray[i, :, :] = data_gray
        return masks_gray

    # DONE
    def get_all_frame_area(self):
        # 500 pixels -> 10 cm; 2500 pixel^2 -> 1cm^2
        return np.count_nonzero(self.masks.reshape(self.T, -1), axis=1) / 2500

    # DONE
    def frame_area(self, frame_num):
        return self.all_frame_area_in_cm2[frame_num - self.start]

    # DONE
    def percentage(self, frame_s, frame_l):
        return (
            self.all_frame_area_in_cm2[frame_l - self.start]
            - self.all_frame_area_in_cm2[frame_s - self.start]
        ) / self.all_frame_area_in_cm2[frame_l - self.start]

    # DONE
    def find_min_or_max_extreme_area(self, flag):
        if flag == "max":
            return (
                np.max(self.all_frame_area_in_cm2),
                np.argmax(self.all_frame_area_in_cm2) + self.start,
            )
        if flag == "min":
            return (
                np.min(self.all_frame_area_in_cm2),
                np.argmin(self.all_frame_area_in_cm2) + self.start,
            )


if __name__ == "__main__":
    excel_name = "E.xlsx"
    r_e = read_excel.r_excel(excel_name)

    clip_names = []
    with open("GH_E_list.txt") as file:
        clip_names = file.readlines()
        clip_names = [clip.rstrip() for clip in clip_names]

    for i in range(len(clip_names)):

        r_c = read_excel.clip_info(r_e.df_excel, clip_names[i])

        a = area(r_e.df_excel, clip_names[i])
        ghr, ghm = (
            int(r_c.df_clip["GHR"].iloc[0]),
            int(r_c.df_clip["GHM"].iloc[0]),
        )
        ghr_area = a.frame_area(ghr)
        ghm_area = a.frame_area(ghm)
        anno_percentage = a.percentage(ghm, ghr)
        gh_maximum_area_cal, gh_maximum_cal = a.find_min_or_max_extreme_area("max")
        gh_minimum_area_cal, gh_minimum_cal = a.find_min_or_max_extreme_area("min")
        cal_percentage = a.percentage(gh_minimum_cal, gh_maximum_cal)
        print(clip_names[i])
        print("area: anno vs. cal")
        print(ghr_area, ghm_area, anno_percentage)
        print(gh_maximum_area_cal, gh_minimum_area_cal, cal_percentage)
        print("frame number: anno vs. cal")
        print(ghr, ghm, gh_maximum_cal, gh_minimum_cal)

