
# encoding:utf-8
'''
# 将同一个image的labels（traffic、object）合并到一个json文件
# 遍历文件夹中所有json中的imagename
# 前提是两个文件夹的文件是包含关系
2020.4.27
'''

import os
import shutil
import json

cur_dir = 'D:\工作\object_detection_dataset\\'


# labels
traffic_dir = os.path.join(cur_dir, 'anno_out-1')  # traffic #写入文件夹，将另一个文件夹的标注信息写到这个里面
object_dir = os.path.join(cur_dir, 'repeat')  # object #输出文件夹
#repeat_dir = os.path.join(cur_dir, 'repeat')
out_patth = os.path.join(cur_dir,'anno_out-2')

filelist_t = os.listdir(traffic_dir)#该文件夹下所有的文件（包括文件夹）
filelist_o = os.listdir(object_dir)#该文件夹下所有的文件（包括文件夹）

#print(filelist_t)
for file_t in filelist_t:  # 遍历所有文件

    out_json = open(os.path.join(out_patth,file_t),'w') # 新json文件输出路径

    filedir_t = os.path.join(traffic_dir, file_t)  # traffic的文件路径
    #print(filedir)

    t_json = open(filedir_t ,        encoding='GBK') #遇到报错，将“utf-8”改为“GBK”
    data_t = json.load(t_json) #data_t是个列表

    image_t = []
    print(len(data_t))



    for i in range(len(data_t)):
    #for t in data_t:#image_t 图片id #t是个字典
        label_t = data_t[i]['labels'] #label_t是第i个图片里的labels组成的列表
        #print(type(label_t))

        image_t.append(data_t[i]) #图片的数量
        #print(label_t)
        #x = len(label_t)
        name_t = data_t[i]['name']

        for file_o in filelist_o:
            filedir_o = os.path.join(object_dir, file_o)  # object的文件路径
            o_json = open(filedir_o,
                          encoding='utf-8')
            data_o = json.load(o_json)
            image_o = []

            for o in data_o:  # image_t 图片id
                label_o = o['labels']
                print(type(label_o))
                image_o.append(o)  # 图片的数量

                name_o = o['name']

                #print(label_o)

                if name_o == name_t :
                    if label_o:         ##防止label类型为nonetype报错
                        if label_t:
                            data_t[i]['labels'] = label_t + label_o
                        else:
                            data_t[i]['labels'] = label_o
                    elif label_t:

                        data_t[i]['labels'] = label_t
                    else:
                        data_t[i]['labels'] = data_t[i]['labels']









                else:
                    continue
            o_json.close()

    #out_json.write(json.dumps(data_t,indent=2))
    out_json.write(json.dumps(data_t, ensure_ascii=False, indent=2)) #带缩进的json格式，防止中文变ASCII码
    t_json.close()
    out_json.close()







