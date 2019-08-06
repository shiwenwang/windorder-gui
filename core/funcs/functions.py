# -*- coding: utf-8 -*-
"""
Main run

@author: 36719
"""

from functools import partial
from collections import OrderedDict
from ..models import WindParse
from ..models import CalcRatedWindSpeed
from ..models import CalcLoad
from ..models import TiInterp
from ..models import TowerDataBase
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os
import re

THIS_DIR = os.path.dirname(__file__)
REF_WIND = dict()

def find_available_tower(wind_path, turbine_type, db_data={}, sorted_by_weight=True, loads = {}):
    global REF_WIND
    if loads:
        loads = loads
    else:
        loads = calc_loads(wind_path, turbine_type, db_data, turbine_or_wind='turbine')
    sorted_loads_ul = loads['ul'].sort_values(ascending=False)
    sorted_loads_fl = loads['fl'].sort_values(ascending=False)

    available_tower_fl = OrderedDict()
    for label in sorted_loads_fl.index:
        if label not in REF_WIND.keys():
            break
        else:
            available_tower_fl[label] = REF_WIND[label]['tower_weight']

    available_tower_ul = OrderedDict()
    for label in sorted_loads_ul.index:
        if label not in REF_WIND.keys():
            sit_max_lable = label            
            break
        else:
            highly_recommended = True if label in available_tower_fl else False
            available_tower_ul[label] = {'weight': REF_WIND[label]['tower_weight'],
                                         'highly_recommended': highly_recommended,
                                         'load_attr': sorted_loads_fl[label]}
#    if not available_tower_ul:
#        index = sorted_loads_ul.index
#        try:
#            max_lbl = [index[i] for i, d in enumerate(sorted_loads_ul.values) if abs(d-1.0)<1e-4 and index[i] in REF_WIND.keys()][0]
#            available_tower_ul[max_lbl] = REF_WIND[max_lbl]['tower_weight']
#        except IndexError:
#            pass
    
    # # 查找遗漏的参考塔架
    # try:
    #     reset_tower = [lbl for lbl in sorted_loads_ul.index if lbl in REF_WIND.keys() 
    #                and abs(sorted_loads_ul[lbl] - sorted_loads_ul[sit_max_lable]) < 0.0008][0]
    #     available_tower_ul[reset_tower] = REF_WIND[reset_tower]['tower_weight']
    # except IndexError:
    #     pass
           
    available_tower = available_tower_ul
    if sorted_by_weight:
        available_tower = sorted(available_tower.items(), key=lambda x:x[1])
        # available_tower = {kv[0]: kv[1] for kv in available_tower_list}
    
    return available_tower

def main_run(wind_path, ref_wind):
    """
    wind-order startup function
    :param enter_dir: the dir of file calling this function
    :param wind_path: farm wind parameter path
    :param ref_path: reference wind parameter path
    :param regress_ul_folder: dir of ultimate load regressor
    :param regress_fl_folder: dir of fatigue load regressor
    :return:
    """

    custom_wind_name = os.path.splitext(os.path.split(wind_path)[-1])[0]

    loads = calc_loads(wind_path, ref_wind)
    ultimate_load = loads['ul']
    fatigue_load = loads['fl']

    global THIS_DIR, REF_WIND
    color_path = os.path.abspath(os.path.join(THIS_DIR, '../../files/color/color.json'))

    with open(color_path, 'r') as f:
        colors = json.load(f)
    color_list = list(colors.values())

    # plt.close()
    # fig = plt.figure(figsize=(9, 5))
    bar_plot = partial(draw, ref_wind=REF_WIND, wind_name=custom_wind_name, color_list=color_list)
    # bar_plot(fig, ultimate_load, 211)
    # bar_plot(fig, fatigue_load, 212)
    # plt.tight_layout()
    # fig.suptitle(custom_wind_name, y=1, fontsize=14, weight='bold')
    # plt.show()
    return bar_plot, loads

    return 



