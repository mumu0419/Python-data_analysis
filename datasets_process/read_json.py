import os
import shutil
import json
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt

# 图片可用中文标题
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

cur_dir = 'D:\wsm\datasets\\'
json_dir = os.path.join(cur_dir, 'self_annotation')
txt_dir = os.path.join(cur_dir, 'txt_out')

json_name = '553_707.json'
txt_name = 'out-3.txt'

json_path = os.path.join(json_dir, json_name)  # 标注文件路径
txt_path = os.path.join(txt_dir,txt_name)

t_json = open(json_path ,  encoding='utf-8')
data_t = json.load(t_json)

t_txt = open(txt_path,'w')

annotation = []
area_gan = []
aera_deng = []
aera_biao = []
n = 10

'''
## 边框信息获取及输出
'''
for i in range(len(data_t)):
    label_t = data_t[i]['labels']  # label_t是第i个图片里的labels组成的列表

    for i in range(len(label_t)):

        classname = label_t[i]['category']
        x1 = label_t[i]['box2d']['x1']
        y1 = label_t[i]['box2d']['y1']
        x2 = label_t[i]['box2d']['x2']
        y2 = label_t[i]['box2d']['y2']
        area = (x2 - x1) * (y2 - y1)
        if classname == '杆':
            classname = classname
            area_gan.append(area)
        elif classname == '红绿灯':
            classname = classname
            aera_deng.append(area)
        else:
            classname = '交通标志'
            aera_biao.append(area)
        print(area)

        box_info = "%s,%s,%s,%s,%s,%s" % (classname,x1,y1,x2,y2,area)
        print(box_info)
        t_txt.write(box_info)
        t_txt.write('\n')
t_txt.close()

'''
## 面积统计及画图
'''
Area = [area_gan,aera_deng,aera_biao]
print('%d交通标志'%len(aera_biao),'%d杆'%len(area_gan),'%d灯'%len(aera_deng))
print('***************************')
for area in Area:
    if len(area) == len(area_gan):
        name = '杆'
    elif len(area)==len(aera_deng):
        name = '红绿灯'
    else:
        name = '交通标志'
    ## 对所有面积及统计值取整
    area = np.rint(area)
    a_mean = int(np.mean(area))
    a_var = np.rint(np.var(area))
    a_std = np.rint(np.std(area))
    a_max = np.rint(np.max(area))
    a_min = np.rint(np.min(area))
    d_value = a_max-a_min
    collection_num = Counter(area)
    most_n = collection_num.most_common(10)
    print(len(area))
    print("平均值为：%f" % a_mean)
    print("方差为：%f" % a_var)
    print("标准差为:%f" % a_std)
    print("最小值是：", a_min)
    print("最大值是：", a_max)
    print('最多的面积是：',most_n)
    #print(collection_num)

    '''
    ## 按个数分段
    '''
    area.sort()
    x = np.array_split(area, 10)
    # print(x[0])
    for j in range(len(x)):  #x是list，但x[j]是ndarray
        x[j] = x[j].tolist() #把ndarray转换成list
    # print(x)
    for j in range(len(x)):
        if j == len(x)-1:
            continue
        else:
            r = 0
            for z in x[j+1]:
                if z in x[j]:
                    r+=1
            # print(r)
            list_z = x[j+1][:r]
            # print(list_z)
            x[j].extend(list_z)
            del x[j+1][:r]
    # print(x[0])
    # print(x[1])
    range_list = []
    num_list = []
    for j in range(len(x)):
        a = '%s—%s'%(x[j][0],x[j][-1])
        b = len(x[j])
        range_list.append(a)
        num_list.append(b)
    print(range_list)
    print(num_list)
    print('***********************************************************************')

    '''
    画图
    '''
    xValue = range_list
    yValue = num_list
    titile_name = name+ '：' + str(len(area))
    label = name + '：' + str(len(area))
    pic_name = name + '-按数量分段'
    plt.title(titile_name)
    plt.tick_params(axis='x', labelsize=8,rotation=-15)
    plt.bar(xValue,yValue, width=0.5,color="steelblue",label = label)
    plt.xlabel("面积范围")  # 设置X轴Y轴名称
    plt.ylabel("目标个数")
    for a,b in zip(range_list,num_list):  # 柱状图柱子上标出面积的个数
        plt.text(a,b+0.5,'%s'%b,ha='center',fontweight='bold')
    pic_path = os.path.join(txt_dir,pic_name)
    # plt.tight_layout()
    plt.savefig(pic_path, dpi=300)
    plt.show()





