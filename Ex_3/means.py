import numpy as np


def kmeans(x,k,maxIt):
    numPoints,numDim = x.shape
    dataset = np.zeros((numPoints,numDim+1))  # 多加一列存储类别
    dataset[:,:-1] = x
    centroids = dataset[np.random.randint(numPoints,size=k)]     # 随机选取k个中心点
    centroids[:,-1] = range(1,k+1)
    iteration = 0
    oldCentroids = None
    while not shouldStop(oldCentroids,centroids,iteration,maxIt):
        oldCentroids=np.copy(centroids)
        iteration +=1
        updataLable(dataset,centroids)    # 重新分类
        centroids = getCentriods(dataset,k)  # 得到新的中心点
    return dataset


def shouldStop (oldCentroids,centroids,iteration,maxIt):    # 满足了两个结束条件
    if iteration>maxIt:
        return True
    return np.array_equal(oldCentroids,centroids)      # !!!!!!!!!!!比较两个array是否相等

def updataLable(dataset,centroids):
    numPoints,numDim = dataset.shape
    for i in range(0,numPoints):
        dataset[i,-1] = getLableFromClosestCentriod(dataset[i,:-1],centroids)

def getLableFromClosestCentriod(dataSetRow,centroids):
    lable = centroids[0,-1]
    minDist = np.linalg.norm(dataSetRow-centroids[0,:-1])  # 求范数，跟求欧氏距离一个道理
    for i in range(1,centroids.shape[0]):
        dist = np.linalg.norm(dataSetRow-centroids[i,:-1])
        if dist<minDist :
            minDist = dist
            lable = centroids[i,-1]
    return lable


def getCentriods(dataset,k):
    result = np.zeros((k,dataset.shape[1]))
    for i in range(1,k+1):
        oneCluster = dataset[dataset[:,-1]==i,:-1]      # 取出最后一列等于指定值的样本行
        result[i-1,:-1] = np.mean(oneCluster,axis=0)    # 对传入矩阵，求列的平均值，即可以求到该簇的中心向量
        result[i-1,-1] = i
    return result

x1 = np.array([1,2])
x2 = np.array([2,1])
x3 = np.array([4,3])
x4 = np.array([5,4])
x = np.vstack((x1,x2,x3,x4))
print(x)
result = kmeans(x,2,10)
print("result",result)