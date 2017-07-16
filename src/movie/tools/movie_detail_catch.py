import re
import string
from bs4 import BeautifulSoup

"""
  抓取单部电影
"""
url = open('D:/workplace/pythonwork/douban_book_catch_zzq/src/movie_detail_message/1990/1305995童年记趣.html', 'rb')
url_content = url.read()
soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
"""
#  查找对应的meta标签，返回的是整个标签的内容
movie_no = soup.find('meta', attrs={'name': 'mobile-agent'})
# 这里是有问题的，meta标签没闭合
# 求电影的编号
movie_no = movie_no['content'].split('subject/')[1].replace('/', '')
print("编号："+movie_no)
# 电影名.
try:
    movie_name = soup.find('span', {'property': 'v:itemreviewed'}).get_text().replace(" ", "").strip()
    movie_name = movie_name.replace("'", '\'')
except:
    print("获取电影名失败")
    movie_name = u'-'
# movie_name = soup.td.a['title']  # 电影名称
print("电影名："+movie_name)
# 上映日期 (split去掉括弧) (replace去掉年和月，进行数据清洗)
movie_year = soup.find('span', attrs={"class": "year"}).text.split('(')[1].split(')')[0].replace('年', '.').replace('月', '')
print("电影制作完成时间："+movie_year)

movie_info = soup.find('div', attrs={"id": "info"})  # 电影信息
# print("电影信息："+movie_info.get_text())
try:
    movie_dir = soup.select("div.article div#info span:nth-of-type(1) span.attrs")
    soup_dir = BeautifulSoup(str(movie_dir), 'html.parser')
    movie_director = soup_dir.a.string  # xpath('//*[@id="info"]/span[1]/a/text()').extract()
except:
    movie_director = '无'
#print(movie_dir)
print("导演:" + movie_director)

try:
    movie_pl1 = soup.select("div.article div#info span:nth-of-type(4) span.attrs ")
    soup_pl = BeautifulSoup(str(movie_pl1), 'html.parser')
    movie_pl2 = soup_pl.findAll('a')
    movie_pl = ''
    for i in movie_pl2:
        movie_pl += i.string + '/'
    movie_pl = movie_pl.strip(string.punctuation).strip()  # 去掉后多出来的/
except:
    movie_pl = '无'
#print(movie_pl1)
print("编剧:"+movie_pl)

try:
    movie_act1 = soup.select("div.article div#info span:nth-of-type(7) span.attrs")
    soup_act = BeautifulSoup(str(movie_act1), 'html.parser')
    movie_act2 = soup_act.findAll('a')
    movie_actor = ''
    for i in movie_act2:
        movie_actor += i.string + '/'
    movie_actor = movie_actor.strip(string.punctuation).strip()
except:
    movie_actor = '无'
print("主演:"+movie_actor)
# 类型：
try:
    infoType = movie_info.findAll('span',{'property':'v:genre'})
    # 获取类型
    typestr = ''  # 先初始化为空字符串
    for i in infoType:
        typestr += i.string+'/'
    movie_type = typestr.strip(string.punctuation).strip()
except:
    print("抓取类型出错")
    movie_type = u'-'
print("类型:"+movie_type)

# 语言，地区
try:
    items = movie_info.findAll('span', attrs={'class': 'pl'})
    for item in items:
         if item.string == u"语言:":  # .string之后是unicode，get_text()才是string
            language = item.nextSibling.strip().split("/")[0].strip()
         if item.string == u"制片国家/地区:":
            country = item.nextSibling.strip().split("/")[0].strip()
except:
    print ("抓取语言和国家时出错")
    language = u'-'
    country = u'-'
print("制片国家/地区:" + country)
print("语言：" + language)


# 上映时间
try:
    infoReleaseDate = movie_info.findAll('span', {'property': 'v:initialReleaseDate'})[0]
    movie_ReleaseDate = re.search(u'\d*-*\d*-*\d*', infoReleaseDate.get_text()).group().strip()
except:
    movie_ReleaseDate = u'-'
print("上映时间："+movie_ReleaseDate)
# 片长:
try:
    infoRunTime = movie_info.find('span', {'property': 'v:runtime'})
    runtime = re.search(u'\d+', infoRunTime.get_text()).group().strip()  # 采用正则表达式
except:
    runtime = u'-'
print("片长:"+runtime+"分钟")


# 评论人数：
try:
    infoVoteNum = soup.find('span', {'property': 'v:votes'})
    votenum = infoVoteNum.get_text().strip()
except:
    print("评论人数不足")
    votenum = u'-'
print("评论人数："+votenum)

# 星级评价：
try:
    stars = '-'
    infostar = soup.find('strong', {'class': 'll rating_num'})
    stars = infostar.get_text().strip()
except:
    print("抓取评价出错")
    stars = u'-'  # 使用u或者U处理unicode文本
print("星级评价："+stars)

ratio = soup.findAll('span', attrs={"class", "rating_per"})  # 人数的比例
voteratio = []
for i in ratio:
    voteratio.append(i.text)
print("人数比例：")
print(voteratio)

# 剧情介绍
try:
    movie_intro = []
    movie_intro1 = soup.findAll('span', attrs={"property": "v:summary"})  # 剧情介绍
    for j in movie_intro1:
        movie_intro.append(j.get_text().replace(' \n', '').replace('\n ', '').replace(' ', '').replace('\u3000', ' '))  #.decode('unicode_escape')
        # print(j.text.strip())
except:
    print('暂无剧情介绍')
    movie_intro = '-'

print("剧情介绍:")
print(movie_intro)
# 爬相关电影
try:
    movie_like = soup.find('div', attrs={"class": "recommendations-bd"})  # 相关电影推荐 可能不存在
    recommendations = []
    movie = movie_like.findAll('dl')
    for i in movie:
         recommendations.append(["电影名称："+i.dd.a.string, "相关链接："+i.dd.a['href']])
         # print("电影名称："+i.dd.a.string+",相关链接："+i.dd.a['href'])
except:
    recommendations = '暂无推荐'
print("相关推荐：")
print(recommendations)

# 评论
comments = []
movie_comment = soup.findAll('div', attrs=['class', 'comment-item'])
for comment in range(0, len(movie_comment)-1):
    simple_comment = BeautifulSoup(str(movie_comment[comment]), 'html.parser')
    movie_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
    comment_id = movie_comment1.find('a').string
    print("评论id:"+comment_id)
    movie_comment11 = BeautifulSoup(str(movie_comment1), 'html.parser')
    movie_comment2 = simple_comment.find('p').get_text()  # 评论详情
    print("评论内容："+movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''))
    movie_comment3 = movie_comment11.select("span:nth-of-type(3)")  # 评价等级
    #print(movie_comment3)
    try:
        movie_comment33 = str(movie_comment3).split('title="')[1].split('">')[0]
    except:
        movie_comment33 = 'none'
    print("评价等级:"+movie_comment33)
    movie_comment4 = simple_comment.find('span', attrs=['class', 'votes']).get_text()  # 该评价有用程度
    print("有用程度："+movie_comment4)
    comments.append(['评论ID：' + comment_id, '评论内容：' + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''), '有用程度：' + movie_comment4])   # \xa0是不间断空白符


"""
#return [movie_no, movie_name, movie_year, movie_director, movie_pl, movie_actor, movie_type, country, language, movie_ReleaseDate, runtime, votenum ,stars, voteratio, movie_intro, recommendations, comments]
movie_no = soup.find('meta', attrs={'name': 'mobile-agent'})
# 求电影的编号
movie_no = movie_no['content'].split('subject/')[1].replace('/', '')
#print("编号：" + movie_no)
# 电影名.
try:
     movie_name = soup.find('span', {'property': 'v:itemreviewed'}).get_text().replace(" ", "").strip()
    # movie_name = movie_name.replace("'", '\'')
