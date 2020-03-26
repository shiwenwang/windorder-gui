# -*- coding: utf-8 -*-

import os
import sys

THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(THIS_DIR, '..')))

from core import find_available_tower, main_run
from core.models import MySQLDataBase

wind_path = os.path.abspath(os.path.join(THIS_DIR, '../files/wind/huaneng_140-2.5-140m_341.5t.xlsx'))
config = {'数据库名称:': 'test', '表名称:': '定版塔架数据库_copy1', '主机:': 'localhost',
              '端口:': '3306', '用户:': 'root', '密码:': ''}

db_mysql = MySQLDataBase(**config)
db_mysql.connect()

filter_inputs = {'机组名称': '', '叶片名称': '', '塔架类型': ''}
tower_list = db_mysql.query('塔架编号', filter_inputs)
ref_wind = db_mysql.get_wind_info(tower_list)
main_run(wind_path, ref_wind)
# result = find_available_tower(wind_path, ref_wind)
# print(result)
