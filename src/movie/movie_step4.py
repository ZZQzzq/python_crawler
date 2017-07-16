import time
from src.tool.ExcelManager import listFiles, readExcel
from src.tool.ProxyManager import makeProxyAddress
import urllib.parse
import os
from src.movie.tools.Html_manager import getHtml, getBinaryHtml
import re

# 抓取各标签列表页
# 按年份进行抓取，共有43820部电影
"""
	输入参数为:
	requireip 是否使用代理，默认否
	v 是否限制爬虫速度，默认否，时间为1秒仿人工
	lockprefix 文件加锁后缀
"""
requreip = 0
lockprefix = 'html'
v = 1.2
# 进行计时
# 开始时间
startTime = time.clock()
# 从excel文件中读取标签列表。返回序列
tagList = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\database/movie_year_tag.xlsx')  # 按年份提取
# (标签名，标签链接，点击量)
# 代理IP数组
proxyAddress = makeProxyAddress()
changeIP = 0  # 代理IP数组
# 循环对标签进行抓取
for i in range(1, len(tagList)):
    tagName = tagList[i][0]  # 标签名
    tag = urllib.parse.quote(tagName)  # url中文转码
    localDir = 'D:\workplace\pythonwork\douban_book_catch_zzq\web抓取_电影/' + tagName
    # 先构建目录，已经存在就不需要
    if os.path.exists(localDir):
        pass
    else:  # 否则新建
        print('新建标签文件夹：' + localDir)
        os.makedirs(localDir)
    """
    mulu = localDir + '/' + tagName
    # 存在标签文件夹则跳过
    if os.path.exists(mulu):
        pass
    else:  # 否则新建方便网页存放
        print('新建标签文件夹' + mulu)
        os.makedirs(mulu)
    """

    # 网络中断后重新抓取时判断是否加锁
    ok = listFiles(localDir, '.' + lockprefix)
    if ok:
        print('标签：' + tagName + '----已经抓完')  # 抓完
        continue
    url = 'http://movie.douban.com/tag/' + tag + '?start='  # 基础网址
    pagesize = 20  # 每页20部
    i = 0  # 翻页助手
    while True:
        # 需要爬取的网页
        site = url + str(i * pagesize)
        # 开始爬取
        # 构造文件名称
        # D:\workplace\pythonwork\douban_book_catch_zzq\web抓取/爱情/0.html
        src = localDir + '/' + str(i * 20) + '.html'
        # 判断文件是否存在，存在则不抓取节省时间
        if (os.path.exists(src) == True):
            pass
        else:
            # 写入本地文件
            print('准备抓取：【' + site + '】  标签：【' + tagName + '】')
            iprefuse = 1  # 如果抓取成功设为0
            # 如果抓取出错那重新抓取
            while iprefuse:
                try:
                    daili1 = proxyAddress[changeIP]  # 代理ip
                    # 爬虫速度控制
                    if v:
                        a = time.clock()  # 初试时间
                        time.sleep(v)
                        b = time.clock()
                        print('时间暂停:' + str(v))
                        print('真实时间暂停（Unix CPU时间,Windows 真实时间):' + str(b - a))
                    # 不需要代理
                    if requreip == 0:
                        # 获得网址内容
                        webcontent = getHtml(site).encode('utf-8')  # 爬取
                        # 搜索是否出现dl标签
                        notnull = re.search(r'<p>', webcontent.decode('utf-8', 'ignore'))  # 匹配看是否抓取到末页
                    else:  # 需要代理
                        print('代理：' + daili1)
                        webcontent = getBinaryHtml(site, daili1)
                        # 获取网址内容
                        notnull = re.search(r'<p>', webcontent.decode('utf-8', 'ignore'))
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
                    # break

            # 如果抓不到<p>标签，证明已经抓取完
            if notnull:
                webfile = open(src, 'wb')  # 保存网页到本地
                webfile.write(webcontent)
                webfile.close()
                print("已经抓取:" + site + '----标签：' + tagName)
            else:
                lock = open(src.replace('html', lockprefix), 'w')  # 抓取完毕了
                # 日期：http://blog.csdn.net/u012175089/article/details/62044335
                finish = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
                lock.write('抓取完成时间：' + finish)
                print("抓取完毕：" + tagName)
                break
        i += 1  # 加页
# 计时
endTime = time.clock()
print("爬取总共运行时间 : %.03f 秒" % (endTime - startTime))
