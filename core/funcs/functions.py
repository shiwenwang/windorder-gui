# -*- coding: utf-8 -*-
"""
Main run

@author: 36719
"""

from functools import partial
from collections import OrderedDict
from ..models import WindParse
from ..models import CalcLoad
from ..models import TiInterp
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import json
import os


THIS_DIR = os.path.dirname(__file__)

def find_available_tower(wind_path, ref_wind, sorted_by_weight=True, loads = {}):
    if loads:
        loads = loads
    else:
        loads = calc_loads(wind_path, ref_wind)
    sorted_loads_ul = loads['ul'].sort_values(ascending=False)
    sorted_loads_fl = loads['fl'].sort_values(ascending=False)

    global THIS_DIR
    config_path = os.path.abspath(os.path.join(THIS_DIR, '../../config/config.json'))

    with open('./config/config.json', 'r', encoding='utf-8') as f:
        config = json.load(f)
        threshold = config['threshold']

    # 疲劳推荐
    fl_index_site = [lbl for lbl in sorted_loads_fl.index if lbl not in ref_wind.keys()]
    fl_index_tower = [lbl for lbl in sorted_loads_fl.index if lbl in ref_wind.keys()]

    site_max_fl = sorted_loads_fl.at[fl_index_site[0]]
    tower_limit = {lbl: ref_wind[lbl]['tower_limit'] if ref_wind[lbl]['tower_limit'] else '-'
                   for lbl in ref_wind.keys()}
    tower_ma = {lbl: ref_wind[lbl]['tower_ma'] if ref_wind[lbl]['tower_ma'] else '-'
                for lbl in ref_wind.keys()}
    tower_buckling = {lbl: ref_wind[lbl]['tower_buckling'] if ref_wind[lbl]['tower_buckling'] else '-'
                for lbl in ref_wind.keys()}
    tower_fatigue = {lbl: ref_wind[lbl]['tower_fatigue'] if ref_wind[lbl]['tower_fatigue'] else '-'
                for lbl in ref_wind.keys()}
    accessories_fatigue = {lbl: ref_wind[lbl]['accessories_fatigue'] if ref_wind[lbl]['accessories_fatigue'] else '-'
                for lbl in ref_wind.keys()}    
    tower_sec = {lbl: ref_wind[lbl]['tower_sec'] if ref_wind[lbl]['tower_sec'] else '-'
                for lbl in ref_wind.keys()}  
    base_type = {lbl: ref_wind[lbl]['base_type'] if ref_wind[lbl]['base_type'] else '-'
                for lbl in ref_wind.keys()}                                          
    available_tower_fl = {tower_id: 
                         {'weight': ref_wind[tower_id]['tower_weight'],
                          'tower_limit': tower_limit[tower_id],
                          'wind_limit': 'F',
                          'fl_prop': str(round(sorted_loads_fl.at[tower_id] / np.max(sorted_loads_fl.values), 3)),
                          'ul_prop': '-',
                          'tower_ma': tower_ma[tower_id],
                          'tower_buckling': tower_buckling[tower_id],
                          'tower_fatigue': tower_fatigue[tower_id],
                          'accessories_fatigue': accessories_fatigue[tower_id],
                          'tower_sec': tower_sec[tower_id],
                          'base_type': base_type[tower_id]
                          }
                          for tower_id in fl_index_tower
                          if sorted_loads_fl.at[tower_id] > float(threshold['fl']) * site_max_fl}

    # 极限推荐
    ul_index_site = [lbl for lbl in sorted_loads_ul.index if lbl not in ref_wind.keys()]
    ul_index_tower = [lbl for lbl in sorted_loads_ul.index if lbl in ref_wind.keys()]

    site_max_ul = sorted_loads_ul.at[ul_index_site[0]]
    
    tag = {label: 'A' if label in available_tower_fl.keys() else 'U' for label in ul_index_tower}
    fl_prop = {label: available_tower_fl[label]['fl_prop'] if label in available_tower_fl.keys()
                else '-' for label in ul_index_tower}
    tower_limit = {lbl: ref_wind[lbl]['tower_limit'] if ref_wind[lbl]['tower_limit'] else '-'
                   for lbl in ref_wind.keys()}
    tower_ma = {lbl: ref_wind[lbl]['tower_ma'] if ref_wind[lbl]['tower_ma'] else '-'
                for lbl in ref_wind.keys()}
    tower_buckling = {lbl: ref_wind[lbl]['tower_buckling'] if ref_wind[lbl]['tower_buckling'] else '-'
                for lbl in ref_wind.keys()}
    tower_fatigue = {lbl: ref_wind[lbl]['tower_fatigue'] if ref_wind[lbl]['tower_fatigue'] else '-'
                for lbl in ref_wind.keys()}
    accessories_fatigue = {lbl: ref_wind[lbl]['accessories_fatigue'] if ref_wind[lbl]['accessories_fatigue'] else '-'
                for lbl in ref_wind.keys()} 
    tower_sec = {lbl: ref_wind[lbl]['tower_sec'] if ref_wind[lbl]['tower_sec'] else '-'
                for lbl in ref_wind.keys()}  
    base_type = {lbl: ref_wind[lbl]['base_type'] if ref_wind[lbl]['base_type'] else '-'
                for lbl in ref_wind.keys()}   
    available_tower_ul = {tower_id: 
                         {'weight': ref_wind[tower_id]['tower_weight'],
                          'tower_limit': tower_limit[tower_id],
                          'wind_limit': tag[tower_id],
                          'ul_prop': str(round(sorted_loads_ul.at[tower_id] / np.max(sorted_loads_ul.values), 3)),
                          'fl_prop': fl_prop[tower_id],
                          'tower_ma': tower_ma[tower_id],
                          'tower_buckling': tower_buckling[tower_id],
                          'tower_fatigue': tower_fatigue[tower_id],
                          'accessories_fatigue': accessories_fatigue[tower_id],
                          'tower_sec': tower_sec[tower_id],
                          'base_type': base_type[tower_id]
                         }
                          for tower_id in ul_index_tower
                          if sorted_loads_ul.at[tower_id] > float(threshold['ul']) * site_max_ul}
    # 合并
    available_tower = available_tower_ul
    available_tower.update({k: v for k, v in available_tower_fl.items() if k not in available_tower_ul.keys()})
    if sorted_by_weight:
        available_tower = sorted(available_tower.items(), key=lambda x:x[1]['weight'])
    
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

    global THIS_DIR
    color_path = os.path.abspath(os.path.join(THIS_DIR, '../../files/color/color.json'))

    with open(color_path, 'r') as f:
        colors = json.load(f)
    color_list = list(colors.values())

    bar_plot = partial(draw, ref_wind=ref_wind, wind_name=custom_wind_name, color_list=color_list)

    return {'bar_plot': bar_plot, 'loads': loads}

