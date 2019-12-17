# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 20:18
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : original_proc.py 
# @Software: PyCharm

import jieba.posseg as pseg

from music163.tool import json_tool
words =pseg.cut("我爱北京天安门")
for w in words:
	print(w.word, w.flag)


file = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\rank_list_data\\original_lyric.json'
data = json_tool.load_json(file)


