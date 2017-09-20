#!/usr/bin/python3
"""
    This file contains functions that get rid of invalid data and write
    another file for valid data

    GSOD data at ftp://ftp.ncdc.noaa.gov/pub/data/gsod/

    Name: Howard Cheung
    email: howard.at (at) gmail.com
    Date of creation: 2017/09/14 2240 +0800
"""

# internal modules
from math import isnan


# third party modules
import numpy as np
import pandas as pd


# user-defined modules


# global variables


# user-defined classes


# user functions
def datafiltering(csvfilename: str, newfilename: str) -> pd.DataFrame:
    """
        This function filters the data by filling 0 to nan in snowfall and
        precipitation data and drop all other nan rows. Return the filtered
        data.

        Inputs:
        ==========
        csvfilename: str
            path to the csv file from simple_monthly_class.py

        newfilename: str
            path to the new csv file after filtering
    """

    # read the file
    df = pd.read_csv(csvfilename, index_col=0)

    # fill in all nan in the precipitation and snowfall columns by zeros
    for col in df.columns:
        for colnm in ['prec', 'sndp']:
            if colnm in col:
                df.loc[df[col].apply(isnan), col] = 0

    # drop all nan columns
    df = df.dropna(0)

    # write to file and return the df
    df.to_csv(newfilename)

    return df


def read_history(histfilename: str) -> pd.DataFrame:
    """
        This function reads the history file of gsod for the locations
        of the stations. Return a pandas DataFrame with the location info.
        with the following columns:
            USAF: code in GSOD file
            WBAN: code in GSOD file
            STN_NM: name of station
            CTRY: code for country
            ST: code for US state
            CALL: code in GSOD file
            LAT: latitude
            LON: longitude
            ELEV: elevation
            BEGIN: begin date in string
            END: end date in string
    """

    # read file
    return pd.read_fwf(
        histfilename, widths=[7, 6, 30, 5, 3, 5, 9, 9, 8, 9, 9],
        header=0, skiprows=21, names=[
            'USAF', 'WBAN', 'STN_NM', 'CTRY', 'ST', 'CALL', 'LAT', 'LON',
            'ELEV', 'BEGIN', 'END'
        ]
    )


# testing functions
if __name__ == '__main__':

    FILTERED_DF = datafiltering(
        '../results/gsod_2016_monthly.csv', '../results/gsod_filtered.csv'
    )
    print(FILTERED_DF)

    HISTORY_DF = read_history('../data/gsod/isd-history.txt')
    print(HISTORY_DF)
    print('data_filteirng.py is ok')
    