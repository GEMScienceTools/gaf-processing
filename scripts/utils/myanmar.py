def process_myanmar(myr_df):
    """
    Master processing function for the Myanmar database. 
    This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """

    #myr_df = modify_slip_type(myr_df) # already done to GeoJSON manually
    myr_df = format_dip(myr_df)
    myr_df['net_slip_rate'] = myr_df.apply(format_slip_rate, axis=1)

    return myr_df


def modify_slip_type(myr_df):

    myr_slip_d = {'Reverse': 'Reverse',
                  'Strike-Slip': 'Strike-Slip',
                  'Anticline': 'Anticline',
                  'Strike-slip': 'Strike-Slip',
                  'Normal': 'Normal',
                  'Strike-Slip/Normal': 'Strike-Slip-Normal'}
    
    myr_df['slip_type'] = [myr_slip_d[row['fault type']]
                           for i, row in myr_df.iterrows()]

    return myr_df


def format_dip(myr_df):

    myr_df['average_dip'] = ['({},,)'.format(dip) for dip in myr_df['dip']]
    
    return myr_df


def format_slip_rate(row):
    u = row['upper slip']
    l = row['lower slip']

    if u == -999:
        if l == -999:
            sr = None
        else:
            sr = '({},,{})'.format(l, l)
    else:
        if l == -999:
            sr = '({},{},)'.format(u, u)
        else:
            sr = '({},{},{})'.format((u+l)/2, u, l)

    return sr
