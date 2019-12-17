# -*- coding: utf-8 -*-
# @Time : 2019/11/28 16:26
# @Author : hangzhouwh
# @Email: hangzhouwh@gmail.com
# @File : song_lyric.py
# @Software: PyCharm


import json
import time

import scrapy

from music163.items import SongUrlItem
from music163.tool import file_tool, json_tool

song_count = 0
miss = 0

class SongUrlSpider(scrapy.Spider):
	name = 'song_url'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		file_count = 0
		files = file_tool.eachFile('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\')
		for file in files:
			print("…………………………This is ", file_count, " file:   ", file)
			file_count = file_count + 1
			song_data = json_tool.load_json(file)
			time.sleep(10)
			count = 0
			for song in song_data:
				song_id = song["song_id"]
				if count % 10 == 0:
					url = 'http://localhost:3000/song/url?id=' + str(song_id)
				else:
					url = url + "," + str(song_id)
				if count % 10 == 9:
					yield scrapy.Request(url=url, dont_filter=False)
				count = count + 1


	def parse(self, response):
		global song_count, miss

		res = json.loads(response.body)
		song_url_item = SongUrlItem()
		song_urls = res['data']
		for song_url in song_urls:
			if song_url['code'] == 200:
				song_url_item['song_id'] = song_url['id']
				song_url_item['song_url'] = song_url['url']
			else:
				song_url_item['song_id'] = song_url['id']
				song_url_item['song_url'] = song_url['url']
				miss = miss + 1

			if song_count % 1000 == 0:
				print("miss: ", miss)
				time.sleep(5)

			song_count = song_count + 1
			print("爬取第 ", song_count, " 首单曲的URL")
			yield song_url_item
