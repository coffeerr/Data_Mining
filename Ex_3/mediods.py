import  numpy as np
from numpy import *

data_list = []  # 列表，用来表示，列表中的每个元素也是一个二维的列表；这个二维列表就是一个样本，样本中包含有我们的属性值和类别号。
# 与我们所熟悉的矩阵类似，最终我们将获得N*2的矩阵，
fileIn = open("./data.txt")  # 是正斜杠
for line in fileIn.readlines():
    temp = []
    lineArr = line.strip().split()  # line.strip()把末尾的'\n'去掉
    temp.append(float(lineArr[0]))
    temp.append(float(lineArr[1]))
    data_list.append(temp)
    # dataSet.append([float(lineArr[0]), float(lineArr[1])])#上面的三条语句可以有这条语句代替
fileIn.close()


def choice_center(data, k):
    centers = []
    for i in np.random.choice(len(data), k):
        centers.append(data[i])
    print("随机选取的中心点(第一次):\n", centers)
    return centers


def distance(a, b):
    dis = []
    for i in range(len(a)):
        dis.append(pow(a[i] - b[i], 2))
#    print(sqrt(sum(dis)))
    return sqrt(sum(dis))


def k_center(data_list,center):
    flag = True
    i = 0
    while flag:
        flag = False
        for i in range(len(data_list)):                       # 遍历所有样本，最后一列标记该样本所属簇
            min_index = -2
            min_dis = inf
            for j in range(len(center)):
                dis = distance(data_list[i][1:3],center[j][1:3])
                if dis < min_dis:
                    min_dis = dis
                    min_index = j
            if data_list[i][-1] != min_index:
                flag = True
            data_list[i][-1] = min_index
        print("分类结果111：",data_list)
        # 重新计算簇中心
        for k in range(len(center)):                      # 遍历中心向量，取出属于当前中心向量簇的样本
            current_k = []
            for i in range(len(data_list)):
                if data_list[i][-1] == k:
                    current_k.append(data_list[i])
#            print(k, "：", current_k)
            old_dis = 0.0
            for i in range(len(current_k)):
                old_dis += distance(current_k[i][1:3], center[k][1:3])
            for m in range(len(current_k)):
                new_dis = 0.0
                for n in range(len(current_k)):
                    new_dis += distance(current_k[m][1:3], current_k[n][1:3])
                if new_dis < old_dis:
                    old_dis = new_dis
                    center[k][:] = current_k[m][:]
                    # flag = True
        # print("新中心点", center)
        # i +=1
        # print("循环次数：
    print("选中的最终中心点", center)
    for i in range(len(data_list)):  # 遍历所有样本，最后一列标记该样本所属簇
        min_index = -2
        min_dis = inf
        for j in range(len(center)):
            dis = distance(data_list[i][1:3], center[j][1:3])
            if dis < min_dis:
                min_dis = dis
                min_index = j
        data_list[i][-1] = min_index
    print("分类结果222：", data_list)



centers = choice_center(data_list,3)
k_center(data_list,centers)