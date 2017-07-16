"""
读出在movie_step5中 保存在excel中的图片，保存在pic文件夹下的movie_lpic目录下
策略：1.读出rootdir目录下的所有.xlsx文件
     2.在savepath下创建文件夹。保存图片到该文件夹中
"""


import os
from PIL import Image
import urllib.request
from src.tool.ExcelManager import readExcel


save_path = 'D:/workplace/pythonwork/douban_book_catch_zzq/pic/movie_pic'
try:
    rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\src\movie\movie_message_order_by_year'   # 各个分类目录
    prefix = '.xlsx'
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
                    savepath1 = save_path + '/' + filename1
                    if os.path.exists(savepath1):
                        print("文件夹已经存在")
                        continue
                    else:
                        os.makedirs(savepath1)  # 否则新建文件夹
                    path = str(parent) + '\\' + filename  # 即将打开的xlsx文件地址
                    print(path)
                    taglist = readExcel(path)
                    del taglist[0]
                    print(taglist)
                    i = 0
                    for col in taglist:
                        print(col)
                        pic_url = col[2]
                        movie_url = col[1]
                        movie_no = movie_url.split('/')[-2].replace("'", "\\'").replace('"', '\\"')  # 编号
                        print(pic_url)
                        try:
                            try:
                                im = Image.open(savepath1 + '/' + movie_no + '.jpg')
                            except:
                                im = ''
                            if im == '':
                                work_path = os.path.join(savepath1 + '/', movie_no + '.jpg')
                                urllib.request.urlretrieve(pic_url, '%s' % work_path)
                                print("下载第" + str(i) + "张图片成功")
                            else:
                                print("图片已经存在")
                                continue
                        except:
                            f = open('D:/workplace/pythonwork/douban_book_catch_zzq/pic/movie_pic/wrong.txt', 'a+')
                            f.write(savepath1 + '《==》' + pic_url + '\n')
                            print(savepath1 + '《==》' + pic_url + '\n')
                        i += 1

except:
    print("somthing wrong")
    pass