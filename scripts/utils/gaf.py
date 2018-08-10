from .data_checks import change_triple_sort


def process_gaf(gaf_df):

    gaf_df['upper_seis_depth'] = gaf_df.apply(upper_seis_depth, axis=1)
    gaf_df['lower_seis_depth'] = gaf_df.apply(lower_seis_depth, axis=1)

    return gaf_df


def upper_seis_depth(row):
    if row['ns_upper_sm_depth'] is not None:
        sm =  row['ns_upper_sm_depth']
    elif row['fs_upper_sm_depth'] is not None:
        sm = row['fs_upper_sm_depth']
    else:
        sm = None

    if sm is not None:
        sm = change_triple_sort(sm)

    return sm


def lower_seis_depth(row):
    if row['ns_lower_sm_depth'] is not None:
        sm =  row['ns_lower_sm_depth']
    elif row['fs_lower_sm_depth'] is not None:
        sm = row['fs_lower_sm_depth']
    else:
        sm = None

    if sm is not None:
        sm = change_triple_sort(sm)

    return sm
