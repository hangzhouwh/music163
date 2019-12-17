import MySQLdb
conn = MySQLdb.connect(host="139.9.63.6", user="root", passwd="123456", db="music163", charset="utf8")
cursor = conn.cursor()


class GetAlbumSize(object):
    def get_album_size(self):
        sql = """
			select artist_id, album_size
			from artist
		"""
        result = cursor.execute(sql)
        return cursor.fetchall()


class GetSong(object):
    def get_song_from_album(self):
        sql = """
        	select album_id
        	from album
        		"""
        result = cursor.execute(sql)
        return cursor.fetchall()


if __name__ == "__main__":
    get = GetSong()
    info = get.get_song_from_album()
    print(info)