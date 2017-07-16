


import re  # 正则表达式相关的模块


# 转换成代理ip
# proxy.txt的内容是从网上复制黏贴下来的。这个代理地址可能会有时限性。
# 其实可以改成网上爬下来最新的。

def makeProxyAddress():
    # 打开代理文件
    file = open('D:\workplace\pythonwork\douban_book_catch_zzq\src\\tool/proxy.txt', 'rb')
    # 读取出来，以换行符分割
    data = file.read().decode('utf-8', 'ignore').split('\n')  # data是一个元素为list的list
    print(data)
    # random.shuffle(data) # ip数组打乱
    # 把字符串编译成正则表达对象，方便后面使用，提高效率。匹配带有@的字符串
    reExp = re.compile(r'(.*)@(.*)')
    for i in range(0, len(data)):  # len(data)表示列表元素个数
        mo = reExp.match(data[i])
        #  print(mo.group(1)) 通过match函数匹配到每个元素 e.g.匹配到58.247.98.178:80@HTTP#上海市 联通
        data[i] = mo.group(1)  # 获取第一组  （使用group函数进行截取，@之前为第一组，@之后为第二组）
        """ group函数的最终运行结果与正则表达式有关。若换成:
         reExp = re.compile(r'(.*)#(.*)')
         mo = reExp.match(data[i])
         则打印出来mo.group(1)为58.247.98.178:80@HTTP
        """
    file.close()
    file = open('proxy1.txt', 'w')  # 打开文件（若没有，则新建）
    file2 = open('D:\workplace\pythonwork\douban_book_catch_zzq\src\movie\proxy1.txt', 'w')
    file.write('\n'.join(data))  # 没插入一项，就换行
    file2.write('\n'.join(data))
    file.close()  # 关闭文件
    file2.close()
    return data


if __name__ == '__main__':
    a = makeProxyAddress()
    print(a)
