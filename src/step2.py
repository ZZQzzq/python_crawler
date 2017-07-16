# 第二步，获取标签页的内容
import os

from src.tool.HtmlManager import getHtml, getBinaryHtml

# 抓取分类标签页
tag = getHtml('http://book.douban.com/tag/')  # 获取html
file = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/booktag.html', 'wb')  # 保存这些内容
file.write(tag.encode())
file.close()
""""
# 抓取列表页方便测试
tag1 = getHtml("http://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
# 在本地建立一个txt文件，将通过getHtml函数得到的字符串保存在里面
file1 = open('D:\workplace\pythonwork\HelloWorld\database/books.html', 'wb')
file1.write(tag1.encode())
file1.close()

# 抓取图书页方便测试
tag3 = getHtml("https://book.douban.com/subject/26698660/")
file2 = open('D:\workplace\pythonwork\HelloWorld\database/book.html', 'wb')
file2.write(tag3.encode())
file2.close()
print("成功")


tag = getBinaryHtml('http://book.douban.com/tag/')
addr = 'D:/workplace/pythonwork/HelloWorld/src/booktag.html'

if os.path.exists(addr):
    pass
else:  # 否则新建
    print('新建：' + addr)
    os.makedirs(addr)

file = open('D:/workplace/pythonwork/HelloWorld/src/booktag.html', 'wb')  # 以写二进制的方式，写入获得的内容
file.write(tag.encode('utf-8'))
file.close()
# 下载某个页面
content1 = getHtml("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
addr1 = 'D:/workplace/pythonwork/HelloWorld/src//books.html'
if os.path.exists(addr1):
    pass
else:  # 否则新建
    print('新建：' + addr1)
    os.makedirs(addr1)
file1 = open(content1, 'wb')
file1.write(content1.encode('utf-8'))
file1.close()

content2 = getHtml("https://book.douban.com/subject/26698660/")
addr2 = 'D:/workplace/pythonwork/HelloWorld/src//book.html'
if os.path.exists(addr2):
    pass
else:  # 否则新建
    print('新建：' + addr2)
    os.makedirs(addr2)
file2 = open(addr2, 'wb')
file2.write(content2.encode('utf-8'))
file2.close()
"""
