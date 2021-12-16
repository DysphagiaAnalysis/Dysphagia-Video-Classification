import pandas as pd


class r_excel:
    def __init__(self, excel_name):
        self.excel_file = excel_name
        self.df_excel = self.excel2df()

    def excel2df(self):
        cols = pd.read_excel(self.excel_file, header=None).iloc[0].to_numpy()
        df = pd.read_excel(self.excel_file, header=None)
        df.columns = cols
        return df


class clip_info:
    def __init__(self, df_excel, clip_name):
        self.clip_file = clip_name
        self.df_clip = df_excel[df_excel["Video Name"].str.lower() == clip_name]
        self.zero_frame = int(self.df_clip["SS"].iloc[0])
        self.last_frame = int(self.df_clip["SE"].iloc[0])
        # most of final frames are se + 50, and humming start se - 20

    def swallow_info(self):
        swallowing_start = int(self.df_clip["SS"].iloc[0])
        swallowing_end = int(self.df_clip["SE"].iloc[0])
        ss = swallowing_start - self.zero_frame
        se = swallowing_end - self.zero_frame
        return ss, se

    def hyoid_info(self):
        hb_onset = int(self.df_clip["HBR"].iloc[0])
        hb_maximum = int(self.df_clip["HBM"].iloc[0])
        hb_offset = int(self.df_clip["HBOS"].iloc[0])
        hb_on = hb_onset - self.zero_frame
        hb_m = hb_maximum - self.zero_frame
        hb_off = hb_offset - self.zero_frame
        return hb_on, hb_m, hb_off

    def gh_info(self):
        gh_onset = int(self.df_clip["GHR"].iloc[0])
        gh_maximum = int(self.df_clip["GHM"].iloc[0])
        gh_offset = int(self.df_clip["GHRE"].iloc[0])
        gh_on = gh_onset - self.zero_frame
        gh_m = gh_maximum - self.zero_frame
        gh_off = gh_offset - self.zero_frame
        return gh_on, gh_m, gh_off


if __name__ == "__main__":
    excel_name = "A.xlsx"
    r = r_excel(excel_name)
    df = r.df_excel

    clip_name = "a01_5ml-l0-5"
    c1 = clip_info(df, clip_name)
    print(c1.swallow_info())
    print(c1.hyoid_info())
    print(c1.gh_info())

