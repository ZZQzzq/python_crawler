
from src.movie.tools.Html_manager import getHtml, getBinaryHtml
import time
import os.path
from src.tool.ExcelManager import validateTitle
import re
from src.tool.ProxyManager import makeProxyAddress
from src.movie.tools.Db_manager import DbManager


# 第7步:抓取电影
# 读取movie表，读取movie_tag表，抓取电影详情网页到不同标签目录
web504 = ['1470617']
# 抓取电影详情页
'''
# 读取movie表，读取movie_tag表，抓取图书网页拷贝多份到不同标签目录
def catchmovie(requreip = 0, v=0,startmovie=0):
	"""
	输入参数为:
	是否使用代理，默认否
	是否限制爬虫速度，默认否，时间为1秒仿人工
	startmovie = 0 查询起始位置,如果处理过程失败，可以抽取数据库第startmovie条数据之后进行爬取
'''
requreip = 0
v = 1.2
startmovie = 0
# 进行计时
start = time.clock()
webe = []
selecttotal = 'select count(distinct movie_no) from movie_tag'   # 选出所有的电影（按编号选取）
selectsql = 'SELECT movie_name,movie_no,movie_kind FROM movie_tag group by movie_no'  # 按编号分组

dbManager = DbManager()
total = dbManager.execQuery(selecttotal)  # 总记录（执行该语句，找出所有图书）
total = int(total[0][0])  # 不同书籍总数目
daili0 = makeProxyAddress()  # 代理IP数组
daili_no = 0
change_ip = 0  # 代理ip下标

# 循环对分类进行抓取
while startmovie < total+100:
	selectsql1 = selectsql+' limit '+str(startmovie)+',100'  # 每一百部抓一次
	taglist = dbManager.execQuery(selectsql1)
	for i in range(0, len(taglist)):
		try:
			"""
			由selectsql1查找表的时候，按照编号分组.
			movie_tag（movie_name,movie_no，movie_kind）
			所以，taglist[i][0]表示电影名...
			"""
			movie_name = taglist[i][0]  # 电影名
			movie_kind = taglist[i][2]   # 所在标签（年代）
			movie_no = taglist[i][1]   # 电影编号
			url = 'http://movie.douban.com/subject/'+movie_no   # 抓取网址
			# eg.http://movie.douban.com/subject/26580232
		except:
			raise
		mulu0 = '../movie_detail_message/'+movie_kind
		# 存在大分类文件夹则跳过
		if os.path.exists(mulu0):
			pass
		else:  # 否则新建
			print('新建标签：'+mulu0)
			os.makedirs(mulu0)
		# 判断文件是否存在，存在则不抓取节省时间
		try:
			filename = mulu0+'/'+movie_no + validateTitle(movie_name)+'.html'  # 新建html文件名称
			if(os.path.exists(filename) == True):
				print(filename+'：已经存在')
				continue
			elif movie_no in web504:
				# 写入本地文件
				print('----'*5)
				print("504错误,跳过："+movie_no)
				print('----'*5)
				continue
			else:
				# print("-"*50)
				print('准备抓取：'+url+'年代：'+movie_kind)
		except:
			print(filename+"文件名异常")
			continue
		iprefuse = 1  # 如果抓取成功设为0
		# 如果抓取出错那重新抓取
		while iprefuse:
			try:
				daili1 = daili0[change_ip]  # 代理ip
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
					print("已经抓取:"+url+'类别：'+movie_kind)
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
					print("已经抓取:"+url+'类别：'+movie_kind)
					iprefuse = 0
					daili_no += 1
					print('此次转换代理次数:'+str(daili_no))
					if daili_no > 15: #代理15次仍然抓取不到，则认为主机不可达
						daili_no = 0
						requreip = 0   # 代理100次后转为非代理
						break
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
						webe.append(movie_no)
						break
				elif hasattr(e, 'reason'):
						print("无法到达主机.")
						print('Reason:  ', e.reason)
				print(e)
				if requreip:
					change_ip += 1  # 更换ip下标
					if change_ip == len(daili0):   # 到达ip数组末循环再来
						change_ip = 0
					print('更换代理：'+daili0[change_ip])
					daili_no += 1
					print('此次转换代理次数:'+str(daili_no))
					if daili_no > 15:
						daili_no = 0
						requreip = 0   # 代理100次后转为非代理
						break   # 跳出while循环
				else:
					print("IP被封或断网")
					requreip = 1   # 转为代理
	print('已经抓了'+str(startmovie+100)+'部')
	print()  # 三行空格
	print()
	print()
	startmovie += 100
	if len(webe) > 20:
		print(webe)
		webep = open("../movie_detail_message/movie_detail.txt", 'a+')
		webep.write(','.join(webe)+'/n')
		webep.close()
		webe = []
	else:
		pass

end = time.clock()
print("爬取总共运行时间 : %.03f 秒" % (end-start))