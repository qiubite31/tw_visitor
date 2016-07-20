# coding=UTF-8
import sqlite3


class SqliteDBObject:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cursor = self.conn.cursor()

    def non_select_query(self, sql):
        self.cursor.execute(sql)
        self.conn.commit()

    def select_query(self, sql):
        return self.cursor.execute(sql)

    def db_close(self):
        self.conn.close()

