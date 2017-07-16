import string

from bs4 import BeautifulSoup


"""
	抓取单本书
"""
url = open('D:/workplace/pythonwork/douban_book_catch_zzq/book_detail_message/经管/1011772泥鸽靶.html', 'rb')
url_content = url.read()
soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
# 查找对应的meta标签，返回的是整个标签的内容
book_no = soup.find('meta', attrs={'http-equiv': 'mobile-agent'})
# 书编号
book_no = book_no['content'].split('subject/')[1].replace('/', '')
print('编号：'+book_no)
# 书名，不知道为什么是有空格和换行符的，看html源文件是没有的，但是取出来就有了。
book_name = soup.find('h1').text.replace('\n', '')
print('书名：'+book_name)
book_info = soup.find('div', attrs={"id": "info"})  # 出版信息
"""
try:
    book_info = book_info.text.replace(' \n', '').replace('\n ', '').replace(' ', '')
except:
    book_info = ''
"""
# 作者
try:
    book_au = soup.select("div.article div#info a:nth-of-type(1)")
    #print(book_au)
    soup_au = BeautifulSoup(str(book_au), 'html.parser')
    book_author =soup_au.get_text().replace(' \n', '').replace('\n ', '').replace(' ', '') #.replace('[', '').replace(']', '')
except:
    book_author = '未检索到作者信息'
print("作者："+book_author)
# 译者
try:
    book_tra = soup.select("div.article div#info a:nth-of-type(2)")
    # print(book_tra)
    soup_tra = BeautifulSoup(str(book_tra), 'html.parser')
    book_trans = soup_tra.text.replace(' \n', '').replace('\n ', '').replace(' ', '')
except:
    book_trans = '-'
print('译者：'+book_trans)

# 出版年，页数，定价，出版社
book_message = book_info.findAll('span', attrs={'class': 'pl'})
try:
    book_year = u'-'
    book_price = u'-'
    book_page = u'-'
    book_public = u'-'
    for item in book_message:
        if item.string == u"出版年:":
            book_year = item.nextSibling.strip().split("/")[0].strip()
        if item.string == u"页数:":
            book_page = item.nextSibling.strip().split("/")[0].strip()
        if item.string == u"定价:":
            book_price = item.nextSibling.strip().split("/")[0].strip()
        if item.string == u"出版社:":
            book_public = item.nextSibling.strip().split("/")[0].strip()
except:
    print("抓取出版年和页数，定价时出错")
    book_year = '未检索到年份信息'
    book_price = '未检索到价格'
    book_page = '未检索到页数'
    book_public = '未检索到出版社信息'
print('出版社：'+book_public)
print('出版年：' + book_year)
print('页数:' + book_page)
print('定价:' + book_price)

# 评论人数：
try:
    infoVoteNum = soup.find('span', {'property': 'v:votes'})
    votenum = infoVoteNum.get_text().strip()
except:
    # print("评论人数不足")
    votenum = u'-'

print("评论人数：" + votenum)

# 星级评价：
infostar = soup.find('strong', {'property': 'v:average'})
#print(infostar)
try:
    stars = "-"
    stars = infostar.get_text().strip()
except:
    print("抓取评价出错")
    stars = "-"  # 使用u或者U处理unicode文本
print("星级评价：" + stars)

# 评价人数的比例
try:
    ratio = soup.findAll('span', attrs={"class", "rating_per"})
    voteratio = []
    for i in ratio:
        voteratio.append(i.text)
except:
    voteratio = "-"
print("人数比例：")
print(voteratio)

# 作者及书籍简介
introduce = soup.findAll('div', attrs={"class": "intro"})  # 书籍及作者介绍
# print(introduce)
book_intro = ''
author_intro = ''
if len(introduce) == 2:
    try:
        intro1 = introduce[0].findAll('p')
    except:
        intro1 = []
    try:
        intro2 = introduce[1].findAll('p')
    except:
        intro2 = []
if len(introduce) == 3:
    try:
        intro1 = introduce[1].findAll('p')
    except:
        intro1 = []
    try:
        intro2 = introduce[2].findAll('p')
    except:
        intro2 = []

# 相当于去除<p>和</p>
for i in intro1:
    book_intro = book_intro + i.text + '\n'
for i in intro2:
    author_intro = author_intro + i.text + '\n'
print('书籍简介：\n'+book_intro)
print('作者简介：\n'+author_intro)

# 丛书信息 可能不存在
book_oth = soup.findAll('div', attrs={"class": "subject_show block5"})
try:
    book_others = book_oth[0].text.replace('\n', '').replace(' ', '')
except:
    book_others = '-'
print('丛书：'+book_others)
# 目录
mu_lu = soup.select('div[id*="dir"]')  # 表示获得所有id属性中包含dir的div
#print(mu_lu)
if len(mu_lu) == 1:
    try:
        mu_lu = mu_lu[0].text.replace(' ', '')
    except:
        mu_lu = '-'
if len(mu_lu) == 2:
    try:
        mu_lu = mu_lu[1].text.replace(' · · · · · ·     (收起)', '').replace(' ', '').replace('\n', '|')
    except:
        mu_lu = '-'

print('目录：'+mu_lu)

# 推荐书籍
try:
    movie_like = soup.find('div', attrs={"class": "content clearfix"})  # 相关电影推荐 可能不存在
    recomm = ''
    movie = movie_like.findAll('dl')
    for i in movie:
        recomm += i.dd.a.string + ','
    recommendations = recomm.strip(string.punctuation).strip()
except:
    recommendations = '暂无推荐'
print('推荐书籍:'+recommendations)

# 获取评论信息
comments = []
bookcomment = soup.findAll('li', attrs=['class', 'comment-item'])
for comment in bookcomment:
    simple_comment = BeautifulSoup(str(comment), 'html.parser')
    book_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
    book_comment2 = simple_comment.find('p', attrs=['class', 'comment-content'])  # 评论详情
    book_comment11 = BeautifulSoup(str(book_comment1), 'html.parser')
    book_comment3 = book_comment11.select("span:nth-of-type(2)")  # 评价等级
   # print(book_comment3)
    try:
        book_comment33 = str(book_comment3).split('title="')[1].split('">')[0]
    except:
        book_comment33 = 'none'
    comments.append(
        ['评论ID：'+book_comment1.find('a').get_text(), '评论内容：'+book_comment2.get_text(),
                       '星级：'+book_comment33.replace('\xa0', '\n')])  # \xa0是不间断空白符
print(comments)


# 构建了表book
dbManager.execNonQuery(r"""
CREATE TABLE book (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  book_no varchar(45) NOT NULL COMMENT '书编号',
  book_name varchar(100) NOT NULL COMMENT '书名',
  book_url varchar(150) NOT NULL COMMENT '书入口',
  book_img varchar(150) DEFAULT NULL COMMENT '书图片',
  book_info text DEFAULT NULL COMMENT '书出版信息',
  book_star varchar(45) DEFAULT NULL COMMENT '书评价星数',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书表';
""")
# 构建了表book_tag（书标签）
dbManager.execNonQuery(r"""
CREATE TABLE book_tag (
  id int(11) NOT NULL AUTO_INCREMENT,
  book_name varchar(100) DEFAULT NULL COMMENT '书名',
  book_no varchar(45) DEFAULT NULL COMMENT '书编号',
  book_tag varchar(45) DEFAULT NULL COMMENT '书标签',
  book_kind varchar(45) DEFAULT NULL COMMENT '书分类',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='书标签';
""")






