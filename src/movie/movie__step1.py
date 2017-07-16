# -*- coding:utf-8 -*-
# 创建相关的数据库

import src.movie.tools.Db_manager
# 已经在里面进行初始连接了
from src.movie.tools import Db_manager
"""
刚开始老师出错，显示dbmanager has no attribute cur。
后来发现是因为数据库在连接的时候必须是已经存在的，进入数据库后才能新建schema
所以把数据库连接的database改成dou_ban_book以后果然成功

"""
dbManager = Db_manager.DbManager()
# 创建数据库，原来不用加的。
dbManager.execNonQuery(r"create database dou_ban_movie;")
# 使用新创建的数据库
dbManager.execNonQuery(r"use dou_ban_movie;")
# 构建了表movie
dbManager.execNonQuery(r"""
CREATE TABLE movie (
  id int(11) NOT NULL AUTO_INCREMENT COMMENT '自增ID',
  movie_no varchar(100) NOT NULL COMMENT '电影编号',
  movie_name varchar(100) NOT NULL COMMENT '电影名称',
  movie_url varchar(150) NOT NULL COMMENT '电影链接',
  movie_img varchar(150) DEFAULT NULL COMMENT '电影图片',
  movie_info varchar(500) DEFAULT NULL COMMENT '电影阵容',
  movie_star varchar(45) DEFAULT NULL COMMENT '星级评价',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影表';
""")

# 构建了表movie_tag（电影标签）
dbManager.execNonQuery(r"""
CREATE TABLE movie_tag (
  id int(11) NOT NULL AUTO_INCREMENT,
  movie_name varchar(100) DEFAULT NULL COMMENT '电影名',
  movie_no varchar(100) NOT NULL COMMENT '电影编号',
  movie_kind varchar(10) DEFAULT NULL COMMENT '电影类型',
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='电影标签';
""")

# 构建了表movie_detail(电影详细介绍)
dbManager.execNonQuery(r"""
CREATE TABLE movie_detail (
  id int(11) NOT NULL AUTO_INCREMENT,
  movie_no varchar(20) NOT NULL COMMENT '电影编号',
  movie_name varchar(100) NOT NULL COMMENT '电影名',
  movie_year varchar(10) NOT NULL COMMENT '公布时间',
  movie_director varchar(100) DEFAULT NULL COMMENT '导演',
  movie_pl varchar(100) DEFAULT NULL COMMENT '编剧',
  movie_actor varchar(500) DEFAULT NULL COMMENT '演员列表',
  movie_type  varchar(100) DEFAULT NULL COMMENT '类型',
  country  varchar(100) DEFAULT NULL COMMENT '国家/地区',
  language varchar(20) DEFAULT NULL COMMENT '语言',
  movie_ReleaseDate varchar(20) DEFAULT NULL COMMENT '上映时间',
  runtime varchar(10) DEFAULT NULL COMMENT '时长（分钟）',
  votenum int(11) DEFAULT NULL COMMENT '评价人数',
  stars varchar(8) DEFAULT NULL COMMENT '电影星级',
  voteratio  varchar(100) DEFAULT NULL COMMENT '评论人数比例',
  movie_intro mediumtext COMMENT '剧情介绍',
  recommendations mediumtext COMMENT '相关推荐',
  comments mediumtext COMMENT '短评',
  PRIMARY KEY (id),
  UNIQUE KEY movie_no_UNIQUE (movie_no)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='电影详情表';
""")


dbManager.execNonQuery(r"""
CREATE TABLE user_data (
  movie_name varchar(100) DEFAULT NULL COMMENT '电影名',
  movie_no varchar(100) NOT NULL COMMENT '电影编号',
  movie_kind varchar(10) DEFAULT NULL COMMENT '电影类型',
  movie_star varchar(45) DEFAULT NULL COMMENT '星级评价',
  PRIMARY KEY (movie_no)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='用户记录';
""")











