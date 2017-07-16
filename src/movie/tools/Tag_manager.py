# -*- coding:utf-8 -*-
import re
import string

from bs4 import BeautifulSoup  # 解析html结构的模块
from src.tool.ExcelManager import writeExcel
import urllib.request
def makeMovieListInfo(url_content):#抓取电影列表信息
    movies = []  # 初始化为一个空列表
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    movietable = soup.select('div#content div.article div table')  # 找到所有电影信息所在标记
    for movie in movietable: # 循环遍历电影列表
        simplemovie = movie   # movie为movietable1下面的一个table标签
        subsoup = BeautifulSoup(str(simplemovie), 'html.parser')  # 单部电影进行解析
        movie_link = subsoup.td.a['href']  # 直接使用标签，然后获得属性的值  # 电影封面：
        movie_large_img = subsoup.td.img['src']  # 图片链接
        img_temp = movie_large_img.split('/')  # 将该链接以‘/’进行切分
        img_temp[len(img_temp) - 2] = 'spic'
        movie_name = subsoup.td.a['title']  # 电影名称
        movie_info = subsoup.p.string    # 电影主演信息
        try:
            movie_star = subsoup.find('span', attrs={"class": "rating_nums"}).string  # 电影星级
        except:
            movie_star = '-'
            pass
        try:
            movie_info = movie_info.strip(' \n')  # strip用来去掉换行符和空格
        except:
            movie_info = '-'
        movies.append([movie_name, movie_link, movie_large_img, movie_info, movie_star])  # 构建自己的信息结构
    return movies  # 返回电影列表

"""
def makeMovieInfo(url_content):
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    #  查找对应的meta标签，返回的是整个标签的内容
    movie_no = soup.find('meta', attrs={'name': 'mobile-agent'})
    # 这里是有问题的，meta标签没闭合
    # 求电影的编号
    movie_no = movie_no['content'].split('subject/')[1].replace('/', '')
  #  print("编号："+movie_no)
    # 电影名，不知道为什么是有空格和换行符的，看html源文件是没有的，但是取出来就有了。
    movie_name = soup.find('h1').text.replace('\n', '')
  #  print("电影名："+movie_name)
    movie_year = soup.find('span', attrs={"class": "year"}).text  # 上映日期
  #  print("上映时间："+movie_year)
    movie_info = soup.find('div', attrs={"id": "info"}).text  # 电影信息
  #  print("电影信息："+movie_info)

    peoples = soup.find('a', attrs={"class", "rating_people"}).text  # 评分的人数
 #   print("评分人数："+peoples)
    ratio = soup.findAll('span', attrs={"class", "rating_per"})  # 人数的比例
    stars = []
    for i in ratio:
        stars.append(i.text)
  #  print("人数比例：")
  #  print(stars)
    # 爬剧情
    movie_intro1 = []
    movie_intro = soup.findAll('span', attrs={"class": "all hidden"}) # 剧情介绍
    for j in movie_intro:
       movie_intro1.append(j.text.replace(' \n', '').replace('\n ', '').replace(' ', ''))
     #  print("剧情介绍："+j.text.replace(' \n', '').replace('\n ', '').replace(' ', ''))
       # print(j.text.strip())
    # 爬相关电影
    movie_like = soup.find('div', attrs={"class": "recommendations-bd"})  # 相关电影推荐 可能不存在
    recommendations = []
    movie = movie_like.findAll('dl')
    for i in movie:
        recommendations.append(["\n电影名称："+i.dd.a.string, "相关链接："+i.dd.a['href']])
    #   print("电影名称："+i.dd.a.string+",相关链接："+i.dd.a['href'])
    # 爬评论
    comments = []
    # 获取评论信息
    movie_comment = soup.findAll('div', attrs=['class', 'comment-item'])
    for comment in range(0, len(movie_comment)-1):
        #print("大框架："+str(comment))
        simple_comment = BeautifulSoup(str(movie_comment[comment]), 'html.parser')
        movie_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
        #print("评论id:"+str(movie_comment1))
        comment_id = movie_comment1.find('a').string
       # print("评论id:"+comment_id)
        movie_comment11 = BeautifulSoup(str(movie_comment1), 'html.parser')
        movie_comment2 = simple_comment.find('p').get_text()  # 评论详情
       # print("评论详情："+movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''))
        movie_comment3 = movie_comment11.select("span:nth-of-type(3)")  # 评价等级
        try:
            movie_comment33 = movie_comment3.find('span', 'title')
        except:
            movie_comment33 = 'none'
       # print("评价等级:"+movie_comment33)
        movie_comment4 = simple_comment.find('span', attrs=['class', 'votes']).get_text()  # 该评价有用程度
       # print("有用程度："+movie_comment4)
        comments.append(['评论ID：' + comment_id, '评论内容：' + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''), '有用程度：' + movie_comment4])   # \xa0是不间断空白符

    # 所以，核心内容是那几个提取的函数find，findAll，select。理解这三个函数。其他部分都不重要了。
    # 构造成一个列表
    return [movie_no, movie_name, movie_year, movie_info, movie_intro1, int(peoples.replace('人评价', '')), '  ,'.join(stars),
            recommendations, comments]
""" """
	抓取单部电影
	"""
