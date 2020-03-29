# encoding=utf-8
import jieba
jieba.load_userdict("NewDict.txt")   # 加载用户自定义词典
from sklearn.feature_extraction.text import TfidfVectorizer
# print(dir(TfidfVectorizer))

def cut(txt_name1, txt_name2):
    with open(txt_name1, 'r') as f1:    # 以只读方式打开文件
        txt = f1.read()
        txt_encode = txt.encode('utf-8')
        txt_cut = jieba.cut(txt_encode)         # 切词
        result = ' '.join(txt_cut)
        # print(result)
    with open(txt_name2, 'w') as f2:    # 分词结果写入文件保存
        f2.write(result)
    f1.close()
    f2.close()

cut('范例1.txt', '提取结果1.txt')     # 分别对文件调用cut方法分词
cut('范例2.txt', '提取结果2.txt')

# 将停用词表从文件读出，并切分成一个数组备用
stopWords_dic = open('stop_words.txt', 'rb')     # 从文件中读入停用词
stopWords_content = stopWords_dic.read()
stopWords_list = stopWords_content.splitlines()     # 转为list备用
stopWords_dic.close()

with open('提取结果1.txt', 'r') as f3:
    res3 = f3.read()
with open('提取结果2.txt', 'r') as f4:
    res4 = f4.read()

corpus = [res3, res4]
# print(corpus)
vector = TfidfVectorizer(stop_words=stopWords_list)
tf_idf = vector.fit_transform(corpus)
# print(tf_idf)

word_list = vector.get_feature_names()      # 获取词袋模型的所有词
weight_list = tf_idf.toarray()
# result1 = ''.join(word_list)
# result2 = ''.join(weight_list)
# print(result1, result2)
# with open('words_list.txt', 'w') as f3:
#     f3.write(result)


# 打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
for i in range(len(weight_list)):
    print("-------第", i+1, "段文本的词语tf-idf权重------")
    for j in range(len(word_list)):
        print(word_list[j], weight_list[i][j])

