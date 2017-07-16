# -*- coding:utf-8 -*-

# 对movie_step5_add步未能提取到的数据缩小范围进行提取，每本提取一次。
import time
import os.path
from src.movie.tools import Tag_manager
from src.tool.ExcelManager import listFiles, readExcel, writeExcel
from src.movie.tools.Tag_manager import makeMovieListInfo
start = time.clock()
putplace = 'movie_message_order_by_year'

# 判断存放位置是否存在
if os.path.exists(putplace):
    pass
else:  # 否则新建
    print('新建电影提取存放excel处：'+putplace)
    os.makedirs(putplace)

taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_year_tag.xlsx')  # 读取标签列表
del taglist[0]   # 第一行删去，因为没有实际意思，是table的属性说明。真正的内容从第二行开始
# 对于每个标签
for tag in taglist:
    # 电影按照标签存放于文件夹中
    #if __name__ == '__main__':
    mulu = putplace+'/'+tag[0]  # tag[0]是标签名 eg.爱情
    if os.path.exists(mulu):  # 该目录存在，则跳过
        pass
    else:
        os.makedirs(mulu)  # 否则新建文件夹
    excelpath = mulu + '/' + tag[0] + '.xlsx'  # 创建该类标签的excel
    #  存在处理过的excel文件则跳过
    if os.path.exists(excelpath):
        print(excelpath + '已经存在')
        continue
    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_电影/'+tag[0]  # 构造读取文件夹入口
    print('本地提取：'+path)
    # 查找目录下已经抓取的Html
    files = listFiles(path)
    # 遍历分析
    j = len(files)  # 文件长度
    print(j)
    for num in range(1, int(j/10)+1):
        excelpath = mulu + '/' + tag[0] + '.' + str(num)+'.xlsx'  # 创建该类标签的excel
        # 存在处理过的excel文件则跳过
        if os.path.exists(excelpath):  # 2009.1(10页的excel是否存在)
            print(excelpath + '已经存在')
            continue
        for k in range(1, 11):  # 每页一提取
            tagmovies = []
            total = (num-1) * 10 + k
            if total == j:
                try:
                    writeExcel(excelpath1, tagmovies)
                    # print('写入成功：' + excelpath1)
                except:
                    print('写入' + excelpath1 + '失败！！')
                break
            excelpath1 = mulu + '/' + tag[0] + '.' + str(num) + '(' + files[total] + ')' + '.xlsx'
            file = path + '/' + files[total]  # 找到将要访问的文件目录
            print('提取：' + file)
            content = open(file, 'rb').read()  # rb表示以二进制读的方式打开
            movies = Tag_manager.makeMovieListInfo(content)  # 提取电影列表
            tagmovies.extend(movies)  # 把电影放进去（movies是一个列表，使用extend可以将列表中的元素放入tagmovies中，而append会把整个列表当层一个元素放入）
            try:
                writeExcel(excelpath1, tagmovies)
                print('写入成功：' + excelpath1)
            except:
                print('写入' + excelpath1 + '失败！！')

                pass
end = time.clock()
print("提取电影列表总共运行时间 : %.03f 秒" % (end - start))



"""
# 逐条检测。提取失败的网页分别为2009/1740.html,2008/1520.html,2008/220.html,2007/1920.html
file = open('D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_电影/2007/1920.html', 'rb')
content = file.read()
movies = makeMovieListInfo(content)
j = 0
for i in movies:
    movie = []
    try:
        path = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/movie/movie_message_order_by_year/2007/'+str(j)+'.xlsx'
        movie.append(i)
        writeExcel(path, movie)
       # print(i)
        j += 1
    except:
        print(i)
"""
