def process_myanmar(myr_df):
    """
    Master processing function for the Myanmar database. 
    This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """

    myr_df = modify_slip_type(myr_df)
    myr_df = format_dip(myr_df)

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
