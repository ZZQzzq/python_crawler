# -*- coding:utf-8 -*-
# 提取各标签列表页到excel
import time
import os.path

from src.movie.tools import Tag_manager
from src.tool.ExcelManager import listFiles, readExcel, writeExcel
from src.movie.tools.Tag_manager import makeMovieListInfo
start = time.clock()
putplace = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\movie\movie_message_order_by_year'


# 判断存放位置是否存在
if os.path.exists(putplace):
    pass
else:  # 否则新建
    print('新建电影提取存放excel处：'+putplace)
    os.makedirs(putplace)
# 按年份提取
taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_year_tag.xlsx')  # 读取标签列表
del taglist[0]   # 第一行删去，因为没有实际意思，是table的属性说明。真正的内容从第二行开始

# 对于每个标签
for tag in taglist:
    # 电影按照标签存放于文件夹中
    if __name__ == '__main__':
        mulu = putplace+'/'+tag[0]  # tag[0]是标签名 eg.爱情
    if os.path.exists(mulu):  # 该目录存在，则跳过
        pass
    else:
        os.makedirs(mulu)  # 否则新建文件夹
    excelpath = mulu + '/' + tag[0] + '.xlsx'  # 创建该类标签的excel
    # 存在处理过的excel文件则跳过
    if os.path.exists(excelpath):
        print(excelpath + '已经存在')
        continue
    tagmovies = [['电影名', 'URL入口', '图片地址', '电影信息', '星级评价']]   # 该标签所有书存放处（列表中每个元祖又是一个列表）
    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_电影/'+tag[0]  # 构造读取文件夹入口
    print('本地提取：'+path)
    # 查找目录下已经抓取的Html
    files = listFiles(path)
    # 遍历分析
    # 全部提取后一次性存入excel
    for i in files:
        file = path + '/' + i  # 找到将要访问的文件目录
        print('提取：'+file)
        content = open(file, 'rb').read()  # rb表示以二进制读的方式打开
        movies = Tag_manager.makeMovieListInfo(content)   # 提取电影列表
        tagmovies.extend(movies)  # 把电影放进去（movies是一个列表，使用extend可以将列表中的元素放入tagmovies中，而append会把整个列表当层一个元素放入）
    print("提取完毕！！！")
    # 将信息写入本地文件中
    try:
        writeExcel(excelpath, tagmovies)
        print('写入成功：' + excelpath)
    except:
        print('写入' + excelpath + '失败！')
        pass

    """
    # 每50页提取一次，存入一个excel表格中。
    j = len(files)
    #print(int(j/100))
    for num in range(1, int(j/50)+1):
        excelpath = mulu + '/' + tag[0] + '.' + str(num) +'.xlsx'  # 创建该类标签的excel
        # 存在处理过的excel文件则跳过
        if os.path.exists(excelpath):
            print(excelpath + '已经存在')
            continue
        tagmovies = [['电影名', 'URL入口', '图片地址', '电影信息', '星级评价']]
        for k in range(0, 51):
            total = (num-1) * 50 + k
            if total == j:
                break
            file = path + '/' + files[total]  # 找到将要访问的文件目录
            print('提取：' + file)
            content = open(file, 'rb').read()  # rb表示以二进制读的方式打开
            movies = Tag_manager.makeMovieListInfo(content)  # 提取电影列表
            tagmovies.extend(movies)  # 把电影放进去（movies是一个列表，使用extend可以将列表中的元素放入tagmovies中，而append会把整个列表当层一个元素放入）
        print("bingo!!")
        try:
            writeExcel(excelpath, tagmovies)
            print('写入成功：' + excelpath)
        except:
            print('写入' + excelpath + '失败！')
            pass
        if total == j:
            break
    """

end = time.clock()
print("提取电影列表总共运行时间 : %.03f 秒" %(end-start))