'''
从json文件输出每个图像的类别到一个txt中
自己采集数据集2019/2020
2020.4.21

'''
import json
import os
from collections import defaultdict

path = 'D:\工作\object_detection_dataset\\test-4221\\' #json文件存放路径
filelist = os.listdir(path)#该文件夹下所有的文件（包括文件夹）
no_label = 0
image_num = 0

for files in filelist:  # 遍历所有文件
    # 新建txt文件，存放json中的信息
    f = open('test_anno.txt', 'a')
    #f.write(files+':'+'定位'+'\n')  #写入json文件名#测试用

    filedir = os.path.join(path, files)  # 原始文件路径

    f_json = open(filedir ,
        encoding='utf-8')
    data = json.load(f_json)
    image_num += len(data)



    for ant in data:
        image_name = ant['name']
        #image_name = image_name.split('/')[-1]
        #f.write(image_name) #写入图片名
        annotation = image_name
        labels = ant['labels']

        if labels:  #判断是否有标注信息
            for num in labels:
                cat = num['category']
                annotation += ','+cat
        else:
            print('没有标注')
            no_label += 1  #统计没内容的label

        print(annotation)
        f.write(annotation)
        f.write('\n')
    f.close()

print('%d个没内容的标注'%no_label)
print(image_num)


