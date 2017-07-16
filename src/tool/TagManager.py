# -*- coding:utf-8 -*-
import string

from bs4 import BeautifulSoup  # 解析html结构的模块
from src.tool.ExcelManager import writeExcel
import urllib.request

def makeBookListInfo(url_content):
    """
	抓取图书列表信息
	"""
    books = []  # 初始化为一个空列表
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    list = soup.select("div.article div#subject_list ul.subject-list")
    listsoup = BeautifulSoup(str(list), 'html.parser')  # 开始解析
    booktable1 = listsoup.findAll("li")  # 找到所有图书信息所在标记
    for book in booktable1: # 循环遍历图书列表
        simplebook = book   # book为booktable1下面的一个dl标签
        subsoup = BeautifulSoup(str(simplebook), 'html.parser')  # 单本书进行解析
        book_large_img = subsoup.img['src']  # 直接使用标签，然后获得属性的值 # 图书封面：
        # print(str(book_large_img)) # 打印图片链接
        img_temp = book_large_img.split('/')  # 将该链接以‘/’进行切分
        img_temp[len(img_temp) - 2] = 'spic'
        message = subsoup.find('div', attrs={"class": "info"}) # 图书信息
        book_link = message.a['href']  # 图书链接
        book_name = message.a['title']  # 图书名称
        book_info = subsoup.find('div', attrs={"class": "pub"}).string.replace('\n ', '').replace(' \n', '').replace(' ', '')    # 图书出版信息
        try: book_star = subsoup.find('span', attrs={"class": "rating_nums"}).string  # 图书星级
        except:
            book_star = '-'
            pass
        book_info = book_info.strip(' \n')  # strip用来去掉换行符和空格
        books.append([book_name, book_link, book_large_img, book_info, book_star])  # 构建自己的信息结构
    return books  # 返回图书列表

