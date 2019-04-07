import time
datapath = './4.txt'
resultpath = './result_100K.txt'


def loadDataSet():
    f=open(datapath,'r')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n').strip()
        temp2=temp1.split(' ')
        for i in range(len(temp2)):
            temp2[i] = int(temp2[i])
        dataset.append(temp2)
    return dataset
def createC1(dataSet):
    C1 = []
    for transaction in dataSet:
        for item in transaction:
            if not [item] in C1:
                C1.append([item])
    C1.sort()

    # frozenset() 返回一个冻结的集合，冻结后集合不能再添加或删除任何元素。
    return list(map(frozenset, C1))
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
    if(len(retList)>0):
        with open (resultpath,'a',encoding='utf-8') as f:
            a = '频繁{}项集为：\n'.format(len(retList[0]))
            f.write(a)
            for li in retList:
                f.write(''.join('%s' % li))
                f.write('\n')
        print('频繁{}项集为：'.format(len(retList[0])))
        for li in retList:
            print(li)

    return retList, supportData
def aprioriGen(Lk, k):
    retList = []
    lenLk = len(Lk)
    for i in range(lenLk):
        # 两两组合遍历
        for j in range(i + 1, lenLk):
            L1 = list(Lk[i])[:k - 2]
            L2 = list(Lk[j])[:k - 2]
            L1.sort()
            L2.sort()
            # 若两个组合的前k-2个项相同时，则将这两个集合合并
            if L1 == L2:
                retList.append(Lk[i] | Lk[j])
    return retList
def apriori(dataSet, minSupport=0.5):
    # 创建数据集中所有单一元素组成的集合保存在C1中
    C1 = createC1(dataSet)
    # 将数据集元素转为set集合然后将结果保存为列表
    D = list(map(set, dataSet))
    # 从C1生成L1并返回符合条件的元素，符合条件的元素及其支持率组成的字典
    L1, supportData = scanD(D, C1, 0.01)

    # for i in supportData:
    #     print('{}------{}'.format(i,supportData[i]))


    # 将符合条件的元素转换为列表保存在L中L会包含L1、L2、L3......
    L = [L1]
    k = 2
    # L[n]就代表n+1元素集合,例如L[0]代表1个元素的集合
    # L[0]=[frozenset({5}), frozenset({2}), frozenset({3}), frozenset({1})]
    while (len(L[k - 2]) > 0):
        Ck = aprioriGen(L[k - 2], k)
        Lk, supK = scanD(D, Ck, minSupport)
        # dict.update(dict2) 字典update()函数把字典dict2的键/值对更新到dict里。
        supportData.update(supK)
        L.append(Lk)
        k += 1
        # flag = len(L) - 1
        # print('-'*50)
        # print('频繁{}项集为：\n'.format(flag))
        # for item in L:
        #     for i in item:
        #        print(i)

    return L, supportData
def generateRules(L, supportData, minConf=0.7):
    # 存储所有的关联规则
    bigRuleList = []
    # 只获取两个或更多集合的项目
    # 两个及以上才可能有关联一说，单个元素的项集不存在关联问题
    for i in range(1, len(L)):
        for freqSet in L[i]:
            # 该函数遍历L中的每一个频繁项集并对每个频繁项集创建只包含单个元素集合的列表H1
            H1 = [frozenset([item]) for item in freqSet]
            if (i > 1):
                # 如果频繁项集元素数目超过2，那么会考虑对它做进一步的合并
                rulesFromConseq(freqSet, H1, supportData, bigRuleList, minConf)
            else:
                # 第一层时，i为1
                calcConf(freqSet, H1, supportData, bigRuleList, minConf)
    return bigRuleList
def calcConf(freqSet, H, supportData, br1, minConf=0.5):
    # 返回满足最小可信度要求的项列表
    prunedH = []
    # 遍历L中的某一个（i）频繁项集的每个元素
    for conseq in H:
        # 可信度计算，结合支持度数据
        conf = supportData[freqSet] / supportData[freqSet - conseq]
        if conf >= minConf:
            # 如果某条规则满足最小可信度值，那么将这些规则输出到屏幕显示
            print(freqSet - conseq, '-->', conseq, 'conf:', conf)
            # 添加到规则里，br1是前面通过检查的bigRuleList
            br1.append((freqSet - conseq, conseq, conf))
            # 通过检查的项进行保存
            prunedH.append(conseq)
    return prunedH
def rulesFromConseq(freqSet, H, supportData, br1, minConf=0.7):
    m = len(H[0])
    # 频繁项集元素数目大于单个集合的元素数
    if (len(freqSet) > (m + 1)):
        # 存在不同顺序、元素相同的集合，合并具有相同部分的集合
        Hmp1 = aprioriGen(H, m + 1)
        # 计算可信度
        Hmp1 = calcConf(freqSet, Hmp1, supportData, br1, minConf)
        # 满足最小可信度要求的规则列表多于1，则递归来判断是否可以进一步组合这些规则
        if (len(Hmp1) > 1):
            rulesFromConseq(freqSet, Hmp1, supportData, br1, minConf)

if __name__ == '__main__':
    dataSet = loadDataSet()
    start = time.time()
    L, supportData = apriori(dataSet, 0.01)
    end = time.time()
    with open(resultpath,'a',encoding='utf-8') as f:
        f.write('\n'+'消耗时间：%.4f s'%(end-start))
    print('消耗时间：%.4f s'%(end-start))