# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 20:18
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : original_proc.py 
# @Software: PyCharm
import re

import jieba.posseg as pseg
import pandas as pd

from music163.analysis import lyric_analysis
from music163.tool import json_tool


def get_lyric_flag(file, output):
	songs = json_tool.load_json(file)

	count = {}
	flags = []
	for song in songs:
		lyric = song['lyric']
		lyric_list = lyric_analysis.wash(lyric)
		lyric = '.'.join(lyric_list)
		words = pseg.cut(lyric)
		for w in words:
			# w.word w.flag
			flags.append(w.flag)
			count[w.flag] = count.get(w.flag, 0) + 1

	flags = list(set(flags))
	count_flag = {}
	for flag in flags:
		count_flag[lyric_analysis.get_flag(flag)] = count.get(flag, 0)

	flags_output = []
	count_output = []
	for i in count_flag:
		flags_output.append(i)
		count_output.append(count_flag.get(i))

	df = pd.DataFrame([flags_output, count_output], index=['flags', 'count'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv(output, encoding='utf_8_sig')



def get_high_fre(input, output):
	songs = json_tool.load_json(input)

	word_lists = []
	count = 0
	for song in songs:
		lyric = song['lyric']
		wash_list = lyric_analysis.wash(lyric)
		word_list = lyric_analysis.word_spilt(wash_list)
		word_list = lyric_analysis.filter_stopwords(word_list)
		word_lists.extend(word_list)
		count += 1
		print(count, '/', len(songs))

	str = '~!@#$%^&*()'
	for word in reversed(word_lists):
		if re.search('[a-z]', word) or word in str:
			word_lists.remove(word)

	word_frequency = lyric_analysis.get_word_frequency(word_lists)
	word_rate = lyric_analysis.cal_word_rate(word_frequency)

	key = []
	key_fre = []
	key_rate = []
	for word in word_frequency:
		if word[1] >= 10:
			key.append(word[0])
			key_fre.append(word[1])
			key_rate.append(word_rate.get(word[0]))

	df = pd.DataFrame([key, key_fre, key_rate], index=['word', 'frequency', 'rate'])
	df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
	df.to_csv(output, encoding='utf_8_sig')


if __name__ == "__main__":
	file_original = '../data/rank_list_data/original_lyric.json'
	file_output = '../result/网易原创歌曲榜高频词.csv'
	get_lyric_flag(file_original, file_output)
	get_high_fre(file_original, file_output)

	# file_saysong = '../data/rank_list_data/saysong_lyric.json'
	# file_output = '../result/网易说唱歌曲榜高频词.csv'
	# # get_lyric_flag(file_saysong, file_output)
	# get_high_fre(file_saysong, file_output)