"""
def makeBookInfo(url_content):

#抓取单本书

    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    #  查找对应的meta标签，返回的是整个标签的内容
    book_no = soup.find('meta', attrs={'http-equiv': 'mobile-agent'})
    # 这里是有问题的，meta标签没闭合
    #  去除那本书的编号
    book_no = book_no['content'].split('subject/')[1].replace('/', '')
    # 书名，不知道为什么是有空格和换行符的，看html源文件是没有的，但是取出来就有了。
    book_name = soup.find('h1').text.replace('\n', '')
    book_info = soup.find('div', attrs={"id": "info"})  # 出版信息
    peoples = soup.find('a', attrs={"class", "rating_people"})  # 评分的人数
    books = soup.findAll('span', attrs={"class", "rating_per"})  # 人数的比例

    book_intro = soup.findAll('div', attrs={"class": "intro"})  # 书籍及作者介绍
    book_alot = soup.findAll('div', attrs={"class": "subject_show block5"})  # 丛书信息 可能不存在

    # 使用css的选择器来获得标签。
    # 认真看了一下这部分获取的东西，html代码里面，这部分只是一些文字，用css装饰了一下。好像通过标签确实找不到
    # 而且有些分了好多层，所以才用css的选择器拉获取吧。

    mu_lu = soup.select('div[id*="dir"]')  # 表示获得所有id属性中包含dir的div
    #bookhotcomment1 = soup.select('div#wt_1 div.ctsh div.tlst div.ilst a')  # 评论头像
    #bookhotcomment2 = soup.select('div#wt_1 div.ctsh div.tlst div.nlst h3 > a')  # 评论详情
    #bookhotcomment3 = soup.select('div#wt_1 div.ctsh div.tlst div.clst span.starb')  # 用户简介
    comments = []
    # 获取评论信息
    bookhotcomment = soup.findAll('li', attrs=['class', 'comment-item'])
    for comment in bookhotcomment:
        # print(comment)
        simple_comment = BeautifulSoup(str(comment), 'html.parser')
        book_hot_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
        book_hot_comment2 = simple_comment.find('p', attrs=['class', 'comment-content'])  # 评论详情
        book_hot_comment3 = simple_comment.find('span', attrs=['class', 'user-stars allstar50 rating'])  # 评价等级
        try:
            book_hot_comment33 = book_hot_comment3.title()
        except:
            book_hot_comment33 = 'none'
        comments.append(
            '<br />'.join(['评论ID：'+book_hot_comment1.find('a').get_text(), '\n评论内容：'+book_hot_comment2.get_text(), '\n星级：'+book_hot_comment33.replace('\xa0', '\n')]))  # \xa0是不间断空白符
    mu_lu = soup.select('div[id*="dir"]')  # 表示获得所有id属性中包含dir的div

    try:
        # 获取出来的东西很多换行符和空格，不知道什么原理。这个串联有点像C++的输入输出哇。
        book_info = book_info.text.replace(' \n', '').replace('\n ', '').replace(' ', '')
    except:
        book_info = ''
    # 内容里面分了好多的段落，这些写得有点硬了，稍微变更一下就不能用了。

    try:
        bookintro1 = book_intro[0].findAll('p')
    except:
        bookintro1 = []
    try:
        bookintro2 = book_intro[1].findAll('p')
    except:
        bookintro2 = []
    book_intro = ''
    author_intro = ''
    # 相当于去除<p>和</p>
    for i in bookintro1:
        book_intro = book_intro + i.text + '\n'
    for i in bookintro2:
        author_intro = author_intro + i.text + '\n'
    try:
        bookalot = book_alot[0].text.replace('\n', '').replace(' ', '')
    except:
        bookalot = '.>_<.无丛书信息'
    peoples = peoples.text
    try:
        mu_lu = mu_lu[0].text.replace(' ', '')
        mu_lu = mu_lu[1].text.replace(' ', '')
    except:
        mu_lu = '.>_<.未检索到目录信息'


    stars = []
    for i in books:
        stars.append(i.text)
    # 写在函数最后，这个函数就是将书本页面的内容提取出来，按自己的格式构造一下。
    # 所以，核心内容是那几个提取的函数find，findAll，select。理解这三个函数。其他部分都不重要了。
    # 构造成一个列表

    return [book_no, book_name, book_info, book_intro, author_intro, int(peoples.replace('人评价', '')), '  ,'.join(stars), bookalot, mu_lu,
            '<hr />'.join(comments)]
"""   """
    抓取单本书
   """