except:
    print("获取电影名失败")
    movie_name = u'-'

#print("电影名：" + movie_name)
# 上映日期 (split去掉括弧) (replace去掉年和月，进行数据清洗)
try:
    movie_year = soup.find('span', attrs={"class": "year"}).text.split('(')[1].split(')')[0].replace('年', '.').replace('月', '')
except:
    movie_year = 'none'
#print("电影制作完成时间：" + movie_year)

movie_info = soup.find('div', attrs={"id": "info"})  # 电影信息
# print("电影信息："+movie_info.get_text())
try:
    movie_dir = soup.select("div.article div#info span:nth-of-type(1) span.attrs")
    soup_dir = BeautifulSoup(str(movie_dir), 'html.parser')
    movie_director = soup_dir.a.string  # xpath('//*[@id="info"]/span[1]/a/text()').extract()
except:
    movie_director = '无'
    # print(movie_dir)
   # print("导演:" + movie_director)

try:
    movie_pl1 = soup.select("div.article div#info span:nth-of-type(4) span.attrs ")
    soup_pl = BeautifulSoup(str(movie_pl1), 'html.parser')
    movie_pl2 = soup_pl.findAll('a')
    movie_pl = ''
    for i in movie_pl2:
        movie_pl += i.string + '/'
    movie_pl = str(movie_pl.strip(string.punctuation).strip()) # 去掉后多出来的/
