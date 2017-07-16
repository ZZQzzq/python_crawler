  # 多线程同时向数据库写入数据
  # 生产者消费者模式：一个主线程用来读取xlsx文件中数据，保存至队列中；
  #                 其他从属线程从队列中获取数据并插入数据库（注意县城在访问数据库时要互斥，可采用令牌的方式实现）

import time
from src.tool.ExcelManager import readExcel
from src.tool.DbManager import DbManager

start = time.clock()
taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/booktag_keji.xlsx')  # 读取标签列表
del taglist[0]  # 数据从第二行开始   taglist = [['标签类别', '标签名', '标签链接', '图书数量']]
dbManager = DbManager()
for tag in taglist:  # 遍历所有标签
    book_kind = tag[0]    # 大类
    book_tag = tag[1]  # 标签
    excelpath = 'book_message_order_by_tag/' + book_kind + '/' + book_tag + '.xlsx'  # 本地文件
    try:
        datas = readExcel(excelpath)  # 读取当前表
    except Exception as e:
        print(e)
        continue
    del datas[0]  # 去掉标题（有效数据从第二行开始）
    # print(datas)
    # 提取图书插入数据库
    for data in datas:
        # 提取各个字段的数据
        book_name = data[0].replace("'", "\\'").replace('"', '\\"')  # 书名
        book_url = data[1].replace("'", "\\'").replace('"', '\\"')  # url
        book_img = data[2].replace("'", "\\'").replace('"', '\\"')  # 图片地址
        book_no = book_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
        try:
            book_info = data[3].replace("'", "\\'").replace('"', '\\"')
        except:
            book_info = '-'
            pass
        try:
            book_star = data[4]
        except:
            book_star = '-'
            pass
        # 构造查询函数select * from `book` where `bookno`='dc'
        searchsql1 = "select * from `book` where `book_no`='" + book_no + "'"
        print(searchsql1)
        try:
            # 先查询一下数据是否已经存在了
            isexist1 = dbManager.execQuery(searchsql1)
        except Exception as e:
            print(e)
            continue
        # 如果图书记录存在，插Book_tag表
        if isexist1:
            print(book_name + ':' + book_url + '已经存在')
            # 已经存在的
        else:
            # 插入数据
            insertbooksql = "INSERT INTO `book` (`book_no`,`book_name`, `book_url`, `book_img`, `book_info`, `book_star`) VALUES ('" \
                            "{book_no}','{book_name}', '{book_url}', '{book_img}', '{book_info}', '{book_star}')"
            insert1 = insertbooksql.format(book_no=book_no, book_name=book_name, book_url=book_url, book_img=book_img, book_info=book_info,
                                           book_star=book_star)
            print(insert1)
            try:
                dbManager.execNonQuery(insert1)
            except Exception as e:
                print(e)
                pass
        # 如果图书标签存在，则不插入
        searchsql = "select * from `book_tag` where `book_no`='{book_no}' and `book_tag`='{book_tag}' and `book_kind`='{book_kind}'"
        searchsql2 = searchsql.format(book_no=book_no, book_tag=book_tag, book_kind=book_kind)
        print(searchsql2)
        try:
            isexist2 = dbManager.execQuery(searchsql2)
        except Exception as e:
            print(e)
            pass
        if isexist2.__len__() == 0:
            inserttag = "INSERT INTO `book_tag`(`book_name`,`book_no`,`book_tag`,`book_kind`) VALUES ('" \
                        "{book_name}', '{book_no}', '{book_tag}', '{book_kind}')"
            insert2 = inserttag.format(book_name=book_name, book_no=book_no, book_tag=book_tag, book_kind=book_kind)
            print(insert2)
            try:
                dbManager.execNonQuery(insert2)
            except Exception as e:
                print(e)
                pass
        print('-' * 100)

print("插入数据库结束")
end = time.clock()
print("合并图书列表进数据库总共运行时间 : %.03f 秒" % (end - start))



