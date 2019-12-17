# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 20:17
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : lyric_analysis.py 
# @Software: PyCharm

import re


# 清洗歌词
# 删除时间戳,删除作词作曲信息
import jieba


def wash(musicLrcStr):
	str = re.sub('\[\d{2}:\d{2}.\d{2,3}\]', '', musicLrcStr)
	str = str.lower()
	line_list = str.split('\n')
	for line in reversed(line_list):
		if line == '':
			line_list.remove(line)
		elif '作曲' in line:
			line_list.remove(line)
		elif '作词' in line:
			line_list.remove(line)
		elif '编曲' in line:
			line_list.remove(line)
		elif '录音' in line:
			line_list.remove(line)
		elif '混音' in line:
			line_list.remove(line)
		elif '制作' in line:
			line_list.remove(line)
		elif '出品' in line:
			line_list.remove(line)
		elif '母带处理' in line:
			line_list.remove(line)

	return line_list


# 分词
def word_spilt(str_list):
	word_list = []
	for str_ele in str_list:
		seg_list = jieba.cut(str_ele)
		for seg in seg_list:
			word_list.append(seg)
	return word_list


# 过滤停用词
def filter_stopwords(word_list):
	stop = []
	standard_stop = []

	# 停用词表
	files_stop = [r'D:\\WorkSpace\\Pycharm\\music163\\music163\\words\\中文停用词表.txt',
				  r'D:\\WorkSpace\\Pycharm\\music163\\music163\\words\\哈工大停用词表.txt',
				  r'D:\\WorkSpace\\Pycharm\\music163\\music163\\words\\四川大学机器智能实验室停用词库.txt',
				  r'D:\\WorkSpace\\Pycharm\\music163\\music163\\words\\百度停用词表.txt']

	for file_stop in files_stop:
		with open(file_stop, 'r', encoding='utf-8-sig') as f:
			lines = f.readlines()  # lines是list类型
			for line in lines:
				lline = line.strip()  # line 是str类型,strip 去掉\n换行符
				stop.append(lline)  # 将stop 是列表形式

		# stop 的元素是一行一行的 句子,需要进行转化为一个词一行,即下面:
		for i in range(0, len(stop)):
			for word in stop[i].split():
				standard_stop.append(word)

	standard_stop = list(set(standard_stop))
	standard_stop.append('…')

	word_set = list(set(word_list))

	# 过滤停用词
	for word in reversed(word_set):
		if word.strip() == '':
			word_set.remove(word)
		elif word in standard_stop:
			word_set.remove(word)

	for word in reversed(word_list):
		if word not in word_set:
			word_list.remove(word)

	return word_list


# 统计词频
def get_word_frequency(word_list):
	counts = {}
	for word in word_list:
		counts[word] = counts.get(word, 0) + 1

	items = list(counts.items())
	items.sort(key=lambda x: x[1], reverse=True)
	return items


# 计算词出现的比例（为绘制词云做准备）
def cal_word_rate(word_frequency):
	word_rate = {}
	sum = 0
	for word in word_frequency:
		sum = sum + word[1]

	for word in word_frequency:
		word_rate[word[0]] = word[1] / sum

	return word_rate