except:
    movie_pl = '无'
    # print(movie_pl1)
    #print("编剧:" + movie_pl)

try:
    movie_act1 = soup.select("div.article div#info span:nth-of-type(7) span.attrs")
    soup_act = BeautifulSoup(str(movie_act1), 'html.parser')
    movie_act2 = soup_act.findAll('a')
    movie_actor = ''
    for i in movie_act2:
        movie_actor += i.string + '/'
    movie_actor = str(movie_actor.strip(string.punctuation).strip())
except:
    movie_actor = '无'
# print("主演:" + movie_actor)
# 类型：
try:
    infoType = movie_info.findAll('span', {'property': 'v:genre'})
    # 获取类型
    typestr = ''  # 先初始化为空字符串
    for i in infoType:
        typestr += i.string + '/'
    movie_type = typestr.strip(string.punctuation).strip()
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
# print("制片国家/地区:" + country)
# print("语言：" + language)

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
    votenum = u'-'
# print("评论人数：" + votenum)

# 星级评价：
try:
    stars = "-"
    infostar = soup.find('strong', {'class': 'll rating_num'})
    stars = infostar.get_text().strip()
except:
    print("抓取评价出错")
    stars = "-"  # 使用u或者U处理unicode文本
   # print("星级评价：" + stars)

try:
    ratio = soup.findAll('span', attrs={"class", "rating_per"})  # 人数的比例
    voteratio = ''
    for i in ratio:
        voteratio += i.text + ','
        voteratio = str(voteratio.strip(string.punctuation).strip())
        if(voteratio == ''):
            voteratio = '-'
except:
    voteratio = "-"


   # print("人数比例：")
   # print(voteratio)

    # 剧情介绍
try:
    movie_intro = ''
    movie_intro1 = soup.findAll('span', attrs={"property": "v:summary"})  # 剧情介绍
    for j in movie_intro1:
        movie_intro += j.get_text().replace(' \n', '').replace('\n ', '').replace(' ', '').replace('\u3000', ' ')   # .decode('unicode_escape')
         # print(j.text.strip())
    movie_intro = str(movie_intro)
except:
    print('暂无剧情介绍')
    movie_intro = '-'

   # print("剧情介绍:")
   # print(movie_intro)
    # 爬相关电影
try:
    movie_like = soup.find('div', attrs={"class": "recommendations-bd"})  # 相关电影推荐 可能不存在
    recomm = ''
    movie = movie_like.findAll('dl')
    for i in movie:
        recomm += i.dd.a.string + ','  #  , "相关链接：" + i.dd.a['href']])
    recommendations = recomm.strip(string.punctuation).strip()
            # print("电影名称："+i.dd.a.string+",相关链接："+i.dd.a['href'])
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
        comment_id = movie_comment1.find('a').string
       # print("评论id:" + comment_id)
        movie_comment11 = BeautifulSoup(str(movie_comment1), 'html.parser')
        movie_comment2 = simple_comment.find('p').get_text()  # 评论详情
        #print("评论内容：" + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''))
        movie_comment3 = movie_comment11.select("span:nth-of-type(3)")  # 评价等级
        # print(movie_comment3)
        try:
            movie_comment33 = str(movie_comment3).split('title="')[1].split('">')[0]
        except:
            movie_comment33 = 'none'
       # print("评价等级:" + movie_comment33)
        movie_comment4 = simple_comment.find('span', attrs=['class', 'votes']).get_text()  # 该评价有用程度
       # print("有用程度：" + movie_comment4)
       # comments.append(
       #     '<br />'.join(['评论ID：' + comment_id, '评论内容：' + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''),
       #                 '评论等级：' + movie_comment33.replace('\xa0', '\n'), '有用程度：' + movie_comment4])
      #  )  # \xa0是不间断空白符
        comments.append(['评论ID：' + comment_id, '评论内容：' + movie_comment2.replace(' \n', '').replace('\n ', '').replace(' ', ''),
                           '评论等级：' + movie_comment33.replace('\xa0', '\n'), '有用程度：' + movie_comment4])
         # \xa0是不间断空白符

print(movie_no, movie_name, movie_year, movie_director, movie_pl, movie_actor, movie_type, country, language,
            movie_ReleaseDate, runtime, votenum, stars, voteratio, movie_intro, recommendations,  comments)
