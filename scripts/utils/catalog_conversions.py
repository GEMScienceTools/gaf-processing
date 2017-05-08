from ast import literal_eval as leval
import json
import sqlalchemy as sqa
import numpy as np
import pandas as pd

master_df = ''

def merge_regional_df_into_master(regional_df, master_df, merge_dict,
                                  catalog_name=None):
    """
    Merge a DataFrame of regional faults into the master catalog, using
    the `merge_dict` dictionary to describe the column conversions.

    Returns a new DataFrame.

    :param regional_df:
        Regional fault DataFrame.

    """
    merge_gen = (pd.Series({k:row[v] for k, v in merge_dict.items()})
                 for i, row in regional_df.iterrows())
    new_df = pd.concat(merge_gen, axis=1).T
    new_df['catalog_name'] = catalog_name
    
    return pd.concat((master_df, new_df), axis=0, ignore_index=True)


def ata_slip_rate_parse(row):
    sr_ = row['slip_rate']
    
    if sr_ is None:
        sr_tup = None
    else:
        sr = sr_.replace(' mm/yr','')
        if ' - ' in sr:
            _sr = sr.split(' - ')
            sr_lo = leval(_sr[0])
            sr_hi = leval(_sr[1])
            sr_av = np.mean((sr_lo, sr_hi))
            sr_tup = '({},{},{})'.format(sr_av, sr_lo, sr_hi)
        elif '-' in sr:
            _sr = sr.split('-')
            sr_lo = leval(_sr[0])
            sr_hi = leval(_sr[1])
            sr_av = np.mean((sr_lo, sr_hi))
            sr_tup = '({},{},{})'.format(sr_av, sr_lo, sr_hi)
        else:
            sr_tup = '({},,)'.format(leval(sr))
    return sr_tup


def ltype_to_kinematics(row):
    """
    Converts the 'ltype' (linetype) field from the ATA and HimaTibetMap
    datasets to kinematic type.

    Operates on a row from a DataFrame.

    """
    ltype = row['convention']
    
    conv_d = {1111: 'Reverse', 1211: 'Normal', 1311: 'Dextral', 
              1411: 'Sinistral', 0:''}
    
    return conv_d[ltype]



