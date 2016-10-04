# coding=UTF-8
import sqlite3
import re


class SqliteDBObject:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def non_select_query(self, sql, bind_var=None, print_sql=False):
        if print_sql:
            self.print_sql_str(sql, bind_var)
        try:
            self.cursor.execute(sql, bind_var)
        except ValueError as err:
            self.cursor.execute(sql)

        self.conn.commit()

    def select_query(self, sql, bind_var=None, print_sql=False):
        if print_sql:
            self.print_sql_str(sql, bind_var)
        try:
            self.cursor.execute(sql, bind_var)
        except ValueError as err:
            self.cursor.execute(sql)

    def print_sql_str(self, sql, bind_var):

        try:
            bind_var = map(lambda var: "'" + var + "'" if isinstance(var, str)
                           else var, bind_var)
            sql_str = re.sub('\?|:\d{1,2}', '{}', sql)
            sql_str = sql_str.format(*bind_var)
        except TypeError as err:
            sql_str = sql

        print(sql_str)

    def db_close(self):
        self.conn.close()
