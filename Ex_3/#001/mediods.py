import  numpy as np
from numpy import *
import time

def K_Center(testData, K, Corelist):  # K-中心算法
    num = len(testData)  # 参与聚簇点个数
    L = len(testData[0])
    testData = mat(testData)
    Core = mat(Corelist)
    flag = True  # 簇中心改变否？
    global K_Center_IterCount
    global K_Center_IterTime
    start = time.time()
    while (flag):
        K_Center_IterCount += 1  # 迭代次数+1
        flag = False
        for i in range(num):  # 计算每个点与簇中心的距离
            mD = inf  # 最小距离记录
            mI = -1  # 与第标记为mI的簇中心距离最近
            for j in range(K):  # 计算与每个中心的距离
                tempD = distForm(Core[j, 1:], testData[i, 1:L - 1])
                if (tempD < mD):
                    mD = tempD
                    mI = j + 1
            if (testData[i, 0] != mI):
                flag = True  # 若不等则改变标志量
            testData[i, 0] = mI
            testData[i, L - 1] = pow(mD, 2)

        for k in range(K):  # 计算新的簇中心
            idxset = nonzero(testData[:, 0].A == k + 1)[0].tolist()  # 该簇的所有点的下标
            noKPointSet = testData[idxset, :]  # 该簇的所有点
            idxset.remove(int(Core[k, 0]))  # 除去中心点的所有点的下标
            dist1 = sum(noKPointSet[:, L - 1])  # 之前所有点到中心点的距离之和
            dist2 = dist1 + 1
            tempcoreid = Core[k, 0]
            while (idxset and dist2 - dist1 > 0):  # 若所有点到新的中心点的距离小于之前的则视为改变
                dist2 = 0
                tempcoreid = random.sample(idxset, 1)[0]  # 随机生成下一个中心点
                for i in range(len(idxset)):  # 计算其他所有点到簇中心的距离
                    dist2 = dist2 + distForm(testData[idxset[i], 1:L - 1], testData[tempcoreid, 1:L - 1])
                dist2 = dist2 + pow(distForm(Core[k, 1:], testData[tempcoreid, 1:L - 1]), 2)
                idxset.remove(tempcoreid)
            if (not idxset):
                continue
            # print(nonzero(testData[:, 0].A == k + 1)[0])
            # print(Core[k,0])
            Core[k, 1:] = testData[tempcoreid, 1:L - 1]
            Core[k, 0] = tempcoreid

        end = time.time()
        K_Center_IterTime = end - start
    return Core, [testData[:, 0], testData[:, L - 1]]
