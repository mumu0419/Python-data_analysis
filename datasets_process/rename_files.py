#
'''
# 批量重命名coco2014的image文件名

'''

import os

path = 'D:\工作\COCO2014\COCOimages\JPEGImages\\'#文件夹地址

def rename():

    filelist=os.listdir(path)#该文件夹下所有的文件（包括文件夹）

    for files in filelist:  # 遍历所有文件

        Olddir = os.path.join(path, files) # 原来的文件路径

        if os.path.isdir(Olddir):  # 如果是文件夹则跳过
            continue;

        filename = os.path.splitext(files)[0]  # 文件名
        filetype = os.path.splitext(files)[1]  # 文件扩展名

        if filename.find('2014_') >= 0:  # 如果文件名中含有2014_
            Newdir = os.path.join(path, filename.split('2014_')[1] + filetype)

        if not os.path.isfile(Newdir):
             os.rename(Olddir, Newdir)

        print(Newdir)
rename()

nfilelist = os.listdir(path)
print(len(nfilelist))



