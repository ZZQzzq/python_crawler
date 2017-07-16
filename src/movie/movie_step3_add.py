# -*- coding:utf-8 -*-
# 提取年代标签保存在excel【Movie_year_tag】，按该标签进行电影提取

from bs4 import BeautifulSoup  # 解析html结构的模块
from src.tool.ExcelManager import writeExcel

file = open('D:/workplace/pythonwork/douban_book_catch_zzq/database/movie_tag.html', 'rb')
content = file.read()
soup = BeautifulSoup(content, 'html.parser')  # 开始解析
movie2 = soup.select('div#content div.article table:nth-of-type(4)')  # 找出该大类下对应的分类所在table
# css选择器，.后面跟类class名，#后面跟id名。table:nth-of-type(4)表示前面父类标签的第四个table子标签
print(movie2)
taglist = [['标签名', '标签链接', '点击量']]  # Excel里面的标题
for movietag in movie2:
            soup2 = BeautifulSoup(str(movietag), 'html.parser')  # 开始解析
            movietag3 = soup2.findAll("a")  # 标签名
            #print("标签名："+movietag3)
            movietag4 = soup2.findAll("b")   # 该标签下的电影访问量
            #print("访问量："+movietag4)
            for i in range(0, len(movietag4)):  # len(booktag4)就可以表示一行有多少种不同类型的分类
                tag = movietag3[i].string  # 标签名
                link = movietag3[i]['href']  # 链接
                print("标签名："+tag)
                print("链接："+link)
                taglink = 'https://movie.douban.com'+link  # 链接
                tagnum = movietag4[i].string
                print("访问量："+tagnum)
                taglist.append([tag.strip(), taglink.strip(), tagnum.strip()])  # 把内容加进去，按照标题的顺序
print(taglist)
writeExcel('D:/workplace/pythonwork/douban_book_catch_zzq/database/movie_year_tag.xlsx', taglist)  # 将内容写入excel中
print("写入EXCEL成功")

