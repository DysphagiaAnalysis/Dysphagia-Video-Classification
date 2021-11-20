from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import read_excel


class area:
    # TODO
    def __init__(self, df_excel, clip_name):
        self.c = read_excel.clip_info(df, clip_name)
        self.mask_folder_path = "clip_name"  ####
        self.start = self.c.zero_frame
        self.end = self.c.lastframe
        self.T = self.end - self.start + 1
        self.mask_frame_path = np.zeros(self.T)
        self.masks = self.get_masks()  # T*W*H
        self.all_frame_area = self.get_all_frame_area()  # T*1

    # TODO
    def get_masks(self):
        image = Image.open(self.mask_frame_path)
        # image = Image.open(
        #     "data/task_a01_5ml-l0-5-2021_06_04_08_51_29-segmentation mask 1.1/SegmentationObject/frame_000000.png"
        # )
        data = np.asarray(image)
        data_gray = 1 / 3 * (data[:, :, 0] + data[:, :, 1] + data[:, :, 2])

    # DONE 
    def get_all_frame_area(self):
        return np.count_nonzero(np.reshape(self.masks, (self.T, np.product(self.masks.shape))), axis=1)

    # DONE
    def frame_area(self, frame_num):
        return self.all_frame_area[frame_num - self.start]

    # DONE 
    def percentage(self, frame_s, frame_l):
        return (self.all_frame_area[frame_l - self.start] - self.all_frame_area[frame_s - self.start]) / self.all_frame_area[frame_l - self.start]

    # TODO 
    def find_min_or_max_extreme_area(self):
        pass


if __name__ == "__main__":
    excel_name = "A.xlsx"
    r_e = read_excel.r_excel(excel_name)
    df = r_e.df_excel

    clip_name = "a01_5ml-l0-5"
    r_c = read_excel.clip_info(df, clip_name)
    df_clip = r_c.df_clip
    gh_onset = int(df_clip["GHR"].iloc[0])
    gh_maximum = int(df_clip["GHM"].iloc[0])

# max_value = np.max(data)
# summarize some details about the image
# print(image.format)
# print(image.size)
# print(image.mode)
# plt.imshow(data[:, :, 0].astype(np.uint8), cmap=plt.cm.gray)
# plt.show()
# print(type(data))
# print(data.shape)
