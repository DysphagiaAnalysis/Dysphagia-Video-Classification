# unzip the file
import os
import zipfile
import glob

# file_path = "./D07 Annotations/"
data_dir = os.path.join(os.path.abspath(os.getcwd()), "HB_Anno_A", "*", "*.zip")
data_file_names = glob.glob(data_dir)
# for file_name in data_file_names:
for exact_filepath in data_file_names:
    zip_file = zipfile.ZipFile(exact_filepath)  # obtain the zipped file
    file_name = ".".join(exact_filepath.split("/")[-1].split(".")[:-1])
    file_path = "/".join(exact_filepath.split("/")[:-2])
    # newfile_path = file_name.split(".", 1)[0]
    newfile_path = os.path.join(file_path, file_name)
    if os.path.isdir(newfile_path):
        pass
    else:
        os.mkdir(newfile_path)
    for name in zip_file.namelist():
        zip_file.extract(name, newfile_path)
    zip_file.close()
