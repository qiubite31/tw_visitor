# coding=UTF-8
import sqlite3


class SqliteDBObject:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def non_select_query(self, sql, bind_var=None, print_sql=False):
        if bind_var is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, bind_var)
        self.conn.commit()

        if print_sql:
            print(sql.replace('?', '{}').format(*bind_var))

    def select_query(self, sql):
        return self.cursor.execute(sql)

    def db_close(self):
        self.conn.close()
