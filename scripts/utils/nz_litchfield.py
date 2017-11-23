
def process_nz_litchfield(nz_df):

    nz_df['slip_type'] = nz_df.apply(get_slip_type, axis=1)
    nz_df['average_rake'] = nz_df.apply(get_rake, axis=1)
    nz_df['average_dip'] = nz_df.apply(get_dip, axis=1)
    nz_df['net_slip_rate'] = nz_df.apply(get_slip_rate, axis=1)
    nz_df['epistemic_quality'] = nz_df['Qual_Code'] - 1

    return nz_df


def get_slip_type(row):

    main_slip_type = row['Sense_Dom'].capitalize()

    if row['Sense_Sec'] is None:
        return main_slip_type
    else:
        return main_slip_type + '-' + row['Sense_Sec'].capitalize()


def format_tup(best, mini, maxi):
    return '({},{},{})'.format(best, mini, maxi)


def get_rake(row):
    return format_tup(row.Rake_Best, row.Rake_Min, row.Rake_Max)


def get_dip(row):
    return format_tup(row.Dip_Best, row.Dip_Min, row.Dip_Max)


def get_slip_rate(row):
    return format_tup(row.SR_Best, row.SR_Min, row.SR_Max)
