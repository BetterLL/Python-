
#coding=UTF-8
import random
import re
from numpy import *
 
#解析英文文本，并返回列表
def textParse(bigString):
    #将文本以非单词字符划分
    listOfTokens = re.split(r'\W', bigString)    
    #去除单词长度小于2的无用单词
    return [tok.lower() for tok in listOfTokens if len(tok)>2]
 
#去列表中重复元素，并以列表形式返回
def createVocaList(dataSet):
    vocabSet = set({})
    #去重复元素，取并集
    for document in dataSet:
        vocabSet = vocabSet | set(document)
    return list(vocabSet)
 
#统计每一文档（或邮件）在单词表中出现的次数，并以列表形式返回
def setOfWordsToVec(vocabList,inputSet): 
    #创建0向量，其长度为单词量的总数
    returnVec = [0]*len(vocabList)
    #统计相应的词汇出现的数量
    for word in inputSet:
        if word in vocabList:
            returnVec[vocabList.index(word)] += 1
    return returnVec
 
#朴素贝叶斯分类器训练函数
def trainNB0(trainMatrix,trainCategory): 
    #获取训练文档数
    numTrainDocs = len(trainMatrix)
    #获取每一行词汇的数量
    numWords = len(trainMatrix[0])
    #侮辱性概率(计算p(Ci))，计算垃圾邮件的比率
    pAbusive = sum(trainCategory)/float(numTrainDocs)
    #统计非垃圾邮件中各单词在词数列表中出现的总数（向量形式）
    p0Num = ones(numWords)
    #统计垃圾邮件中各单词在词数列表中出现的总数（向量形式）
    p1Num = ones(numWords)
    #统计非垃圾邮件总单词的总数（数值形式）
    p0Denom = 2.0
    #统计垃圾邮件总单词的总数（数值形式）
    p1Denom = 2.0
    #拉普拉斯平滑解决零概率问题

    for i in range(numTrainDocs):
        #如果是垃圾邮件
        if trainCategory[i] == 1:
            p1Num += trainMatrix[i]
            p1Denom +=sum(trainMatrix[i])
        #如果是非垃圾邮件
        else:
            p0Num += trainMatrix[i]
            p0Denom +=sum(trainMatrix[i])
    #计算每个单词在垃圾邮件出现的概率（向量形式）
    p1Vect = log(p1Num/p1Denom)
    #计算每个单词在非垃圾邮件出现的概率（向量形式）
    p0Vect = log(p0Num/p0Denom)         
    return p0Vect,p1Vect,pAbusive

#朴素贝叶斯分类函数
def classifyNB(vec2Classify,p0Vec,p1Vec,pClass1):
    p1 = sum(vec2Classify*p1Vec)+log(pClass1)
    p0 = sum(vec2Classify*p0Vec)+log(1.0 - pClass1)
    if p1 > p0:
        return 1
    else :
        return 0
#test
def spamtest():
    #导入并解析文本文件
    docList =[];classList=[];fullText = []
    for i in range(1,26):
        #读取第i篇垃圾文件，并以列表形式返回
        wordList = textParse(open('email/spam/{0}.txt'.format(i)).read())
        #转化成二维列表
        docList.append(wordList)
        #一维列表进行追加
        fullText.extend(wordList)
        #标记文档为垃圾文档
        classList.append(1)
        #读取第i篇非垃圾文件，并以列表形式返回
        wordList = textParse(open('email/ham/{0}.txt'.format(i)).read())
        #转化成二维列表
        docList.append(wordList)
        #一维列表进行追加
        fullText.extend(wordList)
        #标记文档为非垃圾文档
        classList.append(0)
    #去除重复的单词元素
    vocabList = createVocaList(docList)
    #训练集，先放入全部50个样本
    trainingSet = list(range(50))
    testSet = []
    #选出10篇txt作测试集
    for i in range(10):
        randIndex = int(random.uniform(0,len(trainingSet)))
        testSet.append(trainingSet[randIndex])
        del trainingSet[randIndex]          #从训练集中删除作为测试集的样本

    trainMat = [];trainClasses=[]
    #选出40篇txt作训练集
    for docIndex in trainingSet:
        trainMat.append(setOfWordsToVec(vocabList, docList[docIndex]))          # 将生成的词集模型添加到训练矩阵中
        trainClasses.append(classList[docIndex])                    # 将类别添加到训练集类别标签系向量中
    p0V,p1V,pSpam = trainNB0(array(trainMat), array(trainClasses))

    #对测试集分类
    errorCount = 0
    for docIndex in testSet:
        wordVector = setOfWordsToVec(vocabList,docList[docIndex])   # 测试集的词集模型
        if classifyNB(array(wordVector), p0V, p1V, pSpam)!=classList[docIndex]:
            errorCount+=1
            print("分类错误的测试集：", docList[docIndex])
    print("错误率为：{0}".format(float(errorCount)/len(testSet)))

if __name__ == '__main__':
    spamtest()