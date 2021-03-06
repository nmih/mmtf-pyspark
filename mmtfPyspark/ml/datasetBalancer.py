#!/user/bin/env python
'''
dataBalancer.py:

Creates a balanced dataset for classification problems by either
downsampling the majority classes or upsampling the  minority classes.
It randomly samples each class and returns a dataset with approximately
the same number of samples in each class

Authorship information:
    __author__ = "Mars (Shih-Cheng) Huang"
    __maintainer__ = "Mars (Shih-Cheng) Huang"
    __email__ = "marshuang80@gmail.com:
    __status__ = "Done"
'''

from pyspark.sql import DataFrame
from pyspark.sql import Row
from functools import reduce
import math


def downsample(data, columnName, seed = 7):
    '''
    Returns a balanced dataset for the given column name by downsampling
    the majority classes.
    The classification column must be of type String

    Attributes:
        data (Dataframe)
        columnName (String): column to be balanced by
        seed (Int): random number seed
    '''

    # TODO specify max ratio between minority and majority class

    counts = data.groupby(columnName).count().collect()

    count = [int(x[1]) for x in counts]
    names = [y[0] for y in counts]
    minCount = min(count)

    samples = [data.filter(columnName + "='%s'"%n) \
               .sample(False,minCount/float(c),seed) \
               for n,c in zip(names, count)]

    return reduce(lambda x,y: x.union(y), samples)


def upsample(data, columnName, seed = 7):
    '''
    Returns a balanced dataset for the given column name by upsampling
    the majority classes.
    The classification column must be of type String

    Attributes:
        data (Dataframe)
        columnName (String): column to be balanced by
        seed (Int): random number seed
    '''

    counts = data.groupby(columnName).count().collect()

    count = [int(x[1]) for x in counts]
    names = [y[0] for y in counts]
    maxCount = max(count)

    samples = [data.filter(columnName + "='%s'"%n) \
               .sample(False,maxCount/float(c),seed) \
               if abs(1-maxCount/float(c)) > 1.0 \
               else data.filter(columnName + "='%s'"%n) \
               for n,c in zip(names, count)
               ]

    return reduce(lambda x,y: x.union(y), samples)
