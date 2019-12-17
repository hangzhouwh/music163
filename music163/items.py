# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Music163Item(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


class ArtistItem(scrapy.Item):
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    album_size = scrapy.Field()
    music_size = scrapy.Field()
    artist_pic_url = scrapy.Field()


class AlbumItem(scrapy.Item):
    album_id = scrapy.Field()
    album_name = scrapy.Field()
    artist_id = scrapy.Field()
    album_pic_url = scrapy.Field()
    publish_time = scrapy.Field()


class AlbumInfoSongItem(scrapy.Item):
    album_id = scrapy.Field()
    introduction = scrapy.Field()
    comment_count = scrapy.Field()
    like_count = scrapy.Field()
    share_count = scrapy.Field()
    song_id = scrapy.Field()
    song_name = scrapy.Field()


class SongLyricItem(scrapy.Item):
    song_id = scrapy.Field()
    content = scrapy.Field()


class SongUrlItem(scrapy.Item):
    song_id = scrapy.Field()
    song_url = scrapy.Field()


class SongCommentCountItem(scrapy.Item):
    song_id = scrapy.Field()
    song_comment_count = scrapy.Field()


class SongCanPlayItem(scrapy.Item):
    song_id = scrapy.Field()
    song_can_play = scrapy.Field()


class BaikeArtistItem(scrapy.Item):
    attr_name = scrapy.Field()
    attr_value = scrapy.Field()
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()


class ChinesePopularSongItem(scrapy.Item):
    artist_id = scrapy.Field()
    artist_name = scrapy.Field()
    song_id = scrapy.Field()
    song_name = scrapy.Field()


class CSPSLyricItem(scrapy.Item):
    song_name = scrapy.Field()
    artist_name = scrapy.Field()
    lyric = scrapy.Field()


class CommentItem(scrapy.Item):
    song_name = scrapy.Field()
    artist_name = scrapy.Field()
    total = scrapy.Field()
    content = scrapy.Field()
    like_count = scrapy.Field()