# -*- coding: utf-8 -*- 
# @Time : 2019/12/11 22:14
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : csps_lyric.py 
# @Software: PyCharm

import json
import random
import time
import scrapy

from music163.items import CSPSLyricItem
from music163.tool import json_tool

song_count = 0


class CSPSLyricSpider(scrapy.Spider):
	name = 'csps_lyric'
	allowed_domains = ['localhost:3000']

	def start_requests(self):

		# filepath = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\chinese_singer_popular_song\\chinese_singer_popular_songs.json'

		filepath_head = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\chinese_singer_popular_song\\csps"
		url_head = 'http://localhost:3000/lyric?id='
		aa=[16, 17, 18]
		for i in aa:
			filepath = filepath_head+str(i)+'.json'
			print(filepath)
			songs = json_tool.load_json(filepath)
			for song in songs:
				# artist_id = song['artist_id']
				artist_name = song['artist_name']
				song_id = song['song_id']
				song_name = song['song_name']
				url = url_head + str(song_id)
				yield scrapy.Request(url=url, meta={'artist_name': artist_name, 'song_name': song_name}, dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)

		if 'lrc' in res.keys() and 'lyric' in res['lrc'].keys():
			lrc = res['lrc']
			artist_name = response.meta['artist_name']
			song_name = response.meta['song_name']
			lyric = lrc['lyric']

			csps_lyric_item = CSPSLyricItem()
			csps_lyric_item["song_name"] = artist_name
			csps_lyric_item["artist_name"] = song_name
			csps_lyric_item["lyric"] = lyric

			song_count += 1
			print("热门音乐:  ", song_count)

			if song_count % 500 == 0:
				sec = random.randint(3, 9)
				print('休眠 ', sec, 's')
				time.sleep(sec)

			yield csps_lyric_item
		else:
			pass
