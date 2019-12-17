# -*- coding: utf-8 -*- 
# @Time : 2019/11/20 2:42
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : time_tool.py 
# @Software: PyCharm
import time


def time_2_date(time_stamp):
    time_array = time.localtime(time_stamp/1000)
    format_time = time.strftime("%Y-%m-%d %H:%M:%S", time_array)
    return format_time


if __name__ == "__main__":
    print(time_2_date(1558086389878))
