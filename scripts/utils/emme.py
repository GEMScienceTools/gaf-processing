import numpy as np

def process_emme(emme_df):
    """
    Master processing function for the Earthquake Model of the Middle East
    (EMME) database. This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """

    emme_df['slip_type'] = emme_df.apply(get_slip_type_from_rake, axis=1)
    emme_df['rake'] = emme_df.apply(rake_to_tup, axis=1)
    emme_df['dip'] = emme_df.apply(dip_to_tup, axis=1)
    emme_df['slip_rate'] = emme_df.apply(slip_rate_to_tup, axis=1)
    emme_df['epistemic_quality'] = emme_df.apply(epist_quality, axis=1)

    return emme_df


def epist_quality(row):
    if row['CLASS'] == 'A':
        return 1
    elif row['CLASS'] == 'B':
        return 2
    elif row['CLASS'] == 'C':
        return 3


def rake_to_tup(row):
    """
    Converts the `rakemin` and `rakemax` data into a tuple
    with the mean rake as the mid range value.
    """
    rkmin = row['RAKEMIN']
    rkmax = row['RAKEMAX']
    rkav = np.mean((rkmin, rkmax))
    
    return '({},{},{})'.format(int(rkav), rkmin, rkmax)


def dip_to_tup(row):
    """
    Converts the `rakemin` and `rakemax` data into a tuple
    with the mean rake as the mid range value.
    """
    dpmin = row['DIPMIN']
    dpmax = row['DIPMAX']
    dpav = np.mean((dpmin, dpmax))
    
    return '({:.1f},{},{})'.format(dpav, dpmin, dpmax)


def slip_rate_to_tup(row):
    """
    Converts the `ratemin` and `ratemax` data into a tuple
    with the mean rate as the mid range value.
    """
    srmin = row['SRMIN']
    srmax = row['SRMAX']
    srav = np.mean((srmin, srmax))
    return '({:.1f},{},{})'.format(srav, srmin, srmax)


def get_slip_type_from_rake(row):
    rake = np.mean([row['RAKEMIN'], row['RAKEMAX']])

    if (-22.5 <= rake < 22.5) or (337.5 <= rake <= 360):
        slip_type = 'Sinistral'
    elif 22.5 <= rake < 67.5:
        slip_type = 'Sinistral-Reverse'
    elif 67.5 <= rake < 112.5:
        slip_type = 'Reverse'
    elif 112.5 <= rake < 157.5:
        slip_type = 'Dextral-Reverse'
    elif 157.5 <= rake < 180:
        slip_type = 'Dextral'
    elif (-67.5 <= rake < 22.5) or (292.5 <= rake <= 337.5):
        slip_type = 'Sinistral-Normal'
    elif (-112.5 <= rake < -67.5) or (247.5 <= rake < 292.5):
        slip_type = 'Normal'
    elif (-157.5 <= rake < -112.5) or (202.5 <= rake < 247.5):
        slip_type = 'Dextral-Normal'
    elif (-180 <= rake < -157.5) or (180 <= rake < 202.5):
        slip_type = 'Dextral'
    else:
        slip_type = None
    return slip_type