def calc_loads(wind_path, ref_turbine_or_wind, 
               db_data={}, turbine_or_wind='wind', save_loads=False):
    """
    Calculate loads(U,F) according to wind resource parameter and regressor
    
    db_data = {} 时，重新在路径下读取json
    db_data有数据时，这里不需要读json

    ref_turbine_or_wind： 可以是机组信息的字典， 也可以是根据塔架确定的风参信息
    
    """
    global THIS_DIR, REF_WIND

    if turbine_or_wind == 'turbine':
        db_folder = os.path.abspath(os.path.join(THIS_DIR, '../../files/Tower_Database/'))
        json_files = os.listdir(db_folder)
        db = TowerDataBase(db_data)
        if db_data:
            db.update(mode='a')
        else:
            for f in json_files:
                full_path = os.path.join(db_folder, f)
                db.update(full_path, mode='a')

        result = db.filter(**ref_turbine_or_wind)
        REF_WIND = db.get_wind_info(result)
    else:
        REF_WIND = ref_turbine_or_wind
    
    """ wind_parse model """
    wind = WindParse(path=wind_path)
    wind.run()
    wind_outputs = wind.pop()

    # from time import time
    # start = time()
    wind_cluster = {'farm': wind_outputs}
    tower_loads_json_file = os.path.abspath(os.path.join(THIS_DIR, '../../files/Loads/tower_loads.json'))
    if not os.path.isfile(tower_loads_json_file):
        with open(tower_loads_json_file, 'w') as f:
            json.dump({'ul': {}, 'fl': {}}, f)
    with open(tower_loads_json_file, 'r') as f:
        data = json.load(f)

    saved_tower = []
    for tower_id, wind in REF_WIND.items():
        if tower_id in data['ul'].keys():
            saved_tower.append(tower_id)
        else:
            wind_cluster.update({tower_id: wind})        

    ''' turbulence intensity interpolation '''    
    ti_interp = TiInterp(**wind_cluster)
    ti_interp.run()

    ''' calculate load '''
    cl_inputs = OrderedDict(wind=wind_cluster, ti=ti_interp.pop())
    cl = CalcLoad(**cl_inputs)
    cl.run()
    loads = cl.pop()
    ultimate_load = loads['ul']
    fatigue_load = loads['fl']

    # 追加已经存档的载荷
    saved_loads_ul = {k: v for k, v in data['ul'].items() if k in saved_tower}
    saved_loads_fl = {k: v for k, v in data['fl'].items() if k in saved_tower}
    ultimate_load = ultimate_load.append(pd.Series(saved_loads_ul))
    fatigue_load = fatigue_load.append(pd.Series(saved_loads_fl))

    merged_loads = {}
    merged_loads['ul'] = ultimate_load / max(ultimate_load)
    merged_loads['fl'] = fatigue_load / max(fatigue_load)
    # end = time()
    # print(end-start)

    if save_loads:
        save_path = os.path.abspath(os.path.join(THIS_DIR, '../../files/Loads/loads.xlsx'))
        with pd.ExcelWriter(save_path) as writer:
            ultimate_load.to_excel(writer, sheet_name='Ultimate Load')
            fatigue_load.to_excel(writer, sheet_name='Fatigue Load')
    
    return merged_loads


def draw(fig, load, sub, ref_wind, wind_name, color_list):
    """
    plot bar
    :param fig:
    :param load:
    :param sub:
    :param ref_load_path:
    :param custom_wind_name:
    :return:
    """
    fig.add_subplot(sub)

    # # raw_labels = list(load.index)
    # ref_labels = list(ref_wind.keys())

    load_sorted = load.sort_values(ascending=False)

    x_label, values, color_show, legend_handles = bar_config(load_sorted, ref_wind, wind_name, color_list)

    if len(x_label) < 10:
        plt.bar(x_label, values, color=color_show, width=0.3)
    else:
        plt.bar(x_label, values, color=color_show)

    y_label = {211: 'Ultimate_load', 212: 'Fatigue_load'}
    plt.ylabel(y_label[sub])

    y_ticks_min = max(round(min(values), 2) - 0.2, 0)
    y_ticks_max = 1.5
    plt.ylim(y_ticks_min, y_ticks_max)
    plt.yticks(np.arange(y_ticks_min, y_ticks_max, 0.2), fontsize=8)

    plt.legend(handles=legend_handles, ncol=6, fontsize='xx-small') #len(ref_labels) + 1
    # mode="expand"（平铺， 默认向右靠拢）  loc='upper right' (默认),

    if len(x_label) > 5:
        plt.xticks(rotation=45, horizontalalignment='right', size=6)
    for a, b in zip(x_label, values):
        plt.text(a, b + 0.005, '%.3f' % b, ha='center', va='bottom', fontsize=6)


def bar_config(load_sorted, ref_Wind, wind_name, color_list):
    """
    set bar plot attributes(color, label, legend)
    :param load_sorted:
    :param custom_wind_name:
    :param raw_labels:
    :param ref_labels:
    :return:
    """
    values = load_sorted.values
    ref_labels = list(ref_Wind.keys())

    sorted_labels = list(load_sorted.index)
    show_labels = [ref_Wind[lbl]['label'][0] if lbl in ref_labels else lbl for lbl in sorted_labels]

    color_show = []

    for lbl in sorted_labels:
        if lbl in ref_labels:
            color_show.append(color_list[ref_labels.index(lbl)]) 
        else:
            color_show.append('b')

    handles = list()
    handles.append(mpatches.Patch(color='b', label=wind_name))

    for lbl in ref_labels:
        handles.append(mpatches.Patch(color=color_show[sorted_labels.index(lbl)], label=lbl))

    return show_labels, values, color_show, handles


def json_parse(ref_loads_path):
    """
    count reference labels
    :param ref_loads_path:
    :return:
    """
    ref_labels = {}
    if len(ref_loads_path) > 0:
        for path in ref_loads_path:
            with open(path, 'r') as f:
                loads = json.load(f)
                filename = os.path.splitext(os.path.split(path)[-1])[0][:-6]
                ref_labels[filename] = list(loads['ul'].keys())

    return ref_labels


# -- discarded --
# def get_same_string(s_list):
#     set_s = get_sub_string(s_list[0])
#     for s in s_list[1:]:
#         set_s = set_s.intersection(get_sub_string(s))
#
#     strlen_list = [len(s) for s in list(set_s)]
#
#     return list(set_s)[strlen_list.index(max(strlen_list))]
#
#
# def get_sub_string(s):
#     len_s = len(s)
#     list_s = set()
#
#     for i in range(0, len_s):
#         for j in range(i + 1, len_s):
#             two_s = s[i:j]
#             list_s.add(two_s)
#
#     return list_s
