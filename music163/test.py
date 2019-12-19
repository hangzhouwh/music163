# -*- coding: utf-8 -*- 
# @Time : 2019/11/20 2:06
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : test.py 
# @Software: PyCharm
import pandas as pd

from music163.tool import json_tool


file = './data/baike_awards_dirty.json'
datas = json_tool.load_json(file)
ar = []
huojiang_count = []
timing_count = []
for data in reversed(datas):
	artist_id = data['artist_id']
	artist_name = data['artist_name']
	awards = data['awards']
	cnt1 = 0
	cnt2 = 0
	for awd in awards:
		if '获奖' in awd:
			cnt1 += 1
		elif '提名' in awd:
			cnt2 += 1
	ar.append(artist_name)
	huojiang_count.append(cnt1)
	timing_count.append(cnt2)


df = pd.DataFrame([ar, huojiang_count, timing_count], index=['歌手', '获奖次数', '提名次数'])
df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
output = './result/awards_result.csv'
df.to_csv(output, encoding='utf_8_sig')




