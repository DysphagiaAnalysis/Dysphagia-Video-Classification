import os
from xml.etree import ElementTree
import numpy as np
import glob
import pandas as pd


data_dir = os.path.join(
    os.path.abspath(os.getcwd()), "HB_Anno_A", "*", "annotations.xml",
)
data_file_names = glob.glob(data_dir)
# for file_name in data_file_names:
for file_name in data_file_names:
    mytree = ElementTree.parse(file_name)
    myroot = mytree.getroot()
    file_path = "/".join(file_name.split("/")[:-1])
    newfile_path = os.path.join(file_path, file_name)
    for child in myroot:
        if child.tag == "track":
            structure = child.attrib["label"]
            newfile_path = os.path.join(file_path, structure + ".csv")
            frames = []
            xs = []
            ys = []
            for i in child:
                frames.append(int(i.attrib["frame"]))
                x, y = i.attrib["points"].split(",")
                xs.append(float(x))
                ys.append(float(y))
            df = pd.DataFrame(list(zip(frames, xs, ys)), columns=["frame", "x", "y"],)
            # print(df)
            df.to_csv(newfile_path, index=False)
