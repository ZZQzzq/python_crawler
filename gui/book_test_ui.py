# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'book_test_ui.ui'
#
# Created by: PyQt5 UI code generator 5.8.1
#
# WARNING! All changes made in this file will be lost!

import os
import sys
import time
import urllib.request
from bs4 import BeautifulSoup
import xlrd, xlwt
from xlutils3.copy import copy
import time

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from src.tool.DbManager import DbManager
from src.tool.ExcelManager import readExcel, writeExcel
from src.tool.HtmlManager import getHtml
from src.tool.TagManager import makeBookInfo


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1258, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # —————————————————————————— 搜索栏布局 ————————————————————————————
        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 311, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.select_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.select_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.select_gridLayout.setObjectName("select_gridLayout")
        # 书名编辑text
        self.searchEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.searchEdit.setObjectName("searchEdit")
        self.select_gridLayout.addWidget(self.searchEdit, 0, 2, 1, 1)
        # 搜索按钮
        self.find_but = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.find_but.setObjectName("find_but")
        self.select_gridLayout.addWidget(self.find_but, 0, 3, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())  # 布局调整
        # 书名label
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setObjectName("label_3")
        self.select_gridLayout.addWidget(self.label_3, 0, 1, 1, 1)
        # 搜索结果显示table
        self.find_result_tab = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.find_result_tab.setObjectName("find_result_tab")
        self.find_result_tab.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        #self.find_result_tab = QTableWidget(0, 3)
        #self.find_result_tab.setHorizontalHeaderLabels([u'书名', u'作者', u'评分'])
        self.find_result_tab.resizeColumnsToContents()  # 各属性列的大小自适性
        self.find_result_tab.resizeRowsToContents()

        item = QtWidgets.QTableWidgetItem()
        self.find_result_tab.setColumnCount(3)  # 指定列数（3列）
        self.find_result_tab.setRowCount(1000)
        self.find_result_tab.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_tab.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_tab.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_tab.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
        self.select_gridLayout.addWidget(self.find_result_tab, 1, 1, 1, 3)

       # —————————————————————————— 详细信息显示栏布局————————————————————————————
        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(330, 10, 571, 471))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.show_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.show_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.show_gridLayout.setObjectName("show_gridLayout")
        # 书名label
        self.bname = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bname.setObjectName("bname")
        self.show_gridLayout.addWidget(self.bname, 0, 0, 1, 1)
        # 书名显示
        self.lineEdit_bname = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bname.setObjectName("lineEdit_bname")
        self.show_gridLayout.addWidget(self.lineEdit_bname, 0, 1, 1, 1)

        # 编号label
        self.bno = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bno.setObjectName("bno")
        self.show_gridLayout.addWidget(self.bno, 1, 0, 1, 1)
        # 编号显示
        self.lineEdit_bno = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bno.setObjectName("lineEdit_bno")
        self.show_gridLayout.addWidget(self.lineEdit_bno, 1, 1, 1, 1)

        # 作者label
        self.bauthor = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bauthor.setObjectName("bauthor")
        self.show_gridLayout.addWidget(self.bauthor, 2, 0, 1, 1)
        # 作者显示
        self.lineEdit_bauthor = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bauthor.setObjectName("lineEdit_bauthor")
        self.show_gridLayout.addWidget(self.lineEdit_bauthor, 2, 1, 1, 1)

        # 评分label
        self.bstar = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bstar.setObjectName("bstar")
        self.show_gridLayout.addWidget(self.bstar, 3, 0, 1, 1)
        # 评分显示
        self.lineEdit_bstar = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bstar.setObjectName("lineEdit_bstar")
        self.show_gridLayout.addWidget(self.lineEdit_bstar, 3, 1, 1, 1)

        # 出版社label
        self.bpub = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bpub.setObjectName("bpub")
        self.show_gridLayout.addWidget(self.bpub, 4, 0, 1, 1)
        # 出版社显示
        self.lineEdit_bpub = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bpub.setObjectName("lineEdit_bpub")
        self.show_gridLayout.addWidget(self.lineEdit_bpub, 4, 1, 1, 1)

        # 出版时间label
        self.byear = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.byear.setObjectName("byear")
        self.show_gridLayout.addWidget(self.byear, 5, 0, 1, 1)
        # 出版时间显示
        self.lineEdit_byear = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_byear.setObjectName("lineEdit_byear")
        self.show_gridLayout.addWidget(self.lineEdit_byear, 5, 1, 1, 1)

        # 价格label
        self.bprice = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bprice.setObjectName("bprice")
        self.show_gridLayout.addWidget(self.bprice, 6, 0, 1, 1)
        # 价格显示
        self.lineEdit_bprice = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bprice.setObjectName("lineEdit_bprice")
        self.show_gridLayout.addWidget(self.lineEdit_bprice, 6, 1, 1, 1)

        # 看过label
        self.bnum = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bnum.setObjectName("bnum")
        self.show_gridLayout.addWidget(self.bnum, 7, 0, 1, 1)
        # 看过的人数显示
        self.lineEdit_bnum = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_bnum.setObjectName("lineEdit_bnum")
        self.show_gridLayout.addWidget(self.lineEdit_bnum, 7, 1, 1, 1)

        # url label
        self.burl = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.burl.setObjectName("burl")
        self.show_gridLayout.addWidget(self.burl, 8, 0, 1, 1)
        # url显示
        self.lineEdit_burl = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_burl.setObjectName("lineEdit_burl")
        self.show_gridLayout.addWidget(self.lineEdit_burl, 8, 1, 1, 1)

        # 书籍介绍label
        self.bintro = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bintro.setObjectName("bintro")
        self.show_gridLayout.addWidget(self.bintro, 10, 0, 1, 1)
        # 书籍介绍显示
        self.book_intro = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        self.book_intro.setObjectName("book_intro")
        self.show_gridLayout.addWidget(self.book_intro, 10, 1, 1, 1)

        # 作者介绍label
        self.bauintro = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bauintro.setObjectName("bauintro")
        self.show_gridLayout.addWidget(self.bauintro, 11, 0, 1, 1)
        # 作者介绍显示
        self.bookau_intro = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        self.bookau_intro.setObjectName("bookau_intro")
        self.show_gridLayout.addWidget(self.bookau_intro, 11, 1, 1, 1)

        # 评论label
        self.bcomment = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.bcomment.setObjectName("bcomment")
        self.show_gridLayout.addWidget(self.bcomment, 0, 2, 1, 1)
        # 评论显示
        self.book_comment = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.book_comment.sizePolicy().hasHeightForWidth())
        self.book_comment.setSizePolicy(sizePolicy)
        self.book_comment.setObjectName("book_comment")
        self.show_gridLayout.addWidget(self.book_comment, 1, 2, 11, 1)

        # 添加书籍按钮
        self.addb_pushB = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.addb_pushB.setObjectName("addb_pushB")
        self.show_gridLayout.addWidget(self.addb_pushB, 12, 0, 1, 2)
        # 删除书籍按钮
        self.delb_pushB = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.delb_pushB.setObjectName("delb_pushB")
        self.show_gridLayout.addWidget(self.delb_pushB, 12, 2, 1, 1)

       # —————————————————————————— 我的书架显示栏布局————————————————————————————

        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(910, 10, 331, 471))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.myshelf_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.myshelf_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.myshelf_gridLayout.setObjectName("myshelf_gridLayout")
        # 书架label
        self.label_shujia = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_shujia.sizePolicy().hasHeightForWidth())
        self.label_shujia.setSizePolicy(sizePolicy)
        self.label_shujia.setObjectName("label_shujia")
        self.myshelf_gridLayout.addWidget(self.label_shujia, 0, 0, 1, 1)
        # 书架table
        self.bookshelf = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.bookshelf.sizePolicy().hasHeightForWidth())
        self.bookshelf.setSizePolicy(sizePolicy)
        self.bookshelf.setObjectName("bookshelf")
        self.bookshelf.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑

        self.bookshelf.resizeColumnsToContents()  # 各属性列的大小自适性
        self.bookshelf.resizeRowsToContents()
        self.bookshelf.setObjectName("bookshelf")
        self.bookshelf.setColumnCount(3)  # 指定列数（3列）
        self.bookshelf.setRowCount(1000)  # 指定行数（3行）
        item = QtWidgets.QTableWidgetItem()
        self.bookshelf.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.bookshelf.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.bookshelf.setHorizontalHeaderItem(2, item)
        self.myshelf_gridLayout.addWidget(self.bookshelf, 1, 0, 1, 1)

       # —————————————————————————— 推荐书籍显示栏布局————————————————————————————

        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 490, 1231, 171))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.recomm_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.recomm_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.recomm_gridLayout.setObjectName("recomm_gridLayout")
        # 推荐table
        self.recomm_table = QtWidgets.QTableWidget(self.gridLayoutWidget_4)
        self.recomm_table.setObjectName("recomm_table")
        self.recomm_table = QTableWidget(3, 0)
        self.recomm_table.setVerticalHeaderLabels([u'书名', u'评分', u'封面'])
        self.recomm_table.setObjectName("recomm_table")
        self.recomm_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.recomm_table.setSelectionBehavior(QAbstractItemView.SelectColumns)  # 整列选中的方式
        self.recomm_table.resizeRowsToContents()
        self.recomm_gridLayout.addWidget(self.recomm_table, 0, 0, 1, 1)
        # 爬虫按钮
        self.crawl_Button = QtWidgets.QPushButton(self.centralwidget)
        self.crawl_Button.setGeometry(QtCore.QRect(220, 460, 101, 23))
        self.crawl_Button.setObjectName("crawl_Button")

        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 460, 54, 12))
        self.label_1.setObjectName("label_1")

        MainWindow.setCentralWidget(self.centralwidget)

    # —————————————————————————— signal信号和槽slot———————————————————————————
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.label.setText(_translate("MainWindow", "根据"))
        # self.label_sel.setText(_translate("MainWindow", "查询"))
        self.find_but.setText(_translate("MainWindow", "搜索"))
        self.label_3.setText(_translate("MainWindow", "书名："))
        self.bname.setText(_translate("MainWindow", "书名："))
        self.byear.setText(_translate("MainWindow", "出版时间："))
        self.bno.setText(_translate("MainWindow", "编号："))
        self.bprice.setText(_translate("MainWindow", "价格："))
        self.bauthor.setText(_translate("MainWindow", "作者："))
        self.bstar.setText(_translate("MainWindow", "评分："))
        self.bnum.setText(_translate("MainWindow", "看过："))
        self.bpub.setText(_translate("MainWindow", "出版社："))
        self.addb_pushB.setText(_translate("MainWindow", "加入书架"))
        self.delb_pushB.setText(_translate("MainWindow", "从书架删除"))
        self.bintro.setText(_translate("MainWindow", "书籍简介："))
        self.burl.setText(_translate("MainWindow", "url:"))
        self.bauintro.setText(_translate("MainWindow", "作者简介："))
        self.bcomment.setText(_translate("MainWindow", "评价："))
        self.label_shujia.setText(_translate("MainWindow", "我的书架："))
        self.crawl_Button.setText(_translate("MainWindow", "爬虫窗口"))
        self.label_1.setText(_translate("MainWindow", "猜你喜欢："))
        # 查询结果显示

        item = self.find_result_tab.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "书名"))
        #self.find_result_tab.horizontalHeaderItem(0).setText(_translate("MainWindow", "书名"))
        item = self.find_result_tab.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作者"))
        item = self.find_result_tab.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "评分"))

        # 书架书籍显示
        item = self.bookshelf.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "书名"))
        item = self.bookshelf.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "作者"))
        item = self.bookshelf.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "评分"))
        """
        # 推荐书籍显示
        item = self.recomm_table.verticalHeaderItem(0)
        item.setText(_translate("MainWindow", "编号"))
        item = self.recomm_table.verticalHeaderItem(1)
        item.setText(_translate("MainWindow", "书名"))
        item = self.recomm_table.verticalHeaderItem(2)
        item.setText(_translate("MainWindow", "封面"))
        """

