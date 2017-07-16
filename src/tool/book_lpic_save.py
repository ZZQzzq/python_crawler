# _*_ coding:utf-8 _*_
__author__ = 'zzq'
__data__ = '2017/4/19 16:07'

"""
读出在step5中 保存在excel中的图片，保存在pic文件夹下的book_lpic目录下
"""

import os
from PIL import Image
import time
import urllib.request
from src.tool.ExcelManager import readExcel

#['文化', '文学',  '经管', '流行', '科技','生活' ]
list = ['文学']
save_path = 'D:/workplace/pythonwork/douban_book_catch_zzq/lpic/book_pic'
try:
    for kind in list:
        print(kind)
        rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\\book_message_order_by_tag\\'+kind   # 各个分类目录
        prefix = '.xlsx'
        savepath = save_path + '/' + kind
        if os.path.exists(savepath):
            print("文件夹已经存在")
            pass
        else:
            os.makedirs(savepath)  # 否则新建文件夹
        for parent, dirnames, filenames in os.walk(rootdir):
                """
                使用 os.walk 方法返回的是一个三元tupple(dirpath, dirnames, filenames),
                其中第一个为起始路径，
                第二个为起始路径下的文件夹,
                第三个是起始路径下的文件.
                dirpath是一个string，代表目录的路径,
                dirnames是一个list，包含了dirpath下所有子目录的名字,
                filenames是一个list，包含了非目录文件的名字.
                """
                for filename in filenames:
                    #print(filenames)
                    if filename.endswith(prefix):  # 寻找所有以xlsx结尾的文件
                        filename1 = filename.split('.')[0]
                        print(filename1)
                        savepath1 = savepath + '/' + filename1
                        if os.path.exists(savepath1):
                            print("文件夹已经存在")
                            continue
                        else:
                            os.makedirs(savepath1)  # 否则新建文件夹
                        path = str(parent) + '\\' + filename  # 即将打开的xlsx文件地址
                        #print(path)
                        taglist = readExcel(path)
                        del taglist[0]
                        #print(taglist)
                        i = 0
                        for col in taglist:
                            print(col)
                            pic = col[2]
                            pic_url = pic.replace(pic.split('/')[-2],'lpic')
                            # print(pic_url)

                            book_url = col[1]
                            book_no = book_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
                            # print(pic_url)
                            try:
                                try:
                                    im = Image.open(savepath1 + '/' + book_no + '.jpg')
                                except:
                                    im = ''
                                if im == '':
                                    work_path = os.path.join(savepath1 + '/', book_no + '.jpg')
                                    urllib.request.urlretrieve(pic_url, '%s' % work_path)
                                    print("下载第" + str(i) + "张图片成功")
                                else:
                                    print("图片已经存在")
                                    continue
                            except:
                                f = open('D:/workplace/pythonwork/douban_book_catch_zzq/lpic/book_pic/wrong.txt', 'a+')
                                f.write(savepath1 + '《==》' + pic_url + '\n')
                                print(savepath1 + '《==》' + pic_url + '\n')
                            i += 1
                        time.sleep(1)

except:
        print("somthing wrong")
        pass
