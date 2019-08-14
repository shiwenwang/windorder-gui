# -*- coding: utf-8 -*-
"""
Get wind parameter from standard excel file

@author: 36719
"""

import os
import numpy as np
import pandas as pd
from . import Base


class WindParse(Base):

    def run(self):

        """
        --- Parse wind parameters from EXCEL ---
        """
        
        wind_path = self._inputs['path']

        cur_wind_params = self.__excel_paras(wind_path)        

        self._outputs = cur_wind_params

    def __excel_paras(self, path):
        wind_params = {}

        # ExcelFile.parse is faster than read_excel in this application
        xls = pd.ExcelFile(path)

        # base data
        # wind_condition = pd.read_excel(path, sheet_name='Site Condition', index_col=0)
        wind_condition = xls.parse('Site Condition')
        wind_condition = self.__clean_data(wind_condition)
        wind_condition.index = wind_condition['label']

        # wind base parameters
        wind_params['condition'] = wind_condition

        # turbine sites
        wind_params['site_label'] = list(wind_condition.index)  # label: sites or tower_id

        # turbulence m1
        # wind_data_m1 = pd.read_excel(path, sheet_name='M=1')
        wind_data_m1 = xls.parse('M=1')
        wind_params['m1'] = self.__clean_data(wind_data_m1)

        # turbulence m10
        # wind_data_m10 = pd.read_excel(path, sheet_name='M=10')
        wind_data_m10 = xls.parse('M=10')
        wind_params['m10'] = self.__clean_data(wind_data_m10)

        # turbulence etm
        # wind_data_etm = pd.read_excel(path, sheet_name='ETM')
        wind_data_etm = xls.parse('ETM')
        wind_params['etm'] = self.__clean_data(wind_data_etm)

        wind_params['filename'] = os.path.splitext(os.path.split(path)[-1])[0]

        return wind_params

    # @staticmethod
    def __clean_data(self, df_raw):
        """
        --- Remove useless data ---
        :param df_raw: original data frame
        :return df_fine: data frame except useless data (e.g. Note)
        """

        rows = df_raw.shape[0]
        header = df_raw.columns
        for head_idx, head_str in enumerate(header):
            if 'unnamed:' in head_str.lower():
                if 'ieff' in header[head_idx - 1].lower():
                    continue
                else:
                    cols = head_idx
                    break
        else:
            cols = head_idx + 1

        df_fine = df_raw.iloc[0:rows, 0:cols].dropna(how='all')
        df_fine.drop(df_fine.index[0], inplace=True)  # drop first line (unit)
        df_fine.index = range(len(df_fine.index))  # index start with 0

        if 'Wind Speed' not in df_fine.columns:
            lower_header = [s.lower() for s in df_fine.columns]
            df_fine.columns = lower_header

        return self.__fill_data(df_fine)

    @staticmethod
    def __fill_data(df):
        for row_i, row_name in enumerate(df.index):
            if pd.isnull(df.loc[row_name]).any():
                line = [df.iloc[row_i - 1, col_i] if pd.isnull(data)
                    else data for col_i, data in enumerate(df.loc[row_name])]
                df.loc[row_name] = np.array(line)
            
        return df

