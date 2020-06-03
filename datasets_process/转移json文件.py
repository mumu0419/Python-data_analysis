'''
获取traffic_annotation和object_annotation
不相交的json文件——移动到different
相交但object_annotation中名字代码重复json文件——移动到repeat
2020.4.23
'''
# encoding:utf-8

import os
import shutil

cur_dir = 'D:\工作\object_detection_dataset\\'

# labels
traffic_dir = os.path.join(cur_dir, 'traffic_annotation')  # traffic
object_dir = os.path.join(cur_dir, 'object_annotation')  # object
repeat_dir = os.path.join(cur_dir, 'repeat')
dif_dir = os.path.join(cur_dir, 'different')

tfile_dic = {}#文件代号为键，文件名为值
pfile_dic = {}

traffic_list = []#用于对比的文件代号列表
object_list = []
repeat_list = []#重复的文件代号列表

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

# 转移重复的文件
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

#转移不相交的部分
for i in diff_list:
    name = pfile_dic[i]
    full_path = os.path.join(object_dir, name)
    despath = os.path.join(dif_dir, name)
    if os.path.exists(full_path):
        shutil.move(full_path, despath)
    else:
        continue

print(len(repeat_list))



