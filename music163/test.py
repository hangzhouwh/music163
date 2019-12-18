# -*- coding: utf-8 -*- 
# @Time : 2019/11/20 2:06
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : test.py 
# @Software: PyCharm
from music163.tool import json_tool


str = ['1', '2', '(3)', '4', '(5)']
tmp = ''
a = []
xxx = 0
for i in range(len(str)):
	if '(' in str[i] and ')' in str[i]:
		ssss = ''.join(str[xxx:i+1])
		xxx = i+1
		a.append(ssss)

print(1)



