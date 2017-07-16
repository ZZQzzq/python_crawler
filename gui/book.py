# -*- coding: utf-8 -*-
# 测试使用xlrd,xlwt,xxlutils进行excel操作
import os
import xlrd, xlwt
from xlutils3.copy import copy
from src.movie.tools.Html_manager import getHtml
from src.movie.tools.Tag_manager import makeMovieInfo
url = 'http://movie.douban.com/subject/26605946/'
excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\newmovie.xls'  # 创建保存记录的excel
if os.path.exists(excelpath):
    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/movie_select_dic/newmovies/26605946.html'
    if not os.path.exists(path):
        tag = getHtml(url).encode('utf-8')
        file = open(path, 'wb')
        file.write(tag)
    content = open(path, 'rb').read()
    movie = makeMovieInfo(content)
    print(movie)
    try:
        oldWb = xlrd.open_workbook(excelpath, formatting_info=True)  #获取需要插入数据的excel
        this_sheet = oldWb.sheet_by_name(u"sheet1")  # 获取sheet1
        row = this_sheet.nrows
        newWb = copy(oldWb)  # 拷贝原始文件
        sheet = newWb.get_sheet(0)  # 原始文件中存在sheetname=0的文件
        for i in range(0, len(movie)):
            sheet.write(row, i, movie[i])  # row行，col列，data追加的数据，style数据样式
        print("=====写完啦=======")
        newWb.save(excelpath)
        print("添加成功")
    except Exception as e:
        print(e)
else:
        newmovies = ['电影编号', '电影名', '公布时间', '导演', '编剧', '主演', '类型', '国家/地区', '语言',
                '上映时间', '时长', '评价人数', '电影星级', '评价人数比例', '剧情介绍', '相关推荐', '短评']
        try:
            file = xlwt.Workbook()  # 创建工作簿
            sheet1 = file.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
            for i in range(0, len(newmovies)):
                sheet1.write(0, i, newmovies[i])
            file.save(excelpath)
            print('写入成功：' + excelpath)
        except:
            print('写入' + excelpath + '失败！')
            pass
