# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'movie_test_ui.ui'
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

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QIcon
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *

from src.movie.tools.Db_manager import DbManager
from src.movie.tools.Html_manager import getHtml
from src.movie.tools.Tag_manager import makeMovieInfo
from src.tool.ExcelManager import writeExcel, readExcel


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1258, 717)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        # # 根据
        # self.label = QtWidgets.QLabel(self.centralwidget)
        # self.label.setGeometry(QtCore.QRect(10, 20, 54, 12))
        # self.label.setObjectName("label")
        # # 下拉选择combobox
        # self.selectway_box = QtWidgets.QComboBox(self.centralwidget)
        # self.selectway_box.setGeometry(QtCore.QRect(40, 10, 69, 22))
        # sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        # sizePolicy.setHorizontalStretch(0)
        # sizePolicy.setVerticalStretch(0)
        # sizePolicy.setHeightForWidth(self.selectway_box.sizePolicy().hasHeightForWidth())
        # self.selectway_box.setSizePolicy(sizePolicy)
        # self.selectway_box.setObjectName("selectway_box")
        # # 查询label
        # self.label_sel = QtWidgets.QLabel(self.centralwidget)
        # self.label_sel.setGeometry(QtCore.QRect(120, 20, 54, 12))
        # self.label_sel.setObjectName("label_sel")

        # —————————————————————————— 搜索栏布局 ————————————————————————————

        self.gridLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(10, 10, 311, 441))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.select_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.select_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.select_gridLayout.setObjectName("select_gridLayout")
        # 电影名输入
        self.lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.lineEdit.setObjectName("lineEdit")
        self.select_gridLayout.addWidget(self.lineEdit, 0, 2, 1, 1)
        # 查询button
        self.find_but = QtWidgets.QPushButton(self.gridLayoutWidget)
        self.find_but.setObjectName("find_but")
        self.select_gridLayout.addWidget(self.find_but, 0, 3, 1, 1)
        # 电影名label
        self.movie_name = QtWidgets.QLabel(self.gridLayoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.movie_name.sizePolicy().hasHeightForWidth())
        self.movie_name.setSizePolicy(sizePolicy)
        self.movie_name.setObjectName("movie_name")
        self.select_gridLayout.addWidget(self.movie_name, 0, 1, 1, 1)
        # 查询电影显示table
        self.find_result_table = QtWidgets.QTableWidget(self.gridLayoutWidget)
        self.find_result_table.setObjectName("find_result_table")
        self.find_result_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.find_result_table.resizeColumnsToContents()  # 各属性列的大小自适性
        self.find_result_table.resizeRowsToContents()
        item = QtWidgets.QTableWidgetItem()
        self.find_result_table.setColumnCount(3)  # 指定列数（3列）
        self.find_result_table.setRowCount(1000)
        self.find_result_table.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_table.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_table.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.find_result_table.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
        self.select_gridLayout.addWidget(self.find_result_table, 1, 1, 1, 3)

        # —————————————————————————— 详细信息显示栏布局 ————————————————————————————

        self.gridLayoutWidget_2 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_2.setGeometry(QtCore.QRect(330, 10, 571, 471))
        self.gridLayoutWidget_2.setObjectName("gridLayoutWidget_2")
        self.show_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_2)
        self.show_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.show_gridLayout.setObjectName("show_gridLayout")
        # 电影名label
        self.mname = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mname.setObjectName("mname")
        self.show_gridLayout.addWidget(self.mname, 0, 0, 1, 1)
        # 电影类型label
        self.mtype = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mtype.setObjectName("mtype")
        self.show_gridLayout.addWidget(self.mtype, 5, 0, 1, 1)
        # 评价显示
        self.lineEdit_mstar = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mstar.setObjectName("lineEdit_mstar")
        self.show_gridLayout.addWidget(self.lineEdit_mstar, 6, 1, 1, 1)
        # 电影名显示
        self.lineEdit_mname = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mname.setObjectName("lineEdit_mname")
        self.show_gridLayout.addWidget(self.lineEdit_mname, 0, 1, 1, 1)
        # 电影类型显示
        self.lineEdit_mtype = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mtype.setObjectName("lineEdit_mtype")
        self.show_gridLayout.addWidget(self.lineEdit_mtype, 5, 1, 1, 1)
        # 电影编号label
        self.mno = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mno.setObjectName("mno")
        self.show_gridLayout.addWidget(self.mno, 1, 0, 1, 1)
        # 评价label
        self.mstar = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mstar.setObjectName("mstar")
        self.show_gridLayout.addWidget(self.mstar, 6, 0, 1, 1)
        # 导演label
        self.mauthor = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mauthor.setObjectName("mauthor")
        self.show_gridLayout.addWidget(self.mauthor, 2, 0, 1, 1)
        # 电影编号显示
        self.lineEdit_mno = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mno.setObjectName("lineEdit_mno")
        self.show_gridLayout.addWidget(self.lineEdit_mno, 1, 1, 1, 1)
        # 主演显示
        self.mactor = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mactor.setObjectName("mactor")
        self.show_gridLayout.addWidget(self.mactor, 3, 0, 1, 1)
        # 地区国家label
        self.mcountry = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mcountry.setObjectName("mcountry")
        self.show_gridLayout.addWidget(self.mcountry, 7, 0, 1, 1)
        # 导演显示
        self.lineEdit_mauthor = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mauthor.setObjectName("lineEdit_mauthor")
        self.show_gridLayout.addWidget(self.lineEdit_mauthor, 2, 1, 1, 1)
        # 主演显示
        self.lineEdit_mactor = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mactor.setObjectName("lineEdit_mactor")
        self.show_gridLayout.addWidget(self.lineEdit_mactor, 3, 1, 1, 1)
        # 上映时间label
        self.myear = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.myear.setObjectName("myear")
        self.show_gridLayout.addWidget(self.myear, 4, 0, 1, 1)
        # 上映时间显示
        self.lineEdit_myear = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_myear.setObjectName("lineEdit_myear")
        self.show_gridLayout.addWidget(self.lineEdit_myear, 4, 1, 1, 1)
        # 添加电影到影集button
        self.addb_pushB = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.addb_pushB.setObjectName("addb_pushB")
        self.show_gridLayout.addWidget(self.addb_pushB, 12, 0, 1, 2)
        # 从影集删除button
        self.delb_pushB = QtWidgets.QPushButton(self.gridLayoutWidget_2)
        self.delb_pushB.setObjectName("delb_pushB")
        self.show_gridLayout.addWidget(self.delb_pushB, 12, 2, 1, 1)
        # 语言显示
        self.lineEdit_mlanguage = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mlanguage.setObjectName("lineEdit_mlanguage")
        self.show_gridLayout.addWidget(self.lineEdit_mlanguage, 8, 1, 1, 1)
        # 国家显示
        self.lineEdit_mcountry = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_mcountry.setObjectName("lineEdit_mcountry")
        self.show_gridLayout.addWidget(self.lineEdit_mcountry, 7, 1, 1, 1)
        # 链接label
        self.murl = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.murl.setObjectName("murl")
        self.show_gridLayout.addWidget(self.murl, 10, 0, 1, 1)
        # 语言label
        self.mlanguage = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mlanguage.setObjectName("mlanguage")
        self.show_gridLayout.addWidget(self.mlanguage, 8, 0, 1, 1)
        # 剧情简介显示
        self.TexEdit_mintro = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        self.TexEdit_mintro.setObjectName("TexEdit_mintro")
        self.show_gridLayout.addWidget(self.TexEdit_mintro, 11, 1, 1, 1)
        # 剧情简介label
        self.mintro = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mintro.setObjectName("mintro")
        self.show_gridLayout.addWidget(self.mintro, 11, 0, 1, 1)
        # 影评label
        self.mcomment = QtWidgets.QLabel(self.gridLayoutWidget_2)
        self.mcomment.setObjectName("mcomment")
        self.show_gridLayout.addWidget(self.mcomment, 0, 2, 1, 1)
        # 影评显示
        self.TexEdit_mcomment = QtWidgets.QTextEdit(self.gridLayoutWidget_2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.TexEdit_mcomment.sizePolicy().hasHeightForWidth())
        self.TexEdit_mcomment.setSizePolicy(sizePolicy)
        self.TexEdit_mcomment.setObjectName("TexEdit_mcomment")
        self.show_gridLayout.addWidget(self.TexEdit_mcomment, 1, 2, 11, 1)
        # 链接显示
        self.lineEdit_url = QtWidgets.QLineEdit(self.gridLayoutWidget_2)
        self.lineEdit_url.setObjectName("lineEdit_url")
        self.show_gridLayout.addWidget(self.lineEdit_url, 10, 1, 1, 1)

        # —————————————————————————— 我的影集栏布局 ————————————————————————————

        self.gridLayoutWidget_3 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_3.setGeometry(QtCore.QRect(910, 10, 331, 471))
        self.gridLayoutWidget_3.setObjectName("gridLayoutWidget_3")
        self.myshelf_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_3)
        self.myshelf_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.myshelf_gridLayout.setObjectName("myshelf_gridLayout")
        # 影集label
        self.label_movieshelf = QtWidgets.QLabel(self.gridLayoutWidget_3)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_movieshelf.sizePolicy().hasHeightForWidth())
        self.label_movieshelf.setSizePolicy(sizePolicy)
        self.label_movieshelf.setObjectName("label_movieshelf")
        self.myshelf_gridLayout.addWidget(self.label_movieshelf, 0, 0, 1, 1)
        # 影集显示table
        self.movieshelf = QtWidgets.QTableWidget(self.gridLayoutWidget_3)
        self.movieshelf.setObjectName("movieshelf")
        self.movieshelf.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.movieshelf.resizeColumnsToContents()  # 各属性列的大小自适性
        self.movieshelf.resizeRowsToContents()
        item = QtWidgets.QTableWidgetItem()
        self.movieshelf.setColumnCount(3)  # 指定列数（3列）
        self.movieshelf.setRowCount(1000)
        self.movieshelf.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.movieshelf.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.movieshelf.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.movieshelf.setSelectionBehavior(QAbstractItemView.SelectRows)  # 整行选中的方式
        #self.movieshelf.setColumnCount(0)
        #self.movieshelf.setRowCount(0)
        self.myshelf_gridLayout.addWidget(self.movieshelf, 1, 0, 1, 1)

        # —————————————————————————— 推荐栏布局 ————————————————————————————

        self.gridLayoutWidget_4 = QtWidgets.QWidget(self.centralwidget)
        self.gridLayoutWidget_4.setGeometry(QtCore.QRect(10, 490, 1231, 171))
        self.gridLayoutWidget_4.setObjectName("gridLayoutWidget_4")
        self.recomm_gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget_4)
        self.recomm_gridLayout.setContentsMargins(0, 0, 0, 0)
        self.recomm_gridLayout.setObjectName("recomm_gridLayout")
        # 推荐电影显示
        self.recomm_table = QtWidgets.QTableWidget(self.gridLayoutWidget_4)
        self.recomm_table.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        self.recomm_table.setObjectName("recomm_table")
        self.recomm_table = QTableWidget(3, 0)  # 表示三列，0行
        self.recomm_table.setVerticalHeaderLabels([u'电影名', u'评分', u'类型']) # 各属性行名称
        # self.recomm_table.resizeColumnsToContents()
        # self.recomm_table.resizeRowsToContents()
        # item = QtWidgets.QTableWidgetItem()
        # self.recomm_table.setVerticalHeaderItem(0, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.recomm_table.setVerticalHeaderItem(1, item)
        # item = QtWidgets.QTableWidgetItem()
        # self.recomm_table.setVerticalHeaderItem(2, item)
        # self.recomm_table.setColumnCount(1000)  # 指定列数（3列）
        # self.recomm_table.setRowCount(3)  # 指定行数（3行）
        self.recomm_table.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 禁止编辑
        self.recomm_table.setSelectionBehavior(QAbstractItemView.SelectColumns)  # 整列选中的方式
        self.recomm_table.resizeRowsToContents()
        #self.recomm_table.setColumnCount(0)
        #self.recomm_table.setRowCount(0)
        self.recomm_gridLayout.addWidget(self.recomm_table, 0, 0, 1, 1)

        # 爬虫窗口button
        self.crawlButton = QtWidgets.QPushButton(self.centralwidget)
        self.crawlButton.setGeometry(QtCore.QRect(220, 460, 101, 23))
        self.crawlButton.setObjectName("crawlButton")
        # 猜你喜欢label
        self.label_1 = QtWidgets.QLabel(self.centralwidget)
        self.label_1.setGeometry(QtCore.QRect(10, 465, 54, 12))
        self.label_1.setObjectName("label_1")
        MainWindow.setCentralWidget(self.centralwidget)
        """
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1258, 23))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        self.menu_2 = QtWidgets.QMenu(self.menubar)
        self.menu_2.setObjectName("menu_2")
        self.menu_3 = QtWidgets.QMenu(self.menubar)
        self.menu_3.setObjectName("menu_3")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.menubar.addAction(self.menu.menuAction())
        self.menubar.addAction(self.menu_2.menuAction())
        self.menubar.addAction(self.menu_3.menuAction())
        """

        self.retranslateUi(MainWindow)
        """
        self.find_but.clicked.connect(MainWindow.slot_search_keyword)
        self.find_result_table.itemClicked['QTableWidgetItem*'].connect(MainWindow.slot_click_search_table)
        self.addb_pushB.clicked.connect(MainWindow.slot_join_movieshelf)
        self.delb_pushB.clicked.connect(MainWindow.slot_delete_from_movieshelf)
        self.movieshelf.itemClicked['QTableWidgetItem*'].connect(MainWindow.slot_click_movieshelf_table)
        self.recomm_table.itemClicked['QTableWidgetItem*'].connect(MainWindow.slot_click_recommend_table)
        """
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        # self.label.setText(_translate("MainWindow", "根据"))
        # self.label_sel.setText(_translate("MainWindow", "查询"))
        self.find_but.setText(_translate("MainWindow", "搜索"))
        self.movie_name.setText(_translate("MainWindow", "电影名："))
        self.mname.setText(_translate("MainWindow", "电影名："))
        self.mtype.setText(_translate("MainWindow", "类型："))
        self.mno.setText(_translate("MainWindow", "编号："))
        self.mstar.setText(_translate("MainWindow", "评分："))
        self.mauthor.setText(_translate("MainWindow", "导演："))
        self.mactor.setText(_translate("MainWindow", "主演："))
        self.mcountry.setText(_translate("MainWindow", "国家/地区："))
        self.myear.setText(_translate("MainWindow", "上映时间："))
        self.addb_pushB.setText(_translate("MainWindow", "加入我的影集"))
        self.delb_pushB.setText(_translate("MainWindow", "从我的影集删除"))
        self.murl.setText(_translate("MainWindow", "链接："))
        self.mlanguage.setText(_translate("MainWindow", "语言："))
        self.mintro.setText(_translate("MainWindow", "剧情简介："))
        self.mcomment.setText(_translate("MainWindow", "热门影评："))
        self.label_movieshelf.setText(_translate("MainWindow", "我的影集："))
        self.crawlButton.setText(_translate("MainWindow", "爬虫窗口"))
        self.label_1.setText(_translate("MainWindow", "猜你喜欢："))
