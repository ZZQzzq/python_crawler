# -*- coding:utf-8 -*-
'''
  找出所有单本书籍的详细介绍url并存入book_detail_url文件中
'''
from DbManager import DbManager


def catch_url():
    url_list = []
    select_total = 'select count(distinct book_no) from book_tag'   #  group by book_no'  # 选出所有的图书（按编号选取）
    # select_total = 'SELECT count(*) FROM dou_ban_book.book_tag;'  # 选出所有的图书（按编号选取）
    select_sql = 'SELECT book_name,book_kind,book_no FROM book_tag group by book_no'  # 按编号分组
    dbManager = DbManager()
    total = dbManager.execQuery(select_total)  # 总记录（执行该语句，找出所有图书）
    total = int(total[0][0])  # total记录书数目（不同book_no）,共22457本
    # select_sql1 = select_sql + ' limit ' + str(start_book) + ',100'
    tag_list = dbManager.execQuery(select_sql)
    # print('按编号分组图书共有：')
    # print(len(tag_list))
    # print('共有图书：')
    # print(total)
    for i in range(0, len(tag_list)):
        try:
            """ 由selectsql1查找表的时候，按照编号分组.
            临时新建关系（book_name,book_kind,book_no）
            所以，taglist[i][0]表示书名...
            """
            book_name = tag_list[i][0]  # 书名
            book_kind = tag_list[i][1]  # 分类
            book_no = tag_list[i][2]  # 图书编号
            url = 'http://book.douban.com/subject/' + book_no  # 抓取网址
            url_list.append(url)
        except:
            raise
    return url_list


if __name__ == '__main__':
    print(catch_url())
    print(len(catch_url()))
    file = open('book_detail_url.txt', 'w')  # 打开文件（若没有，则新建）
    file.write('\n'.join(catch_url()))  # 每插入一项，就换行
    file.close()  # 关闭文件
