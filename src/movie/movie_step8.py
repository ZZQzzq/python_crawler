from src.movie.tools.Db_manager import DbManager
from src.movie.tools import Tag_manager
import os

# 扫描movie目录，找出所有电影详情表进行提取，插入数据库

rootdir = '../movie_detail_message'
prefix = '.html'
dbManager = DbManager()
insertbooksql = "INSERT INTO `movie_detail` (`movie_no`, `movie_name`, `movie_year`, `movie_director`, `movie_pl`, `movie_actor`, `movie_type`, `country`, `language`, `movie_ReleaseDate`, `runtime`, `votenum`,`stars`, `voteratio`, `movie_intro`, `recommendations`, `comments`)" \
                " VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',{11},'{12}','{13}','{14}','{15}','{16}')"
#
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
                draw = Tag_manager.makeMovieInfo(content)  # 返回的是一个list
            except:
                print("解析错误!")
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
                                           draw[16]
                                           )
            try:
                dbManager.execNonQuery(insert1)
                os.rename(path, path + 'lockl')  # 添加到数据库中的电影详情页添加文件后缀lockl
            except Exception as e:
                print(e)
                continue
        else:
            pass
