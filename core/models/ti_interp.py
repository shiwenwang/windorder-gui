# -*- coding: utf-8 -*-
"""
Turbulent intensity interpolation at [rated, cut-out, rated-2, rated+2] wind speed

@author: 36719
"""
import numpy as np
import pandas as pd
from scipy.interpolate import interp1d
from collections import OrderedDict
from . import Base
from . import CalcRatedWindSpeed
from functools import partial


class TiInterp(Base):

    def run(self):
        """

        :return ti: turbulence intensity
        """
        ti_cluster = {}

        for k, wind in self._inputs.items():

            wind_condition = wind['condition']
            ti_m1 = wind['m1']
            ti_m10 = wind['m10']
            ti_etm = wind['etm']

            rated_wind_speed = self.calc_rated_wind_speed(wind_condition)  # dict

            if k == 'farm':
                turbine_sites = wind['label']  # label: sites
            else:
                turbine_sites = [k]  # label: tower_id

            min_windspeed = ti_m1['Wind Speed'].values[0]
            wind_cut_in = 2.5 if min_windspeed < 3 else 3
            wind_cut_out = int(ti_etm['Wind Speed'].iloc[-1])

            f_wind_end = partial(self.calc_wind_end, wind_condition, wind_cut_out)
            sequence = np.append(np.arange(3, 20, 2), 20)
            etm_index = ['ETM' + str(d) for d in sequence]
            m10_index = [''.join(['I', str(d), '_m10']) for d in sequence]

            ul_index = etm_index + ['Ir-2_m1', 'Ir_m1', 'Ir+2_m1', 'Iout_m1']
            fl_index = m10_index + ['Iin_m10', 'Ir_m10', 'Iout_m10', 'Iend_m10']

            ti = self.interpolation(turbine_sites, rated_wind_speed, wind_cut_in, wind_cut_out,
                                    ti_m1, ti_m10, ti_etm, ul_index, fl_index, f_wind_end)

            ti_cluster.update(ti)

        self._outputs = {'ti': ti_cluster, 'cut_in': wind_cut_in, 'cut_out': wind_cut_out}

    @staticmethod
    def calc_rated_wind_speed(wind_condition):
        """ calc_rated_wind_speed model """
        calc_vr_inputs = OrderedDict(wind_condition=wind_condition)
        calc_vr = CalcRatedWindSpeed(**calc_vr_inputs)
        calc_vr.run()
        rated_wind_speed = calc_vr.pop()

        return rated_wind_speed

    def interpolation(self, turbine_sites, rated_wind_speed, wind_cut_in, wind_cut_out, ti_m1, ti_m10, ti_etm,
                      ul_index, fl_index, f_wind_end):
        ti = {}
        sequence = np.append(np.arange(3, 20, 2), 20)
        for turbine_id in turbine_sites:
            wind_end = f_wind_end(turbine_id)

            # 3-20，湍流插值
            ti_ul = self.ti_seq(ti_etm, turbine_id, sequence)
            ti_fl = self.ti_seq(ti_m10, turbine_id, sequence)

            # 特殊点插值
            m1_ext_seq = np.array([rated_wind_speed[turbine_id] - 2, rated_wind_speed[turbine_id],
                                   rated_wind_speed[turbine_id] + 2, wind_cut_out])
            m10_ext_seq = np.array([wind_cut_in, rated_wind_speed[turbine_id], wind_cut_out])

            ti_ul = np.append(ti_ul, self.ti_seq(ti_m1, turbine_id, m1_ext_seq))
            ti_fl = np.append(ti_fl, self.ti_seq(ti_m10, turbine_id, m10_ext_seq))
            ti_fl = np.append(ti_fl, self.calc_ti_end(ti_fl, wind_end))

            ti_ul_ser = pd.Series(ti_ul, index=ul_index)
            ti_fl_ser = pd.Series(ti_fl, index=fl_index)

            ti[turbine_id] = pd.concat([ti_ul_ser, ti_fl_ser])

        return ti

    def ti_seq(self, ti, turbine_id, sequence):
        try:
            interpolator = interp1d(ti['Wind Speed'].values, ti[turbine_id].values, kind='linear')
        except ValueError as e:
            interpolator = interp1d(self.fix_data(ti['Wind Speed'].values),
                                    self.fix_data(ti[turbine_id].values), kind='linear')
            print(f"[INFO]: {turbine_id}, 湍流格式有误！{e}")

        max_wind_speed = np.max(ti['Wind Speed'].values)
        inner_sequence = [d for d in sequence if d <= max_wind_speed]
        outer_sequence = [d for d in sequence if d not in inner_sequence]

        ti_inner_sequence = interpolator(inner_sequence)  # inner_sequence (m/s) 的的插值

        ti_outer_sequence = [ti_inner_sequence[-1]] * len(outer_sequence)
        ti_sequence = np.append(ti_inner_sequence, ti_outer_sequence)  # sequence范围外的插值

        if np.all(sequence in np.append(np.arange(3, 20, 2), 20)):
            ti_sequence[-1] = ti_inner_sequence[-1]     # 将切出风速湍流赋值给 ETM20 和 I20_m10

        return ti_sequence

    @staticmethod
    def calc_wind_end(wind_condition, wind_cut_out, turbine_id):
        v_end = (0.7 * wind_condition.loc[turbine_id]['v50'] if 0.7 * wind_condition.loc[turbine_id]['v50'] >
                 wind_cut_out + 1 else wind_cut_out + 2)
        return v_end
    
    @staticmethod
    def calc_ti_end(ti_fl, wind_end):
        ti_end = ti_fl[6] * (0.75 + 5.6 / wind_end) / (0.75 + 5.6 / 15)
        return ti_end

    @staticmethod
    def fix_data(arr):
        result = []
        for i, d in enumerate(arr):
            if isinstance(d, (int, float)) and d == d:
                result.append(d)
            else:
                if i:
                    result.append(result[i - 1])
                else:
                    result.append(0)
        return result


