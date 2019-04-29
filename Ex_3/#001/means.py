def K_Means(testData, K, Corelist):  # K-Means算法
    num = len(testData)  # 参与聚簇点个数
    L = len(testData[0])
    testData = mat(testData)
    Core = mat(Corelist)
    flag = True  # 簇中心改变否？
    global K_Mean_IterCount
    global K_Mean_IterTime
    start = time.time()
    while (flag):
        K_Mean_IterCount += 1  # 迭代次数+1
        flag = False
        for i in range(num):  # 计算每个点与簇中心的距离
            mD = inf  # 最小距离记录
            mI = -1  # 与第标记为mI的簇中心距离最近
            for j in range(K):  # 计算与每个中心的距离
                tempD = distForm(Core[j, 1:], testData[i, 1:L - 1])
                if (tempD < mD):
                    mD = tempD  # 改变最小距离
                    mI = j + 1  # 改变簇编号
            if (testData[i, 0] != mI):
                flag = True  # 若不等则改变标志量
            testData[i, 0] = mI
            testData[i, L - 1] = pow(mD, 2)

        for k in range(K):  # 计算新的簇中心
            noKPointSet = testData[nonzero(testData[:, 0].A == k + 1)[0], 1:L - 1]
            Core[k, 0] = k + 1
            Core[k, 1:] = mean(noKPointSet, axis=0)
    end = time.time()
    K_Mean_IterTime = end - start
    return Core, [testData[:, 0], testData[:, L - 1]]
