# -*- coding: utf-8 -*- 
# @Time : 2019/12/18 12:41
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : summary.py 
# @Software: PyCharm
from music163.analysis import lyric_analysis
from music163.proc.douyin_lyric_proc import make_summary
from music163.tool import json_tool

file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\csps_lyric\\csps_lyrics.json'
songs = json_tool.load_json(file)

summary = []
cnt = 0
for song in songs:
	cnt += 1
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
	print(cnt, "/", len(songs))

file_output = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\csps_lyrics_summary.json'
json_tool.write_json(summary, file_output)


