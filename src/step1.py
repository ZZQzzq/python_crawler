# -*- coding:utf-8 -*-
# 创建相关的数据库

import tool.DbManager

# 已经在里面进行初始连接了
dbManager = tool.DbManager.DbManager()
# 创建数据库，原来不用加的。
dbManager.execNonQuery(r"create database dou_ban_book;")
# 使用新创建的数据库
dbManager.execNonQuery(r"use dou_ban_book;")
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


# 构建了表book_tail(书详细介绍)
dbManager.execNonQuery(r"""
CREATE TABLE book_detail (
  id int(11) NOT NULL AUTO_INCREMENT,
  book_no varchar(45) NOT NULL COMMENT '书编号',
  book_name varchar(100) NOT NULL COMMENT '书名',
  book_author varchar(100) DEFAULT  NULL COMMENT '作者',
  book_public varchar(100) DEFAULT  NULL COMMENT '出版社',
  book_trans  varchar(100) DEFAULT  NULL COMMENT '译者',
  book_year varchar(20) DEFAULT  NULL COMMENT '出版年',
  book_page int(11) DEFAULT  NULL COMMENT '页数',
  book_price VARCHAR(10) DEFAULT NULL COMMENT '价格',
  votenum int(11) DEFAULT NULL COMMENT '评价人数',
  stars varchar(5) DEFAULT NULL COMMENT '星级情况',
  voteratio varchar(100) DEFAULT NULL COMMENT '评价比例',
  book_intro text COMMENT '书介绍',
  author_intro text COMMENT '作者介绍',
  book_others text COMMENT '其他信息',
  mu_lu mediumtext COMMENT '图书目录',
  recommendations varchar(250) DEFAULT NULL COMMENT '相关推荐',
  comments mediumtext COMMENT '评论',
  book_info text COMMENT '书出版信息',
  PRIMARY KEY (id),
  UNIQUE KEY book_no_UNIQUE (book_no)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='图书详情表';
""")


dbManager.execNonQuery(r"""
CREATE TABLE user_data (
  id int(11) NOT NULL AUTO_INCREMENT,
  book_no varchar(45) DEFAULT NULL COMMENT '书编号',
  book_name varchar(100) DEFAULT NULL COMMENT '书名',
  book_author varchar(100) DEFAULT  NULL COMMENT '作者',
  book_tag varchar(45) DEFAULT NULL COMMENT '书标签',
  book_kind varchar(45) DEFAULT NULL COMMENT '书分类',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户记录';
""")



