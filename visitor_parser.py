# coding=UTF-8
import os
import sqlite3
from xlrd import open_workbook
# from xlrd.sheet import ctype_text
import pandas as pd
# import db_connect

# print(os.path.dirname(__file__))

# Open tw visitor xls report
xls_path = 'C:/Users/Dragon/tour_statistic/mysite/tours/vistor_history/1602.xls'
wb = open_workbook(xls_path, formatting_info=True)
sheet = wb.sheet_by_name('Sheet3')

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
for i in range(0, sheet.ncols-1):
    data = []
    for j in range(0, sheet.nrows-1):
        if sheet.cell(j, i).ctype == 2:  # ctype = 2 is number
            # not extract total cell value
            if not('Total' in sheet.cell_value(j, 2) or
                   'Total' in sheet.cell_value(j, 1)):
                data.append(sheet.cell(j, i).value)
        # add a data row into data list
        if j == sheet.nrows - 2 and len(data) > 0:
            data_list.append(data)

visitor_df = pd.DataFrame(data_list, visitor_reason, visitor_area,)
# print(visitor_df.head)

conn = sqlite3.connect('tw_visitor.db')
cursor = conn.cursor()


def insert_record(date, area, reason, value):
    sql = "INSERT INTO tw_visitor VALUES ('{0}', '{1}', '{2}', {3})"
    sql = sql.format(date, area, reason, value)
    cursor.execute(sql)
    conn.commit()

rows = visitor_df.iterrows()
for row in rows:
    for idx in range(0, row[1].size):
        date = '2016-02'
        area = row[0]
        reason = row[1].index[idx]
        value = row[1][idx]
        insert_record(date, area, reason, value)
        # print(row[1].index[idx])
        # print(row[1][idx])

sql = 'SELECT * FROM tw_visitor'
for row in cursor.execute(sql):
    print(row) 