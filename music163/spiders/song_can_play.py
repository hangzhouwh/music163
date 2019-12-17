# -*- coding: utf-8 -*- 
# @Time : 2019/11/28 16:26
# @Author : hangzhouwh
# @Email: hangzhouwh@gmail.com
# @File : song_lyric.py
# @Software: PyCharm

import json
import time
import scrapy

from music163.items import SongCanPlayItem
from music163.tool import file_tool, json_tool

song_count = 0
can = 0
cannot = 0


class SongCanPlaySpider(scrapy.Spider):
	name = 'song_can_play'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		global song_count
		file_count = 0
		files = file_tool.eachFile('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\')
		for file in files:
			print("…………………………This is ", file_count, " file:   ", file)
			file_count = file_count + 1
			song_data = json_tool.load_json(file)
			time.sleep(20)
			for song in song_data:
				song_id = song["song_id"]
				url = 'http://localhost:3000/check/music?id=' + str(song_id)
				song_count = song_count + 1
				print("爬取第 ", song_count, " 首单曲是否可用信息")
				yield scrapy.Request(url=url, dont_filter=False)

	def parse(self, response):
		global can, cannot

		res = json.loads(response.body)
		song_can_play_item = SongCanPlayItem()

		song_id = response.url.replace("http://localhost:3000/check/music?id=", "")
		song_can_play_item['song_id'] = song_id
		song_can_play_item['song_can_play'] = res['success']

		if res['success']:
			can = can + 1
		else:
			cannot = cannot + 1

		if song_count % 500 == 0:
			print("can: ", can)
			time.sleep(5)

		yield song_can_play_item
