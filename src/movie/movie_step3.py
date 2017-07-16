# -*- coding:utf-8 -*-
from src.movie.tools import Tag_manager
from src.movie.tools.Tag_manager import makeMovieListInfo, makeMovieInfo

"""
# 提取标签页到excel
file = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_tag.html', 'rb')
content = file.read()
Tag_manager.makeMovieTag(content, r'D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_tag.xlsx')
"""



# 测试抓取单部电影的函数（makeMovieInfo）是否正确
print('D:\workplace\pythonwork\douban_book_catch_zzq\src\movie_detail_message\\1992/1293124惊情四百年.html')
file = open('D:\workplace\pythonwork\douban_book_catch_zzq\src\movie_detail_message\\1992/1293124惊情四百年.html', 'rb')  # 读取文件
content = file.read()
movie = makeMovieInfo(content)
for i in movie:
    print('*' * 50)  # 分割一下，方便查看
    print(i)  # 打印一下内容
    # print('*' * 50)  # 分割一下，方便查看


"""
# 测试抓取一个页面的电影信息
file = open('D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_电影/2009/1740.html', 'rb')
content = file.read()
movies = makeMovieListInfo(content)
for i in movies:
    print(i)
    """

