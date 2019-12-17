# -*- coding: utf-8 -*- 
# @Time : 2019/11/28 16:26
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : song_lyric.py
# @Software: PyCharm

import json
import re
import time
import scrapy

from music163.items import SongLyricItem
from music163.tool import file_tool, json_tool


song_count = 0


class SongLyricSpider(scrapy.Spider):
    name = 'song_lyric'
    allowed_domains = ['localhost:3000']

    def start_requests(self):
        file_count = 0
        files = file_tool.eachFile('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\song\\')
        for file in files:
            print("-------------这是第 ", file_count, " songfile-------------")
            file_count = file_count + 1
            song_data = json_tool.load_json(file)
            # time.sleep(10)
            for song in song_data:
                song_id = song["song_id"]

                url = 'http://localhost:3000/lyric?' + 'id=' + str(song_id)
                # url = 'http://localhost:3000/lyric?' + 'id=' + str(song_id) + '&proxy=http://' + getproxies()

                yield scrapy.Request(url=url, dont_filter=False)

    def parse(self, response):
        global song_count

        res = json.loads(response.body)
        song_lyric_item = SongLyricItem()

        song_id = response.url.replace("http://localhost:3000/lyric?id=", "")
        if 'uncollected' in res.keys() or 'nolyric' in res.keys():
            song_lyric_item["song_id"] = song_id
            song_lyric_item["content"] = None
        else:
            song_lyric_item["song_id"] = song_id
            lyric = res['lrc']['lyric']
            lyric = re.sub('\[\d{2}:\d{2}.\d{2,3}\]', '', lyric)
            song_lyric_item["content"] = lyric

        if song_count % 1000 == 0:
            time.sleep(10)
        song_count = song_count + 1
        print("爬取第 ", song_count, " 首单曲的歌词")
        yield song_lyric_item
