# -*- coding: utf-8 -*- 
# @Time : 2019/12/16 23:29
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : simi_artist.py 
# @Software: PyCharm
import json

import scrapy

from music163.tool import json_tool


ar_count = 0

class SimiArtistSpider(scrapy.Spider):
	name = 'simi_artist'
	allowed_domains = ['localhost:3000']

	def start_requests(self):
		global ar_count
		artists = []
		codes = [1001, 1002, 1003]
		for code in codes:
			filepath = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\artist\\artist_' + str(code) +'.json'
			ars = json_tool.load_json(filepath)
			artists.extend(ars)

		url_head = 'http://localhost:3000/simi/artist?id='

		artists = sorted(artists, key=lambda e: e.__getitem__('music_size'), reverse=True)

		for artist in artists:
			if ar_count == 500:
				break
			artist_id = artist['artist_id']
			artist_name = artist['artist_name']
			url = url_head + str(artist_id)
			yield scrapy.Request(url=url, meta={'artist_id': artist_id, 'artist_name': artist_name}, dont_filter=False)
			ar_count += 1

	def parse(self, response):
		res = json.loads(response.body)

		artist_id = response.meta['artist_id']
		artist_name = response.meta['artist_name']

		pass
		#
		# 	csps_lyric_item = CSPSLyricItem()
		# 	csps_lyric_item["song_name"] = artist_name
		# 	csps_lyric_item["artist_name"] = song_name
		# 	csps_lyric_item["lyric"] = lyric
		#
		# 	song_count += 1
		# 	print("热门音乐:  ", song_count)
		#
		# 	if song_count % 500 == 0:
		# 		sec = random.randint(3, 9)
		# 		print('休眠 ', sec, 's')
		# 		time.sleep(sec)
		#
		# 	yield csps_lyric_item
		# else:
		# 	pass
