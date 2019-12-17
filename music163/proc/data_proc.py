# -*- coding: utf-8 -*- 
# @Time : 2019/11/20 23:46
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : data_proc.py
# @Software: PyCharm
from collections import ChainMap

from music163.tool.json_tool import load_json, distinct, write_json


def artist_unique():
    data = load_json('D:\\wuh_workspace\\music163\\music163\\data_zero\\album_1.json')


def album_unique():
    data1 = load_json('D:\\wuh_workspace\\music163\\music163\\data_zero\\album_1.json')
    data2 = load_json('D:\\wuh_workspace\\music163\\music163\\data_zero\\album_2.json')

    data = data1
    data.extend(data2)
    data = distinct(data, key='album_id')

    print("一共有 ", len(data), " 条数据！")

    epoch = 10000
    length = int(len(data)/epoch)+1
    for i in range(length):
        if i < length-1:
            data_output = data[i*epoch:(i+1)*epoch-1]
        else:
            data_output = data[i*epoch:-1]
        output_file = "D:\\wuh_workspace\\music163\\music163\\data\\album\\" + "album_" + str(i) + ".json"
        print("正在写入文件 ", i)
        write_json(data_output, output_file)


def album_proc():
    data_new = []
    for i in range(42):
        file1 = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\data_all\\album_" + str(i) + ".json"
        file2 = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data_zero\\album&song\\album&song_" + str(i) + ".json"
        data1 = load_json(file1)
        data2 = load_json(file2)
        data3 = distinct(data2, key='album_id')
        j = 0
        k = 0
        while j < len(data1) and k < len(data3):
            if data1[j]['album_id'] == data3[k]['album_id']:
                del data3[k]['song_id']
                del data3[k]['song_name']
                data_chain = dict(ChainMap(data1[j], data3[k]))
                data_new.append(data_chain)
                j += 1
                k += 1
            else:
                j += 1
        print(i, "       ", j-k)

    data_write = distinct(data_new, key='album_id')

    print("一共有 ", len(data_write), " 条数据！")

    epoch = 10000
    length = int(len(data_write)/epoch)+1
    for i in range(length):
        if i < length:
            data_output = data_write[i*epoch:(i+1)*epoch-1]
        else:
            data_output = data_write[i*epoch:-1]
        output_file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\album\\" + "album_" + str(i) + ".json"
        print("正在写入文件 ", i)
        write_json(data_output, output_file)


# song_id song_name artist_id album_id
def song_proc():
    song_list = []
    for i in range(42):
        file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data_zero\\album&song\\album&song_" + str(i) + ".json"
        data = load_json(file)
        print("正在处理第 ", i, "个文件")
        for j in range(len(data)):
            del data[j]['introduction']
            del data[j]['comment_count']
            del data[j]['like_count']
            del data[j]['share_count']
            song_list.append(data[j])

    song = distinct(song_list, key='song_id')
    print("一共有 ", len(song), " 条数据！")

    epoch = 10000
    length = int(len(song)/epoch)+1
    for i in range(length):
        if i < length-1:
            data_output = song[i*epoch:(i+1)*epoch-1]
        else:
            data_output = song[i*epoch:-1]
        output_file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\" + "song_" + str(i) + ".json"
        print("正在写入文件 ", i)
        write_json(data_output, output_file)


def song_wash():
    song_list = []
    for i in range(360):
        file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\" + "song_" + str(i) + ".json"
        data = load_json(file)
        print("清洗进度 ", i, "/", 360)
        for j in range(len(data)):
            if data[j]['song_id'] < 0:
                data[j]['song_id'] = -data[j]['song_id']

        output_file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\" + "song_" + str(i) + ".json"
        write_json(data, output_file)


def csps_proc():
    song_list = []

    file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\chinese_singer_popular_song\\chinese_singer_popular_songs.json"
    data = load_json(file)

    epoch = 10000
    length = int(len(data)/epoch)+1
    for i in range(length):
        if i < length-1:
            data_output = data[i*epoch:(i+1)*epoch-1]
        else:
            data_output = data[i*epoch:-1]
        output_file = "D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\chinese_singer_popular_song\\" + "csps" + str(i) + ".json"
        print("正在写入文件 ", i)
        write_json(data_output, output_file)


if __name__ == "__main__":
    csps_proc()
