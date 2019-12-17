# -*- coding: utf-8 -*- 
# @Time : 2019/12/9 16:24
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : baidu_artist.py 
# @Software: PyCharm
import re
import time

import scrapy

from music163.items import BaikeArtistItem
from music163.tool import json_tool

artist_count = 0
request_count = 0


class BaiduArtistSpider(scrapy.Spider):
	name = 'baidu_artist'
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
		baike_artist_item = BaikeArtistItem()

		artist_id = response.meta['artist_id']
		artist_name = response.meta['artist_name']
		# artist_name  # 中文名
		# nationality  # 国籍
		# nation  # 民族
		# occupation  # 职业
		# birthday  # 出生日期
		# IBEC  # 经济公司
		# is_changed_name  # 是否改过名（有原名）
		# university  # 毕业院校

		attr_name = response.xpath('//dt[@class="basicInfo-item name"]//text()').extract()  # 属性名称
		attr_value_selector = response.xpath('//dd[@class="basicInfo-item value"]')  # 属性值选择器
		attr_value = attr_value_selector.xpath('string(.)').extract()  # 属性值

		attr_name_list = []
		attr_value_list = []

		pattern = r'^\[\d{1,2}]$'

		for i in range(len(attr_name)):
			attr_name[i] = attr_name[i].replace("\xa0", "")

			# 删除重复项
			if '展开' in attr_value[i] and '收起' in attr_value[i]:
				attr_value[i] = 'null'

			cut_txt = attr_value[i].replace("\xa0", "")
			txt_list = re.split("、|\n", cut_txt)

			for j in range(len(txt_list)):
				if '' in txt_list:
					txt_list.remove('')
				if '展开' in txt_list:
					txt_list.remove('展开')
				if '收起' in txt_list:
					txt_list.remove('收起')
				for txt in txt_list:
					if re.match(pattern, txt):
						txt_list.remove(txt)

			if attr_value[i] != 'null':
				attr_name_list.append(attr_name[i])
				attr_value_list.append(txt_list)

		baike_artist_item['artist_id'] = artist_id
		baike_artist_item['artist_name'] = artist_name
		baike_artist_item['attr_name'] = attr_name_list
		baike_artist_item['attr_value'] = attr_value_list

		global artist_count
		artist_count = artist_count + 1
		print("爬取歌手百科信息： ", artist_count)

		yield baike_artist_item
