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
import json


class CalcLoad(Base):

    def run(self):
        """
        --- Import regressor for calculating ultimate load ---
        :param self.regressor_dir: folder of regress_ul excel
        :return ultimate Load - Mxy at Tower Bottom
        """
        wind_condition = self._inputs['wind']['farm']['condition']
        ti = self._inputs['ti']['ti']

        self.this_dir = os.path.dirname(__file__)

        regress_ul_dir = os.path.abspath(os.path.join(self.this_dir, '../../files/Regress_UL'))
        regress_fl_dir = os.path.abspath(os.path.join(self.this_dir, '../../files/Regress_FL'))
        
        for k, wind in self._inputs['wind'].items():
            if k != 'farm':
                wind_condition = pd.concat([wind_condition, wind['condition']], sort=False)

        wind_condition_part = wind_condition[['θmean', 'α', 'ρ', 'v50']]
        wind_condition_part.columns = ['inflow_angle', 'wind_shear', 'air_density', 'V50']
        label = list(wind_condition.index)
        
        wind_cut_in = self._inputs['ti']['cut_in']
        wind_cut_out = self._inputs['ti']['cut_out']
        V50_alpha_beta = wind_condition[['v50', 'k', 'a']]

        u_pattern = re.compile(r'Regress_UL_.+\.csv')
        f_pattern = re.compile(r'Regress_RF_Case\d+\.csv')

        # get regress_ul
        regressor_ul = self.__get_regressor(regress_ul_dir, u_pattern, 'UL_TB_Mxy')

        # get Regress_RF
        regressor_fl = self.__get_regressor(regress_fl_dir, f_pattern, 'RF_TB_My_m4')

        # calculate ultimate load
        ultimate_load = self.__calc_load(regressor_ul, label, wind_condition_part, ti)
        ultimate_load_max = self.__get_ultimate_load_max(label, ultimate_load)

        # calculate fatigue load
        fatigue_load = self.__calc_load(regressor_fl, label, wind_condition_part, ti)
        p_case = self.__fatigue_case_proportion(label, wind_cut_in, wind_cut_out, V50_alpha_beta)
        fatigue_load_equivalence = \
            self.__get_fatigue_load_equivalence(label, fatigue_load, p_case) # dataframe

        self._outputs = {'ul': ultimate_load_max, 'fl': fatigue_load_equivalence}

    def __get_regressor(self, folder, pattern, load_name):
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

    @staticmethod
    def __calc_load(regressor, turbine_sites, wind_condition, ti):
        load = {}
        for turbine_id in turbine_sites:
            turbine_load = {}
            turbine_wind_condition = wind_condition.loc[turbine_id]
            turbine_ti = ti[turbine_id]
            for dlc, reg in regressor.items():
                observed_load = 0
                for var in reg.index:
                    if var in turbine_wind_condition.index:
                        observed_load += reg[var] * turbine_wind_condition[var]
                    elif var in turbine_ti.index:
                        observed_load += reg[var] * turbine_ti[var]
                    else:
                        observed_load += reg[var]
                turbine_load[dlc[11:]] = abs(observed_load)

            # sorted_load = sorted(turbine_load.items(), key=lambda x: x[1], reverse=True)
            # print(f'[{turbine_id}]: {sorted_load[0]}')

            load[turbine_id] = pd.Series(turbine_load)

        return load

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

    # @staticmethod
    def __get_ultimate_load_max(self, turbine_sites, ultimate_load):
        ultimate_load_max = {}
        for turbine_id in turbine_sites:
            ultimate_load_max[turbine_id] = np.max(ultimate_load[turbine_id].values)

        ser_ultimate_load_max = pd.Series(ultimate_load_max, name='UL1')
        self.save_loads(ser_ultimate_load_max, 'ul')

        # ser_ultimate_load_max = ser_ultimate_load_max / max(ser_ultimate_load_max)

        return ser_ultimate_load_max

    # @staticmethod
    def __get_fatigue_load_equivalence(self, turbine_sites, fatigue_load, p_case):
        fatigue_load_equivalence = {}
        for turbine_id in turbine_sites:
            fatigue_load_equivalence[turbine_id] = \
                np.power(np.power(fatigue_load[turbine_id].values, 4).dot(np.array(p_case[turbine_id])), 1/4)

        ser_fatigue_load_equivalence = pd.Series(fatigue_load_equivalence, name='FL1')
        self.save_loads(ser_fatigue_load_equivalence, 'fl')

        # ser_fatigue_load_equivalence = ser_fatigue_load_equivalence / max(ser_fatigue_load_equivalence)

        return ser_fatigue_load_equivalence

    def __fatigue_case_proportion(self, turbine_sites, cut_in, cut_out, V50_alpha_beta):
        """
        calculate proportion of fatigue case
        :param cut_in:
        :param cut_out:
        :param v50:
        :return: list of proportion
        """
        p_dict = {}
        V50 = V50_alpha_beta['v50']
        alpha = V50_alpha_beta['k']
        beta = V50_alpha_beta['a']

        wind_linspace = np.append(np.arange(3, 20, 2), 20)
        for turbine_id in turbine_sites:
            wind_end = (0.7 * V50[turbine_id] if 0.7 * V50[turbine_id] > cut_out + 1 else cut_out + 2)
            p_list = []
            for d in wind_linspace[:8]:
                    v = (self.__cdf(d + 1, alpha[turbine_id], beta[turbine_id]) -
                         self.__cdf(d - 1, alpha[turbine_id], beta[turbine_id])) / 6 / \
                         self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id])

                    p_list.extend([v]*6)

            v_19 = (self.__cdf(19.5, alpha[turbine_id], beta[turbine_id]) -
                    self.__cdf(18, alpha[turbine_id], beta[turbine_id])) / 6 / \
                    self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id])
            v_20 = (self.__cdf(21, alpha[turbine_id], beta[turbine_id]) -
                    self.__cdf(19.5, alpha[turbine_id], beta[turbine_id])) / 6 / \
                    self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id])
            p_list.extend([v_19] * 6 + [v_20] * 6)
            p_list.extend([9.50644441867142E-07] * 24)
            p_list.extend([1.90128888373428E-06] * 24)
            p_list.extend([0.001901289, 9.50644E-05, 9.50644E-05])
            v_lt2 = (self.__cdf(2, alpha[turbine_id], beta[turbine_id]) -
                    self.__cdf(0, alpha[turbine_id], beta[turbine_id])) / 6 / \
                   self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id])
            v_gt20 = (self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id]) -
                    self.__cdf(21, alpha[turbine_id], beta[turbine_id])) / 6 / \
                   self.__cdf(wind_end, alpha[turbine_id], beta[turbine_id])

            p_list.extend([v_lt2] * 6 + [v_gt20] * 6)

            p_dict[turbine_id] = p_list

        return p_dict

    def save_loads(self, loads, type):
        loads_json_file = os.path.abspath(os.path.join(self.this_dir, '../../files/Loads/tower_loads.json'))
        tower_loads_dict = {k: v for k, v in loads.to_dict().items() if '60.00.' in k}

        if not os.path.isfile(loads_json_file):
            with open(loads_json_file, 'w') as f:
                json.dump({'ul': {}, 'fl': {}}, f)
        
        with open(loads_json_file, 'r') as f:
            data = json.load(f)

        data_partial = data[type]     
        data_partial.update(tower_loads_dict)
        data.update({type: data_partial})
        with open(loads_json_file, 'w') as f:
            json.dump(data, f)        
