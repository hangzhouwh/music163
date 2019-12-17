# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 14:50
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : douyin_rank.py 
# @Software: PyCharm
import json

import scrapy

from music163.items import CSPSLyricItem
from music163.tool import json_tool


class DouyinRankSpider(scrapy.Spider):
	name = 'douyin'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		filepath = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\rank_list\\抖音排行榜.json"
		data = json_tool.load_json(filepath)
		url_head = 'http://localhost:3000/lyric?id='
		playlist = data['playlist']
		for song in playlist['tracks']:
			song_id = song['id']
			song_name = song['name']
			artist_name = song['ar'][0]['name']
			url = url_head + str(song_id)
			yield scrapy.Request(url=url,
								 meta={'artist_name': artist_name, 'song_name': song_name},
								 dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)

		song_name = response.meta['song_name']
		artist_name = response.meta['artist_name']

		if 'lrc' in res.keys() and 'lyric' in res['lrc'].keys():
			lrc = res['lrc']
			lyric = lrc['lyric']

			csps_lyric_item = CSPSLyricItem()
			csps_lyric_item["song_name"] = artist_name
			csps_lyric_item["artist_name"] = song_name
			csps_lyric_item["lyric"] = lyric
			yield csps_lyric_item

		else:
			pass
