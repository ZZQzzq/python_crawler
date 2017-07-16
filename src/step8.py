from tool.DbManager import DbManager
from tool import TagManager
import os

# 扫描book目录，找出所有图书详情表进行提取，插入数据库

rootdir = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/book_detail_message'
prefix = '.html'
database = DbManager()
insertbooksql = "INSERT INTO `book_detail` (`book_no`,`book_name`,`book_author`,`book_public`,`book_trans`,`book_year`,`book_page`,`book_price`,`votenum`,`stars`," \
                "`voteratio`, `book_intro`, `author_intro`,`book_others`, `mu_lu`, `recommendations`, `comments`, `book_info`)" \
                " VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}',{6},'{7}',{8},'{9}','{10}', '{11}','{12}','{13}','{14}','{15}','{16}','{17}')"
# book_no0, 1book_name, 2book_author, 3book_public, 4book_trans, 5book_year, 6book_page(int), 7book_price,
# 8votenum(int),9stars, 10voteratio, 11book_intro, 12author_intro, 13book_others, 14mu_lu,
# 15recommendations, 16comments, 17book_info.text.replace(' \n', '').replace('\n ', '').replace(' ', '')]
i = 0
for parent, dirnames, filenames in os.walk(rootdir):
    """
    使用 os.walk 方法返回的是一个三元tupple(dirpath, dirnames, filenames),
    其中第一个为起始路径，
    第二个为起始路径下的文件夹,
    第三个是起始路径下的文件.
    dirpath是一个string，代表目录的路径,
    dirnames是一个list，包含了dirpath下所有子目录的名字,
    filenames是一个list，包含了非目录文件的名字.
    """
    for filename in filenames:
        if filename.endswith(prefix):  # 寻找所有以html结尾的文件
            path = str(parent) + '/' + filename
            print(path)
            content = open(path, 'rb').read()
            try:
                draw = TagManager.makeBookInfo(content)
            except:
                continue
            insert1 = insertbooksql.format(draw[0],
                                           draw[1],
                                           draw[2],
                                           draw[3],
                                           draw[4],
                                           draw[5],
                                           draw[6],
                                           draw[7],
                                           draw[8],
                                           draw[9],
                                           draw[10],
                                           draw[11],
                                           draw[12],
                                           draw[13],
                                           draw[14],
                                           draw[15],
                                           draw[16],
                                           draw[17]
                                           )
            try:
                database.execNonQuery(insert1)
                os.rename(path, path + 'lockl')
            except Exception as e:
                print(e)
                f = open('D:/workplace/pythonwork/douban_book_catch_zzq/src/book_detail_message/wrong.txt', 'a+')
                i += 1
                f.write(draw[0] + '<==>' + str(i) + '\n')
                print(draw[0])
                continue
        else:
            pass
