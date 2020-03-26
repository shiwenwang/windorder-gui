# -*- coding: utf-8 -*-
"""
prepare regressor data

@author: 36719
"""
import pandas as pd
import os
import re
import time


def timer(func):
    def wrapper(*args, **kwargs):
        begin_time = time.perf_counter()
        value = func(*args, **kwargs)
        end_time = time.perf_counter()
        run_time = end_time - begin_time
        print(f'{func.__name__} 耗时：{run_time} s')
        return value
    return wrapper

def excel2csv(exl_dir, csv_dir, pattern):
    if not os.path.isdir(csv_dir):
        os.makedirs(csv_dir)
    for file in os.listdir(exl_dir):
        if pattern.match(file):
            exl_path = os.path.join(exl_dir, file)
            df = pd.read_excel(exl_path, index_col=0, header=None)
            df.drop([df.index[0], df.index[2]], inplace=True)
            df.columns = df.loc[df.index[0]]
            df.drop(df.index[0], inplace=True)
            df.index = __repl_zh(df.index)

            csv_path = os.path.join(csv_dir, file.replace('.xls', '.csv'))
            df.to_csv(csv_path)

@timer
def get_regressor(folder, pattern, load_name):
    """
    Regressor read and regularization
    :param df:
    :return:
    """
    regressor = {}
    for file in os.listdir(folder):
        if pattern.match(file):
            path = os.path.join(folder, file)
            df = pd.read_excel(path, index_col=0, header=None)
            df.drop([df.index[0], df.index[2]], inplace=True)
            df.columns = df.loc[df.index[0]]
            df.drop(df.index[0], inplace=True)
            df.index = __repl_zh(df.index)
            regressor[os.path.splitext(file)[0]]= df[load_name]  # pd.Series

    return regressor

@timer
def get_regressor2(folder, pattern, load_name):
    """
    Regressor read and regularization
    :param df:
    :return:
    """
    regressor = {}
    for file in os.listdir(folder):
        if pattern.match(file):
            path = os.path.join(folder, file)
            df_index = pd.read_csv(path, index_col=0, usecols=[0])
            df = pd.read_csv(path, header=0, usecols=[load_name])
            df.index = df_index.index
            regressor[os.path.splitext(file)[0]] = df[load_name]  # pd.Series

    return regressor

def __repl_zh(list_zh):
    """
    --- Convert chinese character to alphanumeric character ---
    :param list_zh:
    :return list_en:
    """

    look_up = {'常量': 'const', '最大入流角β': 'inflow_angle', '平均入流角β': 'inflow_angle',
                '风切变α': 'wind_shear', '空气密度ρ': 'air_density', '极限风速V50': 'V50'}
    list_en = [look_up[zh] for zh in list_zh if zh in look_up.keys()]
    if list_zh[-1] not in look_up.keys():
        list_en.append(list_zh[-1])

    return list_en

if __name__ == "__main__":
    this_dir = os.path.dirname(__file__)

    ul_dir = os.path.abspath(os.path.join(this_dir, '../../res/files/Regress_UL_01-39'))
    fl_dir = os.path.abspath(os.path.join(this_dir, '../../res/files/Regress_FL_001-123'))

    ul_dir_csv = os.path.abspath(os.path.join(this_dir, '../../res/files/Regress_UL'))
    fl_dir_csv = os.path.abspath(os.path.join(this_dir, '../../res/files/Regress_FL'))

    u_pattern = re.compile(r'Regress_UL_.')
    f_pattern = re.compile(r'Regress_RF_Case\d+\.')

    # excel2csv(ul_dir, ul_dir_csv, u_pattern)
    # excel2csv(fl_dir, fl_dir_csv, f_pattern)

    ul_reg1 = get_regressor(ul_dir, u_pattern, 'UL_TB_Mxy')
    fl_reg1 = get_regressor(fl_dir, f_pattern, 'RF_TB_My_m4')

    ul_reg2 = get_regressor2(ul_dir_csv, u_pattern, 'UL_TB_Mxy')
    fl_reg2 = get_regressor2(fl_dir_csv, f_pattern, 'RF_TB_My_m4')

    print(type(ul_reg1['Regress_UL_01_DLC13_ETM3']), ul_reg1['Regress_UL_01_DLC13_ETM3'])
    print(type(ul_reg2['Regress_UL_01_DLC13_ETM3']), ul_reg2['Regress_UL_01_DLC13_ETM3'])
