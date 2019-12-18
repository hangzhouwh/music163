# -*- coding: utf-8 -*- 
# @Time : 2019/12/18 23:24
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : comment_king.py 
# @Software: PyCharm
import json

import scrapy

from music163.tool import json_tool
from music163.items import CommentItem

class CommentKingSpider(scrapy.Spider):
	name = 'comment_king'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		filepath = "./data/comment_king/comment_king_song.json"
		songs = json_tool.load_json(filepath)
		url_head = 'http://localhost:3000/comment/music?id='

		for song in songs:
			song_id = song['song_id']
			song_name = song['song_name']
			artist_id = song['artist_id']
			artist_name = song['artist_name']
			for i in range(10):
				url = url_head + str(song_id) + '&offset=' + str(i*20)
				yield scrapy.Request(url=url,
									 meta={'song_id': song_id, 'song_name': song_name,
										   'artist_id': artist_id, 'artist_name': artist_name},
									 dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)

		song_id = response.meta['song_id']
		song_name = response.meta['song_name']
		artist_id = response.meta['artist_id']
		artist_name = response.meta['artist_name']

		total = res['total']
		comments = res['comments']

		for comment in comments:
			comment_item = CommentItem()
			comment_item["song_id"] = song_id
			comment_item["song_name"] = song_name
			comment_item["artist_id"] = artist_id
			comment_item["artist_name"] = artist_name
			comment_item["total"] = total
			comment_item["content"] = comment['content']
			comment_item["like_count"] = comment['likedCount']
			yield comment_item
