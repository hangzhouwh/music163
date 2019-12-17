# -*- coding: utf-8 -*- 
# @Time : 2019/11/28 16:53
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : song_comment_count.py 
# @Software: PyCharm

import json
import time

import scrapy

from music163.items import SongUrlItem, SongCommentCountItem
from music163.tool import file_tool, json_tool

song_count = 0
miss = 0

class SongCommentCountSpider(scrapy.Spider):
	name = 'song_comment_count'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		file_count = 0
		files = file_tool.eachFile('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\')
		for file in files:
			print("…………………………This is ", file_count, " file:   ", file)
			file_count = file_count + 1
			song_data = json_tool.load_json(file)
			time.sleep(10)

			for song in song_data:
				song_id = song["song_id"]
				url = 'http://localhost:3000/comment/music?id=' + str(song_id) + '&limit=1'
				yield scrapy.Request(url=url, dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)
		song_comment_count_item = SongCommentCountItem()

		song_id = response.url.replace("http://localhost:3000/check/music?id=", "")
		song_comment_count_item['song_id'] = song_id
		song_comment_count_item['song_comment_count'] = res['total']

		if song_count % 1000 == 0:
			time.sleep(5)

		song_count = song_count + 1
		print("爬取第 ", song_count, " 首单曲评论数量")
		yield song_comment_count_item
