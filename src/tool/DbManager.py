# -*- coding:utf-8 -*-

import pymysql.cursors  # 引入数据库的模块

config = {'host': 'localhost',  # 数据库所在的主机地址，默认localhost
          'user': 'root',  # 用户
          'password': '123456789',  # 密码
          'port': 3306,  # 默认即为3306
          'database': 'dou_ban_book',  # 数据库名称
          'charset': 'utf8'  # 默认即为utf8
          }


class DbManager:
    """
    对pymysql.Connector()的简单封装,实现基本的连接
    """

    def __init__(self):
        self.__initConnect()

    def __initConnect(self):
        """
        得到连接信息
        返回: conn.cursor()
        """
        self.conn = pymysql.Connect(**config)  # 链接，通过这个来操作链接
        self.cur = self.conn.cursor()  # 游标，通过这个访问数据库
        if not self.cur:
            raise (NameError, "连接数据库失败")

    def execQuery(self, sql):
        """
            执行查询语句
            返回的是一个包含tuple（元组）的list（列表），list的元素是记录行，tuple的元素是每行记录的字段
            调用示例：
            resList = dbManager.execQuery("SELECT id,NickName FROM WeiBoUser")
            for (id,NickName) in resList:
                print(str(id),NickName)
        """
        self.cur.execute(sql)
        # print("查询语句："+sql)
        resList = self.cur.fetchall()  # fetchall():接收全部的返回结果行.
        return resList

    def execNonQuery(self, sql):
        """
        执行非查询语句
        调用示例：
            cur = self.__GetConnect()
            cur.execute(sql)
            self.conn.commit()
            self.conn.close()
        """
        try:
            self.cur.execute(sql)
            self.conn.commit()
            print('执行语句成功')
        except Exception:  # 出现异常回滚
            print('执行SQL语句失败：' + sql)
            self.conn.rollback()
            raise   # 使用raise引发异常。一旦出现异常，后续语句不再执行。

    def __del__(self):
        self.cur.close()  # 测试语句


def test_insert():
    dbManager = DbManager()
    dbManager.ExecNonQuery("insert into `book_detail` (book_name) values ('你哈') ")


# 测试语句
def test_select():
    dbManager = DbManager()
    print(dbManager.execQuery('SELECT * FROM t_test_paper limit 10'))


# 测试语句
if __name__ == '__main__':
    # test_insert()
    test_select()
