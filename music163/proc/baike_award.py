# -*- coding: utf-8 -*- 
# @Time : 2019/12/19 6:51
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : baike_award.py 
# @Software: PyCharm
import operator

from music163.tool import json_tool

file = '../data/baike_award.json'
datas = json_tool.load_json(file)
for data in reversed(datas):
	if len(data['awards']) == 0:
		datas.remove(data)

award_count = {}
for data in datas:
	artist_name = data['artist_name']
	awards = data['awards']
	award_count[artist_name] = len(awards)

award_count_sorted = sorted(award_count.items(), key=operator.itemgetter(1), reverse=True)
print(1)