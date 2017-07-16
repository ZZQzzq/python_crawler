# 第二步，获取标签页的内容
import os
# 抓取分类标签页
tag = getHtml('http://movie.douban.com/tag/')  # 获取html
file = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_tag.html', 'wb')  # 保存这些内容
file.write(tag.encode())
file.close()
from src.tool.HtmlManager import getHtml, getBinaryHtml



# 抓取列表页方便测试
tag1 = getHtml("https://movie.douban.com/tag/%E7%88%B1%E6%83%85")
# 在本地建立一个txt文件，将通过getHtml函数得到的字符串保存在里面
file1 = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/movies.html', 'wb')
file1.write(tag1.encode())
file1.close()

# 抓取电影页方便测试
tag3 = getHtml("https://movie.douban.com/subject/25900945/")
file2 = open('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie.html', 'wb')
file2.write(tag3.encode())
file2.close()
print("成功")
