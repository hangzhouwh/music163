# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 19:35
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : douyin_comment.py 
# @Software: PyCharm
import json

import scrapy

from music163.items import CSPSLyricItem, CommentItem
from music163.tool import json_tool


class DouyinCommentSpider(scrapy.Spider):
	name = 'douyin_comment'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		filepath = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\rank_list\\抖音排行榜.json"
		data = json_tool.load_json(filepath)
		url_head = 'http://localhost:3000/comment/music?id='
		playlist = data['playlist']
		for song in playlist['tracks']:
			song_id = song['id']
			song_name = song['name']
			artist_name = song['ar'][0]['name']
			url = url_head + str(song_id) + '&limit=5000'
			yield scrapy.Request(url=url,
								 meta={'artist_name': artist_name, 'song_name': song_name},
								 dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)

		song_name = response.meta['song_name']
		artist_name = response.meta['artist_name']
		total = res['total']
		hot_comments = res['hotComments']
		for comment in hot_comments:
			comment_item = CommentItem()
			comment_item["song_name"] = artist_name
			comment_item["artist_name"] = song_name
			comment_item["total"] = total
			comment_item["content"] = comment['content']
			comment_item["like_count"] = comment['likedCount']
			yield comment_item


