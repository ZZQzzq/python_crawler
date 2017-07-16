# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__date__ = '2017/5/30 15:54'
__function__ = '定期更新数据库'
import time

import os
import re
import os.path
import time
from bs4 import BeautifulSoup
import urllib.request

from src.tool.DbManager import DbManager
from src.tool.ProxyManager import makeProxyAddress
from src.tool import TagManager
from src.tool.ExcelManager import listFiles, readExcel, writeExcel
from src.tool.HtmlManager import getHtml, getBinaryHtml
from src.tool.ExcelManager import validateTitle

class ConnectCrawler():
    def __init__(self):
        self.__initConnect()

    def __initConnect(self):
        import pymysql.cursors  # 引入数据库的模块
        config = {'host': 'localhost',  # 数据库所在的主机地址，默认localhost
                  'user': 'root',  # 用户
                  'password': '123456789',  # 密码
                  'port': 3306,  # 默认即为3306
                  'database': 'crawler',  # 数据库名称（必须是已经存在于数据库中的才能成功）
                  'charset': 'utf8'  # 默认即为utf8
                  }
        self.conn = pymysql.Connect(**config)
        self.cur = self.conn.cursor()  # 游标，通过这个访问数据库
        if not self.cur:
            raise (NameError, "连接数据库失败")

    def CrawlerexecQuery(self, sql):
        self.cur.execute(sql)
        resList = self.cur.fetchall()  # fetchall():接收全部的返回结果行.
        return resList

    def CrawlerexecNonQuery(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print('执行语句成功')
            return 1
        except Exception:  # 出现异常回滚
            print('执行SQL语句失败：' + sql)
            self.conn.rollback()
            raise  # 使用raise引发异常。一旦出现异常，后续语句不再执行。

# 抓取网页下载到本地
def catch_list():
        requreip = 0
        lockprefix = 'html'
        v = 1.2
        startTime = time.clock()
        proxyAddress = makeProxyAddress()
        changeIP = 0  # 代理IP数组
        localDir = 'D:\workplace\pythonwork\douban_book_catch_zzq\web抓取_电影\\2017'
        lockprefix = 'html'
        # 先构建目录，已经存在就不需要
        if os.path.exists(localDir):
                pass
        else:  # 否则新建
                print('新建标签文件夹：' + localDir)
                os.makedirs(localDir)
        # 网络中断后重新抓取时判断是否加锁
        ok = listFiles(localDir, '.' + lockprefix)
        if ok:
            print('----已经更新完毕-----')  # 抓完
        url = 'http://movie.douban.com/tag/2016?start='  # 基础网址 https://movie.douban.com/tag/2016?start=20&type=R
        pagesize = 20  # 每页20部
        i = 0  # 翻页助手
        while i < 2:
            # 需要爬取的网页
            site = url + str(i * pagesize)+'&type=R'
            # 开始爬取

            src = localDir + '/' + str(i * 20) + '.html' # 构造文件名称
            # 判断文件是否存在，存在则不抓取节省时间
            if os.path.exists(src):
                    pass
            else:
                # 写入本地文件
                print('准备抓取：【' + site + '】  标签：【2017】')
                iprefuse = 1  # 如果抓取成功设为0
                # 如果抓取出错那重新抓取
                while iprefuse:
                    try:
                        daili1 = proxyAddress[changeIP]  # 代理ip
                        if v: # 爬虫速度控制
                            a = time.clock()  # 初试时间
                            time.sleep(v)
                            b = time.clock()
                            print('时间暂停:' + str(v))
                            print('真实时间暂停（Unix CPU时间,Windows 真实时间):' + str(b - a))
                        # 不需要代理
                        if requreip == 0:
                            webcontent = getHtml(site).encode('utf-8')  # 获得网址内容
                            notnull = re.search(r'<p>', webcontent.decode('utf-8', 'ignore'))  # 匹配看是否抓取到末页.根据是否有p标签进行判断
                        else:  # 需要代理
                            print('代理：' + daili1)
                            webcontent = getBinaryHtml(site, daili1)
                            notnull = re.search(r'<p>', webcontent.decode('utf-8', 'ignore')) # 获取网址内容
                        iprefuse = 0  # 抓完设置0
                    except Exception as e:  # 抓取过程中出错。
                        print(e)
                        if requreip:  # 换一个ip试试
                            changeIP += 1  # 更换ip下标
                            if changeIP == len(proxyAddress):  # 到达ip数组末循环再来
                                changeIP = 0
                                print('更换代理：' + proxyAddress[changeIP])
                            else:
                                print("IP被封")
                                raise

                    # 如果抓不到<p>标签，证明已经抓取完
                if notnull:
                        webfile = open(src, 'wb')  # 保存网页到本地
                        webfile.write(webcontent)
                        webfile.close()
                        print("已经抓取:" + site)
                else:
                        lock = open(src.replace('html', lockprefix), 'w')  # 抓取完毕了
                        # 日期：http://blog.csdn.net/u012175089/article/details/62044335
                        finish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                        lock.write('抓取完成时间：' + finish)
                        print("抓取完毕")
                        break
                i += 1  # 加页
        # 计时
        endTime = time.clock()
        print("爬取总共运行时间 : %.03f 秒" % (endTime - startTime))
# 获取数据保存到excel
def write_List_to_excel():
    start = time.clock()
    putplace = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\movie\movie_message_order_by_year'
    # 判断存放位置是否存在
    if os.path.exists(putplace):
        pass
    else:  # 否则新建
        print('新建电影提取存放excel处：' + putplace)
        os.makedirs(putplace)
    mulu = putplace + '/2017'
    if os.path.exists(mulu):  # 该目录存在，则跳过
        pass
    else:
        os.makedirs(mulu)  # 否则新建文件夹
    excelpath = mulu + '/2017.xlsx'  # 创建该类标签的excel
    # 存在处理过的excel文件则跳过
    if os.path.exists(excelpath):
        print(excelpath + '已经存在')
    tagmovies = [['电影名', 'URL入口', '图片地址', '电影信息', '星级评价']]  # 该标签所有书存放处（列表中每个元祖又是一个列表）
    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/web抓取_电影/2017'   # 构造读取文件夹入口
    print('本地提取：' + path)
    # 查找目录下已经抓取的Html
    files = listFiles(path)
    # 全部提取后一次性存入excel
    for i in files:
        file = path + '/' + i  # 找到将要访问的文件目录
        print('提取：' + file)
        content = open(file, 'rb').read()  # rb表示以二进制读的方式打开
        movies = TagManager.makeMovieListInfo(content)  # 提取电影列表
        tagmovies.extend(movies)  # 把电影放进去（movies是一个列表，使用extend可以将列表中的元素放入tagmovies中，而append会把整个列表当层一个元素放入）
    print("提取完毕！！！")
    # 将信息写入本地文件中
    try:
        writeExcel(excelpath, tagmovies)
        print('写入成功：' + excelpath)
    except:
        print('写入' + excelpath + '失败！')
        pass
    end = time.clock()
    print("提取电影列表总共运行时间 : %.03f 秒" % (end - start))
# 存入数据库
def save_to_MovieDb():
    start = time.clock()
    dbManager = DbManager()
    cdbManager = ConnectCrawler()
    excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\movie\movie_message_order_by_year\\2017\\2017.xlsx'  # 本地文件
    datas=[]
    try:
        datas = readExcel(excelpath)  # 读取当前表
    except Exception as e:
        print(e)
    del datas[0]  # 去掉标题（有效数据从第二行开始）
    for data in datas:  # 提取电影插入数据库
        # 提取各个字段的数据
        movie_name = data[0].replace("'", "\\'").replace('"', '\\"')  # 电影名
        movie_url = data[1].replace("'", "\\'").replace('"', '\\"')  # url
        movie_img = data[2].replace("'", "\\'").replace('"', '\\"')  # 图片地址
        movie_no = movie_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
        try:
            movie_info = data[3].replace("'", "\\'").replace('"', '\\"')
        except:
            movie_info = '.>_<.无出版信息'
            pass
        try:
            movie_star = data[4]
        except:
            movie_star = '0'
            pass
        # 构造查询函数select * from `book` where `bookno`='dc'
        searchsql1 = "select * from `movie` where `movie_no`='" + movie_no + "'"
        c_searchsql1 = "select * from `movies_movie` where `movie_no`='" + movie_no + "'"
        print(c_searchsql1)
        try:
            # 先查询一下数据是否已经存在了
            isexist1 = dbManager.execQuery(searchsql1)
            c_isexist1 = cdbManager.CrawlerexecQuery(c_searchsql1)
        except Exception as e:
            print(e)
            continue
        # 如果电影记录存在，插movie_tag表
        # 插入dou_ban_movie数据库
        if isexist1:
            print(movie_name + ':' + movie_url + '已经存在')
        else:
            # 插入数据
            insertbooksql = "INSERT INTO `movie` (`movie_no`,`movie_name`, `movie_url`, `movie_img`, `movie_info`, `movie_star`) VALUES ('" \
                            "{movie_no}','{movie_name}', '{movie_url}', '{movie_img}', '{movie_info}', '{movie_star}')"
            insert1 = insertbooksql.format(movie_no=movie_no, movie_name=movie_name, movie_url=movie_url, movie_img=movie_img,
                                           movie_info=movie_info,
                                           movie_star=movie_star)
            try:
                dbManager.execNonQuery(insert1)
            except Exception as e:
                print(e)
                pass
        # 插入crawler数据库
        if c_isexist1:
            print('web数据库'+movie_name + ':' + movie_url + '已经存在')
        else:
                c_insertbooksql = "INSERT INTO `movies_movie`(`movie_name`, `movie_no`, `movie_info`, `movie_url`, `stars`,`click_nums`,`fav_nums`,`image`,`add_time`,`movie_year_id`,`is_banner`)" \
                                  " VALUES ('{0}', '{1}', '{2}','{3}','{4}',{5},{6},'{7}','{8}',{9},{10})"
                c_insert1 = c_insertbooksql.format(movie_name, movie_no, movie_info, movie_url, movie_star,
                                                   0, 0, "movie_detail/2017/05/14/" + movie_no + ".jpg",
                                                   '2017-05-14', 1, 0)
                try:
                    cdbManager.CrawlerexecNonQuery(c_insert1)
                except Exception as e:
                    print(e)
                    pass
        # 如果电影标签存在，则不插入
        searchsql = "select * from `movie_tag` where `movie_no`='{movie_no}' and `movie_kind`='{movie_kind}' "
        searchsql2 = searchsql.format(movie_no=movie_no, movie_kind='2017')
        print(searchsql2)
        try:
            isexist2 = dbManager.execQuery(searchsql2)
        except Exception as e:
            print(e)
            pass
        if isexist2.__len__() == 0:
            inserttag = "INSERT INTO `movie_tag`(`movie_name`,`movie_no`,`movie_kind`) VALUES ('" \
                            "{movie_name}', '{movie_no}', '{movie_kind}')"
            insert2 = inserttag.format(movie_name=movie_name, movie_no=movie_no, movie_kind='2017')
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
# 抓取电影详情页下载到本地
def get_detail():
    requreip = 0
    v = 1.2
    startmovie = 0
    start = time.clock()
    webe = []
    selecttotal = "select count(distinct movie_no) from movie_tag WHERE movie_kind='2017'"  # 选出所有的电影（按编号选取）
    selectsql = "SELECT movie_name,movie_no,movie_kind FROM movie_tag WHERE movie_kind='2017' group by movie_no"  # 按编号分组
    dbManager = DbManager()
    total = dbManager.execQuery(selecttotal)  # 总记录（执行该语句，找出所有图书）
    total = int(total[0][0])  # 不同书籍总数目
    daili0 = makeProxyAddress()  # 代理IP数组
    daili_no = 0
    change_ip = 0  # 代理ip下标
    # 循环对分类进行抓取
    while startmovie < total:
        selectsql1 = selectsql
        taglist = dbManager.execQuery(selectsql1)
        for i in range(0, len(taglist)):
            try:
                """
                由selectsql1查找表的时候，按照编号分组.
                movie_tag（movie_name,movie_no，movie_kind）
                所以，taglist[i][0]表示电影名...
                """
                movie_name = taglist[i][0]  # 电影名
                movie_kind = taglist[i][2]  # 所在标签（年代）
                movie_no = taglist[i][1]  # 电影编号
                url = 'http://movie.douban.com/subject/' + movie_no  # 抓取网址
            # eg.http://movie.douban.com/subject/26580232
            except:
                raise
            mulu0 = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/movie_detail_message/' + movie_kind
            # 存在大分类文件夹则跳过
            if os.path.exists(mulu0):
                pass
            else:  # 否则新建
                print('新建标签：' + mulu0)
                os.makedirs(mulu0)
            try: # 判断文件是否存在，存在则不抓取节省时间
                filename = mulu0 + '/' + movie_no + validateTitle(movie_name) + '.html'  # 新建html文件名称
                if os.path.exists(filename):
                    print(filename + '：已经存在')
                    continue
                else:
                    print('准备抓取：' + url + '年代：' + movie_kind)
            except:
                print(filename + "文件名异常")
                continue
            iprefuse = 1  # 如果抓取成功设为0
            # 如果抓取出错那重新抓取
            while iprefuse:
                try:
                    daili1 = daili0[change_ip]  # 代理ip
                    if v:# 爬虫速度控制
                        a = time.clock()
                        time.sleep(v)
                        b = time.clock()
                        print('时间暂停:' + str(v))
                        print('真实时间暂停（Unix CPU时间,Windows 真实时间):' + str(b - a))

                    if requreip == 0: # 不需要代理
                        webcontent = getHtml(url).encode('utf-8')  # 爬取，有时间限制，应对504错误
                        notnull = re.search(r'<div class="top-nav-doubanapp">', webcontent.decode('utf-8', 'ignore'))
                        if notnull:
                            pass
                        else:
                            raise Exception("抓到的页面不是正确的页面" + filename)
                        webfile = open(filename, 'wb')
                        webfile.write(webcontent)
                        webfile.close()
                        print("已经抓取:" + url + '类别：' + movie_kind)
                        iprefuse = 0  # 抓完设置0
                    else:  # 需要代理
                        print('代理：' + daili1)
                        webcontent = getBinaryHtml(url, daili1)
                        notnull = re.search(r'<div class="top-nav-doubanapp">', webcontent.decode('utf-8', 'ignore'))
                        if notnull:
                            pass
                        else:
                            raise Exception("抓到的页面不是正确的页面" + filename)
                        webfile = open(filename, 'wb')
                        webfile.write(webcontent)
                        webfile.close()
                        print("已经抓取:" + url + '类别：' + movie_kind)
                        iprefuse = 0
                        daili_no += 1
                        print('此次转换代理次数:' + str(daili_no))
                        if daili_no > 15:  # 代理15次仍然抓取不到，则认为主机不可达
                            daili_no = 0
                            requreip = 0  # 代理100次后转为非代理
                            break
                # except urllib.error.URLError as e:
                except Exception as e:
                    if hasattr(e, 'code'):
                        # hasattr(object, name)。
                        # 判断一个对象里面是否有name属性或者name方法，返回BOOL值，有name特性返回True， 否则返回False。
                        # 需要注意的是name要用括号括起来.
                        print('页面不存在或时间太长.')
                        print('Error code:', e.code)
                        if e.code == 404:
                            print('404错误，忽略')
                            webe.append(movie_no)
                            break
                    elif hasattr(e, 'reason'):
                        print("无法到达主机.")
                        print('Reason:  ', e.reason)
                    if requreip:
                        change_ip += 1  # 更换ip下标
                        if change_ip == len(daili0):  # 到达ip数组末循环再来
                            change_ip = 0
                        print('更换代理：' + daili0[change_ip])
                        daili_no += 1
                        print('此次转换代理次数:' + str(daili_no))
                        if daili_no > 15:
                            daili_no = 0
                            requreip = 0  # 代理100次后转为非代理
                            break  # 跳出while循环
                    else:
                        print("IP被封或断网")
                        requreip = 1  # 转为代理
        print('已经抓了' + str(startmovie + 100) + '部')
        print()  # 三行空格
        print()
        print()
        startmovie += 1
        if len(webe) > 20:
            print(webe)
            webep = open("../movie_detail_message/movie_detail.txt", 'a+')
            webep.write(','.join(webe) + '/n')
            webep.close()
            webe = []
        else:
            pass
    end = time.clock()
    print("爬取总共运行时间 : %.03f 秒" % (end - start))
# 获取电影详情下载到本地
def save_to_MovieDetailDb():
    rootdir = 'D:/workplace/pythonwork/douban_book_catch_zzq/src/movie_detail_message/2017'
    prefix = '.html'
    dbManager = DbManager()
    c_dbmanager = ConnectCrawler()
    insertbooksql = "INSERT INTO `movie_detail` (`movie_no`, `movie_name`, `movie_year`, `movie_director`, `movie_pl`, `movie_actor`, `movie_type`, `country`, `language`, `movie_ReleaseDate`, `runtime`, `votenum`,`stars`, `voteratio`, `movie_intro`, `recommendations`, `comments`)" \
                    " VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',{11},'{12}','{13}','{14}','{15}','{16}')"
    c_insertbooksql = "INSERT INTO `movies_moviedetail` (`movie_no`, `movie_name`, `movie_year`, `movie_director`, `movie_pl`, `movie_actor`, `movie_type`, `country`, `language`, `movie_ReleaseDate`, `runtime`, `votenum`,`stars`, `movie_intro`, `recommendations`, `comments`,`click_nums`,`fav_nums`,`add_time`)" \
             " VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',{11},'{12}','{13}','{14}','{15}',{16},{17},'{18}')"
    for parent, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename.endswith(prefix):  # 寻找所有以html结尾的文件
                path = str(parent) + '/' + filename
                print(path)
                content = open(path, 'rb').read()
                try:
                    movie = TagManager.makeBookInfo(content)  # 返回的是一个list
                except:
                    print("解析错误!")
                    # continue
                insert1 = insertbooksql.format(movie[0], movie[1], movie[2],movie[3],movie[4],movie[5], movie[6],movie[7],movie[8], movie[9],movie[10],movie[11],movie[12],movie[13],movie[14],movie[15],movie[16])
                insert2 = c_insertbooksql.format(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7],movie[8],movie[9], movie[10], movie[11], movie[12], movie[14], movie[15], movie[16], 0, 0,'2017-05-14')
                try:
                    dbManager.execNonQuery(insert1)
                    c_dbmanager.CrawlerexecNonQuery(insert2)
                    os.rename(path, path + 'lockl')  # 添加到数据库中的电影详情页添加文件后缀lockl
                except Exception as e:
                    print(e)
                    # continue
                try:
                    path = "https://movie.douban.com/subject/" + movie[0] + "/"
                    tag = getHtml(path).encode('utf-8')
                    soup = BeautifulSoup(tag, 'html.parser')
                    movie_mes = soup.select("div.article div#mainpic")
                    subsoup = BeautifulSoup(str(movie_mes), 'html.parser')
                    pic_url = subsoup.a.img['src']  # 图片链接
                    print(pic_url)
                    savepath = 'D:/workplace/pythonwork/Crawler/media/movie_detail/2017/05/14'
                    work_path = os.path.join(savepath + '/', movie[0] + '.jpg')
                    urllib.request.urlretrieve(pic_url, '%s' % str(work_path))
                    print("下载图片成功")
                except Exception as e:
                    print(e)
            else:
                pass
