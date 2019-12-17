# -*- coding: utf-8 -*-
import json
import socks

import scrapy
from stem.control import Controller


from music163.items import AlbumItem
from music163.tool import json_tool
from music163.tool.time_tool import time_2_date

# controller = Controller.from_port(port=9151)
# controller.authenticate()
# socks.set_default_proxy(socks.SOCKS5)
count = 0


class AlbumSpider(scrapy.Spider):
    name = 'album'
    allowed_domains = ['localhost:3000']

    def start_requests(self):

        artist_data = json_tool.load_json('./data_zero/artist.json')

        for artist in artist_data:
            artist_id = artist["artist_id"]
            ablum_size = artist["album_size"]
            url = 'http://localhost:3000/artist/album?' + 'id=' + str(artist_id) + '&' + 'limit=' + str(ablum_size)

            yield scrapy.Request(url=url, dont_filter=False)

    def parse(self, response):
        global count

        res = json.loads(response.body)
        artist = res['artist']
        artist_id = artist['id']
        albums = res['hotAlbums']

        for album in albums:
            album_item = AlbumItem()
            album_item["album_id"] = album['id']
            album_item["album_name"] = album['name']
            album_item["artist_id"] = artist_id
            album_item["album_pic_url"] = album['blurPicUrl']
            album_item["publish_time"] = time_2_date(album['publishTime'])
            yield album_item
            count = count + 1

        print(count)
        pass