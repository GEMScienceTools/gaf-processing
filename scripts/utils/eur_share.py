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
