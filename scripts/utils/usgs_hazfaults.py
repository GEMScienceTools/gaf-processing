from ast import literal_eval as leval
import re


def process_usgs_hazfaults(usgs_df):
    """
    Processes the USGS HazFaults 2014 dataset for merging with master_df
    """

    usgs_df['average_dip'] = usgs_df.apply(_process_dips, axis=1)
    usgs_df['slip_type'] = usgs_df.apply(_process_slip_type, axis=1)

    return usgs_df


def _process_dips(row):
    dip_str = row['DISP_DIPS']
    dip_tup = '({},{},{})'

    try:
        dip = int(dip_str)
        dip_tup = dip_tup.format(dip, '', '')
    except ValueError:
        try:
            dip_list = dip_str.split('/')
            dips = [int(dip) for dip in dip_list]
            dip_tup = dip_tup.format(*dips)
        except ValueError:
            dip_str = re.sub('\D', '', dip_str)
            dip = int(dip_str)
            dip_tup = dip_tup.format(dip, '', '')

    return dip_tup


def _process_slip_type(row):

    st = row['DISP_SLIP_']

    if st == 'Thrust':
        slip_type = 'Reverse'
    elif st == 'Unassigned':
        slip_type = None
    else:
        slip_type = st

    return slip_type
        
