def process_e_africa(e_af_df):
    """
    Master processing function for the Macgregor AfricaFaults dataset
    (with only East African faults here). This simply runs all of the
    functions below and returns the updated database, ready to merge.
    """
    e_af_df['slip_type'] = e_af_df.apply(e_af_type_to_slip, axis=1)

    return e_af_df


def e_af_type_to_slip(row):
    """
    Returns a slip type consistent with the master database based
    on the fault type in the E. African database
    """
    slip = row['type']
    
    if slip == 'extensional':
        slip_type = 'Normal'
    elif slip == 'transform':
        slip_type = 'Strike-Slip'
    else:
        slip_type = None
    return slip_type

