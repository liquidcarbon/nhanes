# pynhanes/data.py

__doc__ = """
Loading NHANES data.
"""

#-----------------------------------------------------------------------------
# Logging
#-----------------------------------------------------------------------------

import logging
_l = logging.getLogger(__name__)

#-----------------------------------------------------------------------------
# Imports & Options
#-----------------------------------------------------------------------------

# External Imports
import numpy as np
import os
import pandas as pd
import requests

from collections import defaultdict

#-----------------------------------------------------------------------------
# Globals & Constants
#-----------------------------------------------------------------------------

BASE_URL = "https://wwwn.cdc.gov/Nchs/Nhanes"

YEARS = {
    "1999-2000": "",
    "2001-2002": "_B",
    "2003-2004": "_C",
    "2005-2006": "_D",
    "2007-2008": "_E",
    "2009-2010": "_F",
    "2011-2012": "_G",
    "2013-2014": "_H",
    "2015-2016": "_I",
    "2017-2018": "_J",
    "2019-2020": "_K",
}


#-----------------------------------------------------------------------------
# Building Data Index
#-----------------------------------------------------------------------------

def load(datasets, years):
    """Loads NHANES datasets into a dictionary of DataFrames.
    
    Adds a column "year" and concatenates multi-year results."""
    
    if type(years) != tuple or len(years) != 2:
        _l.error('Provide year range as a tuple of ints: (year_start, year_end)')

    y0, y1 = years
    visited = []
    res = defaultdict(list)

    for dataset in datasets:
        for year in range(y0, y1):
            url = nhanes_url(dataset, year) + '.XPT'
            if url in visited:
                continue
            try:
                df = pd.read_sas(url, encoding='windows-1252')
                _l.info('read {0[0]} rows x {0[1]} cols from {1}'.format(
                    df.shape, url
                ))
                df['year'] = year
                res[dataset].append(df)
            except Exception as e:
                _l.error(f'{url}: {e}')
            finally:
                visited.append(url)
        try:
            res[dataset] = pd.concat(res[dataset], axis=0, join='outer')
            _l.info('combined {0} datasets: {1[0]} rows x {1[1]} cols'.format(
                dataset, res[dataset].shape
            ))
        except Exception as e:
            _l.error(e)
    return res


def nhanes_url(dataset: str, year: int=2018) -> str:
    """Build URL to retrieve NHANES dataset."""
    years = [k for k in YEARS.keys() if str(year) in k]
    if len(years) == 1:
        prefix, suffix = years[0], dataset.upper() + YEARS[years[0]]
        return f'{BASE_URL}/{prefix}/{suffix}'
    else:
        _l.error('No NHANES data for this year')
        return ''



#-----------------------------------------------------------------------------
# Special Data
#-----------------------------------------------------------------------------

def load_drugs(url='https://wwwn.cdc.gov/Nchs/Nhanes/1999-2000/RXQ_DRUG.xpt'):
    df = pd.read_sas(url, encoding='windows-1252')
    _l.info('read {0[0]} rows x {0[1]} cols from {1}'.format(
                    df.shape, url
    ))
    return df


#-----------------------------------------------------------------------------
# Misc
#-----------------------------------------------------------------------------

def test():
    print('testing')
    _l.debug('testing')