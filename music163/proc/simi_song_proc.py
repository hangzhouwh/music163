# -*- coding: utf-8 -*- 
# @Time : 2019/12/18 10:09
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : simi_song_proc.py 
# @Software: PyCharm

from music163.analysis import lyric_analysis
from music163.proc.douyin_lyric_proc import make_summary
from music163.tool import json_tool


def wash_111():
	file = '../data/csps_lyric/csps_lyrics.json'
	datas = json_tool.load_json(file)

	# for data in reversed(datas):
	# 	temp = data['song_name']
	# 	data['song_name'] = data['artist_name']
	# 	data['artist_name'] = temp

	# for data in reversed(datas):
	# 	cds = ['许嵩', 'G.E.M.邓紫棋', '徐秉龙', '沈以诚', '陈粒', '群星', '蔡健雅', '汪苏泷', '田馥甄', '孙燕姿', '赵方婧',
	# 		   '王菲', '陈雪凝', '杨千嬅', '任然', 'Beyond', '程佳佳', '杨宗纬', '郭顶', '五月天', '王嘉尔', '房东的猫']
	# 	if data['artist_name'] in cds:
	# 		datas.remove(data)

	for data in reversed(datas):
		lyric = data['lyric']
		lyric_list = lyric_analysis.wash(lyric)
		data['lyric'] = '.'.join(lyric_list)
	# 	lyric_list = lyric_analysis.word_spilt(lyric_list)
	# 	lyric_list = lyric_analysis.filter_stopwords(lyric_list)

	json_tool.write_json(datas, '../data/csps_lyric/csps_lyrics_washed.json')


def get_simi_song_summary():
	file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\simi\\simi_song_lyric.json'
	songs = json_tool.load_json(file)

	word_lists = []
	summary = []
	for song in songs:
		lyric = song['lyric']
		song_name = song['song_name']
		artist_name = song['artist_name']
		wash_list = lyric_analysis.wash(lyric)
		word_list = lyric_analysis.word_spilt(wash_list)
		word_list = lyric_analysis.filter_stopwords(word_list)
		text = ''.join(word_list)
		tfidf, textrank = make_summary(text)

		tfidf_txt = ','.join(tfidf[0])
		textrank_txt = ','.join(textrank[0])
		song_dict = {'song_name': song_name, 'artist_name': artist_name, 'tfidf': tfidf_txt, 'textrank': textrank_txt}
		summary.append(song_dict)

	file_output = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\song_lyric_summary.json'
	json_tool.write_json(summary, file_output)


if __name__ == "__main__":
	# file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\simi\\simi_song_lyric.json'
	# datas = json_tool.load_json(file)

	wash_111()
	# for data in reversed(datas):
	# 	lyric = data['lyric']
	# 	lyric_list = lyric_analysis.wash(lyric)
	# 	lyric_list = lyric_analysis.word_spilt(lyric_list)
	# 	lyric_list = lyric_analysis.filter_stopwords(lyric_list)
