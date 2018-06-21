"""
@Project   : text-classification-cnn-rnn
@Module    : python_mysql.py
@Author    : Deco [deco@cubee.com]
@Created   : 6/21/18 3:22 PM
@Desc      : https://zhuanlan.zhihu.com/p/31456064
如下几个三方库可以连接mysql：

PyMySQL：可以兼容py3.6，据说使用python编写的库，速度较慢
MySQLdb：不能兼容py3
pyodbc：通过ODBC连接到mysql，算是一种曲线救国的方式
最终决定试一下PyMySQL，写了一段脚本如下，成功连接了mysql数据库，并打印了数据库的所有表名。
"""
import pymysql


class mysql_db(object):
    def __init__(self, db_info):
        self.host, self.user, self.password = db_info.split()
        self.connection = None

    """
    build datebase connection
    """

    def connect(self):
        self.connection = pymysql.connect(self.host, self.user, self.password)

    """
    get all the table names
    """

    def get_table_names(self):
        # build datebase connection
        self.connect()

        # select all the table names
        sql = "select table_name from information_schema.tables"
        curs = self.connection.cursor()
        curs.execute(sql)
        table_names = set(x[0] for x in curs.fetchall())

        # close cursor and database connection
        curs.close()
        self.connection.close()

        return table_names


# test
db_info = "xxx.xx.xx.xx user password"
test = mysql_db(db_info)
test.connect()
print(test.get_table_names())
