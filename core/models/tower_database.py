import json
import pandas as pd
from math import gamma, exp, log
import os
import warnings


class TowerDataBase(object):
    def __init__(self, db_data={}):
        self.database = dict()
        self.raw_data = db_data

    def update(self, json_file='', mode='a', set_lower_value=lambda x: x.lower() if isinstance(x, str) else x):
        """
        mode: 覆盖或追加数据
        json_file：用于从json文件中更新数据
        """
        assert mode in ['w', 'a']

        if json_file:
            try:
                with open(json_file, 'r', encoding='utf-8') as f:
                    json_data = json.load(f)
            except FileNotFoundError as e:
                raise(e)

            new_database = {}
            for tower_id, prj in json_data.items():
                for name, details in prj.items():
                    if len(prj.keys()) > 1:
                        k = f'{tower_id}-P{list(prj.keys()).index(name) + 1}'
                    else:
                        k = tower_id
                    
                    lower_details = {k.lower(): set_lower_value(v) for k, v in details.items()}
                    new_database.update({k.lower(): lower_details})
        else:
            new_database = {}
            for tower_id, prj in self.raw_data.items():
                for name, details in prj.items():
                    if len(prj.keys()) > 1:
                        k = f'{tower_id}-P{list(prj.keys()).index(name) + 1}'
                    else:
                        k = tower_id
                    
                    lower_details = {k.lower(): set_lower_value(v) for k, v in details.items()}
                    new_database.update({k.lower(): lower_details})
                
        if mode == 'w':
            self.database = new_database
        else:
            self.database.update(new_database)

    def filter(self, **kwargs):
        filter_args = {k.lower(): v.lower() for k, v in kwargs.items() if v != ''}
        selected = {}
        if not filter_args:
            return selected
        for tower_id, data in self.database.items():
            filter_map = {k.lower(): str(v).lower() for k, v in data.items() if k in filter_args.keys()}
            if filter_args == filter_map:
                selected[tower_id] = data
            else:
                continue

        if not selected:
            print('Warning: No eligible data was found.')

        return selected

    @staticmethod
    def get_basic_info(database):
        turbine_type = set()
        blade_type = set()
        dev_type = set()
        hub_height = set()

        for data in database.values():
            turbine_type.add(str(data['机型']).lower().strip() if data['机型'] == data['机型'] else 'NAN')
            if '' in turbine_type:
                turbine_type.remove('')
            if '匹配叶片' in data.keys():
                blade_type.add(str(data['匹配叶片']).lower().strip() if data['匹配叶片'] == data['匹配叶片'] else 'NAN')
            if '' in blade_type:
                blade_type.remove('')
            dev_type.add(str(data['开发类型']).lower().strip() if data['开发类型'] == data['开发类型'] else 'NAN')
            if '' in dev_type:
                dev_type.remove('')
            hub_height.add(str(data['塔架高度']).lower().strip() if data['塔架高度'] == data['塔架高度'] else 'NAN')
            if '' in hub_height:
                hub_height.remove('')

        return {'turbine_type': turbine_type, 'blade_type': blade_type, 
                'dev_type': dev_type, 'hub_height': hub_height}
    
    def get_wind_info(self, filtered, pick_value=lambda x: x if isinstance(x, float) else x[0]):
        wind = dict()
        filtered_args = {k.lower(): v for k, v in filtered.items() if v != ''}

        for tower_id, data in filtered_args.items():
            if not data['a'] and not data['k']:
                data['k'].append(2)
                data['a'].append(data['vave'][0] / exp(log(gamma(1 + 1 / data['k'][0]))))

            lookup = {"ρ": [1.225], "vave": [6], "α": [0.2], "θmean": [0], "v50": [30]}
            for key in data.keys():
                if key in lookup.keys() and not data[key]:
                    data[key] = lookup[key]
            
            weight = str(data['塔架重量(t)']) if data['塔架重量(t)'] else 0
            
            condition_data = {k: pick_value(v) for k, v in data.items()
                              if k in ["ρ", "vave", "a", "k", "α", "θmean", "v50"]}            
            condition = pd.DataFrame(condition_data, index=[tower_id,])
            
            ti_m1 = pd.DataFrame({'Wind Speed': data['wind speed'], 
                                    tower_id: self.alignment(data['wind speed'], data, 'm=1')})
            ti_m10 = pd.DataFrame({'Wind Speed': data['wind speed'],
                                    tower_id: self.alignment(data['wind speed'], data, 'm=10')})
            ti_etm = pd.DataFrame({'Wind Speed': data['wind speed'], 
                                    tower_id: self.alignment(data['wind speed'], data, 'etm')})

            wind_params = {'condition': condition, 'm1': ti_m1, 
                           'm10': ti_m10, 'etm': ti_etm, 'tower_weight': float(weight),
                           'label': [f'{tower_id[6:]}-{weight}t']}
            wind[tower_id] = wind_params
        
        return wind

    @staticmethod
    def alignment(windspeed, data, ti_item):
        ti = data[ti_item]
        if len(ti) > len(windspeed):
            ti = ti[:len(windspeed)]
        elif len(ti) < len(windspeed):
            if not ti:
                print(f"[INFO]: {data['塔架编号']}, {ti_item} 数据为空。")
                ti = [0]*len(windspeed)
            end = ti[-1]
            ti.extend([end]*(len(windspeed) - len(ti)))
        else:
            pass

        return ti


if __name__ == "__main__":
    db = TowerDataBase()
    db.update('E:\\WorkSpace\\6_PythonScripts\\wind_order\\wind_order-jupyter\\files\\Tower_Database\\twoX_tower_database5_2S.json')
    # type = {'塔架高度': '90', '匹配叶片': 'SW59.5D', '开发类型': '定制化', }
    type = {'机型': '140-2.5', '塔架高度': '140', '匹配叶片': 'SINOMA68.8B', '开发类型': ''}
    result = db.filter(**type)
    # basic_info = db.get_basic_info(result)
    wind = db.get_wind_info(result)
    pass
    print(list(result.keys()))