def makeBookInfo(url_content):
   soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
   # 查找对应的meta标签，返回的是整个标签的内容
   book_no = soup.find('meta', attrs={'http-equiv': 'mobile-agent'})
   book_no = book_no['content'].split('subject/')[1].replace('/', '')   # 书编号
   # print('编号：' + book_no)
   book_name = soup.find('h1').text.replace('\n', '')
   # print('书名：' + book_name)
   book_info = soup.find('div', attrs={"id": "info"})  # 出版信息
   try:  # 作者
       book_au = soup.select("div.article div#info a:nth-of-type(1)")
       # print(book_au)
       soup_au = BeautifulSoup(str(book_au), 'html.parser')
       book_author = soup_au.get_text().replace(' \n', '').replace('\n ', '').replace(' ','')  # .replace('[', '').replace(']', '')
   except:
       book_author = '未检索到作者信息'
   #print("作者：" + book_author)
   book_tra = soup.select("div.article div#info a:nth-of-type(2)")  # 译者
   book_trans = u'-'
   try:
       # print(book_tra)
       soup_tra = BeautifulSoup(str(book_tra), 'html.parser')
       if not soup_tra.text.replace(' \n', '').replace('\n ', '').replace(' ', ''):
          book_trans = str(soup_tra.text.replace(' \n', '').replace('\n ', '').replace(' ', ''))
   except:
       book_trans = '-'
   #print('译者：' + book_trans)
   # 出版年，页数，定价，出版社
   book_message = book_info.findAll('span', attrs={'class': 'pl'})
   try:
       book_year = u'-'
       book_price = u'-'
       book_page = 0
       book_public = u'-'
       for item in book_message:
           if item.string == u"出版年:":
               book_year = item.nextSibling.strip().split("/")[0].strip()  # nextSibling查找下一个兄弟节点 ，strip()去掉空格，split用来分割
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
   #print('出版社：' + book_public)
   #print('出版年：' + book_year)
   #print('页数:' + book_page)
   #print('定价:' + book_price)

   # 评论人数：
   try:
       infoVoteNum = soup.find('span', {'property': 'v:votes'})
       votenum = infoVoteNum.get_text().strip()
   except:
       # print("评论人数不足")
       votenum = '0'

   # print("评论人数：" + votenum)

   # 星级评价：
   infostar = soup.find('strong', {'property': 'v:average'})
   # print(infostar)
   try:
       stars = "0"
       stars = infostar.get_text().strip()
       if stars == '':
           stars = "0"
   except:
       print("抓取评价出错")
       stars = "0"  # 使用u或者U处理unicode文本
   # print("星级评价：" + stars)

   # 评价人数的比例
   try:
       ratio = soup.findAll('span', attrs={"class", "rating_per"})
       voteratio = []
       for i in ratio:
           voteratio.append(i.text)
   except:
       voteratio = "0"
   # print("人数比例：")
   # print(voteratio)
   try:
       book_intro = ''
       author_intro = ''
       total = soup.findAll('h2')
       for previous in total:
           #print(previous)
           #print(previous.text.replace('·', '').replace('\n', '').replace(' \n', '').replace(' ', ''))
           word = previous.text.replace('·', '').replace('\n', '').replace(' \n', '').replace(' ', '')
           if word == '内容简介      ':
               book = previous.find_next_sibling()  # 找下一个节点
               #print(book)
               soup_book = BeautifulSoup(str(book), 'html.parser')
               book_intro1 = soup_book.findAll('div', attrs={"class": "intro"})
               #print(book_intro1)
               #print(len(book_intro1))
               if len(book_intro1) == 1:
                   intro1 = book_intro1[0].findAll('p')
               if len(book_intro1) == 2:
                   intro1 = book_intro1[1].findAll('p')
           if word == '作者简介      ':
                author = previous.find_next_sibling()  # 找下一个节点
                #print(author)
                soup_author = BeautifulSoup(str(author), 'html.parser')
                author_intro1 = soup_author.findAll('div', attrs={"class": "intro"})
                if len(author_intro1) == 1:
                    intro2 = author_intro1[0].findAll('p')
                if len(author_intro1) == 2:
                    intro2 = author_intro1[1].findAll('p')
       for i in intro1:
            book_intro = book_intro + i.text + '\n'
       for i in intro2:
            author_intro = author_intro + i.text + '\n'
       #print(book_intro)
       #print(author_intro)
   except:
        book_intro = '-'
        author_intro = '-'

   # 丛书信息 可能不存在
   book_oth = soup.findAll('div', attrs={"class": "subject_show block5"})
   try:
       book_others = book_oth[0].text.replace('\n', '').replace(' ', '')
   except:
       book_others = '-'
   #print('丛书：' + book_others)
   # 目录
   mu_lu = soup.select('div[id*="dir"]')  # 表示获得所有id属性中包含dir的div
   # print(mu_lu)
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
   else:
       mu_lu = '-'

   #print('目录：' + mu_lu)

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
   #print('推荐书籍:' + recommendations)

   # 获取评论信息
   comments = []
   bookcomment = soup.findAll('li', attrs=['class', 'comment-item'])
   for comment in bookcomment:
       simple_comment = BeautifulSoup(str(comment), 'html.parser')
       book_comment1 = simple_comment.find('span', attrs=['class', 'comment-info'])  # 评论ID
       comment_id = book_comment1.find('a').string.replace("'", "\\'").replace('"', '\\"')
       book_comment2 = simple_comment.find('p', attrs=['class', 'comment-content']).get_text().replace(' \n', '').replace('\n ', '').replace(' ', '').replace("'", "\\'").replace('"', '\\"')  # 评论详情
       book_comment11 = BeautifulSoup(str(book_comment1), 'html.parser')
       book_comment3 = book_comment11.select("span:nth-of-type(2)")  # 评价等级
       # print(book_comment3)
       try:
           book_comment33 = str(book_comment3).split('title="')[1].split('">')[0]
           if book_comment33 == '力荐':
               book_comment33 = '★★★★★'
           elif book_comment33 == '推荐':
               book_comment33 = '★★★★'
           elif book_comment33 == '还行':
               book_comment33 = '★★★'
           elif book_comment33 == '较差':
               book_comment33 = '★★'
           elif book_comment33 == '很差':
               book_comment33 = '★'
           else:
               book_comment33 = '该用户未评分'
       except:
           book_comment33 = '该用户未评分'
       comments.append(
          '<br />'.join(['评论ID：' + comment_id, '评论内容：' + book_comment2,
            '评价等级：' + book_comment33.replace('\xa0', '\n')])
       )# \xa0是不间断空白符
 #-----------如果是写入excel，由于是把每个list元素拆分开写，所以应该是string类型-------
   return [book_no, book_name, book_author, book_public, book_trans, book_year, book_page, book_price, votenum,
           stars, ','.join(voteratio), book_intro, author_intro, book_others, mu_lu, recommendations, '<hr />'.join(comments), book_info.text.replace(' \n', '').replace('\n ', '').replace(' ', '').replace("'", '"')]


