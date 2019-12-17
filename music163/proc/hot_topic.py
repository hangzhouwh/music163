# -*- coding: utf-8 -*- 
# @Time : 2019/12/16 22:00
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : hot_topic.py 
# @Software: PyCharm


from music163.tool import json_tool
import pandas as pd


filepath = 'D:\WorkSpace\Pycharm\music163\music163\data\hot_topic.json'
topics = json_tool.load_json(filepath)
titles = []
count = []

for topic in topics['hot']:
	title = topic['title']
	participate_count = topic['participateCount']
	titles.append(title)
	count.append(participate_count)

df = pd.DataFrame([titles, count], index=['topic', 'participate_count'])
df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\hot_topic.csv', encoding='utf-8')
