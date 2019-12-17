# -*- coding: utf-8 -*- 
# @Time : 2019/11/19 22:41
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : run_timer.py 
# @Software: PyCharm


import os
import time

if __name__ == '__main__':
    while True:
        os.system("scrapy crawl artist")
        # 定时执行: 2小时(60*60*2)/次
        time.sleep(5)
