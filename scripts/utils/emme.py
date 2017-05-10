import numpy as np

def process_emme(emme_df):
    """
    Master processing function for the Earthquake Model of the Middle East
    (EMME) database. This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """

    emme_df['slip_type'] = emme_df.apply(get_slip_type_from_rake, axis=1)

    return emme_df


def get_slip_type_from_rake(row):
    rake = float(row['rake'])

    if -22.5 <= rake < 22.5:
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
