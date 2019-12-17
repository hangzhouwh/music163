# -*- coding: utf-8 -*- 
# @Time : 2019/11/21 14:50
# @Author : hangzhouwh 
# @Email: hangzhouwh@gmail.com
# @File : file_tool.py 
# @Software: PyCharm
import os


def eachFile(filepath):
    pathDir = os.listdir(filepath)
    files = []
    for allDir in pathDir:
        child = os.path.join('%s%s' % (filepath, allDir))
        files.append(child)
    return files


if __name__ == "__main__":
    eachFile('D:\\wuh_workspace\\music163\\music163\\data\\album')