from mysql import connector
from mysql.connector.errors import ProgrammingError, InterfaceError
from functools import partial
import pandas as pd
import numpy as np
from math import gamma, exp, log
import os
import json

THIS_DIR = os.path.dirname(__file__)

class MySQLDataBase(object):
    def __init__(self, **kwargs):
        if kwargs:
            self.set_config(kwargs)            
        else:
            config_path = os.path.abspath(os.path.join(THIS_DIR, '../../config/config.json'))
            with open(config_path, 'r', encoding='utf-8') as f:
                config_ = json.load(f)
            self.set_config(config_)
        self.db = connector.MySQLConnection()

    def set_config(self, kwargs):
        self.config = {'host': kwargs['主机:'],
                       'port': kwargs['端口:'],
                       'user': kwargs['用户:'],
                       'password': kwargs['密码:'],
                       'database': kwargs['数据库名称:']}
        if '表名称:' in kwargs.keys():
            self.table_name = kwargs['表名称:']
        else:
            self.table_name = None

    def connect(self):
        """
        连接数据库，并输出连接信息
        :return:
        """
        try:
            self.db = connector.MySQLConnection(**self.config)
            cursor = self.db.cursor()
            cursor.execute(f"SHOW TABLES")
            result = [r[0] for r in cursor.fetchall()]
            cursor.close()
            print(result)
            print(self.table_name)
            if result:
                if self.table_name is None or self.table_name not in result:
                    self.table_name = result[0]
            else:
                # self.table_name = 
                msg = f"{self.config['database']}数据库无数据表, 请重新配置"
                return False, msg

        except (ProgrammingError, InterfaceError) as e:
            msg = f'数据库连接失败({e.msg})'
            return False, msg
        
        return True, f"数据库连接至: {self.config['database']} - {self.table_name}"
        # if self.db.database:
        #     msg = '数据库已连接'
        # else:
        #     msg = '数据库地址已找到, 需指定数据库名称'
        # return False, msg

    def get_column_name(self):
        cursor = self.db.cursor()
        cursor.execute(f"show columns from {self.table_name}")
        result = cursor.fetchall()
        cursor.close()

        column_name = [n[0] for n in result if n[0]]
        return column_name

    def __query(self, mysql_select_sentence):
        """
        执行MySQL查询语句
        :param mysql_select_sentence:
        :return:
        """
        cursor = self.db.cursor()
        cursor.execute(mysql_select_sentence)
        result = cursor.fetchall()
        cursor.close()

        return result

    def __query_sentence(self, *item, **filter_):
        """
        mysql select sentence(syntax)
        :param item:
        :param filter:
        :return:
        """
        # name_map = {'turbine_type': '机组名称', 'blade_type': '叶片名称',
        #             'tower_type': '塔架类型', 'category': '归档分类',
        #             'tower_id': '塔架编号'}
        filter_phrase = []
        for k, v in filter_.items():
            filter_phrase.append(f"{k}='{str(v)}'")
        filter_sentence = ' and '.join(filter_phrase)

        if filter_:
            mysql_select_sentence = f"SELECT {', '.join(item)} from {self.table_name} where {filter_sentence}"
        else:
            mysql_select_sentence = f"SELECT {', '.join(item)} from {self.table_name}"

        return mysql_select_sentence

    def query(self, *item, **filter_):
        """
        根据filter统计item的值(不重复)
        :param item:
        :param filter_:
        :return:
        """
        column_name = self.get_column_name()
        valid_filter = {k: v for k, v in filter_.items() if v and k in column_name}
        valid_item = tuple([i for i in item if i in column_name])

        if len(valid_item) < 1:
            return []

        mysql_select_sentence = self.__query_sentence(*valid_item, **valid_filter)
        result = self.__query(mysql_select_sentence)

        if len(valid_item) < 2:
            filtered_item = list(set([str(r[0]) for r in result if r[0] or r[0] == 0]))
            return filtered_item

        return result

    def get_wind_info(self, tower_list):
        if not tower_list:
            return {}

        key_words = ', '.join(['塔架编号', '空气密度', '年平均风速', '入流角', '风剪切', 'V50', '威布尔分布A值',
                               '威布尔分布K值', '塔架主体重量', '风速带', 'm为1湍流带', 'm为10湍流带', 'm为ETM湍流带',
                               '受限情况', '塔筒屈曲标准'])
        if len(tower_list) > 1:
            mysql_sentence = f"SELECT {key_words} from {self.table_name} where 塔架编号 in {tuple(tower_list)}"
        else:
            mysql_sentence = f"SELECT {key_words} from {self.table_name} where 塔架编号 = '{tower_list[0]}'"
        query_result = self.__query(mysql_sentence)
        wind_params = self.__get_wind_info(query_result)

        return wind_params

    def __get_wind_info(self, query_result):
        wind_info = {}

        for item in query_result:
            tower_id, air_density, vave, inflow_angle, wind_shear, v50, weibull_a, weibull_k, tower_weight, \
            wind_speed, m1, m10, etm, tower_limit, std_spec = item
            air_density = float(air_density) if self.within(air_density, 0, 2) else 1.225
            vave = float(vave) if vave else 6.0
            inflow_angle = float(inflow_angle) if self.within(inflow_angle, -20, 20) else 0
            wind_shear = float(wind_shear) if self.within(wind_shear, -1, 1) else 0.2
            v50 = float(v50) if self.within(v50, vave, 100) else 37.5
            tower_weight = tower_weight if self.within(tower_weight, 0, 1000) else 0
            weibull_k = float(weibull_k) if self.within(weibull_k, 0, 10) else 2
            weibull_a = float(weibull_a) if self.within(weibull_a, 0, 20) else vave / exp(log(gamma(1 + 1 / weibull_k)))
            tower_limit = tower_limit if tower_limit else ''
            std_spec = std_spec if std_spec else ''

            # 过滤风速带和湍流带中的空数据和单个值
            wind_speed = [float(s) for s in wind_speed.split()] \
                if wind_speed and isinstance(wind_speed, str) else list(np.arange(2.5, 21.5, 1))
            m1 = [float(s) for s in m1.split()] if m1 and isinstance(m1, str) else [0] * len(wind_speed)
            m10 = [float(s) for s in m10.split()] if m10 and isinstance(m10, str) else [0] * len(wind_speed)
            etm = [float(s) for s in etm.split()] if etm and isinstance(etm, str) else [0] * len(wind_speed)

            # 数据对齐
            wind_speed, m1 = self.alignment(wind_speed, m1)
            wind_speed, m10 = self.alignment(wind_speed, m10)
            wind_speed, etm = self.alignment(wind_speed, etm)

            condition_data = {"ρ": air_density, "vave": vave, "a": weibull_a, "k": weibull_k,
                              "α": wind_shear, "θmean": inflow_angle, "v50": v50}

            condition = pd.DataFrame(condition_data, index=[tower_id, ])

            ti_m1 = pd.DataFrame({'Wind Speed': wind_speed, tower_id: m1})
            ti_m10 = pd.DataFrame({'Wind Speed': wind_speed, tower_id: m10})
            ti_etm = pd.DataFrame({'Wind Speed': wind_speed, tower_id: etm})

            tower_limit_map = {'极限受限': 'U', '疲劳受限': 'F', '疲劳受限和极限受限': 'A', '频率受限': 'T', '': ''}

            wind_params = {'condition': condition, 'm1': ti_m1,
                           'm10': ti_m10, 'etm': ti_etm, 'tower_weight': float(tower_weight),
                           'label': [f'{tower_id[6:]}-{tower_weight}t-{tower_limit_map[tower_limit]}'],
                           'tower_limit': tower_limit_map[tower_limit],
                           'std_spec': std_spec}

            wind_info[tower_id] = wind_params

        return wind_info

    @staticmethod
    def within(value, lower, upper):
        return True if value and lower < float(value) < upper else False

    @staticmethod
    def alignment(wind_speed, ti):
        
        # 将湍流为0的值用前一个数代替
        ti = [d if d else ti[i-1] for i, d in enumerate(ti)]
        offset = abs(len(wind_speed) - len(ti))

        if len(ti) > len(wind_speed):
            ti = ti[:-offset]
        else:
            ti.extend([ti[-1]] * offset)

        return wind_speed, ti


