# coding=UTF-8
import sys
import os
import re
import pdb
import sqlite3
from xlrd import open_workbook
# from xlrd.sheet import ctype_text
import pandas as pd
from db_object import SqliteDBObject


def insert_record(year, month, continent, area_cht, area_eng,
                  purpose_cht, purpose_eng, value):
    sql = (
        "INSERT INTO VISITORS_ARRIVALRECORD(REPORT_YEAR, REPORT_MONTH, CONTINENT, AREA_CHT,"
        "            AREA_ENG, PURPOSE_CHT, PURPOSE_ENG, VISITOR_NUM)"
        "VALUES ({year}, {month}, '{continent}', '{area_cht}', '{area_eng}', '{purpose_cht}', '{purpose_eng}', {value})"
        )
    sql = sql.format(**locals())
    db_obj.non_select_query(sql)

db_obj = SqliteDBObject('tw_visitor.db')

# Open tw visitor xls report
xls_path = 'visitor_data/201412.xls'
wb = open_workbook(xls_path, formatting_info=True)
sheet = wb.sheet_by_name('Sheet3')

# Fetch xls report month
report_title = sheet.cell_value(0, 0)
m = re.search(r'(\d{3})年(\d{1,2})月', report_title)
year = int(m.group(1)) + 1911
month = int(m.group(2))
report_month = (
    str(year) + '-' + (str(month) if month-10 >= 0 else '0' + str(month))
    )

# Delete the report_month record before insert data
sql = (
    "DELETE FROM VISITORS_ARRIVALRECORD"
    " WHERE REPORT_YEAR = ?"
    "   AND REPORT_MONTH = ?"
    )
db_obj.non_select_query(sql, (year, month,), print_sql=False)
# pdb.set_trace()

# Read Column Title
visitor_reason = []
for i in range(0, sheet.ncols):
    cell_value = sheet.cell(1, i).value
    # Resident and Total column not extract
    if not (cell_value == '' or 'Residence' in cell_value or
            'Total' in cell_value):
        visitor_reason.append(cell_value.replace('\n', ' '))

visitor_area = []
continent_mapping = {}
continent = 'Default'
for i in range(2, sheet.nrows):  # 跳過標題列，從第2列開始
    cell_value = sheet.cell(i, 1).value

    if not sheet.cell(i, 0).value == '':  # 判斷非空字串來改換成新的洲
        continent = sheet.cell(i, 0).value

    # 不擷取Total加總
    if 'Total' in cell_value or 'Total' in sheet.cell_value(i, 2):
        continue
    # 東南亞地區有合併欄續，需shift欄位判斷
    if '東南亞地區' in cell_value or cell_value == '':
        cell_value_shift = sheet.cell_value(i, 2)
        if not cell_value_shift == '':
            visitor_area.append(cell_value_shift)
            continent_mapping[cell_value_shift] = continent
    else:
        visitor_area.append(cell_value)
        continent_mapping[cell_value] = continent

data_list = []
for i in range(0, 14):  # sheet.ncols有時會到14有時讀到15
    data = []
    for j in range(0, sheet.nrows-1):
        if sheet.cell(j, i).ctype == 2:  # ctype = 2 is number
            # 不擷取Total加總
            if not('Total' in sheet.cell_value(j, 2) or
                   'Total' in sheet.cell_value(j, 1) or
                   'Total' in sheet.cell_value(1, i)):
                data.append(sheet.cell(j, i).value)
        # 整個row資料讀完，加入list
        if j == sheet.nrows - 2 and len(data) > 0:
            data_list.append(data)

visitor_df = pd.DataFrame(data_list, visitor_reason, visitor_area,)

rows = visitor_df.iterrows()
for row in rows:
    for idx in range(0, row[1].size):
        area = row[1].index[idx]
        continent = continent_mapping[area]
        area_cht = area[0:area.index(' ')]
        area_eng = area[area.index(' ')+1:]
        purpose_cht = row[0][0:row[0].index(' ')]
        purpose_eng = row[0][row[0].index(' ')+1:]
        value = row[1][idx]
        insert_record(year, month, continent, area_cht, area_eng, purpose_cht, purpose_eng, value)

print('Finish insert ' + report_month + ' visitor data!')
db_obj.db_close()

"""
def main():
    pass

if(__name__ == 'main'):
    main()
"""
