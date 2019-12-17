# -*- coding: utf-8 -*- 
# @Time : 2019/12/17 15:07
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : douyin_lyric_proc.py 
# @Software: PyCharm

import re
import ssl
import time

import pandas as pd
import jieba.analyse
import json
import urllib.request
import requests
import numpy as np

from music163.proc import lyric_cloudy
from music163.tool import json_tool


def get_emotions(text, access_token):
    try:
        values = {
            'text': text,
        }

        host = 'https://aip.baidubce.com/rpc/2.0/nlp/v1/sentiment_classify?' + \
               'access_token=' + access_token \
               + '&charset=UTF-8' \
               + '&text=' + text

        response = requests.post(host, json=values).json()
        item_values = []
        items = response['items'][0]
        item_values.append(str(items['sentiment']))
        item_values.append(str(items['confidence']))
        item_values.append(str(items['positive_prob']))
        item_values.append(str(items['negative_prob']))

        return item_values
    except Exception as e:
        print(e)
        return []


def get_access_token():
    client_id = 'CwqN23lRUzBG8lEGjFrDLP4Y'
    client_secret = 'LlX7jAv8pGCz4bGYlDxDLKtoal8Udc1g'
    host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id=' + client_id \
           + '&client_secret=' + client_secret
    request = urllib.request.Request(host)
    request.add_header('Content-Type', 'application/json; charset=UTF-8')
    response = urllib.request.urlopen(request)
    content = json.loads(response.read())
    access_token = content['access_token']
    return access_token


def get_douyin_high_frequency_word():
    songs = json_tool.load_json('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\douyin\\douyin_lyric.json')

    word_lists = []
    count = 0

    for song in songs:
        lyric = song['lyric']
        wash_list = lyric_cloudy.wash(lyric)
        word_list = lyric_cloudy.word_spilt(wash_list)
        word_list = lyric_cloudy.filter_stopwords(word_list)
        word_lists.extend(word_list)
        count += 1
        print(count, '/', len(songs))

    str = '~!@#$%^&*()'
    for word in reversed(word_lists):
        if re.search('[a-z]', word) or word in str:
            word_lists.remove(word)

    word_frequency = lyric_cloudy.get_word_frequency(word_lists)
    word_rate = lyric_cloudy.cal_word_rate(word_frequency)

    key = []
    key_fre = []
    key_rate = []
    for word in word_frequency:
        if word[1] >= 10:
            key.append(word[0])
            key_fre.append(word[1])
            key_rate.append(word_rate.get(word[0]))

    df = pd.DataFrame([key, key_fre, key_rate], index=['word', 'frequency', 'rate'])
    df = pd.DataFrame(df.values.T, index=df.columns, columns=df.index)
    df.to_csv('D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\抖音高频词.csv', encoding='utf_8_sig')


# 文本摘要
def make_summary(text):
    text = text.lower()  # 如果有英文,全部变成小写

    # 基于 TF-IDF 算法的关键词抽取
    tfidf_x = []
    tfidf_w = []
    # tags = jieba.analyse.extract_tags(text, topK=5)
    # print(",".join(tags))
    for x, w in jieba.analyse.extract_tags(text, topK=20, withWeight=True):
        tfidf_x.append(x)
        tfidf_w.append(w)
    tfidf = [tfidf_x, tfidf_w]

    # 基于 TextRank 算法的关键词抽取
    textrank_x = []
    textrank_w = []
    # tags = jieba.analyse.textrank(text, topK=5)
    # print(",".join(tags))
    for x, w in jieba.analyse.textrank(text, topK=20, withWeight=True):
        textrank_x.append(x)
        textrank_w.append(w)
    textrank = [textrank_x, textrank_w]

    return tfidf, textrank


def get_lyric_summary():
    # songs = json_tool.load_json('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\douyin\\douyin_lyric.json')
    songs = json_tool.load_json('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\csps_lyric\\csps_lyrics.json')

    word_lists = []
    douyin_summary = []
    for song in songs:
        lyric = song['lyric']
        song_name = song['song_name']
        artist_name = song['artist_name']
        wash_list = lyric_cloudy.wash(lyric)
        word_list = lyric_cloudy.word_spilt(wash_list)
        word_list = lyric_cloudy.filter_stopwords(word_list)
        text = ''.join(wash_list)
        tfidf, textrank = make_summary(text)

        tfidf_txt = ','.join(tfidf[0])
        textrank_txt = ','.join(textrank[0])
        douyin_dict = {'song_name': song_name, 'artist_name': artist_name, 'tfidf': tfidf_txt, 'textrank':textrank_txt}
        douyin_summary.append(douyin_dict)

    # file_output = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\抖音歌词摘要.json'
    file_output = 'D:\\WorkSpace\\Pycharm\\music163\\music163\\result\\csps_歌词摘要.json'
    json_tool.write_json(douyin_summary, file_output)


def douyin_mood():
    ssl._create_default_https_context = ssl._create_unverified_context
    access_token = get_access_token()

    songs = json_tool.load_json('D:\\WorkSpace\\Pycharm\\music163\\music163\\data\\douyin\\douyin_lyric.json')
    count = [0, 0]
    cnt = 0
    for song in songs:
        cnt += 1
        print(cnt, '/', len(songs))
        lyric = song['lyric']
        song_name = song['song_name']
        artist_name = song['artist_name']

        positive = 0
        negative = 0
        wash_list = lyric_cloudy.wash(lyric)
        # print(song_name)
        for str in wash_list:
            time.sleep(1)
            ans = get_emotions(str, access_token)
            # print(len(ans))
            # print(str)
            positive += float(ans[2])
            negative += float(ans[3])

        if positive > negative:
            mood = 1
        elif positive == negative:
            mood = np.random.randint(0, 2)
        else:
            mood = 0

        if mood == 0:
            count[0] += 1
            print('n')
        else:
            count[1] += 1
            print('p')

    # print("n", count[0])
    # print("p", count[1])



if __name__ == "__main__":
    douyin_mood()

