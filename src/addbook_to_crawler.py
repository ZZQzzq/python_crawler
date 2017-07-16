# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__date__ = '2017/5/12 9:45'

# # 将图片在MEDIA文件夹中按照标签存放
# import os
# from src.tool.ExcelManager import readExcel
# from src.tool.DbManager import DbManager
# list = ['文化', '文学', '科技', '经管', '流行', '生活']
# try:
#     for kind in list:
#         rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\\book_message_order_by_tag\\'+kind   # 各个分类目录
#         prefix = '.xlsx'
#         for parent, dirnames, filenames in os.walk(rootdir):
#                 for filename in filenames:
#                     #print(filenames)
#                     if filename.endswith(prefix):  # 寻找所有以xlsx结尾的文件
#                         filename1 = filename.split('.')[0]
#                         path = str(parent) + '\\' + filename  # 即将打开的xlsx文件地址
#                         #print(path)
#                         taglist = readExcel(path)
#                         del taglist[0]
#                         #print(taglist)
#                         i = 0
#                         for col in taglist:
#                             book_url = col[1]
#                             book_no = book_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
#                             try:
#                                     dbManager = DbManager()
#                                     root = 'book_detail/2017/05/'+kind+'/'+filename1+'/'
#                                     print(root)
#                                     updatesql="UPDATE `book_bookdetail` SET image= '{image}' WHERE `book_no`=book_no"
#                                     update = updatesql.format(image=root + book_no +'.jpg')
#                                     dbManager.execNonQuery(update)
#                                     print(book_no+"成功")
#
#                             except Exception as e:
#                                 print(e)
# except:
#         print("somthing wrong")
#
# 修改book_kind_id和book_tag的值
import os
from src.tool.ExcelManager import readExcel
from src.tool.DbManager import DbManager
list = ['文化', '文学', '经管', '流行', '生活']
try:
    for kind in list:
        rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\\book_message_order_by_tag\\'+kind   # 各个分类目录
        prefix = '.xlsx'

        if kind == "文化":
            kindname = 'wh'
        elif kind == '文学':
            kindname = 'wx'
        elif kind == '流行':
            kindname = 'lx'
        elif kind == '生活':
            kindname = 'sh'
        elif kind == '科技':
            kindname = 'kj'
        elif kind == "经管":
            kindname = 'jg'
        print(kindname)
        for parent, dirnames, filenames in os.walk(rootdir):
                for filename in filenames:
                    if filename.endswith(prefix):  # 寻找所有以xlsx结尾的文件
                        filename1 = filename.split('.')[0]
                        path = str(parent) + '\\' + filename  # 即将打开的xlsx文件地址
                        taglist = readExcel(path)
                        del taglist[0]
                        i = 0
                        for col in taglist:
                            book_url = col[1]
                            book_no = book_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
                            try:
                                    dbManager = DbManager()
                                    selectsql = "SELECT id FROM book_bookkind WHERE `book_name`='"+filename1+"'"
                                    kind = dbManager.execQuery(selectsql)
                                    for i in kind:
                                        kindid = i[0]
                                    updatesql="UPDATE `book_book` " \
                                              "SET book_tag= '{book_tag}',book_kind_id={book_kind_id}" \
                                              " WHERE `book_no`= '{book_no}'"
                                    update = updatesql.format(book_tag=kindname,
                                                              book_kind_id=kindid,
                                                              book_no=book_no
                                                              )
                                    dbManager.execNonQuery(update)
                                    print(book_no+"成功")

                            except Exception as e:
                                print(e)
except:
        print("somthing wrong")