# 保持book_book表和book_bookdetail表一致
def keep_thesame():
    c_dbmanager = ConnectCrawler()
    selecttotal = "select count(distinct book_no) from book_bookdetail "
    select_bookno = "SELECT book_no FROM book_bookdetail "  # 找出bookdetail表中所有的图书
    bookno_list = c_dbmanager.CrawlerexecQuery(select_bookno)
    print(bookno_list)
    for i in range(0, len(bookno_list)):
        selectsql = "select * from book_book where book_no = '{0}'" # 如果book表中不存在这本书就删除
        c_selectsql = selectsql.format(bookno_list[i][0])
        print(c_selectsql)
        try:
           result = c_dbmanager.CrawlerexecQuery(c_selectsql)
           print(result)
           if not result:
               delete = "delete from book_bookdetail where book_no='{0}'"
               c_deletesql = delete.format(bookno_list[i][0])
               print(c_deletesql)
               c_dbmanager.CrawlerexecNonQuery(c_deletesql)
        except Exception as e:
               print(e)
        i += 1
# 将评分整齐化
def score_manager():
    c_dbmanager = ConnectCrawler()
    select_stars = "SELECT book_no,stars FROM book_book "  # 找出bookdetail表中所有的图书评分
    stars_list = c_dbmanager.CrawlerexecQuery(select_stars)
    print(stars_list)
    for i in range(0, len(stars_list)):
        try:
            if stars_list[i][1] == 'None':
                print(stars_list[i][1])
                stars_list[i][1] = 0
                update = "UPDATE `book_book` SET stars = '"+ stars_list[i][1] + "' where `book_no`='" + stars_list[i][0] + "'"
                c_dbmanager.CrawlerexecNonQuery(update)
        except Exception as e:
            print(e)




if __name__ == '__main__':
    # catch_list()
    # write_List_to_excel()
    # save_to_MovieDb()
    # get_detail()
    # save_to_MovieDetailDb()
    # keep_thesame()
    score_manager()