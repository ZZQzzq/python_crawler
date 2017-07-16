# -*- coding:utf-8 -*-
from src.tool import TagManager
from src.tool.ExcelManager import writeExcel
from src.tool.TagManager import makeBookInfo, makeBookListInfo
"""
# 提取标签页到excel
file = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/booktag.html', 'rb')
content = file.read()
TagManager.makeBookTag(content, r'D:\workplace\pythonwork\douban_book_catch_zzq\database/bookTag.xlsx')
"""


# 测试抓取单本书的函数（makeBookInfo）是否正确
print('D:\workplace\pythonwork\douban_book_catch_zzq\database/book.html')
file = open('D:/workplace/pythonwork/douban_book_catch_zzq/book_select_dic/html_dic/1208731C++ Primer中文版.html', 'rb')  # 读取文件
content = file.read()
book = makeBookInfo(content)
path = 'D:/workplace/pythonwork/'+book[0]+'.xlsx'
#books = [['图书编号', '书名', '作者', '出版社', '译者', '出版时间', '页数', '价格', '评价人数', '评分', '评价人数比例', '书籍介绍', '作者介绍', '其他信息', '目录', '相关推荐', '短评', '信息汇总']]
#books.append(book)
#writeExcel(path, books)
for i in book:
    print('*' * 50)  # 分割一下，方便查看
    print(i)  # 打印一下内容
    # print('*' * 50)  # 分割一下，方便查看

"""
# 测试抓取一个页面的图书信息
file = open('D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_book/文化/传记/40.html', 'rb')
content = file.read()
books = makeBookListInfo(content)
for i in books:
    print(i)
"""







