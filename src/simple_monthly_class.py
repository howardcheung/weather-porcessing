#!/usr/bin/python3
"""
    This file contains functions that perform machine learning on the
    average and standard deviation of monthly weather data of various cities
    for classification

    GSOD data at ftp://ftp.ncdc.noaa.gov/pub/data/gsod/

    Name: Howard Cheung
    email: howard.at (at) gmail.com
    Date of creation: 2017/09/10 0740 +0800
"""

# internal modules


# third party modules
import pandas as pd


# user-defined modules


# global variables


# user-defined classes
from read_gsod_data import unzip_gsod_files


# user functions
def processing_monthly_data(tarfilename: str,
                            numfile: float=float('inf')) -> pd.DataFrame:
    """
        This function reads an annual gsod data and give the mean, max, min
        and/or sum of temperature, dewpoint, wind speed, precipitation and
        windspeed of each month for each station and put them as
        separate columns

        Inputs:
        ==========
        tarfilename: str
            path to the tar file of gsod files

        numfile: float
            for testing only. Ignore in actual operation
    """

    # read the data
    dfsdict = unzip_gsod_files(tarfilename, numfile)

    # calculate the required columns
    colnames = ['stn']
    for ind in range(1, 13):
        for txt in ['tmp', 'dew', 'stp', 'wpd', 'prec', 'sndp']:
            for cal in ['mean', 'max', 'min']:
                colnames += [''.join([txt, '%02i' % ind, cal])]
    finaldf = pd.DataFrame(columns=colnames)

    # calculate the values
    for fileind, stn in enumerate(dfsdict):
        finaldf.loc[fileind, 'stn'] = stn
        df = dfsdict[stn]
        for ind in range(1, 13):
            for txt in ['tmp', 'dew', 'stp', 'wpd', 'prec', 'sndp']:
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'mean'])] = \
                    df.loc[[dt.month==1 for dt in df['date']], txt].mean()
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'max'])] = \
                    df.loc[[dt.month==1 for dt in df['date']], txt].max()
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'min'])] = \
                    df.loc[[dt.month==1 for dt in df['date']], txt].min()

    return finaldf


# testing functions
if __name__ == '__main__':

    # test the gsod file tarball reader
    FINALDF = processing_monthly_data('../data/gsod/gsod_2016.tar')
    print(FINALDF)
    print('simple_monthly_class.py is ok')
    