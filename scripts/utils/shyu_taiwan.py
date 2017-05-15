import numpy as np
from ast import literal_eval as leval


def process_taiwan(tdf):
    tdf['average_dip'] = tdf.apply(_process_dips, axis=1)
    tdf['slip_type'] = tdf.apply(_process_fault_type, axis=1)
    tdf['net_slip_rate'] = tdf.apply(_process_slip_rate, axis=1)
    tdf['reference'] = tdf.apply(_process_reference, axis=1)

    return tdf


def load_val(obj):
    if isinstance(obj, str):
        return leval(obj)
    else:
        return obj


def _process_dips(row):

    dip1 = load_val(row['DIP_0to1'])
    dip2 = load_val(row['DIP_1to2'])
    dip3 = load_val(row['DIP_2to3'])

    if dip2 == 0:
        avg_dip = dip1

    else:
        z1 = load_val(row['DEPTH_1_KM'])
        z2 = load_val(row['DEPTH_2'])
        x1 = z1 / np.tan(np.radians(dip1))
        x2 = (z2 - z1) / np.tan(np.radians(dip2))
        
        if dip3 == 0:
            total_x = x1 + x2
            avg_dip = np.degrees( np.arctan2( z2, total_x))

        else:
            z3 = load_val(row['DEPTH_3'])
            x3 = (z3 - z2) / np.tan(np.radians(dip3))
            total_x = x1 + x2 + x3
            avg_dip = np.degrees( np.arctan2( z3, total_x))

    return '({},,)'.format(int(avg_dip))


def _process_fault_type(row):

    ft = row['FAULT_TYPE']

    if ft == 'N':
        return 'Normal'
    elif ft == 'R':
        return 'Reverse'
    elif ft == 'SS':
        return 'Strike-Slip'
    elif ft == 'SS/R' or ft == 'R/SS':
        return 'Reverse-Strike-Slip'


def _process_slip_rate(row):

    return '({},{},{})'.format(row['SP_AVE'], row['SP_RATE_Mn'], 
                               row['SP_RATE_Mx'])

def _process_reference(row):

    ref = row['SOURCE'].replace('This study', 'Shyu et al 2016')

    return ref
