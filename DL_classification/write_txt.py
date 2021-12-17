import os
from util_read_excel import clip_info, r_excel

root = 'E:/PhD/Lectures/SSP/Project/DATA1208/'

##
f1 = open('../GH_list_A.txt', 'r')
line = f1.readlines()
GH_list_A = [i.split('\n')[0] for i in line]
f1.close()

f2 = open('../GH_list_D.txt','r')
line = f2.readlines()
GH_list_D = [i.split('\n')[0] for i in line]
f2.close()

f3 = open('../GH_list_E.txt','r')
line = f3.readlines()
GH_list_B_elderly = [i.split('\n')[0] for i in line]
f3.close()


f = open('filename.txt', 'w')
f.truncate(0) # clear original data

for i in os.listdir(root):
    sub_path = root + i

    if i == 'GH_Anno_A':
        # sub_path = root + i   # 'E:/PhD/Lectures/SSP/Project/DATA1208/GH_Anno_A'
        for j in os.listdir(sub_path):
            sub_sub_path = sub_path + '/' + j
            root_1 = 'E:/PhD/Lectures/SSP/Project/'
            excel_name = "A.xlsx"
            r = r_excel(root_1, excel_name)
            df = r.df_excel  # obtain the information of SS ad SE

            for k in os.listdir(sub_sub_path):

                name = k.split('-2021')[0]
                file_name = name.split('task_')[1]
                id = file_name.split('_')[0]

                c1 = clip_info(df, file_name)
                ss, se = c1.swallow_info()
                num_eff_frame = se - ss + 1

                sub_sub_sub_path = sub_sub_path + '/' + k + '/SegmentationObject'  # SegmentationObject
                # JPEGImages
                write_content = sub_sub_sub_path + '--' + str(ss) + '--' + str(se) + '--' + str(num_eff_frame) + '--' + id
                f.writelines(write_content + '\n')

    if i == 'GH_Anno_B_Elderly':
        # sub_path = root + i   # 'E:/PhD/Lectures/SSP/Project/DATA1208/GH_Anno_B_Elderly'
        for j in os.listdir(sub_path):

            sub_sub_path = sub_path + '/' + j
            root_1 = 'E:/PhD/Lectures/SSP/Project/'
            excel_name = "E.xlsx"
            r = r_excel(root_1, excel_name)
            df = r.df_excel  # obtain the information of SS ad SE

            for k in os.listdir(sub_sub_path):

                name = k.split('-2021')[0]
                file_name = name.split('task_')[1]
                id = file_name.split('_')[0]
                # print(file_name)

                c1 = clip_info(df, file_name)
                print(file_name)
                ss, se = c1.swallow_info()
                num_eff_frame = se - ss + 1

                sub_sub_sub_path = sub_sub_path + '/' + k + '/SegmentationObject'  # SegmentationObject
                # JPEGImages
                write_content = sub_sub_sub_path + '--' + str(ss) + '--' + str(se) + '--' + str(num_eff_frame) + '--' + id
                f.writelines(write_content + '\n')

    if i == 'GH_Anno_D':
        # sub_path = root + i   # 'E:/PhD/Lectures/SSP/Project/DATA1208/GH_Anno_D'
        for j in os.listdir(sub_path):
            sub_sub_path = sub_path + '/' + j
            root_1 = 'E:/PhD/Lectures/SSP/Project/'
            excel_name = "D.xlsx"
            r = r_excel(root_1, excel_name)
            df2 = r.df_excel  # obtain the information of SS ad SE

            for k in os.listdir(sub_sub_path):

                name = k.split('-2021')[0]
                file_name = name.split('task_')[1]
                id = file_name.split('_')[0]

                c1 = clip_info(df2, file_name)
                ss, se = c1.swallow_info()
                num_eff_frame = se - ss + 1

                sub_sub_sub_path = sub_sub_path + '/' + k + '/SegmentationObject'  # SegmentationObject  # JPEGImages
                write_content = sub_sub_sub_path + '--' + str(ss) + '--' + str(se) + '--' + str(num_eff_frame) + '--' + id
                f.writelines(write_content + '\n')



f.close()

