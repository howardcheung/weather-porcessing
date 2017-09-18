#!/usr/bin/python3
"""
    This file passes the monthly data into a K-means algorithm

    GSOD data at ftp://ftp.ncdc.noaa.gov/pub/data/gsod/

    Name: Howard Cheung
    email: howard.at (at) gmail.com
    Date of creation: 2017/09/14 2240 +0800
"""

# internal modules
from math import isnan
from collections import namedtuple


# third party modules
import numpy as np
import pandas as pd
from scipy.cluster.vq import kmeans2


# user-defined modules


# global variables


# user-defined classes
ResultTuple = namedtuple('ResultTuple', ['centroids', 'classes'])


# user functions
def kmeans_classify(filename: str, centroidfilename: str,
                    classfilename: str,
                    numclasses: int, numdatapts: int=None) -> ResultTuple:
    """
        This function reads the filtered monthly gsod data and return
        a collections.namedtuple with the following attributes:
            centroids: pandas DataFrame with the same column names as the
                read data (except the station number)
            classes: pandas DataFrame of weather classes in the original file

        Inputs:
        ==========
        filename: str
            path to the csv file from data_filtering.py

        centroidfilename: str
            path to the new csv file storing information of centroids

        classfilename: str
            path to the new csv file storing information of classes

        numclasses: int
            number of classes

        numdatapts: int
            number of data points to be used. Default None (all data points)
    """

    # create x array
    df = pd.read_csv(filename, index_col='stn')
    df = df.drop('Unnamed: 0', axis=1)
    xarray = np.array(df)[:, 1:]  # remove index column
    if numdatapts is not None:
        xarray = xarray[:numdatapts, :]

    # run k-means
    centroids, classes = kmeans2(xarray, numclasses)

    # create new df
    centroiddf = pd.DataFrame(centroids, columns=df.columns[1:])
    df.loc[df.index[0:len(classes)], 'classes'] = classes

    # save files
    centroiddf.to_csv(centroidfilename)
    df.to_csv(classfilename)

    return ResultTuple(centroiddf, df)


# test functions
if __name__ == '__main__':

    RESULTS = kmeans_classify(
        '../results/gsod_filtered.csv',
        '../results/gsod_kmeans_centroids.csv',
        '../results/gsod_kmeans_classes.csv',
        19
    )
    print(RESULTS.classes)
    print(RESULTS.centroids)
    assert isinstance(RESULTS.centroids, pd.DataFrame)
    assert isinstance(RESULTS.classes, pd.DataFrame)
    print('gsod_kmeans.py is ok')
