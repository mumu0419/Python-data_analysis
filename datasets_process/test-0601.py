import os
import shutil
import json
import numpy as np
from collections import Counter
import matplotlib.pyplot as plt
from matplotlib.font_manager import FontProperties
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False



cur_dir = 'D:\wsm\datasets\\'

# json file
json_dir = os.path.join(cur_dir, 'self_annotation')  # traffic #写入文件，将另一个文件夹的标注信息写到这个里面
txt_dir = os.path.join(cur_dir, 'txt_out')  # object #输出文件夹
pic_dir = os.path.join(cur_dir, 'pic_save')

json_name = '553_707.json'
txt_name = 'out-3.txt'

json_path = os.path.join(json_dir, json_name)  # 标注文件路径
txt_path = os.path.join(txt_dir,txt_name)

t_json = open(json_path ,  encoding='utf-8') #遇到报错，将“utf-8”改为“GBK”
data_t = json.load(t_json) #data_t是个列表

t_txt = open(txt_path,'w')

annotation = []
area_gan = []
aera_deng = []
aera_biao = []
n = 11

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

        box_info = "%s,%s,%s,%s,%s,%s" % (
            classname,x1,y1,x2,y2,area)
        print(box_info)
        t_txt.write(box_info)

        #t_txt.write(annotation)
        t_txt.write('\n')
t_txt.close()

def new(size):
    newlist = []
    for i in range(0, size):
        newlist.append([])
    return newlist

Area = [area_gan,aera_deng,aera_biao]
print('%d交通标志'%len(aera_biao),'%d杆'%len(area_gan),'%d灯'%len(aera_deng))
print('***************************')
for i in Area:
    if len(i) == len(area_gan):
        name = '杆'
    elif len(i)==len(aera_deng):
        name = '红绿灯'
    else:
        name = '交通标志'
    i = np.rint(i)
    a_mean = int(np.mean(i))
    a_var = np.rint(np.var(i))
    a_std = np.rint(np.std(i))
    a_max = np.rint(np.max(i))
    a_min = np.rint(np.min(i))
    d_value = a_max-a_min
    collection_num = Counter(i)
    most_n = collection_num.most_common(10)

    print(len(i))
    print("平均值为：%f" % a_mean)
    print("方差为：%f" % a_var)
    print("标准差为:%f" % a_std)
    print("最小值是：", a_min)
    print("最大值是：", a_max)
    # print('最多的面积是：',most_n)
    #print(collection_num)
    i.sort()
    i = i.tolist()
    # print(i)

    x =np.rint(np.linspace(a_min,a_max,num=n))
    x = x.tolist()
    print(x)
    a=0
    list_1 =new(n-1)#创建一个包含n-1个空列表的列表
    for j in range(len(i)):
        if i[j] <= x[a+1] :
            list_1[a].append(i[j])
            #print(len(list_1))
        elif i[j] <= x[a+2] :
            list_1[a+1].append(i[j])
            a = a+1
        else:
            a =a+ 2
            list_1[a].append(i[j])




    print(list_1[9])
    print(len(list_1))





    #按个数分段



    print('**************************')

    range_list = []
    num_list = []
    for j in range(len(list_1)):
        # print(len(j))
        # if j ==[]:

        a = '%s—%s'%(x[j],x[j+1])
        b = len(list_1[j])
        range_list.append(a)
        num_list.append(b)
    #
    print(range_list)
    print(num_list)

    xValue = range_list
    yValue = num_list
    titile_name = name
    label = name+'：'+str(len(i))
    pic_name = name+ '-面积等差分段'
    plt.title(titile_name)
    plt.tick_params(axis='x', labelsize=8,rotation=-15)
    plt.bar(xValue,yValue, width=0.5,color="steelblue",label = label)
    plt.xlabel("面积范围")  # 设置X轴Y轴名称
    plt.ylabel("目标个数")
    plt.legend()
    for a,b in zip(range_list,num_list):
        plt.text(a,b+0.5,'%s'%b,ha='center',fontweight='bold')

    pic_path = os.path.join(pic_dir,pic_name)
    plt.savefig(pic_path, dpi=300)
    plt.show()








