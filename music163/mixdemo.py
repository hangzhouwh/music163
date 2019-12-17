# -*- coding: utf-8 -*- 
# @Time : 2019/12/16 16:02
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : mixdemo.py 
# @Software: PyCharm

import sys


def func(a, b):
	return (a + b)


if __name__ == '__main__':
	a = []
	for i in range(1, len(sys.argv)):
		a.append((int(sys.argv[i])))

	print(func(a[0], a[1]))