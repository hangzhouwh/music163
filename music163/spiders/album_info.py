# -*- coding: utf-8 -*- 
# @Time : 2019/11/21 0:52
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : album_info.py 
# @Software: PyCharm


# -*- coding: utf-8 -*-
import json
import random
import time

import requests
import scrapy
# import socks


from music163.items import AlbumInfoSongItem
from music163.tool import json_tool, file_tool, proxy_tool

album_count = 0
song_count = 0


class AlbumInfoSpider(scrapy.Spider):
    name = 'album_info'
    allowed_domains = ['localhost:3000']

    def start_requests(self):
        # ip = requests.get("http://checkip.amazonaws.com").text
        # print("第*********次IP： ", ip)

        file_count = 0
        files = file_tool.eachFile('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\album\\')
        for file in files:
            print("-------------这是第 ", file_count, " 个albumfile-------------")
            print(file)
            file_count = file_count + 1
            # time.sleep(5)
            print("Wake Up !!!!!!!!!")
            album_data = json_tool.load_json(file)
            for album in album_data:
                time.sleep(0.05)
                album_id = album["album_id"]
                url = 'http://localhost:3000/album?' + 'id=' + str(album_id)
                print(url)
                yield scrapy.Request(url=url, dont_filter=False)

    def parse(self, response):
        global album_count, song_count

        res = json.loads(response.body)
        album = res['album']
        info = album['info']
        songs = res['songs']
        introduction = album['description']
        comment_count = info['commentCount']
        like_count = info['likedCount']
        share_count = info['shareCount']
        album_id = album['id']

        # 这里需要跑两轮，第一次跑album_info, 第二次跑song, 因为要同时写两个文件
        # 或者先写在同一个文件中，之后再进行处理

        for song in songs:
            album_info_song_item = AlbumInfoSongItem()
            album_info_song_item["album_id"] = album_id
            album_info_song_item["introduction"] = introduction
            album_info_song_item["comment_count"] = comment_count
            album_info_song_item["like_count"] = like_count
            album_info_song_item["share_count"] = share_count
            album_info_song_item['song_id'] = song['id']
            album_info_song_item['song_name'] = song['name']

            song_count = song_count + 1
            print("这是第 ", song_count, " 首单曲")
            yield album_info_song_item

        album_count = album_count + 1
        pass