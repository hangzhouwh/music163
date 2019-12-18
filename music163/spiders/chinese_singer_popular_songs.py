# -*- coding: utf-8 -*- 
# @Time : 2019/12/11 21:46
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : chinese_singer_popular_songs.py 
# @Software: PyCharm

import json
import random
import time
import scrapy

from music163.items import ChinesePopularSongItem
from music163.tool import json_tool

singer_count = 0
song_count = 0


class ChineseSingerPopularSongsSpider(scrapy.Spider):
	name = 'chinese_singer_popular_songs'
	allowed_domains = ['localhost:3000']

	def start_requests(self):

		# files = [1001, 1002, 1003]  # 华语男歌手 华语女歌手 华语组合
		# path_head = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\artist\\'
		file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\rank_list\\热门歌手xxx.json'
		url_head = 'http://localhost:3000'
		# for file in files:
		# filepath = path_head + 'artist_' + str(file) + '.json'
		# print(filepath)
		res = json_tool.load_json(file)
		artists = res['artists']
		for artist in artists:
			artist_id = artist['id']
			artist_name = artist['name']
			url = url_head + '/artist/top/song?id=' + str(artist_id)
			yield scrapy.Request(url=url, meta={'artist_id': artist_id, 'artist_name': artist_name},
								 dont_filter=False)

	def parse(self, response):
		global singer_count, song_count

		res = json.loads(response.body)

		songs = res['songs']
		artist_id = response.meta['artist_id']
		artist_name = response.meta['artist_name']

		singer_count += 1
		print("歌手:  ", singer_count)
		for song in songs:
			chinese_popular_song_item = ChinesePopularSongItem()
			chinese_popular_song_item["artist_id"] = artist_id
			chinese_popular_song_item["artist_name"] = artist_name
			chinese_popular_song_item["song_id"] = song['id']
			chinese_popular_song_item["song_name"] = song['name']

			song_count += 1
			print("热门音乐:  ", song_count)
			yield chinese_popular_song_item
