#
'''
# 批量重命名json文件

2020.4.27
'''


import os

path = 'D:\工作\object_detection_dataset\\anno_out-2\\'#文件夹地址

def rename():

    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）
    name = []

    for files in filelist:  # 遍历所有文件

        Olddir = os.path.join(path, files) # 原来的文件路径

        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;

        filename = os.path.splitext(files)[0]  # 文件名
        filetype = os.path.splitext(files)[1]  # 文件扩展名

        name = filename.split('#')
        name[2]= 'A'
        new_name = '#'.join(name)
        Newdir = os.path.join(path, new_name + filetype)

        if not os.path.isfile(Newdir):
             os.rename(Olddir, Newdir)

        print(Newdir)
rename()

nfilelist = os.listdir(path)
print(len(nfilelist))



