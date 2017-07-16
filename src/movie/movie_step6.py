

import time
from src.tool.ExcelManager import readExcel
from src.movie.tools.Db_manager import DbManager

# 合并各标签列表页excel到数据库
# 第六步：书表去重并写入数据库，
# 读取Excel，判断是否重复，先加入movie表，重复则往movietag表插入标签记录

start = time.clock()
taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_year_tag.xlsx')  # 读取标签列表
del taglist[0]  # 数据从第二行开始   taglist = [['标签名', '标签链接', '点击量']]
dbManager = DbManager()
i = 0
for tag in taglist:  # 遍历所有标签
    movie_kind = tag[0]  # 标签
    excelpath = 'movie_message_order_by_year/' + movie_kind + '/' + movie_kind + '.xlsx'  # 本地文件
    try:
        datas = readExcel(excelpath)  # 读取当前表
    except Exception as e:
        print(e)
        continue
    del datas[0]  # 去掉标题（有效数据从第二行开始）
    print(datas)
    # 提取电影插入数据库
    for data in datas:
        # 提取各个字段的数据
        movie_name = data[0].replace("'", "\\'").replace('"', '\\"')  # 电影名
        movie_url = data[1].replace("'", "\\'").replace('"', '\\"')  # url
        movie_img = data[2].replace("'", "\\'").replace('"', '\\"')  # 图片地址
        movie_no = movie_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
        try:
            movie_info = data[3].replace("'", "\\'").replace('"', '\\"')
        except:
            movie_info = ',>_<.无出版信息'
            pass
        try:
            movie_star = data[4]
        except:
            movie_star = '0'
            pass
        # 构造查询函数select * from `book` where `bookno`='dc'
        searchsql1 = "select * from `movie` where `movie_no`='" + movie_no + "'"
        print(searchsql1)
        try:
            # 先查询一下数据是否已经存在了
            isexist1 = dbManager.execQuery(searchsql1)
        except Exception as e:
            print(e)
            continue
        # 如果电影记录存在，插movie_tag表
        if isexist1:
            print(movie_name + ':' + movie_url + '已经存在')
            # 已经存在的
        else:
            # 插入数据
            insertbooksql = "INSERT INTO `movie` (`movie_no`,`movie_name`, `movie_url`, `movie_img`, `movie_info`, `movie_star`) VALUES ('" \
                            "{movie_no}','{movie_name}', '{movie_url}', '{movie_img}', '{movie_info}', '{movie_star}')"
            insert1 = insertbooksql.format(movie_no=movie_no,movie_name=movie_name, movie_url=movie_url, movie_img=movie_img, movie_info=movie_info,
                                           movie_star=movie_star)
            print(insert1)
            try:
                dbManager.execNonQuery(insert1)
            except Exception as e:
                print(e)
                pass
        # 如果图书标签存在，则不插入
        searchsql = "select * from `movie_tag` where `movie_no`='{movie_no}' and `movie_kind`='{movie_kind}' "
        searchsql2 = searchsql.format(movie_no=movie_no, movie_kind=movie_kind)
        print(searchsql2)
        try:
            isexist2 = dbManager.execQuery(searchsql2)
        except Exception as e:
            print(e)
            pass
        if isexist2.__len__() == 0:
            inserttag = "INSERT INTO `movie_tag`(`movie_name`,`movie_no`,`movie_kind`) VALUES ('" \
                        "{movie_name}', '{movie_no}', '{movie_kind}')"
            insert2 = inserttag.format(movie_name=movie_name, movie_no=movie_no, movie_kind=movie_kind)
            print(insert2)
            try:
                dbManager.execNonQuery(insert2)
            except Exception as e:
                print(e)
                pass
        print('-' * 100)

print("插入数据库结束")
end = time.clock()
print("合并电影列表进数据库总共运行时间 : %.03f 秒" % (end - start))
