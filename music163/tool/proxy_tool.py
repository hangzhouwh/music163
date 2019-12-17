# import requests
# import random
#
# ip_pool = []
#
#
# def load_ip():
#     url = 'http://piping.mogumiao.com/proxy/api/get_ip_bs?appKey=5acdfc535a114292bc4cad6f8bc8658c&count=10&expiryDate=0&format=1&newLine=2'
#     resq = requests.get(url)
#     data = resq.json()
#     ip_pool_update = data['msg']
#     global ip_pool
#     ip_pool.extend(ip_pool_update)
#     print(ip_pool)
#
#
# def getproxies():
#     b = random.choice(ip_pool)
#     d = '%s:%s' % (b['ip'], b['port'])
#     return d
#
#
# def test_ip(proxy):
#     url = 'http://localhost:3000/lyric?id=33894312' + '&proxy=http://' + proxy
#     res = requests.get(url)
#     if res.status_code == 200:
#         return proxy
#     else:
#         return False
#
#
# if __name__ == "__main__":
#     load_ip()
#     proxy = getproxies()
#     test_ip(proxy)
#     pass
#
