from ast import literal_eval as leval

def process_htm(htm_df):
    """
    Master processing function for the HimaTibetMap database. 
    This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """

    htm_df = get_slip_type_from_ltype(htm_df)
    htm_df = get_confidence_from_ltype(htm_df)

    return htm_df


def get_slip_type_from_ltype(htm_df):
    """
    Takes the `ltype` (line type) from the HimaTibetMap faults
    and converts it to a kinematic type
    """

    htm_types_dict = {'1111': 'Reverse',
                      '1121': 'Reverse',
                      '1131': 'Reverse',
                      '1211': 'Normal',
                      '1221': 'Normal',
                      '1231': 'Normal',
                      '1311': 'Dextral',
                      '1321': 'Dextral',
                      '1331': 'Dextral',
                      '1411': 'Sinistral',
                      '1421': 'Sinistral',
                      '1431': 'Sinistral',
                      '1611': 'Anticline',
                      '1621': 'Anticline',
                      '1711': 'Syncline',
                      '1721': 'Syncline',
                      }
    htm_df['slip_type'] = [htm_types_dict[htm_df.loc[i, 'ltype']] 
                           for i in htm_df.index]

    return htm_df


def get_confidence_from_ltype(htm_df):
    """
    Takes the confidence number from the line type and extracts
    to new row
    """
    htm_df['conf'] = [leval(row.ltype[2]) for i, row in htm_df.iterrows()]

    return htm_df
    
