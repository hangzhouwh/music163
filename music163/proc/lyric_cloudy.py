import jieba
import jieba.analyse as anls
import re
from music163.tool import json_tool
import pandas as pd

musicLrcStr = """
[00:00.000] 作曲 : 吴剑泓
[00:01.000] 作词 : 林利南/林秋离
[00:19.180]你有多久没有看过那片海
[00:24.589]你到现在对自己究竟多明白
[00:30.379]总是不服输
[00:35.000]永远要比别人快
[00:38.290]在你前方是否有你要的未来
[00:45.100]想到我们的过去
[00:47.529]都让人感慨
[00:52.690]希望所有好朋友都能站起来
[01:00.300]还有你曾经
[01:03.190]疯狂爱上的女孩
[01:06.800]再过几年是不是依旧难以忘怀
[01:14.129]可是andy 活着是不须道理
[01:20.989]谁都可能
[01:24.900]暂时的失去勇气
[01:27.189]外面不安的世界
[01:31.090]骚动的心情
[01:34.489]不能熄灭曾经你拥有炽热的心
[01:42.300]我是真的不会表达我的爱
[01:48.900]却很在乎每个人对我的期待
[01:56.700]平凡的角色
[02:00.100]站在小小的舞台
[02:02.700]我有那么勇敢地说出来
[02:38.728]想到我们的过去
[02:41.046]都让人感慨
[02:44.846]希望所有好朋友都能站起来
[02:54.173]还有你曾经
[02:56.656]疯狂爱上的女孩
[02:59.561]再过几年是不是依旧难以忘怀
[03:06.460]可是andy 活着是不须道理
[03:14.067]谁都可能
[03:18.528]暂时的失去勇气
[03:20.647]外面不安的世界
[03:24.988]骚动的心情
[03:28.620]不能熄灭曾经你拥有炽热的心
[03:34.955]我是真的不会表达我的爱
[03:41.946]却很在乎每个人对我的期待
[03:49.967]平凡的角色
[03:54.118]站在小小的舞台
[03:58.064]我有那么勇敢地说出来
[04:18.940]外面不安的世界
[04:23.269]骚动的心情
[04:26.584]不能熄灭曾经你拥有炽热的心
[04:33.690]可是andy
[04:36.900]Oh…Oh…Oh
[04:41.280]andy  Oh…Oh…Oh
[04:47.989]外面不安的世界
[04:50.917]骚动的心情
[04:54.768]不能熄灭曾经你拥有炽热的心
"""


# 清洗歌词
# 删除时间戳,删除作词作曲信息
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


if __name__ == "__main__":
	songs = json_tool.load_json('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\csps_lyric\\csps_lyrics.json')

	RE = re.compile(u'[\u4e00-\u9fa5]', re.UNICODE)

	word_lists = []

	count = 0
	for song in songs:
		lyric = song['lyric']

		match = re.search(RE, lyric)  # 判断歌词中包不包含中文
		if match is not None:
			wash_list = wash(lyric)
			word_list = word_spilt(wash_list)
			word_list = filter_stopwords(word_list)
			word_lists.extend(word_list)
		count += 1
		print(count, '/', len(songs))

	print("fre start")
	word_frequency = get_word_frequency(word_lists)
	print("fre done")
	print("rate start")
	word_rate = cal_word_rate(word_frequency)
	print("rate done")
	# sorted(word_rate.items(), key=lambda item: item[1])

	key = []
	value = []
	count = 0
	for word in word_rate:
		key.append(word)
		value.append(word_rate.get(word))
		count += 1
		if count == 100:
			break
	df = pd.DataFrame([key, value], index=['word', 'frequency'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\word_fre_100.csv', encoding='utf8')

# # 文本摘要
# str = ''.join(str_list)
# str = str.lower()  # 全部变成小写字符
# for x, w in anls.extract_tags(str, topK=20, withWeight=True):
#     print('%s %s' % (x, w))
