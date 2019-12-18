# -*- coding: utf-8 -*- 
# @Time : 2019/12/18 13:18
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : simi_analysis.py 
# @Software: PyCharm
import re

import jieba
from gensim import corpora, models, similarities

from music163.analysis import lyric_analysis
from music163.tool import json_tool

"""
计算文本相似度：
1. 读取文档
2. 对要计算的多篇文档进行分词
3. 对文档进行整理成指定格式，方便后续进行计算
4. 计算出词语的词频
5. (可选)对词频低的词语进行过滤
6. 建立语料库词典
7. 加载要对比的文档
8. 将要对比的文档通过doc2bow转化为词袋模型
9. 对词袋模型进行进一步处理，得到新语料库
10. 将新语料库通过tfidfmodel进行处理，得到tfidf
11. 通过token2id得到特征数 
12. 稀疏矩阵相似度,从而建立索引
13. 得到最终相似度结果
"""

file_test = '../data/simi/simi_song_lyric_washed.json'
datas_test = json_tool.load_json(file_test)

file_all = '../data/simi/csps_lyrics_washerd.json'
datas_all = json_tool.load_json(file_all)


# 整理目标文档: 放到列表all_doc中
all_doc_cnt = 0
all_doc = []
for data in datas_all:
	all_doc_cnt += 1
	print("整理目标文档：", all_doc_cnt, '/', len(datas_all))
	doc = data['lyric']
	all_doc.append(doc)

# 对目标文档进行分词,保存到all_doc_list中
all_doc_list_cnt = 0
all_doc_list = []
for doc in all_doc:
	all_doc_list_cnt += 1
	print("对目标文档进行分词：", all_doc_list_cnt, '/', len(all_doc))
	doc_list = [word for word in jieba.cut(doc)]
	doc_list = lyric_analysis.filter_stopwords(doc_list)  # 过滤停留词
	all_doc_list.append(doc_list)

# 制作词袋
print("开始制作词袋")
dictionary = corpora.Dictionary(all_doc_list)
print("词袋完毕")

# 词袋中用数字对所有词进行了编号
# print(dictionary.keys())

# 编号与词之间的对应关系
# print(dictionary.token2id)

# 使用doc2bow制作语料库
print("开始制作语料库")
corpus = [dictionary.doc2bow(doc) for doc in all_doc_list]
print("语料库完毕")

# 使用TF-IDF模型对语料库建模
tfidf = models.TfidfModel(corpus)

# 测试文档: 在本次分析中每次循环取的是一首歌的歌词
result = []
count = 0
for data in datas_test:
	song_id = data['song_id']
	song_name = data['song_name']
	artist_name = data['artist_name']

	count += 1
	doc_test = data['lyric']
	doc_test_list = [word for word in jieba.cut(doc_test)]
	doc_test_vec = dictionary.doc2bow(doc_test_list)  # 将测试文档转换为二元组向量
	# 对每个目标文档, 分析测试文档的相似度
	index = similarities.SparseMatrixSimilarity(tfidf[corpus], num_features=len(dictionary.keys()))
	sim = index[tfidf[doc_test_vec]]
	# 根据相似度排序
	sim_sorted = sorted(enumerate(sim), key=lambda item: -item[1])  # tuple[0]-idx tuple[1]-prop
	cnt = 0
	for sim_iteration in sim_sorted:
		cnt += 1
		# if cnt == 1: # 需要去掉本身,后面再清洗叭
		# 	continue
		idx = sim_iteration[0]
		prop = sim_iteration[1]
		target = datas_all[idx]
		sim_song_name = target['song_name']
		sim_artist_name = target['artist_name']
		dic = {'song_id': song_id, 'artist_name': artist_name, 'song_name': song_name,
			   'sim_song_name': sim_song_name, 'sim_artist_name': sim_artist_name, 'p': prop}
		result.append(dic)
		if cnt == 11:
			break

	print('计算相似度：', count, '/', len(datas_test))

file_output = '../result/simi_result.json'
json_tool.write_json(result, file_output)