def makeMovieInfo(url_content):
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    #  查找对应的meta标签，返回的是整个标签的内容
    movie_no = soup.find('meta', attrs={'name': 'mobile-agent'})
    movie_no = movie_no['content'].split('subject/')[1].replace('/', '')    # 电影的编号
    try:    # 电影名.
        movie_name = soup.find('span', {'property': 'v:itemreviewed'}).get_text().replace(" ", "").strip()
        movie_name = movie_name.replace("'", "\\'").replace('"', '\\"')
    except:
        print("获取电影名失败")
        movie_name = u'-'
    #print("电影名：" + movie_name)
    # 上映日期 (split去掉括弧) (replace去掉年和月，进行数据清洗)
    try:
        movie_year = soup.find('span', attrs={"class": "year"}).text.split('(')[1].split(')')[0].replace('年', '.').replace('月', '')
    except:
        movie_year = '-'
    #print("电影制作完成时间：" + movie_year)
    movie_info = soup.find('div', attrs={"id": "info"})  # 电影信息
    # print("电影信息："+movie_info.get_text())
    try:
        movie_dir = soup.select("div.article div#info span:nth-of-type(1) span.attrs")
        soup_dir = BeautifulSoup(str(movie_dir), 'html.parser')
        movie_director = soup_dir.a.string.replace("'", "\\'").replace('"', '\\"')  #.replace("'", '\\"').replace('"', '\\"')  # xpath('//*[@id="info"]/span[1]/a/text()').extract()
    except:
        movie_director = '-'
    # print(movie_dir)
   # print("导演:" + movie_director)

    try:
        movie_pl1 = soup.select("div.article div#info span:nth-of-type(4) span.attrs ")
        soup_pl = BeautifulSoup(str(movie_pl1), 'html.parser')
        movie_pl2 = soup_pl.findAll('a')
        movie_pl = ''
        for i in movie_pl2:
            movie_pl += i.string + '/'
        movie_pl = str(movie_pl.strip(string.punctuation).strip()).replace("'", "\\'").replace('"', '\\"')   #.replace("'", "\\'").replace('"', '\\"') # 去掉后多出来的/
    except:
        movie_pl = '-'
    # print(movie_pl1)
    #print("编剧:" + movie_pl)

    try:
        movie_act1 = soup.select("div.article div#info span:nth-of-type(7) span.attrs")
        soup_act = BeautifulSoup(str(movie_act1), 'html.parser')
        movie_act2 = soup_act.findAll('a')
        movie_actor = ''
        for i in movie_act2:
            movie_actor += i.string + '/'
        movie_actor = str(movie_actor.strip(string.punctuation).strip()).replace("'", "\\'").replace('"', '\\"')  # .replace("'", '\\"').replace('"', '\\"')
    except:
        movie_actor = '-'
   # print("主演:" + movie_actor)
    # 类型：
    try:
        infoType = movie_info.findAll('span', {'property': 'v:genre'})
        # 获取类型
        typestr = ''  # 先初始化为空字符串
        for i in infoType:
            typestr += i.string + '/'
        movie_type = typestr.strip(string.punctuation).strip()
        if movie_type == '':
            movie_type = "无"
    except:
        print("抓取类型出错")
        movie_type = u'-'
    #print("类型:" + movie_type)

    # 语言，地区
    try:
        language = u'-'
        country = u'-'
        items = movie_info.findAll('span', attrs={'class': 'pl'})
        for item in items:
            if item.string == u"语言:":  # .string之后是unicode，get_text()才是string
                language = item.nextSibling.strip().split("/")[0].strip()
            if item.string == u"制片国家/地区:":
                country = item.nextSibling.strip().split("/")[0].strip()
    except:
        print("抓取语言和国家时出错")
        language = u'-'
        country = u'-'
    #print("制片国家/地区:" + country)
    #print("语言：" + language)

    # 上映时间
    try:
        infoReleaseDate = movie_info.findAll('span', {'property': 'v:initialReleaseDate'})[0]
        movie_ReleaseDate = re.search(u'\d*-*\d*-*\d*', infoReleaseDate.get_text()).group().strip()
    except:
        movie_ReleaseDate = u'-'
   # print("上映时间：" + movie_ReleaseDate)
    # 片长:
    try:
        infoRunTime = movie_info.find('span', {'property': 'v:runtime'})
        runtime = re.search(u'\d+', infoRunTime.get_text()).group().strip()  # 采用正则表达式
    except:
        runtime = u'-'
   # print("片长:" + runtime + "分钟")

    # 评论人数：
    try:
        infoVoteNum = soup.find('span', {'property': 'v:votes'})
        votenum = infoVoteNum.get_text().strip()
    except:
       # print("评论人数不足")
        votenum = '0'
    # print("评论人数：" + votenum)
    # 星级评价：
    try:
        infostar = soup.find('strong', {'class': 'll rating_num'})
        stars = infostar.get_text().strip()
        if stars == '':
            stars = "0"

    except:
        print("抓取评价出错")
        stars = "0"  # 使用u或者U处理unicode文本
   # print("星级评价：" + stars)

    try:
        ratio = soup.findAll('span', attrs={"class", "rating_per"})  # 人数的比例
        voteratio = []
        for i in ratio:
            voteratio.append(i.text)
        if voteratio == []:
            voteratio = "-"
    except:
        voteratio = "-"


   # print("人数比例：")
   # print(voteratio)

    # 剧情介绍
    try:
        movie_intro = ''
        movie_intro1 = soup.findAll('span', attrs={"property": "v:summary"})  # 剧情介绍
        for j in movie_intro1:
            movie_intro += j.get_text().replace(' \n', '').replace('\n ', '').replace(' ', '').replace('\u3000', ' ').replace("'", "\\'").replace('"', '\\"')  #.replace("'", '\\"').replace('"', '\\"')  # .decode('unicode_escape')
            # print(j.text.strip())
        movie_intro = str(movie_intro)
        if movie_intro == '':
            movie_intro = '暂无剧情介绍'
    except:
        print('暂无剧情介绍')
        movie_intro = '暂无剧情介绍'

   # print("剧情介绍:")
   # print(movie_intro)
    # 爬相关电影
    try:
        movie_like = soup.find('div', attrs={"class": "recommendations-bd"})  # 相关电影推荐 可能不存在
        recomm = ''
        movie = movie_like.findAll('dl')
        for i in movie:
            recomm += i.dd.a.string + ','  #  , "相关链接：" + i.dd.a['href']])
        recommendations = recomm.strip(string.punctuation).strip().replace("'", "\\'").replace('"', '\\"')  #.replace("'", '\\"').replace('"', '\\"')
            # print("电影名称："+i.dd.a.string+",相关链接："+i.dd.a['href'])
        if recommendations == '':
            recommendations = '暂无推荐'
    except:
        recommendations = '暂无推荐'
   # print("相关推荐：")
   # print(recommendations)

    # 评论
    comments = []
    movie_comment = soup.findAll('div', attrs=['class', 'comment-item'])
    for comment in range(0, len(movie_comment) - 1):
        simple_comment = BeautifulSoup(str(movie_comment[comment]), 'html.parser')
        movie_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
        comment_id = movie_comment1.find('a').string.replace("'", "\\'").replace('"', '\\"')
       # print("评论id:" + comment_id)
        movie_comment11 = BeautifulSoup(str(movie_comment1), 'html.parser')
        movie_comment2 = simple_comment.find('p').get_text().replace(' \n', '').replace('\n ', '').replace(' ', '').replace("'", "\\'").replace('"', '\\"') # 评论详情
        #print("评论内容：" + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''))
        movie_comment3 = movie_comment11.select("span:nth-of-type(3)")  # 评价等级
        # print(movie_comment3)
        try:
            movie_comment33 = str(movie_comment3).split('title="')[1].split('">')[0]
            if movie_comment33 == '力荐':
                movie_comment33 = '★★★★★'
            elif movie_comment33 == '推荐':
                movie_comment33 = '★★★★'
            elif movie_comment33 == '还行':
                movie_comment33 = '★★★'
            elif movie_comment33 == '较差':
                movie_comment33 = '★★'
            elif movie_comment33 == '很差':
                movie_comment33 = '★'
            else:
                movie_comment33 = '该用户未评分'
        except:
            movie_comment33 = '-'
       # print("评价等级:" + movie_comment33)
        movie_comment4 = simple_comment.find('span', attrs=['class', 'votes']).get_text()  # 该评价有用程度
       # print("有用程度：" + movie_comment4)
        comments.append(
           '<br /> '.join(['评论ID：' + comment_id, '评论内容：' + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''),
                        '评论等级：' + movie_comment33.replace('\xa0', '\n'), '点赞次数：' + movie_comment4]) #.replace("'", '\\"').replace('"', '\\"')
        )  # \xa0是不间断空白符

    return [movie_no, movie_name, movie_year, movie_director, movie_pl, movie_actor, movie_type, country, language,
            movie_ReleaseDate, runtime, int(votenum), stars, ','.join(voteratio), movie_intro, recommendations, '<hr />'.join(comments)]

