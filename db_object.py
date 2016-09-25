# coding=UTF-8
import sqlite3


class SqliteDBObject:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def non_select_query(self, sql, bind_var=None, print_sql=False):
        if print_sql:
            self.print_sql_str(sql, bind_var)

        if bind_var is None:
            self.cursor.execute(sql)
        else:
            self.cursor.execute(sql, bind_var)

        self.conn.commit()

    def select_query(self, sql, bind_var=None, print_sql=False):
        if print_sql:
            self.print_sql_str(sql, bind_var)

        if bind_var is None:
            return self.cursor.execute(sql)
        else:
            return self.cursor.execute(sql, bind_var)

    def print_sql_str(self, sql, bind_var):
        if bind_var is None:
            sql_str = sql
        else:
            bind_var = map(lambda var: "'" + var + "'" if isinstance(var, str)
                           else var, bind_var)
            sql_str = sql.replace('?', '{}').format(*bind_var)

        print(sql_str)

    def db_close(self):
        self.conn.close()