#        self.menu.setTitle(_translate("MainWindow", "图书"))
#        self.menu_2.setTitle(_translate("MainWindow", "电影"))
#        self.menu_3.setTitle(_translate("MainWindow", "推荐"))
        # 查询结果显示
        item = self.find_result_table.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "电影名"))
        # self.find_result_tab.horizontalHeaderItem(0).setText(_translate("MainWindow", "书名"))
        item = self.find_result_table.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "类型"))
        item = self.find_result_table.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "评分"))
        # 影集电影显示
        item = self.movieshelf.horizontalHeaderItem(0)
        item.setText(_translate("MainWindow", "电影名"))
        item = self.movieshelf.horizontalHeaderItem(1)
        item.setText(_translate("MainWindow", "类型"))
        item = self.movieshelf.horizontalHeaderItem(2)
        item.setText(_translate("MainWindow", "评分"))

class spider(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(spider, self).__init__()
        self.setupUi(self)
        self.setWindowIcon(QIcon('D:/workplace/pythonwork/douban_book_catch_zzq/spic/bookIcon.jpg'))
        self.spiderGui = SpiderGui()
        self.setWindowTitle('ZZQ_Movie')
        # 显示主窗口
        self.show()
    #-------------- 从数据库获取数据并显示-----------
    """
    # 搜索电影
    def slot_search_keyword(self):
        keyword = self.lineEdit.text()
        print(keyword)
        if keyword is None:
            return
        dbManager = DbManager()
        if keyword.find("%") == -1:
            select = "SELECT movie_name,movie_type,stars FROM `movie_detail` where `movie_name`='" + keyword + "'"  # 从数据库中查找书籍
        else:
            select = "SELECT movie_name,movie_type,stars FROM `movie_detail` where `movie_name` LIKE '" + keyword + "'"  # 从数据库中查找书籍

        try:
            searchsql = dbManager.execQuery(select)
            print(searchsql)
            print(len(searchsql))
            # 显示查询结果
            self.find_result_table.clearContents()
            #self.find_result_tab.setRowCount(0)
            row = 0
            for i in range(0, len(searchsql)):
                #print(searchsql[i])
                self.find_result_table.insertRow(row)
                #print(searchsql[i][0], searchsql[i][1], searchsql[i][2])
                self.find_result_table.setItem(row, 0, QTableWidgetItem(searchsql[i][0]))
                self.find_result_table.setItem(row, 1, QTableWidgetItem(searchsql[i][1]))
                self.find_result_table.setItem(row, 2, QTableWidgetItem(searchsql[i][2]))
                row += 1
                i += 1
                # 搜索table的item
        except:
            print("无这部电影，请重新输入！")

    # 搜索table中的电影
    def slot_click_search_table(self):
        rows = self.find_result_table.currentRow()
        print(self.find_result_table.item(rows, 0).text())
        print(self.find_result_table.item(rows, 1).text())
        print(self.find_result_table.item(rows, 2).text())

        movie_name = self.find_result_table.item(rows, 0).text()
        dbManager = DbManager()
        selectde = "SELECT * FROM `movie_detail` where `movie_name`='" + movie_name + "'"  # 从数据库中查找书籍
        select = "SELECT * FROM `movie` where `movie_name`='" + movie_name + "'"  # 从数据库中查找书籍

        try:
            movie = dbManager.execQuery(select)
            moviede = dbManager.execQuery(selectde)
            print(movie[0])
            print(moviede[0])
            self._display_movie_information(movie[0], moviede[0])
        except:
            print("搜索电影出错")

    # 搜索影集上的电影
    def slot_click_movieshelf_table(self):
        curRow = self.movieshelf.currentRow()  # 当前列
        movie_name = self.movieshelf.item(curRow, 0).text()  # 根据编号查找
        dbManager = DbManager()
        select = "SELECT * FROM `movie` where `movie_name`='" + movie_name + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `movie_detail` where `movie_name`='" + movie_name + "'"  # 从数据库中查找书籍
        try:
            movie = dbManager.execQuery(select)
            moviede = dbManager.execQuery(selectde)
            self._display_movie_information(movie[0], moviede[0])
        except:
            print("搜索电影出错")

    # 搜索推荐电影
    def slot_click_recommend_table(self):
        curCol = self.recomm_table.currentColumn()  # 当前列
        movie_no = self.recomm_table.item(curCol, 0).text()  # 根据编号查找
        dbManager = DbManager()
        select = "SELECT * FROM `movie` where `movie_no`='" + movie_no + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `movie_detail` where `movie_no`='" + movie_no + "'"  # 从数据库中查找书籍
        try:
            movie = dbManager.execQuery(select)
            moviede = dbManager.execQuery(selectde)
            self._display_book_information(movie[0],moviede[0])
            #self._display_book_information(bookde)
        except:
            print("搜索电影出错")

    # 显示电影详细信息

    def _display_movie_information(self, movie, moviede):
        print(movie)
        print(moviede)
        self.lineEdit_mname.setText(movie[2].strip())
        self.lineEdit_mno.setText(movie[1].strip())
        self.lineEdit_mauthor.setText(movie[4].strip())
        self.lineEdit_mactor.setText(movie[6].strip())
        self.lineEdit_myear.setText(moviede[10].strip())
        self.lineEdit_mtype.setText(moviede[7].strip())
        self.lineEdit_mstar.setText(movie[6])
        self.lineEdit_mcountry.setText(moviede[8])
        self.lineEdit_mlanguage.setText(moviede[9])
        self.lineEdit_url.setText(movie[3])
        self.TexEdit_mintro.setText(moviede[15])
        self.TexEdit_mcomment.setHtml(moviede[17])


    # 加入影集
    def slot_join_movieshelf(self):
        movie = {}
        movie[0] = str(self.lineEdit_mname.text())
        movie[1] = str(self.lineEdit_mno.text())
        movie[2] = str(self.lineEdit_mtype.text())
        movie[3] = str(self.lineEdit_mstar.text())

        dbManager = DbManager()
        insertsql="INSERT INTO `user_data`(`movie_name`, `movie_no`, `movie_kind`, `movie_star`)" \
                  " VALUES ('{0}', '{1}', '{2}', '{3}')"
        try:
            insert = insertsql.format( movie[0],
                                       movie[1],
                                       movie[2],
                                       movie[3]
                                       )
            dbManager.execNonQuery(insert)  # 非查询语句用execNonQuery()实现
            print("加入影集成功")
        except Exception as e:
            print(e)
        self._display_movieshelf()   # 显示在影集中
       # self._recommend_good_books()  # 重新计算推荐电影

    # 从影集删除
    def slot_delete_from_movieshelf(self):
        dbManager = DbManager()
        movie_name = str(self.lineEdit_mname.text())
        delsql = "DELETE  FROM `user_data` WHERE `movie_name`='"+movie_name+"'"
        try:
            dbManager.execNonQuery(delsql)
            print("电影："+movie_name+"已从影集删除")
        except Exception as e:
            print(e)
        self._display_movieshelf()
        #self._recommend_good_books()

    # 刷新影集中的电影
    def _display_movieshelf(self):
        try:
            dbManager = DbManager()
            selectsql = "select * from `user_data`"
            doc = dbManager.execQuery(selectsql)
            print(doc)
            # 显示书架上的书
            self.movieshelf.clearContents()
            #self.bookshelf.setRowCount(0)
            row = 0
            for i in range(0, len(doc)):
                print(doc[i])
                self.movieshelf.insertRow(row)
                self.movieshelf.setItem(row, 0, QTableWidgetItem(doc[i][1]))
                self.movieshelf.setItem(row, 1, QTableWidgetItem(doc[i][3]))
                self.movieshelf.setItem(row, 2, QTableWidgetItem(doc[i][4]))
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
    #--------------从网页获取数据并显示--------------
    # 搜索电影
    def slot_search_keyword(self):
            keyword = self.lineEdit.text()
            print(keyword)
            if keyword is None:
                return
            dbManager = DbManager()
            if keyword.find("%") == -1:
                select = "SELECT movie_no,movie_name FROM `movie` where `movie_name`='" + keyword + "'"  # 从数据库中查找电影
            else:
                select = "SELECT movie_no,movie_name FROM `movie` where `movie_name` LIKE '" + keyword + "'"  # 从数据库中查找电影

            try:
                searchsql = dbManager.execQuery(select)
                print(searchsql)
                #print(len(searchsql))
                # 显示查询结果
                self.find_result_table.clearContents()
                # self.find_result_tab.setRowCount(0)
                row = 0
                excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\xlsx_dic\has_searched'+keyword+'.xlsx'  # 创建保存记录的excel
                # 如果已经搜索过，就直接查找记录
                if os.path.exists(excelpath):
                    print(excelpath)
                    taglist = readExcel(excelpath)
                    del taglist[0]
                    for movie in taglist:
                        self.find_result_table.insertRow(row)
                        self.find_result_table.setItem(row, 0, QTableWidgetItem(movie[1]))
                        self.find_result_table.setItem(row, 1, QTableWidgetItem(movie[6]))
                        self.find_result_table.setItem(row, 2, QTableWidgetItem(movie[12]))
                        row += 1
                # 没有搜索过，则直接从网页获取并保存
                else:
                    tagmovies = [['电影编号', '电影名', '公布时间', '导演', '编剧', '主演', '类型', '国家/地区', '语言',
                                  '上映时间', '时长', '评价人数', '电影星级', '评价人数比例', '剧情介绍', '相关推荐', '短评']]
                    for i in range(0, len(searchsql)):
                        url = 'http://movie.douban.com/subject/' + searchsql[i][0]
                        print(url)
                        path = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\html_dic\\'+searchsql[i][0]+searchsql[i][1]+'.html'
                        if not os.path.exists(path):
                            tag = getHtml(url).encode('utf-8')
                            file = open(path, 'wb')
                            file.write(tag)
                        content = open(path, 'rb').read()
                        movie = makeMovieInfo(content)
                        tagmovies.append(movie)
                        self.find_result_table.insertRow(row)
                        self.find_result_table.setItem(row, 0, QTableWidgetItem(movie[1]))
                        self.find_result_table.setItem(row, 1, QTableWidgetItem(movie[6]))
                        self.find_result_table.setItem(row, 2, QTableWidgetItem(movie[12]))
                        row += 1
                        i += 1
                    try:
                        print(len(tagmovies))
                        if len(tagmovies) > 1:
                            writeExcel(excelpath, tagmovies)
                            print('写入成功：' + excelpath)
                    except:
                        print('写入' + excelpath + '失败！')
                        pass

            except:
                print("无这部电影，请重新输入！")
    # 搜索table中的电影
    def slot_click_search_table(self):
        rows = self.find_result_table.currentRow()
        keyword = self.lineEdit.text()
        taglist = readExcel('D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\xlsx_dic\has_searched' + keyword + '.xlsx')  # 读取标签列表
        del taglist[0]
        movie_name = self.find_result_table.item(rows, 0).text()
        movie_type = self.find_result_table.item(rows, 1).text()
        movie_star = self.find_result_table.item(rows, 2).text()
        try:
            for movie in taglist:
                if movie[1] == movie_name and movie[6] == movie_type and movie[12] == movie_star:
                    print(movie)
                    self._display_movie_information(movie)
                    break
        except:
            print("搜索电影出错")
    # 搜索影集上的电影
    def slot_click_movieshelf_table(self):
        curRow = self.movieshelf.currentRow()  # 当前行
        movie_name = self.movieshelf.item(curRow, 0).text().replace("'", "\\'").replace('"', '\\"')  # 电影名
        movie_type = self.movieshelf.item(curRow, 1).text()  # 电影类型
        movie_star = self.movieshelf.item(curRow, 2).text()  # 电影评分
        rootdir = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\xlsx_dic'
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
                        for movie in taglist:
                            if movie[1] == movie_name and movie[6] == movie_type and movie[12] == movie_star:
                                print(path)
                                self._display_movie_information(movie)
                                log = 1
                                break
                        if log == 1:
                            break
                if log == 1:
                    break

        except:
            print("搜索电影出错")
    # 搜索推荐电影
    def slot_click_recommend_table(self):
        curCol = self.recomm_table.currentColumn()  # 当前列
        movie_no = self.recomm_table.item(curCol, 0).text()  # 根据编号查找
        dbManager = DbManager()
        select = "SELECT * FROM `movie` where `movie_no`='" + movie_no + "'"  # 从数据库中查找书籍
        selectde = "SELECT * FROM `movie_detail` where `movie_no`='" + movie_no + "'"  # 从数据库中查找书籍
        try:
            movie = dbManager.execQuery(select)
            moviede = dbManager.execQuery(selectde)
            self._display_book_information(movie[0],moviede[0])
            #self._display_book_information(bookde)
        except:
            print("搜索电影出错")
    # 显示电影详细信息
    def _display_movie_information(self, movie):
        self.lineEdit_mname.setText(movie[1].strip())
        self.lineEdit_mno.setText(movie[0].strip())
        self.lineEdit_mauthor.setText(movie[3].strip())
        actor = movie[5]
        if actor == None:
            actor = "无主演信息"
        else:
            actor = movie[5].strip()
        self.lineEdit_mactor.setText(actor)
        self.lineEdit_myear.setText(movie[9].strip())
        self.lineEdit_mtype.setText(movie[6].strip())
        self.lineEdit_mstar.setText(movie[12])
        self.lineEdit_mcountry.setText(movie[7])
        self.lineEdit_mlanguage.setText(movie[8])
        self.lineEdit_url.setText('http://movie.douban.com/subject/' + movie[0])
        self.TexEdit_mintro.setText(movie[14])
        self.TexEdit_mcomment.setHtml(movie[16])
    # 加入影集
    def slot_join_movieshelf(self):
        movie = {}
        movie[0] = str(self.lineEdit_mname.text())
        movie[1] = str(self.lineEdit_mno.text())
        movie[2] = str(self.lineEdit_mtype.text())
        movie[3] = str(self.lineEdit_mstar.text())

        dbManager = DbManager()
        insertsql="INSERT INTO `user_data`(`movie_name`, `movie_no`, `movie_kind`, `movie_star`)" \
                  " VALUES ('{0}', '{1}', '{2}', '{3}')"
        try:
            insert = insertsql.format( movie[0],
                                       movie[1],
                                       movie[2],
                                       movie[3]
                                       )
            dbManager.execNonQuery(insert)  # 非查询语句用execNonQuery()实现
            print("加入影集成功")
        except Exception as e:
            print(e)
        self._display_movieshelf()   # 显示在影集中
       # self._recommend_good_books()  # 重新计算推荐电影
    # 从影集删除
    def slot_delete_from_movieshelf(self):
        dbManager = DbManager()
        movie_name = str(self.lineEdit_mname.text())
        delsql = "DELETE  FROM `user_data` WHERE `movie_name`='"+movie_name+"'"
        try:
            dbManager.execNonQuery(delsql)
            print("电影："+movie_name+"已从影集删除")
        except Exception as e:
            print(e)
        self._display_movieshelf()
        #self._recommend_good_books()
    # 刷新影集中的电影
    def _display_movieshelf(self):
        try:
            dbManager = DbManager()
            selectsql = "select * from `user_data`"
            doc = dbManager.execQuery(selectsql)
            #print(doc)
            # 显示书架上的书
            self.movieshelf.clearContents()
            #self.bookshelf.setRowCount(0)
            row = 0
            for i in range(0, len(doc)):
                print(doc[i])
                self.movieshelf.insertRow(row)
                self.movieshelf.setItem(row, 0, QTableWidgetItem(doc[i][0]))
                self.movieshelf.setItem(row, 1, QTableWidgetItem(doc[i][2]))
                self.movieshelf.setItem(row, 2, QTableWidgetItem(doc[i][3]))
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
    # def _crawler_window(self):
    #     try:

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
        self.setWindowIcon(QIcon('D:/workplace/pythonwork/douban_book_catch_zzq/spic/cat.png'))
        self.movie_no = QLabel(u'电影编号：')
        self.mnoEdit = QLineEdit()
        self.addTableButton = QPushButton(u'加入数据库')
        self.renewTableButton = QPushButton(u'更新数据库')
        self.outputButton = QPushButton(u'导出xls文件')
        self.spideButton = QPushButton(u'开始爬取')

        icon = QPixmap('')
        iconLabel = QLabel()
        iconLabel.setPixmap(icon)

        layout = QGridLayout(self)
        layout.addWidget(self.movie_no, 0, 0)
        layout.addWidget(self.mnoEdit, 0, 1, 1, 3)
        layout.addWidget(iconLabel, 1, 0, 2, 1)
        layout.addWidget(self.addTableButton, 1, 1)
        layout.addWidget(self.renewTableButton, 1, 2)
        layout.addWidget(self.outputButton, 1, 3)
        layout.addWidget(self.spideButton, 2, 1, 1, 3)

    def _init_slot(self):
        self.addTableButton.clicked.connect(self._addTable)
        self.renewTableButton.clicked.connect(self._renewTable)
        self.spideButton.clicked.connect(self._spide)
        self.outputButton.clicked.connect(self._output_xls)
    # 数据抓取到本地excel之后，将数据新加入到数据库中
    def _addTable(self,):
        try:
            dbmanager = ConnectCrawler()
            excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\newmovie.xls'
            newmovieWb = xlrd.open_workbook(excelpath)  # 获取需要插入数据的excel
            table = newmovieWb.sheet_by_name(u"sheet1")  # 获取sheet1
            success = 0
            already = 0
            for i in range(1, table.nrows):
                movie = table.row_values(i)
                print(movie)
                movie_no = movie[0]
                select = "SELECT * FROM `movies_moviedetail` where `movie_no`='" + movie_no + "'"
                searchsql = dbmanager.CrawlerexecQuery(select)
                if searchsql:
                    already += 1
                    continue
                else:
                    try:
                        is_exist = "select * from `movies_movie` where `movie_no`='" + movie_no + "'"  # 判断是否已经存在
                        is_exist_1 = dbmanager.CrawlerexecQuery(is_exist)
                        if not is_exist_1:
                            addsql2 = "INSERT INTO `movies_movie`(`movie_name`, `movie_no`, `movie_info`, `movie_url`, `stars`,`click_nums`,`fav_nums`,`image`,`add_time`,`movie_year_id`,`is_banner`)" \
                                      " VALUES ('{0}', '{1}', '{2}','{3}','{4}',{5},{6},'{7}','{8}',{9},{10})"
                            insert2 = addsql2.format(movie[1], movie[0], movie[2], "https://movie.douban.com/subject/" + movie[0] + "/",
                                                     movie[12], 0, 0, "movie_detail/2017/05/14/" + movie[0] + ".jpg", '2017-05-14', 1, 0)
                            dbmanager.CrawlerexecNonQuery(insert2)
                    except Exception as e:
                        print(e)
                        # 下载图片到media文件夹
                    try:
                        detail_is_exist = "select * from `movies_moviedetail` where `movie_no`='" + movie_no + "'"
                        detail_is_exist_1 = dbmanager.CrawlerexecQuery(detail_is_exist)
                        if not detail_is_exist_1:
                            addsql = "INSERT INTO `movies_moviedetail` (`movie_no`, `movie_name`, `movie_year`, `movie_director`, `movie_pl`, `movie_actor`, `movie_type`, `country`, `language`, `movie_ReleaseDate`, `runtime`, `votenum`,`stars`, `movie_intro`, `recommendations`, `comments`,`click_nums`,`fav_nums`,`add_time`)" \
                                     " VALUES ('{0}', '{1}', '{2}','{3}','{4}','{5}','{6}','{7}','{8}','{9}','{10}',{11},'{12}','{13}','{14}','{15}',{16},{17},'{18}')"
                            insert = addsql.format(movie[0], movie[1], movie[2], movie[3], movie[4], movie[5], movie[6], movie[7], movie[8],
                                                   movie[9], movie[10], movie[11], movie[12], movie[14], movie[15], movie[16], 0, 0, '2017-05-14')
                            dbmanager.CrawlerexecNonQuery(insert)
                    except Exception as e:
                        print(e)
                    try:
                        path = "https://movie.douban.com/subject/" + movie[0] + "/"
                        tag = getHtml(path).encode('utf-8')
                        soup = BeautifulSoup(tag, 'html.parser')
                        movie_mes = soup.select("div.article div#mainpic")
                        subsoup = BeautifulSoup(str(movie_mes), 'html.parser')
                        pic_url = subsoup.a.img['src']  # 图片链接
                        print(pic_url)
                        savepath = 'D:/workplace/pythonwork/Crawler/media/movie_detail/2017/05/14'
                        work_path = os.path.join(savepath + '/', movie[0] + '.jpg')
                        urllib.request.urlretrieve(pic_url, '%s' % str(work_path))
                        print("下载图片成功")
                    except Exception as e:
                        print(e)
                    success += 1
            if success or already:
                QMessageBox.information(self, u"提示", u"成功加入电影"+str(success)+"部。有"+str(already)+"部已经存在。")
                return
        except Exception as e:
            print(e)
    # 数据抓取到本地excel之后，将数据更新到数据库中
    def _renewTable(self):
        try:
            dbmanager = ConnectCrawler()
            excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\newmovie.xls'
            newmovieWb = xlrd.open_workbook(excelpath)  # 获取需要插入数据的excel
            table = newmovieWb.sheet_by_name(u"sheet1")  # 获取sheet1
            success = 0
            fail = 0
            for i in range(1, table.nrows):
                movie = table.row_values(i)
                print(movie)
                movie_no = movie[0]
                try:
                    update1 = "UPDATE `movies_movie` SET stars = '{stars}' where `movie_no`='" + movie_no + "'"
                    update_sql1 = update1.format(stars=movie[12])
                    updatesql1 = dbmanager.CrawlerexecNonQuery(update_sql1)
                except Exception as e:
                    print(e)
                    pass
                try:
                    update2 = "UPDATE `movies_moviedetail` SET stars = '{stars}' where `movie_no`='" + movie_no + "'"
                    update_sql2 = update2.format(stars=movie[12])
                    updatesql2 = dbmanager.CrawlerexecNonQuery(update_sql2)
                except Exception as e:
                    print(e)
                    pass
                if updatesql1 and updatesql2:
                      success += 1
                else:
                    fail += 1
            if success or fail:
                QMessageBox.information(self, u"提示", u"成功更新"+ str(success) + "部电影。有" + str(fail) + "部更新失败。")
                return


        except:
            print("出错了")

    def _output_xls(self):
        QMessageBox.information(self, u"通知", u"导出xls文件完成！")
        return

    def _spide(self):
        try:
            dbmanager = ConnectCrawler()
            movieno = self.mnoEdit.text()
            if not movieno:
                QMessageBox.information(self, u"提示", u"让我爬谁呀大哥，给个编号")
                return
            print(movieno)
            select = "SELECT * FROM `movies_moviedetail` where `movie_no`='" + movieno + "'"
            searchsql = dbmanager.CrawlerexecQuery(select)
            # 电影已经在数据库中
            if searchsql:
                QMessageBox.information(self, u"提示", u"该电影记录已经存在。")
                return
            # 电影记录不存在，则重新抓取
            else:
                url = 'http://movie.douban.com/subject/'+movieno
                excelpath = 'D:\workplace\pythonwork\douban_book_catch_zzq\movie_select_dic\\newmovie.xls'  # 创建保存记录的excel
                if os.path.exists(excelpath):
                    path = 'D:/workplace/pythonwork/douban_book_catch_zzq/movie_select_dic/newmovies/'+movieno+'.html'
                    if not os.path.exists(path):
                        tag = getHtml(url).encode('utf-8')
                        file = open(path, 'wb')
                        file.write(tag)
                    content = open(path, 'rb').read()
                    movie = makeMovieInfo(content)
                    print(movie)
                    try:
                        oldWb = xlrd.open_workbook(excelpath, formatting_info=True)  # 获取需要插入数据的excel
                        this_sheet = oldWb.sheet_by_name(u"sheet1")  # 获取sheet1
                        row = this_sheet.nrows
                        newWb = copy(oldWb)  # 拷贝原始文件
                        sheet = newWb.get_sheet(0)  # 原始文件中存在sheetname=0的文件
                        for i in range(0, len(movie)):
                            sheet.write(row, i, movie[i])  # row行，col列，data追加的数据，style数据样式
                        print("=====写完啦=======")
                        newWb.save(excelpath)
                        QMessageBox.information(self, u"提示", u"数据添加成功。")
                        return
                    except Exception as e:
                        print(e)
                else:
                    newmovies = ['电影编号', '电影名', '公布时间', '导演', '编剧', '主演', '类型', '国家/地区', '语言',
                                 '上映时间', '时长', '评价人数', '电影星级', '评价人数比例', '剧情介绍', '相关推荐', '短评']
                    try:
                        file = xlwt.Workbook()  # 创建工作簿
                        sheet1 = file.add_sheet(u'sheet1', cell_overwrite_ok=True)  # 创建sheet
                        for i in range(0, len(newmovies)):
                            sheet1.write(0, i, newmovies[i])
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
        self.find_result_table.itemClicked['QTableWidgetItem*'].connect(self.slot_click_search_table)
        self.addb_pushB.clicked.connect(self.slot_join_movieshelf)
        self.delb_pushB.clicked.connect(self.slot_delete_from_movieshelf)
        self.movieshelf.itemClicked['QTableWidgetItem*'].connect(self.slot_click_movieshelf_table)
        self.recomm_table.itemClicked['QTableWidgetItem*'].connect(self.slot_click_recommend_table)
        self.crawlButton.clicked.connect(self.spiderGui.show)
        spider._display_movieshelf(self)  # 打开界面时初始化我的影集


class splashscreen(QSplashScreen):
    def __init__(self):
        super(QSplashScreen, self).__init__(QPixmap('D:/workplace/pythonwork/douban_book_catch_zzq/spic/movie.png'))
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
    #app.aboutToQuit.connect(app.deleteLater)
    splash = splashscreen()
    splash.effect()
    gui = MyWindow()
    splash.finish(gui)  # 关闭启动图片

    app.exec_()



