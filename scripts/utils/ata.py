from ast import literal_eval as leval
import numpy as np
import pandas as pd


def process_ata(ata_df):
    """
    Master processing function for the Active Tectonics of the Andes (ATA)
    database. This simply runs all of the functions below and returns the
    updated database, ready to merge.
    """

    ata_df['slip_rate_tuple'] = ata_df.apply(ata_slip_rate_parse, axis=1)
    ata_df['slip_type'] = ata_df.apply(ata_ltype_to_kinematics, axis=1)
    
    return ata_df


def ata_slip_rate_parse(row):
    """
    Parses the slip rate column, yielding a tuple formatted
    for the master database (mode, min, max).
    """
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


def ata_ltype_to_kinematics(row):
    """
    Converts the 'ltype' (linetype) field from the ATA 
    dataset to kinematic type.

    Operates on a row from a DataFrame.
    """
    ltype = row['convention']
    
    conv_d = {1111: 'Reverse', 1211: 'Normal', 1311: 'Dextral', 
              1411: 'Sinistral', 0: None, 1511: 'Subduction Thrust',
              1611: 'Sinistral Transform', 1711: 'Dextral Transform'}
    
    return conv_d[ltype]
