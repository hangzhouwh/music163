# -*- coding: utf-8 -*- 
# @Time : 2019/11/14 23:40
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : json_tool.py
# @Software: PyCharm
import json
from itertools import groupby
from operator import itemgetter


def load_json(filepath):
    file = open(filepath, 'rb')
    data = json.load(file)
    return data


def write_json(data, filepath):
    with open(filepath, 'w') as f:
        json.dump(data, f)


def distinct(items,key):
    key = itemgetter(key)
    items = sorted(items, key=key)
    return [next(v) for _, v in groupby(items, key=key)]


if __name__ == "__main__":
    data1 = load_json('D:\\wuh_workspace\\music163\\music163\\data_zero\\album_1.json')
    print(len(data1))
    data2 = load_json('D:\\wuh_workspace\\music163\\music163\\data_zero\\album_2.json')
    print(len(data2))
    data = data1
    data.extend(data2)
    print(len(data))
    data_rrr = distinct(data, key='album_id')
    print(len(data_rrr))

    write_json(data, "D:\\wuh_workspace\\music163\\music163\\data_zero\\test.json")