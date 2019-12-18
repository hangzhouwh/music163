# -*- coding: utf-8 -*- 
# @Time : 2019/12/18 12:34
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : simi_analysis_demo.py.py
# @Software: PyCharm

import jieba
from gensim import corpora, models, similarities

# 文档
doc0 = "我不喜欢上海"
doc1 = "上海是一个好地方"
doc2 = "北京是一个好地方"
doc3 = "上海好吃的在哪里"
doc4 = "上海好玩的在哪里"
doc5 = "上海是好地方"
doc6 = "上海路和上海人"
doc7 = "喜欢小吃"
doc_test = "我喜欢上海的小吃"


"""
分词
"""
# 把目标文档放到一个列表all_doc中
all_doc = []
all_doc.append(doc0)
all_doc.append(doc1)
all_doc.append(doc2)
all_doc.append(doc3)
all_doc.append(doc4)
all_doc.append(doc5)
all_doc.append(doc6)
all_doc.append(doc7)

# 对目标文档进行分词，并且保存在列表all_doc_list中
all_doc_list = []
for doc in all_doc:
    doc_list = [word for word in jieba.cut(doc)]
    all_doc_list.append(doc_list)

# 分词后形成的列表显示出来
print(all_doc_list)

# 测试文档
doc_test_list = [word for word in jieba.cut(doc_test)]
doc_test_list

"""
制作语料库
"""
# 获取词袋
dictionary = corpora.Dictionary(all_doc_list)

# 词袋中用数字对所有词进行了编号
print(dictionary.keys())

# 编号与词之间的对应关系
print(dictionary.token2id)

# 使用doc2bow制作语料库
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]

# 用同样的方法，把测试文档也转换为二元组的向量
doc_test_vec = dictionary.doc2bow(doc_test_list)
print(doc_test_vec)

"""
相似度分析
"""
# 使用TF-IDF模型对语料库建模
tfidf = models.TfidfModel(corpus)

# 获取测试文档中，每个词的TF-IDF值
print(tfidf[doc_test_vec])

# 对每个目标文档，分析测试文档的相似度
index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
sim = index[tfidf[doc_test_vec]]
print(sim)

# 根据相似度排序
sorted(enumerate(sim), key=lambda item: -item[1])


