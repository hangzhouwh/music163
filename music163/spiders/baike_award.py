# -*- coding: utf-8 -*- 
# @Time : 2019/12/19 4:03
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : baike_award.py 
# @Software: PyCharm
import re

import scrapy

from music163.items import BaikeAwardItem
from music163.tool import json_tool

artist_count = 0
request_count = 0


class BaiduAwardSpider(scrapy.Spider):
	name = 'baidu_award'
	allowed_domains = ['https://baike.baidu.com/']

	def start_requests(self):
		global request_count

		codes = [1001, 1002, 1003]
		for code in codes:
			file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\artist\\artist_' + str(code) + '.json'
			artist_data = json_tool.load_json(file)

			for artist in artist_data:
				request_count += 1
				print("发送Request: ", request_count)
				# if request_count % 1000 == 0:
				# 	time.sleep(5)

				artist_id = artist['artist_id']
				artist_name = artist['artist_name']
				url = 'https://baike.baidu.com/item/' + str(artist_name)
				yield scrapy.Request(url=url, meta={'artist_id': artist_id, 'artist_name':artist_name}, dont_filter=True)

	def parse(self, response):


		x = response.xpath('//h2[@class="title-text"]/span[contains(text(), "获奖记录")]').extract()
		award_table = response.xpath('//ul[@class ="list-module j-common-module"]//text()').extract()
		tables = []
		for line in reversed(award_table):
			if line == '▪':
				award_table.remove(line)
			elif line.strip() == '':
				award_table.remove(line)
			elif '[' in line and ']' in line:
				award_table.remove(line)
		for line in award_table:
			str = line.strip()
			str = str.replace(' ', '')
			str = str.replace('\n', '')
			tables.append(str)

		pattern = r'^\d{4}'
		years = []
		awards = []
		for value in tables:
			if re.match(pattern, value):
				years.append(value)
			else:
				awards.append(value)

		artist_id = response.meta['artist_id']
		artist_name = response.meta['artist_name']

		award_proced = []
		location = 0
		for i in range(len(awards)):
			if '（' in awards[i] and '）' in awards[i]:
				new_str = ''.join(awards[location: i+1])
				location = i + 1
				award_proced.append(new_str)

		awds = []
		if len(award_proced) == len(years):
			for i in range(len(award_proced)):
				x = years[i] + award_proced[i]
				awds.append(x)

		item = BaikeAwardItem()
		item['artist_id'] = artist_id
		item['artist_name'] = artist_name
		item['awards'] = awds
		yield item
