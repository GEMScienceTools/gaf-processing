from ast import literal_eval
import numpy as np


def process_eur_share(eur_df):
    """
    Master processing function for the European SHARE database. This simply
    runs all of the functions below and returns the updated database, ready to
    merge.  
    """

    eur_df['rake'] = eur_df.apply(eur_rake_to_tup, axis=1)
    eur_df['slip_rate'] = eur_df.apply(eur_slip_rate_to_tup, axis=1)
    eur_df['dip'] = eur_df.apply(eur_dip_to_tup, axis=1)
    eur_df['slip_type'] = eur_df.apply(get_slip_type_from_rake, axis=1)
    eur_df['lower_seis_depth'] = eur_df.apply(lsd, axis=1)
    eur_df['upper_seis_depth'] = eur_df.apply(usd, axis=1)

    return eur_df


def eur_rake_to_tup(row):
    """
    Converts the `rakemin` and `rakemax` data into a tuple
    with the mean rake as the mid range value.
    """
    rkmin = row['rakemin']
    rkmax = row['rakemax']
    rkav = np.mean((rkmin, rkmax))
    
    return '({},{},{})'.format(int(rkav), rkmin, rkmax)


def eur_dip_to_tup(row):
    """
    Converts the `rakemin` and `rakemax` data into a tuple
    with the mean rake as the mid range value.
    """
    dpmin = row['dipmin']
    dpmax = row['dipmax']
    dpav = np.mean((dpmin, dpmax))
    
    return '({:.1f},{},{})'.format(dpav, dpmin, dpmax)


def eur_slip_rate_to_tup(row):
    """
    Converts the `ratemin` and `ratemax` data into a tuple
    with the mean rate as the mid range value.
    """
    srmin = row['srmin']
    srmax = row['srmax']
    srav = np.mean((srmin, srmax))
    return '({:.1f},{},{})'.format(srav, srmin, srmax)


def lsd(row):
    return '({},,)'.format(row['maxdepth'])


def usd(row):
    return '({},,)'.format(row['mindepth'])


def get_slip_type_from_rake(row):
    rake = literal_eval(row['rake'])[0]
    if rake > 180:
        rake -= 360

    if  -22.5 <= rake < 22.5:
        slip_type = 'Sinistral'
    elif 22.5 <= rake < 67.5:
        slip_type = 'Sinistral-Reverse'
    elif 67.5 <= rake < 112.5:
        slip_type = 'Reverse'
    elif 112.5 <= rake < 157.5:
        slip_type = 'Dextral-Reverse'
    elif 157.5 < rake <= 180:
        slip_type = 'Dextral'
    elif -67.5 <= rake < 22.5:
        slip_type = 'Sinistral-Normal'
    elif -112.5 <= rake < -67.5:
        slip_type = 'Normal'
    elif -157.5 <= rake < -112.5:
        slip_type = 'Dextral-Normal'
    elif -180 <= rake < -157.5:
        slip_type = 'Dextral'
    else:
        slip_type = None
    return slip_type
