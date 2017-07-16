# -*- coding:utf-8 -*-
# 提取各标签列表页到excel
import time
import os.path
from src.tool.ExcelManager import listFiles, readExcel, writeExcel
from tool import TagManager 
start = time.clock()
putplace = 'book_message_order_by_tag'

# 判断存放位置是否存在
if os.path.exists(putplace):
    pass
else:  # 否则新建
    print('新建图书提取存放excel处：'+putplace)
    os.makedirs(putplace)
taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/booktag.xlsx')  # 读取标签列表
del taglist[0]   # 第一行删去，因为没有实际意思，是table的属性说明。真正的内容从第二行开始
# 对于每个标签
for tag in taglist:
    # 图书按照标签存放于文件夹中
    if __name__ == '__main__':
        mulu = putplace+'/'+tag[0]  # tag[0]是标签大类 eg.文学
    if os.path.exists(mulu):  # 该目录存在，则跳过
        pass
    else:
        os.makedirs(mulu)  # 否则新建文件夹

    excelpath = mulu+'/'+tag[1]+'.xlsx'  # tag[1]是标签名称，eg.经典（文学中的一种）
    # 存在处理过的excel文件则跳过
    if os.path.exists(excelpath):
        print(excelpath+'已经存在')
        continue

    tagbooks = [['书籍名', '书籍链接', '图片地址', '书籍信息', '星级评价']]   # 该标签所有书存放处（列表中每个元祖又是一个列表）
    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_book/'+tag[0]+'/'+tag[1]  # 构造读取文件夹入口
    print('本地提取：'+path)
    # 查找目录下已经抓取的Html
    files = listFiles(path)
    # 遍历分析
    for i in files:
        file = path+'/'+i  # 找到将要访问的文件目录
        print('提取：'+file)
        content = open(file, 'rb').read()  # rb表示以二进制读的方式打开
        books = TagManager.makeBookListInfo(content)   # 提取图书列表
        tagbooks.extend(books)  # 把书放进去

    # 将信息写入本地文件中
    writeExcel(excelpath, tagbooks)
    print('写入成功：'+excelpath)
end = time.clock()
print("提取图书列表总共运行时间 : %.03f 秒" % (end-start))