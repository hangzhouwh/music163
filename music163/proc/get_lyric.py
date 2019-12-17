# -*- coding: utf-8 -*- 
# @Time : 2019/12/15 16:21
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : get_lyric.py
# @Software: PyCharm


# 对歌数据词进行操作，要求输入一个时间，输出对应时间的歌词内容
# 1、将原始歌词按行存进列表
# 2、将时间和歌词信息分开
# 3、将时间转换成以秒为单位的浮点型数据
# 4、以时间为键，将其对应的歌词存进字典
# 5、利用字典指定输出

musicLrcDict = {}  # 用于存储时间和歌词的字典

musicLrcStr = """
[00:00.000] 作曲 : 吴剑泓
[00:01.000] 作词 : 林利南/林秋离
[00:19.180]你有多久没有看过那片海
[00:24.589]你到现在对自己究竟多明白
[00:30.379]总是不服输
[00:35.000]永远要比别人快
[00:38.290]在你前方是否有你要的未来
[00:45.100]想到我们的过去
[00:47.529]都让人感慨
[00:52.690]希望所有好朋友都能站起来
[01:00.300]还有你曾经
[01:03.190]疯狂爱上的女孩
[01:06.800]再过几年是不是依旧难以忘怀
[01:14.129]可是andy 活着是不须道理
[01:20.989]谁都可能
[01:24.900]暂时的失去勇气
[01:27.189]外面不安的世界
[01:31.090]骚动的心情
[01:34.489]不能熄灭曾经你拥有炽热的心
[01:42.300]我是真的不会表达我的爱
[01:48.900]却很在乎每个人对我的期待
[01:56.700]平凡的角色
[02:00.100]站在小小的舞台
[02:02.700]我有那么勇敢地说出来
[02:38.728]想到我们的过去
[02:41.046]都让人感慨
[02:44.846]希望所有好朋友都能站起来
[02:54.173]还有你曾经
[02:56.656]疯狂爱上的女孩
[02:59.561]再过几年是不是依旧难以忘怀
[03:06.460]可是andy 活着是不须道理
[03:14.067]谁都可能
[03:18.528]暂时的失去勇气
[03:20.647]外面不安的世界
[03:24.988]骚动的心情
[03:28.620]不能熄灭曾经你拥有炽热的心
[03:34.955]我是真的不会表达我的爱
[03:41.946]却很在乎每个人对我的期待
[03:49.967]平凡的角色
[03:54.118]站在小小的舞台
[03:58.064]我有那么勇敢地说出来
[04:18.940]外面不安的世界
[04:23.269]骚动的心情
[04:26.584]不能熄灭曾经你拥有炽热的心
[04:33.690]可是andy
[04:36.900]Oh…Oh…Oh
[04:41.280]andy  Oh…Oh…Oh
[04:47.989]外面不安的世界
[04:50.917]骚动的心情
[04:54.768]不能熄灭曾经你拥有炽热的心
"""

def get_x(musicLrcStr, time):
    # 将原始数据按行存储进列表
    musicLrcList = musicLrcStr.splitlines()
    # 分开时间和歌词
    for lrcLine in musicLrcList:
        lrcLineList = lrcLine.split("]")  # 以“]”为分隔进行切割
        for n in range(len(lrcLineList) - 1):
            timeStr = lrcLineList[n][1:]  # 从下标为一的元素开始取，即弃掉首元素“[”
            timeList = timeStr.split(":")   # 将每个时间的分和秒分开
            timeS = float(timeList[0]) * 60 + float(timeList[1])    # 将时间转化成秒
            musicLrcDict[timeS] = lrcLineList[-1]   # 字典赋值，下标为“-1”表示最后一个元素
    # print(musicLrcDict)

    allTimeList = []    # 存储所有时间，用于排序
    for t in musicLrcDict:  # 访问字典的键
        allTimeList.append(t)   # append():在末尾添加元素
    allTimeList.sort()  # 升序排序并返回排序后的列表
    # 接收时间并输出相应歌词

    getTime = float(time)
    for i in range(len(allTimeList)):
        if getTime < allTimeList[i]:
            break
    if getTime < allTimeList[0]:
        print("时间太小了，什么也没有……")
    else:
        print(musicLrcDict[allTimeList[i - 1]])


if __name__ == "__main__":
    get_x(musicLrcStr, 35)
