# coding=utf-8
import os
import string

import requests
from multiprocessing.dummy import Pool as ThreadPool
import time
from random import random
from src.tool.catch_detail_url import catch_url
from src.tool.DbManager import DbManager
from src.tool.ExcelManager import validateTitle

# 电影html恢复
list=['2016']
for year in list:
    rootdir = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/movie_detail_message/'+year+'/'
    prefix = '.htmllockl'
    files = os.listdir(rootdir)
    for filename in files:
        newname = filename
        newname = newname.split(".")
        if newname[-1] == "htmllockl":
            newname[-1] = "html"
            newname = '.'.join(newname)
            filename = rootdir+filename
            newname = rootdir+newname
            try:
                os.rename(filename, newname)
                print(newname, "updated successfully")
            except FileExistsError as e:
                  raise
# 图书html恢复
# list=['文学']
# for tag in list:
#     rootdir = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/book_detail_message/'+tag+'/'
#     prefix = '.htmllockl'
#     files = os.listdir(rootdir)
#     for filename in files:
#         newname = filename
#         newname = newname.split(".")
#         if newname[-1] == "htmllockl":
#             newname[-1] = "html"
#             newname = '.'.join(newname)
#             filename = rootdir+filename
#             newname = rootdir+newname
#             try:
#                 os.rename(filename, newname)
#                 print(newname, "updated successfully")
#             except FileExistsError as e:
#                   raise








