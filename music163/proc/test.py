# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 18:16
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : test.py 
# @Software: PyCharm
import re

string = "WARNING:tensorflow: 20181011 15:28:39 Initialize training"
pattern = re.compile(r'\d{4}')
res = pattern.findall(string)
print(res)
# ['20181011 15:28:39']
