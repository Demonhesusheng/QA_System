from text2vec import Similarity
import jieba
import heapq
import jieba.analyse
import pandas as pd

"""
问题相似度比较：
为用户提供QA接口服务调用，支持用户在前端页面输入一系列的问题，
然后将问题与数据库中的问题进行相似度比较，如果计算出相似度阈值
大于0.5则返回结果，否则返回answer_id = 0
"""

# 初始化获取停用词表
stop = open("stop_word.txt", 'r+', encoding='utf-8')
stopword = stop.read().split("\n")
key = open('key_word.txt', 'r+', encoding='utf-8')
keyword = key.read().split("\n")

"""
加载初始数据信息
str:文件传输路径
index:所需真实值索引列表
"""


def init_data(str, index):
    dream_data = pd.read_csv(str)
    return dream_data.values[:, index]


"""
对文本内容进行过滤
1、过滤停用词
2、结合关键词/字过滤
"""


def strip_word(seg):
    # 打开写入关键词的文件
    jieba.load_userdict("./key_word.txt")
    print("去停用词:\n")
    wordlist = []
    # 获取关键字
    keywords = jieba.analyse.extract_tags(seg, topK=5, withWeight=False, allowPOS=('n'))
    # 遍历分词表
    for key in jieba.cut(seg):
        print(key)
        # 去除停用词，去除单字且不在关键词库，去除重复词
        if not(key.strip() in stopword) and (len(key.strip()) > 1 or key.strip() in keyword) and not(key.strip() in wordlist):
            wordlist.append(key)
    # 停用词去除END
    stop.close()
    return ''.join(wordlist)


"""
通过text2vec词向量模型计算出来两段处理后的文本相似度
"""


def Similarity_calculation(str_arr, str_2):
    sim = Similarity()
    str_2 = strip_word(str_2)
    result = []
    for item in str_arr:
        item = strip_word(item)
        result.append(sim.get_score(item, str_2))
    return result


"""
将用户细节文本描述转换为关键字文本
"""


def deal_init_data(text_data):
    text_arr = []
    for item in text_data:
        # 做关键词提取
        text_arr.append(strip_word(item))
    key_words = pd.DataFrame(text_arr, columns=['key_text'])
    key_words.to_csv('drean_keywords.csv', sep='', header=True, index=True)
    return key_words


def main():
    key_arr = init_data('base_content.csv', 1)
    # 读取文本的对比数据关键词(即数据集中的关键词）
    demo_arr = init_data('demo.csv', 0)

    for index, item in enumerate(demo_arr):
        result = Similarity_calculation(key_arr, item)
        # 获取相似度最高的一个
        re1 = map(result.index, heapq.nlargest(1, result))
        re2 = heapq.nlargest(1, result)
        for i, val in enumerate(list(re1)):
            # 设置置信阈值
            if re2[i] > 0.7:
                print(i + 1, "、对比结果：", key_arr[val], ",相似度：", re2[i])
            else:
                print("匹配失败, answer_id = 0")  # 后续返回json格式的，answer_id = 0


"""
测试函数专用，后续从https请求中获取关键句子即可
"""
"""
if __name__ == '__main__':
    # 读取文本的对比数据关键词
    key_arr = init_data('base_content.csv', 1)
    # 读取文本的对比数据关键词(即数据集中的关键词）
    demo_arr = init_data('demo.csv', 0)

    for index, item in enumerate(demo_arr):
        result = Similarity_calculation(key_arr, item)
        # 获取相似度最高的一个
        re1 = map(result.index, heapq.nlargest(1, result))
        re2 = heapq.nlargest(1, result)
        for i, val in enumerate(list(re1)):
            # 设置置信阈值
            if re2[i] > 0.7:
                print(i+1, "、对比结果：", key_arr[val], ",相似度：", re2[i])
            else:
                print("匹配失败, answer_id = 0") # 后续返回json格式的，answer_id = 0

"""

