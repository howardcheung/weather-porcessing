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
import numpy as np
import pandas as pd


# user-defined modules
from read_gsod_data import unzip_gsod_files


# global variables


# user-defined classes


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
    total_files = len(dfsdict)
    finaldf = pd.DataFrame(index=np.arange(total_files), columns=colnames)

    # calculate the values
    for fileind, stn in enumerate(dfsdict):
        finaldf.loc[fileind, 'stn'] = stn
        df = dfsdict[stn]
        if fileind % 4 == 0:
            print('Processing station ', stn, ' data')
            print('Stage: ', (fileind+1.0)/total_files)
        for ind in range(1, 13):
            for txt in ['tmp', 'dew', 'stp', 'wpd', 'prec', 'sndp']:
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'mean'])] = \
                    df.loc[df['mn'] == ind, txt].mean()
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'max'])] = \
                    df.loc[df['mn'] == ind, txt].max()
                finaldf.loc[fileind, ''.join([txt, '%02i' % ind, 'min'])] = \
                    df.loc[df['mn'] == ind, txt].min()

    return finaldf


# testing functions
if __name__ == '__main__':

    # test the gsod file tarball reader
    FINALDF = processing_monthly_data('../data/gsod/gsod_2016.tar')
    FINALDF.to_csv('../results/gsod_2016_monthly.csv')
    print(FINALDF)
    print('simple_monthly_class.py is ok')
    