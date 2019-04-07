from itertools import combinations

# data = [['I1', 'I2', 'I5'], ['I2', 'I4'], ['I2', 'I3'], ['I1', 'I2', 'I4'], ['I1', 'I3'],
#         ['I2', 'I3'], ['I1', 'I3'], ['I1', 'I2', 'I3', 'I5'], ['I1', 'I2', 'I3']]

def loadDataSet():
    f=open('./1.txt','r')
    sourceInLine=f.readlines()
    dataset=[]
    for line in sourceInLine:
        temp1=line.strip('\n').strip()
        temp2=temp1.split(' ')
        # for i in range(len(temp2)):
        #     temp2[i] = int(temp2[i])
        dataset.append(temp2)
    return dataset
data = loadDataSet()
# 候选集生成
# 输入：
# f_set: k-1项集, k:项集个数
# 输出：
# k_cand：k项候选集
def apriori_gen(f_set, k):
    k_cand = []
    temp = [frozenset(l) for l in combinations(f_set, k)]
    for t in temp:
        if has_infrequent_subset(t, f_set):
            del t
        else:
            k_cand.append(t)
    return k_cand

# 非频繁项集的超集也是非频繁的
def has_infrequent_subset(c_set, f_set):
    for subset in c_set:
        if not frozenset([subset]).issubset(f_set):
            return True
    return False

# 输入（绝对）最小支持度, min_sup
# 输出：全部频繁项集（不包括一项集）, all_f_set
def get_f_set(min_sup=500):
    all_f_set = []
    L1 = frozenset([d for ds in data for d in ds])
    k = 2
    size = len(L1)
    while k <= size:
        c_k = frozenset(apriori_gen(L1, k))
        for c in c_k:
            count = 0
            for d in data:
                if c.issubset(frozenset(d)):
                    count += 1
            if count >= min_sup:
                all_f_set.append((c, count))
        k += 1
    return all_f_set

if __name__ == '__main__':
    all_frequent_set = get_f_set()
    for i in all_frequent_set:
        print(i)