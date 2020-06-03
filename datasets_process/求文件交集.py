# remove_no_label_image.py
# encoding:utf-8
# 获取标注文件和图片相交的部分(保证每个图片都有标注，每个标注都有图片）

import os
import shutil

cur_dir = 'D:\工作\object_detection_dataset\\'

# labels
traffic_dir = os.path.join(cur_dir, 'traffic_annotation')  # traffic
object_dir = os.path.join(cur_dir, 'object_annotation')  # object
repeat_dir = os.path.join(cur_dir, 'repeat')

tfile_dic = {}#文件代号为键，文件名为值
pfile_dic = {}

traffic_list = []#用于对比的文件代号列表
object_list = []
repeat_list = []#重复的文件代号列表
diff_list = []

pfile_list = []#文件名列表，带拓展名
tfile_list = []

for parent, dirnames, filenames in os.walk(traffic_dir):
    for txt_name in filenames:
        t_name = txt_name.split('#')[0]
        tfile_dic[t_name] = txt_name
        tfile_list.append(txt_name)
        traffic_list.append(t_name)

for parent, dirnames, filenames in os.walk(object_dir):
    for pic_name in filenames:
        p_name = pic_name.split('#')[0]  #
        pfile_dic[p_name] = pic_name
        pfile_list.append(pic_name)
        object_list.append(p_name)

diff_list = tfile_dic.keys() ^ pfile_dic.keys()
print(diff_list)

for i in object_list:
    if object_list.count(i)>1:
        repeat_list.append(i)

for i in repeat_list:
    name = pfile_dic[i]
    full_path = os.path.join(object_dir,name)
    despath = os.path.join(repeat_dir,name)
    if os.path.exists(full_path):
        shutil.move(full_path,despath)
    else:
        continue
    #print(pfile_dic[i])
# x = set(object_list)
# y = set(traffic_list)
# print(len(y-x))

# for i in traffic_list:
#     if traffic_list.count(i)>1:
#         repeat_list.append(i)

#print(repeat_list)
print(len(repeat_list))



#print(diff_list)
#print(len(diff_list))
#print(pfile_list)
#print(tfile_list)
#
#print(traffic_list)

# traffic_set = set(traffic_list)
# object_set = set(object_list)
# # comp=txt_set.difference(pic_set) # 求补集
# # comp = pic_set.symmetric_difference(txt_set)  # 求对称差分，下一步得到txt和pic交集
# comp = traffic_set.symmetric_difference(object_set)  # 求对称差分，下一步得到txt和pic交集
# insect = traffic_set.intersection(object_set)
#
# print("ok")
# print(len(comp))  # 无标注图片数量#改为，不重复的标注或图片数量
# print(len(insect))
#print(object_list)
# 删除那些不与图片重合的标注
# for item in comp:
#     file=txt_dir+'\\'+item+'.txt'
#     if os.path.exists(file):
#         os.remove(file)
#         print(file)


# 删除那些不与标注重合的图片
# for item in insect:
#
#     file_p = object_dir + '\\' + item + '.json'
#     if os.path.exists(file_p):
#         os.remove(file_p)
#         print(file_p)

# for item in comp:
#     file_t=txt_dir+'/'+item+'.txt'
#     if os.path.exists(file_t):
#         os.remove(file_t)
#         print(file_t)
