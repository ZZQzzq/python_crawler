# 通过链接去下载html文件
# 内容比较简单
import os
import urllib.request  # 请求相关
from bs4 import BeautifulSoup  # 网页结构处理
import http.cookiejar  # cookie相关


def getHtml(url):
    """
    伪装头部并得到网页内容
    """
    # cookie类
    cj = http.cookiejar.CookieJar()
    # 通过handler来构建opener
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    # 一些html请求报文表头的字段
    # 操作系统，浏览器相关信息
    user_agent = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'  # 接受的文件格式
    # cookie的内容
    cookie = """
    Cbid ="ll="118390"; bid=1GxPFdYHws0; gr_user_id=a1cfa971-43f2-4767-90dd-affec2ac2d8d; viewed="1007305_26910001"; ps=y; _vwo_uuid_v2=D152593A1ABF239FB9BD5CC25DFF5636|3b524bafd1b9ed8720577b472e430c8e; _pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1490165201%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3DqtuTa9kfJvMQSQs7F7c7D8A3ARj6OPaoHtK7U_Rb4UK%26wd%3D%26eqid%3D9ce3b4e40001d10c0000000658d21dc9%22%5D; _pk_id.100001.8cb4=348f383c879514b3.1486109343.12.1490165201.1490160787.; _pk_ses.100001.8cb4=*; __utmt=1; _ga=GA1.2.1908265381.1486109347; ue="269179723@qq.com"; dbcl2="120679145:ljFHUXdghrY"; ck=DOqi; push_noty_num=0; push_doumail_num=0; __utma=30149280.1908265381.1486109347.1490160789.1490165206.19; __utmb=30149280.1.10.1490165206; __utmc=30149280; __utmz=30149280.1490165206.19.11.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; __utmv=30149280.12067; ap=1
    """
    # 增加内容到表头
    opener.add_handler = {
        ('User-Agent', user_agent),
        ('Accept', Accept),
        ('Cookie', cookie)
    }

    urllib.request.install_opener(opener)  # 转为全局的opener
    # urlopen()是打开这个url，返回一个response对象。read()读取response对象的内容
    html_bytes = urllib.request.urlopen(url).read()
    # 解码，ignore表示遇到不兼容的就跳过
    html_string = html_bytes.decode('utf-8', 'ignore')
    return html_string  # 返回解码后的字符串


# 代理的地址，要在这里获取最新的，不行就一个个试试吧。http://www.youdaili.net/
# http://www.youdaili.net/Daili/http/34265.html 隔一段时间更新一次的
def getBinaryHtml(url, daili='123.59.101.41:80'):
    """
    伪装头部并得到网页原始内容

    """
    cj = http.cookiejar.CookieJar()
    # 设置IP代理
    # ProxyHandler通过这个方法可以设置代理访问网页
    proxy_support = urllib.request.ProxyHandler({'http': 'http://' + daili})
    # 开启代理支持，可以传多个handler进去的
    opener = urllib.request.build_opener(
        proxy_support,
        urllib.request.HTTPCookieProcessor(cj),
        urllib.request.HTTPHandler)
    # 不设置代理
    # opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
    user_agent = 'User-Agent:Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'
    Accept = 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'  # 希望接受的文件格式
    opener.addheaders = [('User-Agent', user_agent),
                         ('Accept', Accept),
                         ('Cookie', '4564564564564564565646540')]

    urllib.request.install_opener(opener)

    html_bytes = urllib.request.urlopen(url).read()
    return html_bytes


def test():
    getBinaryHtml('http://www.douban.com/tag/%E5%B0%8F%E8%AF%B4/book')


def makeSoup(html_content, parse='html.parser'):
    """
    得到网页解析后的对象，方便分拆数据
    """
    return BeautifulSoup(html_content, parse)


# 测试
if __name__ == '__main__':
    # 下载标签页
    tag = getBinaryHtml('http://book.douban.com/tag/')
    addr = 'D:\workplace\pythonwork\HelloWorld\src/booktag.html'
    if os.path.exists(addr):
        pass
    else:  # 否则新建
        print('新建：' + addr)
        os.makedirs(addr)
    file = open('D:\workplace\pythonwork\HelloWorld\src/booktag.html', 'wb')  # 以写二进制的方式，写入获得的内容
    file.write(tag)
    file.close()
    # 下载某个页面
    content1 = getHtml("https://book.douban.com/tag/%E5%B0%8F%E8%AF%B4")
    addr1 = 'D:\workplace\pythonwork\HelloWorld\src/books.html'
    if os.path.exists(addr1):
        pass
    else:  # 否则新建
        print('新建：' + addr1)
        os.makedirs(addr1)
    file1 = open(addr1, 'wb')
    content2 = getHtml("https://book.douban.com/subject/26698660/")
    addr2 = 'D:\workplace\pythonwork\HelloWorld\src/book.html'
    if os.path.exists(addr2):
        pass
    else:  # 否则新建
        print('新建：' + addr2)
        os.makedirs(addr2)
    file2 = open('D:\workplace\pythonwork\HelloWorld\src/book.html', 'wb')
    file1.write(content1.encode('utf-8'))
    file2.write(content2.encode('utf-8'))
    file1.close()
    file2.close()
    # 打开看了一下，发现广告内容也都在，看一下源码。第一次获取的是html。也就是我们保存下来的文件。
    # 浏览器打开后，就会解析里面的内容，看到图片什么的，就根据url再去下载的。
    # 所以如果断网了，保存下来的html文件就无法显示里面的url的内容了。