def makeBookTag(url_content, path='D:\workplace\pythonwork\douban_book_catch_zzq\darabase/bookTag.xlsx'):
    """
	抓取标签提取写入Excel
	"""
    soup = BeautifulSoup(url_content, 'html.parser')  # 开始解析
    booktag1 = soup.select('div#content div.article div div')
    print(str(booktag1))
    taglist = [['标签类别', '标签名', '标签链接', '点击量']]  # Excel里面的标题
    for booktag2 in booktag1:
       # print(str(booktag2))
        soup1 = BeautifulSoup(str(booktag2), 'html.parser')  # 开始解析
        booktag2 = soup1.find('a', attrs={'class': 'tag-title-wrapper'})
        tagType = booktag2['name']  # 标签类别
        booktag3 = soup1.findAll("a")
        booktag4 = soup1.findAll("b")   # 该标签下的图书数量
        for i in range(0, len(booktag4)): # len(booktag4)就可以表示一行有多少种不同类型的分类
            tag = booktag3[i + 1].string  # 标签名
            taglink = 'https://book.douban.com'+booktag3[i + 1]['href']  # 链接
            tagnum = booktag4[i].string
            taglist.append([tagType, tag, taglink, tagnum])  # 把内容加进去，按照标题的顺序
    writeExcel(path, taglist)  # 将内容写入excel中
    print("写入EXCEL成功")


def testBookTag():
    file = open('D:\workplace\pythonwork\douban_book_catch_zzq\darabase/booktag.html', 'rb')
    content = file.read()
    makeBookTag(content, r'D:\workplace\pythonwork\douban_book_catch_zzq\darabase/booktag.xlsx')


def testManyBook():
    file = open('D:/workplace/pythonwork/douban_book_catch_zzq/web抓取/0.html', 'rb')
    content = file.read()
    books = makeBookListInfo(content)
    for i in books:
        print(i)


def testBookInfo():
    print('D:/workplace/pythonwork/HelloWorld/book/流行/1000134三毛流浪记全集.html')
    file = open('D:/workplace/pythonwork/HelloWorld/book/流行/1000134三毛流浪记全集.html', 'rb')  # 读取文件
    content = file.read()
    book = makeBookInfo(content)
    for i in book:
        print('*' * 50)  # 分割一下，方便查看
        print(i)  # 打印一下内容


if __name__ == '__main__':
     # testManyBook()
     testBookInfo()   # 提取书详细页面的信息
    #  testBookTag()  # 测试图书标签抓取是否成功
