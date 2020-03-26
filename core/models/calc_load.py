# -*- coding: utf-8 -*-
"""
Calculate ultimate Load

@author: 36719
"""

import os
import re
import math
import numpy as np
import pandas as pd
from . import Base
from functools import partial


class CalcLoad(Base):

    def run(self):
        """
        --- Import regressor for calculating ultimate load ---
        :param self.regressor_dir: folder of regress_ul excel
        :return ultimate Load - Mxy at Tower Bottom
        """
        wind_condition = self._inputs['wind']['farm']['condition']
        ti = self._inputs['ti']['ti']
        v_end = self._inputs['ti']['v_end']

        wind_condition = wind_condition[['ρ', 'vave', 'a', 'k', 'α', 'θmean', 'v50']]
        for k, wind in self._inputs['wind'].items():
            if k != 'farm':
                wind_condition = pd.concat([wind_condition, wind['condition']], sort=False)

        self.this_dir = os.path.dirname(__file__)

        regress_ul_dir = os.path.abspath(os.path.join(self.this_dir, '../../res/files/Regress_UL'))
        regress_fl_dir = os.path.abspath(os.path.join(self.this_dir, '../../res/files/Regress_FL'))
        u_pattern = re.compile(r'Regress_UL_.+\.csv')
        f_pattern = re.compile(r'Regress_RF_Case\d+\.csv')

        wind_condition_part = wind_condition[['θmean', 'α', 'ρ', 'v50']]
        wind_condition_part.columns = ['inflow_angle', 'wind_shear', 'air_density', 'V50']

        get_case_load = partial(self.__calc_case_load, wind_condition_part, ti)
        case_load_ul = get_case_load(regress_ul_dir, u_pattern, 'UL_TB_Mxy')
        case_load_fl = get_case_load(regress_fl_dir, f_pattern, 'RF_TB_My_m4')

        ultimate_load = self.calc_ultimate_load(case_load_ul)
        fatigue_load = self.calc_fatigue_load(case_load_fl, wind_condition, v_end)

        self._outputs = {'ul': ultimate_load, 'fl': fatigue_load}

    @staticmethod
    def calc_ultimate_load(case_load_ul):
        ultimate_load = case_load_ul.max(0)
        return ultimate_load

    def calc_fatigue_load(self, case_load_fl, wind_condition, v_end):
        case_proportion = self.__case_proportion(wind_condition, v_end)
        fatigue_load_values = np.power(np.sum(np.power(case_load_fl.values, 4)*case_proportion.values, axis=0), 1/4)

        fatigue_load = pd.Series(fatigue_load_values, index=case_load_fl.columns)
        return fatigue_load

    @staticmethod
    def __calc_case_load(wind_condition, ti, folder, pattern, load_name):
        """
        Regressor read and regularization
        :param df:
        :return:
            """
        regressor_data = {}
        multiplier_data = {}
        load_dict = {}
        index = ['const', 'inflow_angle', 'wind_shear', 'air_density', 'ti_data']
        last_index = {}
        # 回归因子
        for file in os.listdir(folder):
            if pattern.match(file):
                case_name = os.path.splitext(file)[0]
                path = os.path.join(folder, file)
                df_index = pd.read_csv(path, index_col=0, usecols=[0])
                last_index[case_name] = df_index.index[-1]
                df = pd.read_csv(path, header=0, usecols=[load_name])
                regressor_array = df[load_name].values
                if case_name in ['Regress_UL_11_DLC14_ALL', 'Regress_UL_22_DLC22_Short',
                                 'Regress_UL_27_DLC41_ALL_2_4',
                                 'Regress_RF_Case109', 'Regress_RF_Case110', 'Regress_RF_Case111']:
                    regressor_array = np.append(regressor_array, 0)
                elif case_name in ['Regress_UL_36_DLC61_ALL', 'Regress_UL_37_DLC62_ALL',
                                   'Regress_UL_38_DLC63_ALL', 'Regress_UL_39_DLC71_ALL']:
                    regressor_array = np.insert(regressor_array, 2, 0)
                else:
                    pass
                regressor_data[case_name] = regressor_array
        regressor = pd.DataFrame(regressor_data, index=index)
        # 乘数
        for turbine_id in wind_condition.index:
            for file in os.listdir(folder):
                if pattern.match(file):
                    case_name = os.path.splitext(file)[0]
                    if case_name in ['Regress_UL_36_DLC61_ALL', 'Regress_UL_37_DLC62_ALL',
                                     'Regress_UL_38_DLC63_ALL', 'Regress_UL_39_DLC71_ALL']:
                        # 此时，ti_data为V50
                        ti_data = wind_condition.at[turbine_id, 'V50']
                    elif case_name in ['Regress_UL_11_DLC14_ALL', 'Regress_UL_22_DLC22_Short',
                                       'Regress_UL_27_DLC41_ALL_2_4',
                                       'Regress_RF_Case109', 'Regress_RF_Case110', 'Regress_RF_Case111']:
                        # 此时，没有ti_data项， 为了数据对齐，赋值为0
                        ti_data = 0
                    else:
                        ti_data = ti[turbine_id].at[last_index[case_name]]
                    multiplier_data[case_name] = [1, wind_condition.at[turbine_id, 'inflow_angle'],
                                                  wind_condition.at[turbine_id, 'wind_shear'],
                                                  wind_condition.at[turbine_id, 'air_density'],
                                                  ti_data]
            multiplier_mat = np.array(list(multiplier_data.values()))

            # multiplier_mat和 regressor矩阵相乘之后的对角线元素即为各个工况的载荷
            load_arr = multiplier_mat.dot(regressor).diagonal()
            load_dict[turbine_id] = load_arr

        case_load = pd.DataFrame(load_dict, index=regressor.keys())

        return case_load

    @staticmethod
    def __cdf(x, alpha, beta):
        """
        Weibull Cumulative distribution function
        :param x:
        :param alpha:  shape parameter
        :param beta:  scale parameter
        :return cum_dist:
        """
        cum_dist = 1 - math.exp(-(x / beta) ** alpha)

        return cum_dist

    def __case_proportion(self, wind_condition, v_end):
        """
        calculate proportion of fatigue case
        :param wind_condition:
        :param v_end:
        :return: list of proportion
        """
        p_dict = {}
        turbine_list = list(wind_condition.index)

        wind_linspace = np.append(np.arange(3, 20, 2), 20)
        for turbine_id in turbine_list:
            alpha = wind_condition.loc[turbine_id, 'k']
            beta = wind_condition.loc[turbine_id, 'a']
            wind_end = v_end[turbine_id]

            p_list = []
            for d in wind_linspace[:8]:
                v = (self.__cdf(d + 1, alpha, beta) -
                     self.__cdf(d - 1, alpha, beta)) / 6 / \
                    self.__cdf(wind_end, alpha, beta)

                p_list.extend([v] * 6)

            v_19 = (self.__cdf(19.5, alpha, beta) -
                    self.__cdf(18, alpha, beta)) / 6 / \
                   self.__cdf(wind_end, alpha, beta)
            v_20 = (self.__cdf(21, alpha, beta) -
                    self.__cdf(19.5, alpha, beta)) / 6 / \
                   self.__cdf(wind_end, alpha, beta)
            p_list.extend([v_19] * 6 + [v_20] * 6)
            p_list.extend([9.50644441867142E-07] * 24)
            p_list.extend([1.90128888373428E-06] * 24)
            p_list.extend([0.001901289, 9.50644E-05, 9.50644E-05])
            v_lt2 = (self.__cdf(2, alpha, beta) -
                     self.__cdf(0, alpha, beta)) / 6 / \
                    self.__cdf(wind_end, alpha, beta)
            v_gt20 = (self.__cdf(wind_end, alpha, beta) -
                      self.__cdf(21, alpha, beta)) / 6 / \
                     self.__cdf(wind_end, alpha, beta)

            p_list.extend([v_lt2] * 6 + [v_gt20] * 6)

            p_dict[turbine_id] = np.array(p_list)

        case_proportion = pd.DataFrame(p_dict)

        return case_proportion
