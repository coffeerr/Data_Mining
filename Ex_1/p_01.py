
def loadDataset():
    return [[1,3,4],[2,3,5],[1,2,3,5],[2,5]]
#将项集里的单个项集组成map
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()
    return map(frozenset,C1)
def scanD(D, Ck, minSupport):
    ssCnt = {}
    # 以下这一部分统计每一个单元素出现的次数
    # 遍历全体样本中的每一个元素
    for tid in D:
        # 遍历单元素列表中的每一个元素
        for can in Ck:
            # s.issubset( x ) 判断集合s是否是集合x子集
            if can.issubset(tid):
                if not can in ssCnt:
                    ssCnt[can] = 1
                else:
                    ssCnt[can] += 1
    # 获取样本中的元素个数
    numItems = float(len(D))
    retList = []
    supportData = {}
    # 遍历每一个单元素
    for key in ssCnt:
        # 计算每一个单元素的支持率
        support = ssCnt[key] / numItems
        # 若支持率大于最小支持率
        if support >= minSupport:
            # insert() 函数用于将指定对象插入列表的指定位置。
            retList.insert(0, key)
        supportData[key] = support
    return retList, supportData

if __name__ == '__main__':
    dataset = loadDataset()
    C1 = createC1(dataset)
    D = list(map(set,dataset))
    for i in C1:
        print(i)
    L1,supportData0 = scanD(D,C1,0.5)
    print(L1)