# -*- coding:utf-8 -*-
import multiprocessing
from src.tool.HtmlManager import getHtml, getBinaryHtml
import time
import os.path
from src.tool.ExcelManager import validateTitle
import re
from src.tool.ProxyManager import makeProxyAddress
from src.tool.DbManager import DbManager


# 第7步:抓取图书
# 读取book表，读取book_tag表，抓取图书网页拷贝多份到不同标签目录
# web504 = ['1010668', '1023322', '10459781', '1915375']

web504 = []  # 抓取图书详情页
'''
# 读取book表，读取booktag表，抓取图书网页拷贝多份到不同标签目录
def catchbook(requreip = 0, v=0,startbook=0):
	"""
	输入参数为:
	是否使用代理，默认否
	是否限制爬虫速度，默认否，时间为1秒仿人工
	startbook = 0 查询起始位置,如果处理过程失败，可以抽取数据库第startbook条数据之后进行爬取
'''
requreip = 0
v = 1.2
startbook = 0
# 进行计时
start = time.clock()
webe = []  # 存放抓取出错的书籍编号
selecttotal = 'select count(distinct book_no) from book_tag'   # 选出所有的图书（按编号选取）
selectsql = 'SELECT book_name,book_kind,book_no FROM book_tag group by book_no'  # 按编号分组

dbManager = DbManager()
total = dbManager.execQuery(selecttotal)  # 总记录（执行该语句，找出所有图书）
total = int(total[0][0])  # 不同书籍总数目
daili0 = makeProxyAddress()  # 代理IP数组
dailino = 0
changeip = 0  # 代理ip下标
# 循环对分类进行抓取
while startbook < total+100:
	selectsql1 = selectsql+' limit '+str(startbook)+',100'
	taglist = dbManager.execQuery(selectsql1)
	for i in range(0, len(taglist)):
		try:
			"""
			由selectsql1查找表的时候，按照编号分组.
			临时新建关系（book_name,book_kind,book_no）
			所以，taglist[i][0]表示书名...
			"""
			book_name = taglist[i][0]  # 书名
			book_kind = taglist[i][1]   # 分类
			book_no = taglist[i][2]   # 图书编号
			url = 'http://book.douban.com/subject/'+book_no   # 抓取网址
			# eg.http://book.douban.com/subject/25862578
		except:
			raise
		mulu0 = '../src/book_detail_message/'+book_kind
		# 存在大分类文件夹则跳过
		if os.path.exists(mulu0):
			pass
		else:  # 否则新建
			print('新建大分类：'+mulu0)
			os.makedirs(mulu0)
		# 判断文件是否存在，存在则不抓取节省时间
		try:
			filename = mulu0+'/'+book_no+validateTitle(book_name)+'.html'  # 新建html文件名称
			if os.path.exists(filename) == True:
				print(filename+'：已经存在')
				continue
			elif book_no in web504:
				# 写入本地文件
				print('----'*5)
				print("504错误,跳过："+book_no)
				print('----'*5)
				continue
			else:
				# print("-"*50)
				print('准备抓取：'+url+'类别：'+book_kind)
		except:
			print(filename+"文件名异常")
			continue
		iprefuse = 1  # 如果抓取成功设为0
		# 如果抓取出错那重新抓取
		while iprefuse:
			try:
				daili1 = daili0[changeip]  # 代理ip
				# 爬虫速度控制
				if v:
					a = time.clock()
					time.sleep(v)
					b = time.clock()
					print('时间暂停:'+str(v))
					print('真实时间暂停（Unix CPU时间,Windows 真实时间):'+str(b-a))
				# 不需要代理
				if requreip == 0:
					webcontent = getHtml(url).encode('utf-8')  # 爬取，有时间限制，应对504错误
					notnull = re.search(r'<div class="top-nav-doubanapp">', webcontent.decode('utf-8', 'ignore'))
					if notnull:
						pass
					else:
						raise Exception("抓到的页面不是正确的页面"+filename)
					webfile = open(filename, 'wb')
					webfile.write(webcontent)
					webfile.close()
					print("已经抓取:"+url+'类别：'+book_kind)
					iprefuse = 0   # 抓完设置0
				else:   # 需要代理
					print('代理：'+daili1)
					webcontent = getBinaryHtml(url, daili1)
					notnull = re.search(r'<div class="top-nav-doubanapp">', webcontent.decode('utf-8', 'ignore'))
					if notnull:
						pass
					else:
						raise Exception("抓到的页面不是正确的页面"+filename)
					webfile = open(filename, 'wb')
					webfile.write(webcontent)
					webfile.close()
					print("已经抓取:"+url+'类别：'+book_kind)
					iprefuse = 0
					dailino += 1
					print('此次转换代理次数:'+str(dailino))
					if dailino > 20:
						dailino = 0
						requreip = 0   # 代理100次后转为非代理
			#  except urllib.error.URLError as e:
			except Exception as e:
				print(url)
				if hasattr(e, 'code'):
			# hasattr(object, name)。
			# 判断一个对象里面是否有name属性或者name方法，返回BOOL值，有name特性返回True， 否则返回False。
			# 需要注意的是name要用括号括起来.
					print('页面不存在或时间太长.')
					print('Error code:', e.code)
					if e.code == 404:
						print('404错误，忽略')
						webe.append(book_no)
						break
				elif hasattr(e, 'reason'):
						print("无法到达主机.")
						print('Reason:  ', e.reason)
				print(e)
				if requreip:
					changeip += 1  # 更换ip下标
					if changeip == len(daili0):   # 到达ip数组末循环再来
						changeip = 0
					print('更换代理：'+daili0[changeip])
					dailino += 1
					print('此次转换代理次数:'+str(dailino))
					if dailino > 15:
						dailino = 0
						requreip = 0   # 代理100次后转为非代理
						break
				else:
					print("IP被封或断网")
					requreip = 1   # 转为代理
	print('已经抓了'+str(startbook+100)+'本')
	print()  # 三行空格
	print()
	print()
	startbook += 100
	if len(webe) > 20:
		print(webe)
		webep = open("../src/book_detail_message/book_detail.txt", 'a+')
		webep.write(','.join(webe)+'/n')
		webep.close()
		webe = []
	else:
		pass

end = time.clock()
print("爬取总共运行时间 : %.03f 秒" % (end-start))