def makeMovieTag(url_content, path='D:/workplace/pythonwork/douban_book_catch_zzq/database/movie_tag.xlsx'):
    """
    #抓取标签提取写入Excel
    """
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    movie2 = soup.select('div#content div.article table ')  # 找出该大类下对应的分类所在table
    # css选择器，.后面跟类class名，#后面跟id名。
    taglist = [['标签名', '标签链接', '点击量']]  # Excel里面的标题
    for movietag in movie2:
            soup2 = BeautifulSoup(str(movietag), 'html.parser')  # 开始解析
            movietag3 = soup2.findAll("a")  # 标签名
            #print("标签名："+movietag3)
            movietag4 = soup2.findAll("b")   # 该标签下的电影访问量
            #print("访问量："+movietag4)
            for i in range(0, len(movietag4)):  # len(booktag4)就可以表示一行有多少种不同类型的分类
                tag = movietag3[i].string  # 标签名
                link = movietag3[i]['href']  # 链接
                print("标签名："+tag)
                print("链接："+link)
                taglink = 'https://movie.douban.com'+link  # 链接
                tagnum = movietag4[i].string
                print("访问量："+tagnum)
                taglist.append([tag.strip(), taglink.strip(), tagnum.strip()])  # 把内容加进去，按照标题的顺序
    writeExcel(path, taglist)  # 将内容写入excel中
    print("写入EXCEL成功")


def testMovieTag():
    file = open('D:\workplace\pythonwork\douban_book_catch_zzq/database/movie_tag.html', 'rb')
    content = file.read()
    makeMovieTag(content, r'D:\workplace\pythonwork\douan_book_catch_zzq\database/movie_tag.xlsx')


def testManyMovie():
    file = open('D:/workplace/pythonwork/douban_book_catch_zzq/database/movies.html', 'rb')
    content = file.read()
    movies = makeMovieListInfo(content)
    for i in movies:
        print(i)


def testMovieInfo():
    print('D:/workplace/pythonwork/douban_book_catch_zzq/database/movies.html')
    file = open('D:/workplace/pythonwork/douban_book_catch_zzq/database/movies.html', 'rb')  # 读取文件
    content = file.read()
    book = makeMovieInfo(content)
    for i in book:
        print('*' * 50)  # 分割一下，方便查看
        print(i)  # 打印一下内容


if __name__ == '__main__':

    # makeMovieTag() # 测试图书标签抓取是否成功
     testMovieInfo()