def calc_loads(wind_path, ref_wind):
    """
    Calculate loads(U,F) according to wind resource parameter and regressor
    
    db_data = {} 时，重新在路径下读取json
    db_data有数据时，这里不需要读json
    
    """
    # from time import time
    # start = time()
    """ wind_parse model """
    wind = WindParse(path=wind_path)
    wind.run()
    wind_outputs = wind.pop()
    # end = time()
    # print(f"读取风参文件耗时：{end - start}s")

    wind_cluster = {'farm': wind_outputs}
    # tower_loads_mysql.json 用于存放计算过的塔架的载荷值
    tower_loads_json_file = os.path.abspath(os.path.join(THIS_DIR, '../../files/Loads/tower_loads_mysql.json'))
    if not os.path.isfile(tower_loads_json_file):
        with open(tower_loads_json_file, 'w') as f:
            json.dump({'ul': {}, 'fl': {}}, f)
    with open(tower_loads_json_file, 'r') as f:
        data = json.load(f)

    saved_tower = []
    for tower_id, wind in ref_wind.items():
        if tower_id in data['ul'].keys():
            saved_tower.append(tower_id)
        else:
            wind_cluster.update({tower_id: wind})

    # from time import time
    # start = time()
    ''' turbulence intensity interpolation '''    
    ti_interp = TiInterp(**wind_cluster)
    ti_interp.run()
    # end = time()
    # print(f"湍流插值耗时：{end - start}s")

    # start = time()
    ''' calculate load '''
    cl_inputs = OrderedDict(wind=wind_cluster, ti=ti_interp.pop())
    cl = CalcLoad(**cl_inputs)
    cl.run()
    loads = cl.pop()
    ultimate_load = loads['ul']
    fatigue_load = loads['fl']
    # end = time()
    # print(f"计算载荷耗时：{end - start}s")

    # 追加已经存档的载荷
    saved_loads_ul = {k: v for k, v in data['ul'].items() if k in saved_tower}
    saved_loads_fl = {k: v for k, v in data['fl'].items() if k in saved_tower}
    ultimate_load = ultimate_load.append(pd.Series(saved_loads_ul))
    fatigue_load = fatigue_load.append(pd.Series(saved_loads_fl))
    # print(ultimate_load)
    # print(fatigue_load)

    merged_loads = {'ul': ultimate_load, 'fl': fatigue_load}

    # 将新计算的塔架载荷存档, 覆盖旧值
    new_items_generated = False
    for label in ultimate_load.index:
        if label in ref_wind.keys():
            if not new_items_generated:
                new_items_generated = True
            data['ul'][label] = ultimate_load.at[label]
            data['fl'][label] = fatigue_load.at[label]

    if new_items_generated:
        with open(tower_loads_json_file, 'w') as f:
            json.dump(data, f)

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
    fake_values = values / np.max(values)

    if len(x_label) < 5:
        plt.bar(x_label, fake_values, color=color_show, width=0.3)
    else:
        plt.bar(x_label, fake_values, color=color_show)

    y_label = {211: 'Ultimate_load', 212: 'Fatigue_load'}
    plt.ylabel(y_label[sub])

    y_ticks_min = max(round(min(fake_values), 2) - 0.2, 0)
    y_ticks_max = 1.5
    plt.ylim(y_ticks_min, y_ticks_max)
    plt.yticks(np.arange(y_ticks_min, y_ticks_max, 0.2), fontsize=8)

    plt.legend(handles=legend_handles, ncol=6, fontsize='xx-small') #len(ref_labels) + 1
    # mode="expand"（平铺， 默认向右靠拢）  loc='upper right' (默认),

    if len(x_label) > 10:
        plt.xticks(rotation=45, horizontalalignment='right', size=6)
    if len(x_label) < 40:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.005, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6)
    elif len(x_label) < 60:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.005, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6, rotation=30, horizontalalignment='center')
    else:
        for a, b in zip(x_label, fake_values):
            plt.text(a, b + 0.01, '%.3f' % b, ha='center', va='bottom',
                     fontsize=6, rotation=90, horizontalalignment='center')

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
