# coding=UTF-8
import sys
import os
import re
import sqlite3
from xlrd import open_workbook
# from xlrd.sheet import ctype_text
import pandas as pd
from db_object import SqliteDBObject


def insert_record(date, area, reason, value):
    sql = "INSERT INTO tw_visitor VALUES ('{0}', '{1}', '{2}', {3})"
    sql = sql.format(date, area, reason, value)
    db_obj.non_select_query(sql)

db_obj = SqliteDBObject('tw_visitor.db')

# Open tw visitor xls report
xls_path = 'visitor_data/201603.xls'
wb = open_workbook(xls_path, formatting_info=True)
sheet = wb.sheet_by_name('Sheet3')

# Fetch xls report month
report_title = sheet.cell_value(0, 0)
m = re.search(r'(\d{3})年(\d{1,2})月', report_title)
year = int(m.group(1)) + 1911
month = int(m.group(2))
report_month = str(year) + '-' + (str(month) if month-10 >= 0 else '0' + str(month))

# Check whether this month data exist in table or not
sql = 'SELECT DISTINCT REPORT_MONTH FROM TW_VISITOR'
exist_month = [month[0] for month in db_obj.select_query(sql)]
if report_month in exist_month:
    print('This month had already extracted!')
    # db_obj.db_close()
    # sys.exit()

# Read Column Title
visitor_reason = []
for i in range(0, sheet.ncols):
    cell_value = sheet.cell(1, i).value
    # Resident and Total column not extract
    if not (cell_value == '' or 'Residence' in cell_value or
            'Total' in cell_value):
        visitor_reason.append(cell_value.replace('\n', ' '))

visitor_area = []
for i in range(0, sheet.nrows):
    cell_value = sheet.cell(i, 1).value
    # Total row not extract
    if 'Total' in cell_value or 'Total' in sheet.cell_value(i, 2):
        continue
    # Merge Cell should shift column
    if '東南亞地區' in cell_value or cell_value == '':
        cell_value_shift = sheet.cell_value(i, 2)
        if not cell_value_shift == '':
            visitor_area.append(cell_value_shift)
    else:
        visitor_area.append(cell_value)

data_list = []
for i in range(0, 14):  # sheet.ncols有時會到14有時讀到15
    data = []
    for j in range(0, sheet.nrows-1):
        if sheet.cell(j, i).ctype == 2:  # ctype = 2 is number
            # not extract total cell value
            if not('Total' in sheet.cell_value(j, 2) or
                   'Total' in sheet.cell_value(j, 1) or
                   'Total' in sheet.cell_value(1, i)):
                data.append(sheet.cell(j, i).value)
        # add a data row into data list
        if j == sheet.nrows - 2 and len(data) > 0:
            data_list.append(data)

visitor_df = pd.DataFrame(data_list, visitor_reason, visitor_area,)

"""
# create table
sql = '''CREATE TABLE tw_visitor
             (report_month text, area text, reason text, value real)'''
db_obj.non_select_query(sql)
"""

rows = visitor_df.iterrows()
for row in rows:
    for idx in range(0, row[1].size):
        date = report_month
        area = row[1].index[idx]
        reason = row[0]
        value = row[1][idx]
        insert_record(date, area, reason, value)

print('Finish insert ' + date + ' visitor data!')
"""
sql = 'SELECT COUNT(*) FROM TW_VISITOR'
for row in db_obj.select_query(sql):
    print(row)
"""
db_obj.db_close()
