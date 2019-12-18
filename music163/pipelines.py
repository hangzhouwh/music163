# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html


import MySQLdb
from scrapy.exporters import JsonItemExporter
from twisted.enterprise import adbapi


# 默认Pipeline(无用)
class Music163Pipeline(object):
    def process_item(self, item, spider):
        return item


# 采用同步的机制写入mysql
class MysqlPipeline(object):
    def __init__(self):
        # 获取connect
        # host,user,pwd,dbname,charset(写入数据库的编码),use_unicode=True
        self.conn = MySQLdb.connect('139.9.63.6', 'root', '123456', 'music163', charset="utf8", use_unicode=True)
        # 获取cursor(实际上是通过cursor进行操作的)
        self.cursor = self.conn.cursor()

    # 需要重载下述方法
    def process_item(self, item, spider):
        """
        爬取高校列表的插入语句
        """
        insert_sql = """
            insert into artist(id, name, album_size, music_size, pic_url)
            VALUES (%s, %s, %s, %s, %s)
        """
        # 执行sql语句，需要写入填充值
        self.cursor.execute(insert_sql, (item["id"], item["name"],
                                         item["album_size"], item["music_size"],
                                         item["pic_url"]))
        # 提交事务（必须要有！）
        self.conn.commit()


# 采用异步的机制写入mysql
class MysqlTwistedPipeline(object):
    def __init__(self, dbpool):
        self.dbpool = dbpool

    @classmethod
    def from_settings(cls, settings):
        # from_settings在spider初始化时被调用，会将setting中的值传递进来
        # 连接参数存在dict(可变化的参数方式)，参数名称需要与connect源码中的名称相同
        dbparms = dict(
            host=settings["MYSQL_HOST"],
            db=settings["MYSQL_DBNAME"],
            user=settings["MYSQL_USER"],
            passwd=settings["MYSQL_PASSWORD"],
            charset='utf8',
            cursorclass=MySQLdb.cursors.DictCursor,
            use_unicode=True,
        )
        # from twisted.enterprise import adbapi 可以将mysqldb的一些操作变成异步操作
        # 使用连接池:第一个指明dbmsql的name  第二个指明连接的参数(即上面的dict)
        dbpool = adbapi.ConnectionPool("MySQLdb", **dbparms)
        # cls即class
        return cls(dbpool)

    def process_item(self, item, spider):
        # 使用twisted将mysql插入变成异步执行
        # para1: 定义的函数，将该函数变成异步的
        # para2: item，需要插入的数据
        query = self.dbpool.runInteraction(self.do_song_insert, item)
        # 异常处理
        # para1:定义的异常处理的方式
        query.addErrback(self.handle_error)

    def handle_error(self, failure):
        # 处理异步插入的异常
        print(failure)

    def do_artist_insert(self, cursor, item):
        # 执行具体的插入
        # 根据不同的item 构建不同的sql语句并插入到mysql中

        # 歌手信息, artist表
        insert_sql = """
             insert into artist(artist_id, name, album_size, music_size, pic_url)
             VALUES (%s, %s, %s, %s, %s)
         """
        # 执行sql语句，需要写入填充值
        cursor.execute(insert_sql, (item["artist_id"], item["name"],
                                    item["album_size"], item["music_size"],
                                    item["pic_url"]))

    def do_album_insert(self, cursor, item):
        # 专辑信息, album表
        insert_sql = """
             insert into album(album_id, album_name, artist_id, blur_pic_url)
             VALUES (%s, %s, %s, %s)
         """
        cursor.execute(insert_sql, (item["album_id"], item["album_name"],
                                    item["artist_id"], item["blur_pic_url"]))

    def do_song_insert(self, cursor, item):
        # 单曲信息, song表
        insert_sql = """
             insert into song(song_id, song_name, album_id, artist_id)
             VALUES (%s, %s, %s, %s)
         """
        cursor.execute(insert_sql, (item["song_id"], item["song_name"],
                                    item["album_id"], item["artist_id"]))


# scrapy提供的export支持多种文件格式
# 调用scrapy提供的json export导出json文件
class JsonExporterPipleline(object):
    def __init__(self):
        # wb代表二进制文件
        self.file = open('./data_zero/comment_king_cotent.json', 'wb')
        # ensure_ascii=False 保证中文不出现问题
        # 需要传递exporter，并且需要使用JsonItemExporter进行实例化
        self.exporter = JsonItemExporter(self.file, encoding="utf-8", ensure_ascii=False)
        self.exporter.start_exporting()

    def close_spider(self, spider):
        self.exporter.finish_exporting()  # 停止导出
        self.file.close()  # 关闭

    def process_item(self, item, spider):
        self.exporter.export_item(item)
        return item