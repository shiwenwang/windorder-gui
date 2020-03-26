import os
import sys


THIS_DIR = os.path.dirname(__file__)
sys.path.append(os.path.abspath(os.path.join(THIS_DIR, '..')))

from wind_order.func_run import main_run
from wind_order.models import TowerDataBase

# REF_STD_FOLDER = os.path.abspath(os.path.join(THIS_DIR, "../enter/参考设计风参/标准设计风参/"))
# REF_CUS_FOLDER = os.path.abspath(os.path.join(THIS_DIR, "../enter/参考设计风参/定制化塔架设计风参/"))
CUS_FOLDER = os.path.abspath(os.path.join(THIS_DIR, "../enter/项目场址风参/"))

wind_path = os.path.join(CUS_FOLDER,'华能通榆团结140-2.5-140m_341.5t.xlsx')
# ref_std_wind_path = [os.path.join(REF_STD_FOLDER, d) for d in os.listdir(REF_STD_FOLDER) if d.endswith('xlsx') or d.endswith('xls')]
# ref_cus_wind_path = [os.path.join(REF_CUS_FOLDER, d) for d in os.listdir(REF_CUS_FOLDER) if d.endswith('xlsx') or d.endswith('xls')]
# ref_wind_path = []
# ref_wind_path.extend(ref_cus_wind_path)
# ref_wind_path.extend(ref_std_wind_path)


db = TowerDataBase()
db.update('E:\\WorkSpace\\6_PythonScripts\\wind_order\\wind_order-jupyter\\files\\Tower_Database\\twoX_tower_database5_2S.json')
type = {'选用机型': '140-2.5', '塔架高度': '140', '匹配叶片': '', '开发类型': ''}
# type = {'选用机型': '130_2500', '塔架高度': '', '匹配叶片': '', '开发类型': ''}
result = db.filter(**type)

# select = {'60.00.00297-P1': result['60.00.00297-P1']}

ref_wind = db.get_wind_info(result)

main_run(THIS_DIR, wind_path, ref_wind)
