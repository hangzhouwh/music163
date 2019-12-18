# -*- coding: utf-8 -*- 
# @Time : 2019/12/19 2:01
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : minmax_proc.py 
# @Software: PyCharm
from music163.tool import json_tool


def get_minmax_albumsize_musicsize():
	file = '../data/artist/artist.json'
	datas = json_tool.load_json(file)

	max_album_size_sorted_ = sorted(datas, key=lambda e: e['album_size'], reverse=True)
	min_album_size_sorted_ = sorted(datas, key=lambda e: e['album_size'], reverse=False)
	max_music_size_sorted = sorted(datas, key=lambda e: e['music_size'], reverse=True)
	min_music_size_sorted_ = sorted(datas, key=lambda e: e['music_size'], reverse=False)

	print(1)




if __name__ == "__main__":
	# get_minmax_albumsize_musicsize()

	pass