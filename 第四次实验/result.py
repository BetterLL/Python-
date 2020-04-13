import codecs
import shutil
import sys,os
import re
import jieba
import jieba.analyse
# 导入自定义词典
# jieba.load_userdict("zydcd.txt")
# Read file and cut
def read_file_cut():
    path = "weibo\\"
    # create path
    respath = "Result01\\"
    if os.path.isdir(respath):
        shutil.rmtree(respath, True)
    os.makedirs(respath)
    num = 1
    while num <= 33:
        name = "%02d" % num
        fileName = path + str(name) + ".txt"
        resName = respath + str(name) + ".txt"
        source = open(fileName, 'r')
        if os.path.exists(resName):
            os.remove(resName)
        result = codecs.open(resName, 'w', 'utf-8')
        line = source.readline()
        line = line.rstrip('\n')
        while line != "":
            line = str(line)
            seglist = jieba.cut(line, cut_all=False)  # 精确模式
            output = ' '.join(list(seglist))  # 空格拼接
            print(output)
            result.write(output + '\r\n')
            line = source.readline()
        else:
            print('End file: ' + str(name))
            source.close()
            result.close()
        num = num + 1
    else:
        print('End All')
targetTxt="result.txt"
with open(targetTxt, 'r', encoding = 'utf-8') as file:
    text = file.readlines()#读取每行的数据
    keywords = jieba.analyse.extract_tags(str(text), topK = 20, withWeight=True, allowPOS=())
    #text : 待提取的字符串类型文本
    #topK : 返回TF-IDF权重最大的关键词的个数，默认为20个
    #withWeight: 是否返回关键词的权重值，默认为False
    #allowPOS : 包含指定词性的词，默认为空,即不筛选
    print(keywords)
    print('TF-IDF法提取关键词结束！')
def loadDataSet(fileName):
    data = np.loadtxt(fileName, delimiter='\t')
    return data
# 欧氏距离计算
def distEclud(x, y):
    return np.sqrt(np.sum((x - y) ** 2))
# 为给定数据集构建一个包含K个随机质心的集合
def randCent(dataSet, k):
    m, n = dataSet.shape
    centroids = np.zeros((k, n))
    for i in range(k):
        index = int(np.random.uniform(0, m))  #
        centroids[i, :] = dataSet[index, :]
    return centroids
# k均值聚类
def KMeans(dataSet, k):
    m = np.shape(dataSet)[0]  # 行的数目
    # 第一列存样本属于哪一簇
    # 第二列存样本的到簇的中心点的误差
    clusterAssment = np.mat(np.zeros((m, 2)))
    clusterChange = True
    # 第1步 初始化centroids
    centroids = randCent(dataSet, k)
    while clusterChange:
        clusterChange = False
        # 遍历所有的样本（行数）
        for i in range(m):
            minDist = 100000.0
            minIndex = -1
            # 遍历所有的质心
            # 第2步 找出最近的质心
            for j in range(k):
                # 计算该样本到质心的欧式距离
                distance = distEclud(centroids[j, :], dataSet[i, :])
                if distance < minDist:
                    minDist = distance
                    minIndex = j
            # 第 3 步：更新每一行样本所属的簇
            if clusterAssment[i, 0] != minIndex:
                clusterChange = True
                clusterAssment[i, :] = minIndex, minDist ** 2
        # 第 4 步：更新质心
        for j in range(k):
            pointsInCluster = dataSet[np.nonzero(clusterAssment[:, 0].A == j)[0]]  # 获取簇类所有的点
            centroids[j, :] = np.mean(pointsInCluster, axis=0)  # 对矩阵的行求均值
    print("Congratulations,cluster complete!")
    return centroids, clusterAssment
def merge_file():
    path = "Resulet01\\"
    resName = "result.txt"
    if os.path.exists(resName):
        os.remove(resName)
    result = codecs.open(resName, 'w', 'utf-8')
    num = 1
    while num <= 33:
        name = "%02d" % num 
        fileName = path + str(name) + ".txt"
        source = open(fileName, 'r')
        line = source.readline()
        line = line.strip('\n')
        line = line.strip('\r')
        while line!="":
            line = str(line)
            line = line.replace('\n',' ')
            line = line.replace('\r',' ')
            result.write(line+ ' ')
            line = source.readline()
        else:
            print ('End file: ' + str(num))
            result.write('\r\n')
            source.close()
        num = num + 1
    else:
        print ('End All')
        result.close()
if __name__ == '__main__':
    read_file_cut()
    dataSet = loadDataSet("test1.txt")
    k = 4
    centroids, clusterAssment = KMeans(dataSet, k)
    merge_file()
