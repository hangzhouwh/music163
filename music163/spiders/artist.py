# -*- coding: utf-8 -*-
import json
import time

import requests
import scrapy
from music163.items import ArtistItem
import numpy as np

count = 0



class ArtistSpider(scrapy.Spider):
    name = 'artist'
    allowed_domains = ['localhost:3000']

    def start_requests(self):
        ip = requests.get("http://checkip.amazonaws.com").text
        print("第 ", count, " 次IP: ", ip)  # 查看包装的ip
        cats = [1001, 1002, 1003, 2001, 2002, 2003, 6001, 6002, 6003, 7001, 7002, 7003, 4001, 4002, 4003]
        # cats = [5001]
        url_begin = 'http://localhost:3000/artist/list?'
        limit = 100

        initial = [0]
        letter = 65
        cnt = 0
        while cnt < 26:
            initial.append(letter)
            letter += 1
            cnt+=1

        for cat in cats:
            for i in initial:
                url = url_begin + 'cat=' + str(cat) + '&' + 'initial=' + str(i) + '&' + 'limit=' + str(limit)
                yield scrapy.Request(url=url, dont_filter=False)

    def parse(self, response):
        global count

        artists = json.loads(response.body)
        artists = artists['artists']

        for artist in artists:
            artist_item = ArtistItem()
            # artist_id = artist['id']
            # name = artist['name']
            # album_size = artist['albumSize']
            # music_size = artist['musicSize']
            # pic_url = artist['picUrl']
            artist_item["artist_id"] = artist['id']
            artist_item["artist_name"] = artist['name']
            artist_item["album_size"] = artist['albumSize']
            artist_item["music_size"] = artist['musicSize']
            artist_item["artist_pic_url"] = artist['picUrl']
            yield artist_item
            count = count + 1

        if count % 1000 == 0:
            time.sleep(np.random.randint(1, 10))
        print("目前抓取歌手 ", count, " 位")
        pass