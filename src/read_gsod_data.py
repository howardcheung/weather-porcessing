#!/usr/bin/python3
"""
    This file contains functions that reads a gsod data file and return a
    pandas DataFrame for the specificed file

    GSOD data at ftp://ftp.ncdc.noaa.gov/pub/data/gsod/

    Name: Howard Cheung
    email: howard.at (at) gmail.com
    Date of creation: 2017/09/10 0740 +0800
"""

# internal modules
from datetime import date

# third party modules
import pandas as pd

# user-defined modules


# global variables


# user-defined classes


# user functions
def read_gsod_file(filename: str) -> pd.DataFrame:
    """
        This function reads a GSOD data file and return a pandas DataFrame
        with the following columns:
            stn: station number in int
            date: date value of the data point in datetime.date object
            tmp: mean temperature in K
            dew: mean dewpoint temperature in K
            stp: standard station pressure in Pa
            wpd: mean wind speed in m/s
            count_tmp: number of observations for temp
            count_dew: number of observations for dew
            count_stp: number of observations for stp
            count_wpd: number of observations for wpd
            max_tmp: maximum temperature in K
            min_tmp: minimum temperature in K
            prec: precipatation in mm
    """

    # read the file first
    raw_df = pd.read_csv(
        filename, delim_whitespace=True, skiprows=1,
        names=[ind for ind in range(22)]
    )

    # build new df
    ori_df = pd.DataFrame(columns=[
        'stn', 'date', 'tmp', 'dew', 'stp', 'wpd',
        'count_tmp', 'count_dew', 'count_stp', 'count_wpd',
        'max_tmp', 'min_tmp', 'prec'
    ])

    # assign columns
    ori_df.loc[:, 'stn'] = raw_df[0]
    print(raw_df[2])
    ori_df.loc[:, 'date'] = [
        date(int(str(text)[0:4]), int(str(text)[4:6]), int(str(text)[6:8]))
        for text in raw_df[2]
    ]
    ori_df.loc[:, 'tmp'] = (raw_df[3].replace(9999.9, float('nan'))-32.0)*5./9.
    ori_df.loc[:, 'dew'] = (raw_df[5].replace(9999.9, float('nan'))-32.0)*5./9.
    ori_df.loc[:, 'stp'] = raw_df[9].replace(9999.9, float('nan'))*100.0
    ori_df.loc[:, 'wpd'] = raw_df[13].replace(999.9, float('nan'))*0.5144444444444
    ori_df.loc[:, 'count_tmp'] = raw_df[4]
    ori_df.loc[:, 'count_dew'] = raw_df[6]
    ori_df.loc[:, 'count_stp'] = raw_df[10]
    ori_df.loc[:, 'count_wpd'] = raw_df[14]
    ori_df.loc[:, 'max_tmp'] = [
        (float(ind.replace('*', ''))-32.0)*5./9.
        if ind != '9999.9' else float('nan')
        for ind in raw_df[17]
    ]
    ori_df.loc[:, 'min_tmp'] = [
        (float(ind.replace('*', ''))-32.0)*5./9.
        if ind != '9999.9' else float('nan')
        for ind in raw_df[18]
    ]
    ori_df.loc[:, 'prec'] = [
        float(ind[:-1])*25.4 if ind != '99.99' else float('nan')
        for ind in raw_df[19]
    ]

    return ori_df


# testing functions
if __name__ == '__main__':

    TEST_DF = read_gsod_file('../data/gsod/010460-99999-2016.op')
    print(TEST_DF)
    assert isinstance(TEST_DF, pd.DataFrame)
    print('read_gsod_data.py is ok')