class spider(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(spider, self).__init__()
        self.setupUi(self)
        self.spiderGui = SpiderGui()
        self.setWindowIcon(QIcon('D:/workplace/pythonwork/douban_book_catch_zzq/spic/bookIcon.jpg'))
        self.setWindowTitle('ZZQ_Book')
        # 显示主窗口
        self.show()
    #-------------- 从数据库获取数据并显示-----------
    """
    # 搜索书籍
    def slot_search_keyword(self):
        keyword = self.searchEdit.text()
        if keyword is None:
            return
        dbManager = DbManager()
        if keyword.find("%") == -1:
            select = "SELECT book_no,book_name,book_star FROM `book` where `book_name`='" + keyword + "'"  # 从数据库中查找书籍
        else:
            select = "SELECT book_no,book_name,book_star FROM `book` where `book_name` LIKE '" + keyword + "'"  # 从数据库中查找书籍

        try:
            searchsql = dbManager.execQuery(select)
            print(searchsql)
            print(len(searchsql))
            # 显示查询结果
            self.find_result_tab.clearContents()
            #self.find_result_tab.setRowCount(0)
            row = 0
            for i in range(0, len(searchsql)):
                #print(searchsql[i])
                self.find_result_tab.insertRow(row)
                #print(searchsql[i][0], searchsql[i][1], searchsql[i][2])
                self.find_result_tab.setItem(row, 0, QTableWidgetItem(searchsql[i][0]))
                self.find_result_tab.setItem(row, 1, QTableWidgetItem(searchsql[i][1]))
                self.find_result_tab.setItem(row, 2, QTableWidgetItem(searchsql[i][2]))
                row += 1
                i += 1
                # 搜索table的item
        except:
            print("无这本书，请重新输入！")
    # 搜索table中的书
    def slot_click_search_table(self):
        rows = self.find_result_tab.currentRow()
        print(self.find_result_tab.item(rows, 0).text())
        print(self.find_result_tab.item(rows, 1).text())
        print(self.find_result_tab.item(rows, 2).text())
        book_name = self.find_result_tab.item(rows, 0).text()
        dbManager = DbManager()
        select = "SELECT * FROM `book` where `book_name`='" + book_name + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `book_detail` where `book_name`='" + book_name + "'"  # 从数据库中查找书籍
        try:
            book = dbManager.execQuery(select)
            #bookde = dbManager.execQuery(selectde)
            print(book[0])
            #bookde = dbManager.execQuery(selectde)
            # book = self.mongodb.search_book_by_url(url)
            self._display_book_information(book[0])
            #self._display_book_information(bookde)

        except:
            print("搜索书籍出错")
    # 搜索书架上的书
    def slot_click_bookshelf_table(self):
        curRow = self.bookshelf.currentRow()  # 当前列
        book_name = self.find_result_table.item(curRow, 0).text()  # 根据编号查找
        dbManager = DbManager()
        select = "SELECT * FROM `book` where `book_name`='" + book_name + "'"  # 从数据库中查找书籍
        try:
            book = dbManager.execQuery(select)
            # book = self.mongodb.search_book_by_url(url)
            self._display_book_information(book)
        except:
            print("搜索书籍出错")
    # 搜索推荐书籍
    def slot_click_recommend_table(self):
        curCol = self.recomm_table.currentColumn()
        book_name = self.find_result_table.item(curCol, 0).text()
        dbManager = DbManager()
        select = "SELECT * FROM `book` where `book_name`='" + book_name + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `book_detail` where `book_name`='" + book_name + "'"  # 从数据库中查找书籍
        try:
            book = dbManager.execQuery(select)
            bookde = dbManager.execQuery(selectde)
            # book = self.mongodb.search_book_by_url(url)
            self._display_book_information(book)
            self._display_book_information(bookde)
        except:
            print("搜索书籍出错")
    # 显示书籍详细信息
    def _display_book_information(self, book):
        print(book)
        self.lineEdit_bname.setText(book[2].strip())
        self.lineEdit_bno.setText(book[1].strip())
        #self.lineEdit_bauthor.setText(bookde[3].strip())
        self.lineEdit_bstar.setText(book[6].strip())
        #self.lineEdit_bpub.setText(bookde[4].strip())
        #self.lineEdit_byear.setText(bookde[6].strip())
        #self.lineEdit_bprice.setText(bookde[8])
        #self.lineEdit_bnum.setText(bookde[9])
        self.lineEdit_burl.setText(book[3])
        #self.book_intro.setText(bookde[12])
        #self.bookau_intro.setText(bookde[13])
        #self.book_comment.setHtml(bookde[16])
    # 加入书架
    def slot_join_bookshelf(self):
        book = {}
        book[0] = str(self.lineEdit_bno.text())
        book[1] = str(self.lineEdit_bname.text())
        book[2] = str(self.lineEdit_bauthor.text())

        dbManager = DbManager()
        selectsql="select book_tag,book_kind from `book_tag` where `book_no`='" + book[0] + "'"
        ans = dbManager.execQuery(selectsql)
        for i in ans:
            book[3] = i[0]
            book[4] = i[1]
        insertsql = "INSERT INTO `user_data`(`book_no`, `book_name`, `book_author`, `book_tag`, `book_kind`)" \
                  " VALUES ('{0}', '{1}', '{2}','{3}','{4}')"
        try:
            insert = insertsql.format( book[0],
                                       book[1],
                                       book[2],
                                       book[3],
                                       book[4]
                                       )
            dbManager.execNonQuery(insert)
            print("加入书架成功")
        except Exception as e:
            print(e)
        self._display_bookshelf()   # 显示在书架上
       # self._recommend_good_books()  # 重新计算推荐书籍
    # 从书架删除
    def slot_delete_from_bookshelf(self):
        dbManager = DbManager()
        book_no = str(self.lineEdit_bno.text())
        delsql = "delete  from `user_data` WHERE `book_no`='"+book_no+"'"
        try:
            dbManager.execNonQuery(delsql)
        except Exception as e:
            print(e)
        self._display_bookshelf()
        #self._recommend_good_books()
    # 刷新书架上的书
    def _display_bookshelf(self):
        try:
            dbManager = DbManager()
            selectsql = "select * from 'user_data'"
            doc = dbManager.execQuery(selectsql)
            # 显示书架上的书
            self.bookshelf.clearContents()
            self.bookshelf.setRowCount(0)
            row = 0
            for i in doc:
                self.bookshelf.insertRow(row)
                self.bookshelf.setItem(row, 0, QTableWidgetItem(i[0]))
                self.bookshelf.setItem(row, 1, QTableWidgetItem(i[1]))
                self.bookshelf.setItem(row, 2, QTableWidgetItem(i[2]))
                row += 1
                i += 1
        except:
            print("读取用户表错误")
    # 显示推荐书籍
    def _display_recommend_books(self):
        self.recomm_table.clearContents()  # 每次进行推荐之前先把上次的结果清空
        self.recomm_table.setColumnCount(0)
        column = 0
        for url in self.recommendUrls:
            book = self.mongodb.search_book_by_url(url)
            if book is None:
                continue
            self.recommendTable.insertColumn(column)
            self.recommendTable.setColumnWidth(column, 107)
            self.recommendTable.setItem(0, column, QTableWidgetItem(book['bookName']))
            self.recommendTable.setItem(1, column, QTableWidgetItem(book['score']))
            column += 1
     """

    # --------------从网页获取数据并显示--------------
    # 搜索书籍
    def slot_search_keyword(self):
        keyword = self.searchEdit.text()
        print(keyword)
        if keyword is None:
            return
        dbManager = DbManager()
        if keyword.find("%") == -1:
            select = "SELECT book_no,book_name FROM `book` where `book_name`='" + keyword + "'"  # 从数据库中查找书籍
        else:
            select = "SELECT book_no,book_name FROM `book` where `book_name` LIKE '" + keyword + "'"  # 从数据库中查找书籍

        try:
            searchsql = dbManager.execQuery(select)
            print(searchsql)
            # 显示查询结果
            self.find_result_tab.clearContents()
            row = 0
            excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\xlsx_dic\has_searched' + keyword + '.xlsx'  # 创建保存记录的excel
            # 如果已经搜索过，就直接查找记录
            if os.path.exists(excelpath):
                taglist = readExcel(excelpath)
                del taglist[0]
                for book in taglist:
                    self.find_result_tab.insertRow(row)
                    self.find_result_tab.setItem(row, 0, QTableWidgetItem(book[1]))
                    self.find_result_tab.setItem(row, 1, QTableWidgetItem(book[2]))
                    self.find_result_tab.setItem(row, 2, QTableWidgetItem(book[9]))
                    row += 1
            # 没有搜索过，则直接从网页获取并保存
            else:
                tagbooks = [['图书编号', '书名', '作者', '出版社', '译者', '出版时间', '页数', '价格', '评价人数', '评分', '评价人数比例', '书籍介绍', '作者介绍', '其他信息', '目录', '相关推荐', '短评', '信息汇总']]
                for i in range(0, len(searchsql)):
                    url = 'http://book.douban.com/subject/' + searchsql[i][0]
                    print(url)
                    path = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\html_dic\\' + searchsql[i][0] + searchsql[i][1] + '.html'
                    if not os.path.exists(path):
                        tag = getHtml(url).encode('utf-8')
                        file = open(path, 'wb')
                        file.write(tag)
                    content = open(path, 'rb').read()
                    try:
                        book = makeBookInfo(content)
                        print(book)
                        tagbooks.append(book)
                        writeExcel(excelpath, tagbooks)
                        self.find_result_tab.insertRow(row)
                        self.find_result_tab.setItem(row, 0, QTableWidgetItem(book[1]))
                        self.find_result_tab.setItem(row, 1, QTableWidgetItem(book[2]))
                        self.find_result_tab.setItem(row, 2, QTableWidgetItem(book[9]))
                        row += 1
                        i += 1
                    except:
                        pass
                try:
                    print(len(tagbooks))
                    if len(tagbooks) > 1:
                        writeExcel(excelpath, tagbooks)
                        print('写入成功：' + excelpath)
                    else:
                        print("无这本书，请重新输入！")


                except:
                    print('写入' + excelpath + '失败！')
                    pass

        except:
            print("无这本书，请重新输入！")


    # 搜索table中的书籍
    def slot_click_search_table(self):
        rows = self.find_result_tab.currentRow()
        keyword = self.searchEdit.text()
        taglist = readExcel(
            'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\xlsx_dic\has_searched' + keyword + '.xlsx')  # 读取标签列表
        del taglist[0]
        book_name = self.find_result_tab.item(rows, 0).text()
        book_director = self.find_result_tab.item(rows, 1).text()
        book_star = self.find_result_tab.item(rows, 2).text()
        try:
            for book in taglist:
                if book[1] == book_name and book[2] == book_director and book[9] == book_star:
                    print(book)
                    self._display_book_information(book)
                    break
        except:
            print("搜索图书出错")

    # 搜索书架上的书籍
    def slot_click_bookshelf_table(self):
        curRow = self.bookshelf.currentRow()  # 当前行
        book_name = self.bookshelf.item(curRow, 0).text()  # 书名
        book_director = self.bookshelf.item(curRow, 1).text()  # 作者
        book_star = self.bookshelf.item(curRow, 2).text()  # 评分
        print(book_name+book_director+book_star)
        rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\xlsx_dic'
        prefix = '.xlsx'
        log = 0
        try:
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
                    if filename.endswith(prefix):  # 寻找所有以xlsx结尾的文件
                        path = str(parent) + '\\' + filename
                        # print(path)
                        taglist = readExcel(path)
                        for book in taglist:
                            if book[1] == book_name and book[2] == book_director and book[9] == book_star:
                                print(path)
                                self._display_book_information(book)
                                log = 1
                                break
                        if log == 1: break

                if log == 1: break

        except:
            print("搜索书籍出错")

    # 搜索推荐书籍
    def slot_click_recommend_table(self):
        curCol = self.recomm_table.currentColumn()  # 当前列
        book_no = self.recomm_table.item(curCol, 0).text()  # 根据编号查找
        dbManager = DbManager()
        select = "SELECT * FROM `book` where `book_no`='" + book_no + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `book_detail` where `book_no`='" + book_no + "'"  # 从数据库中查找书籍
        try:
            book = dbManager.execQuery(select)
            bookde = dbManager.execQuery(selectde)
            self._display_book_information(book[0], bookde[0])
            # self._display_book_information(bookde)
        except:
            print("搜索电影出错")

    # 显示书籍详细信息
    def _display_book_information(self, book):
        self.lineEdit_bname.setText(book[1].strip())
        self.lineEdit_bno.setText(book[0].strip())
        self.lineEdit_bauthor.setText(book[2].strip())
        self.lineEdit_bstar.setText(book[9].strip())
        self.lineEdit_bpub.setText(book[3].strip())
        self.lineEdit_byear.setText(book[5].strip())
        self.lineEdit_bprice.setText(book[7])
        #print(book[8])
        self.lineEdit_bnum.setText(str(book[8])+'人')
        #print(book[9])
        self.lineEdit_burl.setText('http://book.douban.com/subject/' + book[0])
        self.book_intro.setText(book[11])
        self.bookau_intro.setText(book[12])
        self.book_comment.setHtml(book[16])

    # 加入书架
    def slot_join_bookshelf(self):
        book = {}
        book[0] = str(self.lineEdit_bno.text())
        book[1] = str(self.lineEdit_bname.text())
        book[2] = str(self.lineEdit_bauthor.text())
        book[5] = str(self.lineEdit_bstar.text())

        dbManager = DbManager()
        selectsql = "select book_tag,book_kind from `book_tag` where `book_no`='" + book[0] + "'"
        ans = dbManager.execQuery(selectsql)
        for i in ans:
            book[3] = i[0]
            book[4] = i[1]
        dbManager = DbManager()
        insertsql = "INSERT INTO `user_data`(`book_no`, `book_name`, `book_author`, `book_tag`, `book_kind`, `book_star`)" \
                    " VALUES ('{0}', '{1}', '{2}','{3}','{4}', '{5}')"
        try:
            insert = insertsql.format(book[0],
                                      book[1],
                                      book[2],
                                      book[3],
                                      book[4],
                                      book[5]
                                      )
            dbManager.execNonQuery(insert)
            print("加入书架成功")
        except Exception as e:
            print(e)
        self._display_bookshelf()  # 显示在书架上
        # self._recommend_good_books()  # 重新计算推荐电影

    # 从书架删除
    def slot_delete_from_bookshelf(self):
        dbManager = DbManager()
        book_name = str(self.lineEdit_bname.text())
        delsql = "DELETE FROM `user_data` WHERE `book_name`='" + book_name + "'"
        try:
            dbManager.execNonQuery(delsql)
            print("书籍：" + book_name + "已从书架删除")
        except Exception as e:
            print(e)
        self._display_bookshelf()
        # self._recommend_good_books()

    # 刷新书架中的书籍
    def _display_bookshelf(self):
        try:
            dbManager = DbManager()
            selectsql = "select * from `user_data`"
            doc = dbManager.execQuery(selectsql)
            # print(doc)
            # 显示书架上的书
            self.bookshelf.clearContents()
            # self.bookshelf.setRowCount(0)
            row = 0
            for i in range(0, len(doc)):
                print(doc[i])
                self.bookshelf.insertRow(row)
                self.bookshelf.setItem(row, 0, QTableWidgetItem(doc[i][1]))
                self.bookshelf.setItem(row, 1, QTableWidgetItem(doc[i][2]))
                self.bookshelf.setItem(row, 2, QTableWidgetItem(doc[i][5]))
                row += 1
                i += 1
        except:
            print("读取用户表错误")

    """
    # 显示推荐书籍
    def _display_recommend_books(self):
        self.recomm_table.clearContents()  # 每次进行推荐之前先把上次的结果清空
        self.recomm_table.setColumnCount(0)
        column = 0
        for url in self.recommendUrls:
            book = self.mongodb.search_book_by_url(url)
            if book is None:
                continue
            self.recommendTable.insertColumn(column)
            self.recommendTable.setColumnWidth(column, 107)
            self.recommendTable.setItem(0, column, QTableWidgetItem(book['bookName']))
            self.recommendTable.setItem(1, column, QTableWidgetItem(book['score']))
            column += 1
    """

class ConnectCrawler():
    def __init__(self):
        self.__initConnect()

    def __initConnect(self):
        import pymysql.cursors  # 引入数据库的模块
        config = {'host': 'localhost',  # 数据库所在的主机地址，默认localhost
                  'user': 'root',  # 用户
                  'password': '123456789',  # 密码
                  'port': 3306,  # 默认即为3306
                  'database': 'crawler',  # 数据库名称（必须是已经存在于数据库中的才能成功）
                  'charset': 'utf8'  # 默认即为utf8
                  }
        self.conn = pymysql.Connect(**config)
        self.cur = self.conn.cursor()  # 游标，通过这个访问数据库
        if not self.cur:
            raise (NameError, "连接数据库失败")

    def CrawlerexecQuery(self, sql):
        self.cur.execute(sql)
        resList = self.cur.fetchall()  # fetchall():接收全部的返回结果行.
        return resList

    def CrawlerexecNonQuery(self, sql):
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print('执行语句成功')
            return 1
        except Exception:  # 出现异常回滚
            print('执行SQL语句失败：' + sql)
            self.conn.rollback()
            raise  # 使用raise引发异常。一旦出现异常，后续语句不再执行。

class SpiderGui(QDialog):
    def __init__(self, parent=None):
        QWidget.__init__(self)

        self._init_gui()
        self._init_slot()


    def _init_gui(self):
        self.setWindowTitle("Spider")
        self.book_no = QLabel(u'图书编号：')
        self.bnoEdit = QLineEdit()
        self.addTableButton = QPushButton(u'加入数据库')
        self.renewTableButton = QPushButton(u'更新数据库')
        self.outputButton = QPushButton(u'导出xls文件')
        self.spideButton = QPushButton(u'开始爬取')
        self.setWindowIcon(QIcon('D:/workplace/pythonwork/douban_book_catch_zzq/spic/cat.png'))

        icon = QPixmap('')
        iconLabel = QLabel()
        iconLabel.setPixmap(icon)

        layout = QGridLayout(self)
        layout.addWidget(self.book_no, 0, 0)
        layout.addWidget(self.bnoEdit, 0, 1, 1, 3)
        layout.addWidget(iconLabel, 1, 0, 2, 1)
        layout.addWidget(self.addTableButton, 1, 1)
        layout.addWidget(self.renewTableButton, 1, 2)
        layout.addWidget(self.outputButton, 1, 3)
        layout.addWidget(self.spideButton, 2, 1, 1, 3)
    # 信号和槽函数
    def _init_slot(self):
        self.addTableButton.clicked.connect(self._addTable)
        self.renewTableButton.clicked.connect(self._renewTable)
        self.spideButton.clicked.connect(self._spide)
        self.outputButton.clicked.connect(self._output_xls)
    # 数据抓取到本地excel之后，将数据新加入到数据库中
    def _addTable(self,):
        try:
            dbmanager = ConnectCrawler()
            excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\newbook.xls'
            newbookWb = xlrd.open_workbook(excelpath)  # 获取需要插入数据的excel
            table = newbookWb.sheet_by_name(u"sheet1")  # 获取sheet1
            success = 0
            already = 0
            for i in range(1, table.nrows):
                book = table.row_values(i)
                # print(book)
                book_no = book[0]
                select = "SELECT * FROM `book_bookdetail` where `book_no`='" + book_no + "'"
                searchsql = dbmanager.CrawlerexecQuery(select)
                if searchsql:
                    already += 1
                    continue
                else:
                    # 加入book表
                    try:
                        is_exist = "select * from `book_book` where `book_no`='" + book_no + "'"
                        is_exist_1 = dbmanager.CrawlerexecQuery(is_exist)
                        if not is_exist_1:
                            addsql2 = "INSERT INTO `book_book`(`book_name`, `book_no`, `book_info`, `book_url`, `stars`,`click_nums`,`fav_nums`,`image`,`add_time`,`book_kind_id`,`book_tag`,`is_banner`)" \
                                      " VALUES ('{0}', '{1}', '{2}','{3}','{4}',{5},{6},'{7}','{8}',{9},'{10}',{11})"
                            insert2 = addsql2.format(book[1], book[0], book[17], "https://book.douban.com/subject/" + book[0] + "/",
                                                     book[9], 0, 0, "book_detail/2017/05/18/" + book[0] + ".jpg", '2017-05-18', 99, 'wh', 0)
                            dbmanager.CrawlerexecNonQuery(insert2)
                    except Exception as e:
                        print("加入book表失败")
                        print(e)
                        # 下载图片到media文件夹
                    # 加入bookdetail表
                    try:
                        detail_is_exist = "select * from `book_bookdetail` where `book_no`='" + book_no + "'"
                        detail_is_exist_1 = dbmanager.CrawlerexecQuery(detail_is_exist)
                        if not detail_is_exist_1:
                            addsql = "INSERT INTO `book_bookdetail` (`book_no`, `book_name`, `book_author`, `book_public`, `book_year`, `book_page`, `book_price`,  `votenum`,`stars`, `book_intro`, `author_intro`,`book_others`, `mu_lu`,`recommendations`,`comments`,`book_info`,`click_nums`,`fav_nums`,`add_time`,`image`)" \
                                     " VALUES ('{0}', '{1}', '{2}','{3}','{4}',{5},'{6}',{7},'{8}','{9}','{10}','{11}','{12}','{13}','{14}','{15}',{16},{17},'{18}','{19}')"
                            insert = addsql.format(book[0], book[1], book[2], book[3], book[5], book[6], book[7], book[8],
                                                   book[9],
                                                   book[11], book[12], book[13], book[14], book[15], book[16], book[17], 0, 0,
                                                   '2017-05-18', "book_detail/2017/05/18/" + book[0] + ".jpg")
                            dbmanager.CrawlerexecNonQuery(insert)
                    except Exception as e:
                        print("加入book_detail表失败")
                        print(e)


                    try:
                        path = "https://book.douban.com/subject/" + book[0] + "/"
                        tag = getHtml(path).encode('utf-8')
                        soup = BeautifulSoup(tag, 'html.parser')
                        book_mes = soup.select("div.article div#mainpic")
                        subsoup = BeautifulSoup(str(book_mes), 'html.parser')
                        pic_url = subsoup.a.img['src']  # 图片链接
                        print(pic_url)
                        savepath = 'D:/workplace/pythonwork/Crawler/media/book_detail/2017/05/18'
                        work_path = os.path.join(savepath + '/', book[0] + '.jpg')
                        urllib.request.urlretrieve(pic_url, '%s' % str(work_path))
                        print("下载图片成功")
                    except Exception as e:
                        print(e)
                    success += 1
            if success or already:
                QMessageBox.information(self, u"提示", u"新加入图书"+str(success)+"本。有"+str(already)+"本已经存在。")
                return
        except Exception as e:
            print(e)
    # 数据抓取到本地excel之后，将数据更新到数据库中
    def _renewTable(self):
        try:
            dbmanager = ConnectCrawler()
            excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\newbook.xls'
            newbookWb = xlrd.open_workbook(excelpath)  # 获取需要插入数据的excel
            table = newbookWb.sheet_by_name(u"sheet1")  # 获取sheet1
            success = 0
            fail = 0
            for i in range(1, table.nrows):
                book = table.row_values(i)
                print(book)
                book_no = book[0]
                try:
                    update1 = "UPDATE `book_book` SET stars = '{stars}' where `book_no`='" + book_no + "'"
                    update_sql1 = update1.format(stars=book[9])
                    updatesql1 = dbmanager.CrawlerexecNonQuery(update_sql1)
                except Exception as e:
                    print(e)
                    pass
                try:
                    update2 = "UPDATE `book_bookdetail` SET stars = '{stars}' where `book_no`='" + book_no + "'"
                    update_sql2 = update2.format(stars=book[9])
                    updatesql2 = dbmanager.CrawlerexecNonQuery(update_sql2)
                except Exception as e:
                    print(e)
                    pass
                if updatesql1 and updatesql2:
                      success += 1
                else:
                    fail += 1
            if success or fail:
                QMessageBox.information(self, u"提示", str(success) + "本更新成功。" + str(fail) + "本更新失败。")
                return


        except:
            print("出错了")

    def _output_xls(self):
        QMessageBox.information(self, u"通知", u"导出xls文件完成！")
        return

    def _spide(self):
        try:
            dbmanager = ConnectCrawler()
            bookno = self.bnoEdit.text()
            if not bookno:
                QMessageBox.information(self, u"提示", u"让我爬谁呀大哥，给个编号")
                return
            print(bookno)
            select = "SELECT * FROM `book_bookdetail` where `book_no`='" + bookno + "'"
            searchsql = dbmanager.CrawlerexecQuery(select)
            # 电影已经在数据库中
            if searchsql:
                QMessageBox.information(self, u"提示", u"该图书记录已经存在。")
                return
            # 电影记录不存在，则重新抓取
            else:
                url = 'http://book.douban.com/subject/'+bookno
                excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\\book_select_dic\\newbook.xls'  # 创建保存记录的excel
                if os.path.exists(excelpath):
                    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/book_select_dic/newbooks/'+bookno+'.html'
                    if not os.path.exists(path):
                        tag = getHtml(url).encode('utf-8')
                        file = open(path, 'wb')
                        file.write(tag)
                    content = open(path, 'rb').read()
                    book = makeBookInfo(content)
                    print(book)
                    try:
                        oldWb = xlrd.open_workbook(excelpath, formatting_info=True)  # 获取需要插入数据的excel
                        this_sheet = oldWb.sheet_by_name(u"sheet1")  # 获取sheet1
                        row = this_sheet.nrows
                        newWb = copy(oldWb)  # 拷贝原始文件
                        sheet = newWb.get_sheet(0)  # 原始文件中存在sheetname=0的文件
                        for i in range(0, len(book)):
                            sheet.write(row, i, book[i])  # row行，col列，data追加的数据，style数据样式
                        print("=====写完啦=======")
                        newWb.save(excelpath)
                        QMessageBox.information(self, u"提示", u"数据添加成功。")
                        return
                    except Exception as e:
                        print(e)
                else:
                    newbooks = ['图书编号', '书名', '作者', '出版社','译者', '出版时间', '页数', '价格', '评论人数', '评分','评价人数比例', '书籍介绍',
                                 '作者介绍', '其他信息', '目录',  '相关推荐', '短评','信息汇总']
                    try:
                        file = xlwt.Workbook()  # 创建工作簿
                        sheet1 = file.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
                        for i in range(0, len(newbooks)):
                            sheet1.write(0, i, newbooks[i])
                        file.save(excelpath)
                        QMessageBox.information(self, u"提示", u"本次数据表新建完成，请加入数据。")
                        return
                    except:
                        QMessageBox.information(self, u"提示", u"本次数据表新建失败，请重新创建。")
                        return

        except:
            print("出错了")

class MyWindow(spider):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.find_but.clicked.connect(self.slot_search_keyword)
        self.find_result_tab.itemClicked['QTableWidgetItem*'].connect(self.slot_click_search_table)
        self.addb_pushB.clicked.connect(self.slot_join_bookshelf)
        self.delb_pushB.clicked.connect(self.slot_delete_from_bookshelf)
        self.bookshelf.itemClicked['QTableWidgetItem*'].connect(self.slot_click_bookshelf_table)
        self.recomm_table.itemClicked['QTableWidgetItem*'].connect(self.slot_click_recommend_table)
        self.crawl_Button.clicked.connect(self.spiderGui.show)
        spider._display_bookshelf(self)  # 打开界面时初始化我的影集

class splashscreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__(QPixmap('D:/workplace/pythonwork/douban_book_catch_zzq/spic/book.png'))
    def effect(self):
        self.setWindowOpacity(0)
        t = 0  # 淡入
        while t < 50:
            newOpacity = self.windowOpacity()+0.1
            if newOpacity > 1:
                break
            self.setWindowOpacity(newOpacity)
            self.show()
            t -= 1
            time.sleep(0.04)

        time.sleep(1)
        t = 0 # 淡出
        while t <= 50:
            newOpacity = self.windowOpacity()-0.02
            if newOpacity < 0:
                break
            self.setWindowOpacity(newOpacity)
            t += 1
            time.sleep(0.04)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    # app.aboutToQuit.connect(app.deleteLater)
    splash = splashscreen()
    splash.effect()
    gui = MyWindow()
    splash.finish(gui)  # 关闭启动图片

    app.exec_()


