# -*- coding: utf-8 -*-
# @Time : 2019/11/5 18:18
# @Author : hangzhouwh
# @Email: hangzhouwh@gmail.com
# @File : main.py
# @Software: PyCharm


from scrapy.cmdline import execute
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

"""
执行Scrapy命令 scrapy crawl <spider>
"""
# execute(["scrapy", "crawl", "artist"])  # 歌手
# execute(["scrapy", "crawl", "album"])  # 专辑
# execute(["scraoy", "crawl", "album_info"])  # 专辑详情
# execute(["scrapy", "crawl", "song_lyric"])  # 歌词
# execute(["scrapy", "crawl", "song_url"])  # 音乐播放URL
# execute(["scrapy", "crawl", "song_can_play"])  # 音乐是否可用
# execute(["scrapy", "crawl", "song_comment_count"])
# execute(["scrapy", "crawl", "baidu_artist"])  # 百度百科歌手信息
# execute(["scrapy", "crawl", "chinese_singer_popular_songs"])  # 华语歌手热门五十首歌曲
# execute(["scrapy", "crawl", "csps_lyric"])  # 华语歌手热门五十首歌曲的歌词
# execute(["scrapy", "crawl", "simi_artist"])  # 相似歌手
# execute(["scrapy", "crawl", "douyin"])  # 抖音排行榜
# execute(["scrapy", "crawl", "ktv"])  # ktv歌词
# execute(["scrapy", "crawl", "douyin_comment"])# 抖音评论
# execute(["scrapy", "crawl", "comment_king"])
execute(["scrapy", "crawl", "baidu_award"])