if __name__ == "__main__":
    config = {'数据库名称:': 'test', '表名称:': '定版塔架数据库_copy1', '主机:': 'localhost',
              '端口:': '3306', '用户:': 'root', '密码:': ''}
    db_mysql = MySQLDataBase(**config)
    print(db_mysql.connect())
    # print(db_mysql.get_column_name())
    filter = {'机组名称': 'GW140/3000', '叶片名称': 'GW68.6C(Sinoma68.6E)', '塔架类型': '', '归档分类': ''}
    # filter = {'塔架直径': 4300.0}
    # print(db_mysql.query('塔架编号'))
    tower_list = db_mysql.query('塔架编号')
    # print(db_mysql.get_wind_info(**{'塔架编号': '60.00.00951'}))
    # print(db_mysql.query('塔架直径'))
    from time import time
    start = time()
    cr = db_mysql.db.cursor(buffered=True)
    words = ', '.join(['空气密度', '年平均风速', '入流角', '风剪切', 'V50', '威布尔分布K值',
                       '威布尔分布K值', '风速带', 'm为1湍流带', 'm为10湍流带', 'm为ETM湍流带'])
    cr.execute(f"SELECT 塔架编号, m为ETM湍流带 FROM 定版塔架数据库_copy1 where 塔架编号 in {tuple(tower_list)}")
    # t = ('60.00.00880', '60.00.00909')
    # cr.execute(f"SELECT m为ETM湍流带 FROM 定版塔架数据库_copy1 where 塔架编号 in {t}")
    result = cr.fetchall()
    # for r in result:
    #     if not r[1]:
    #         print(r[0], type(r[1]))
    #     if not isinstance(r[1], str):
    #         print(r[0], type(r[1]))
    # for i in result:
    #     print([float(s) for s in i[0].split() if i[0]])
    w1 = db_mysql.get_wind_info(tower_list)
    end = time()
    print(end - start)

    # start = time()
    # # for t in tower_list:
    # #     cr = db_mysql.db.cursor()
    # #     cr.execute(f"SELECT 风速带 FROM 定版塔架数据库_copy1 where 塔架编号='{t}'")
    # #     result = cr.fetchall()
    # #     # print(result)
    # w2 = db_mysql.get_wind_info2(tower_list)
    # end = time()
    # print(end - start)
