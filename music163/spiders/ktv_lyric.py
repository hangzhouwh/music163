# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 19:20
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : ktv_lyric.py 
# @Software: PyCharm
import scrapy
from pandas._libs import json

from music163.items import CSPSLyricItem
from music163.tool import json_tool


class KtvLyricSpider(scrapy.Spider):
	name = 'ktv'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		# # codes = [1, 2, 3, 4, 5]
		# codes = [1, 2]
		# for code in codes:
		# 	filepath = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\rank_list\\网易原创歌曲榜_week" + str(code) + ".json"
		# 	data = json_tool.load_json(filepath)
		# 	url_head = 'http://localhost:3000/lyric?id='
		# 	playlist = data['playlist']
		# 	for song in playlist['tracks']:
		# 		song_id = song['id']
		# 		song_name = song['name']
		# 		artist_name = song['ar'][0]['name']
		# 		url = url_head + str(song_id)
		# 		yield scrapy.Request(url=url,
		# 							 meta={'artist_name': artist_name, 'song_name': song_name},
		# 							 dont_filter=False)

		file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\simi\\simi_song.json'
		song_data = json_tool.load_json(file)
		for song in song_data:
			song_id = song["song_id"]
			song_name = song['song_name']
			artist_name = song['artist_name']
			url = 'http://localhost:3000/lyric?' + 'id=' + str(song_id)
			# url = 'http://localhost:3000/lyric?' + 'id=' + str(song_id) + '&proxy=http://' + getproxies()

			yield scrapy.Request(url=url,
								 meta={'song_id':song_id, 'artist_name': artist_name, 'song_name': song_name},
								 dont_filter=False)

	def parse(self, response):
		global song_count

		res = json.loads(response.body)

		song_id = response.meta['song_id']
		song_name = response.meta['song_name']
		artist_name = response.meta['artist_name']

		if 'lrc' in res.keys() and 'lyric' in res['lrc'].keys():
			lrc = res['lrc']
			lyric = lrc['lyric']

			csps_lyric_item = CSPSLyricItem()
			csps_lyric_item["song_id"] = song_id
			csps_lyric_item["song_name"] = artist_name
			csps_lyric_item["artist_name"] = song_name
			csps_lyric_item["lyric"] = lyric
			yield csps_lyric_item
		else:
			pass