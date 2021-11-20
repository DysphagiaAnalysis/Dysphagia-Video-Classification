import pandas as pd


class r_excel:
    def __init__(self, excel_name):
        self.excel_file = excel_name
        self.df_excel = self.excel2df()

    def excel2df(self):
        cols = pd.read_excel(self.excel_file).iloc[0].to_numpy()
        df = pd.read_excel(self.excel_file, header=None, skiprows=2)
        df.columns = cols
        return df


class clip_info:
    def __init__(self, df_excel, clip_name):
        self.clip_file = clip_name
        self.df_clip = df_excel[df_excel["Video Name"].str.lower() == clip_name]
        self.zero_frame = int(self.df_clip["SS"].iloc[0])

    def swallow_info(self):
        swallowing_start = int(self.df_clip["SS"].iloc[0])
        swallowing_end = int(self.df_clip["SE"].iloc[0])
        ss = swallowing_start - self.zero_frame + 1
        se = swallowing_end - self.zero_frame + 1
        # most of final frames are se + 50
        return ss, se

    def hyoid_info(self):
        h_onset = int(self.df_clip["HBR"].iloc[0][0])
        h_maximum = int(self.df_clip["HBM"].iloc[0][0])
        h_offset = int(self.df_clip["HBOS"].iloc[0][0])
        h_on = h_onset - self.zero_frame + 1
        h_m = h_maximum - self.zero_frame + 1
        h_off = h_offset - self.zero_frame + 1
        return h_on, h_m, h_off


if __name__ == "__main__":
    excel_name = "A.xlsx"
    r = r_excel(excel_name)
    df = r.df_excel

    clip_name = "a01_5ml-l0-5"
    c1 = clip_info(df, clip_name)
    print(c1.swallow_info())
    print(c1.hyoid_info())

