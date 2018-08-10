def process_eos_se_asia(eos_df):
    eos_df['average_dip'] = [tup_from_scalar(dip)
                             for dip in eos_df['dip']]

    eos_df['average_rake'] = [tup_from_scalar(rake)
                              for rake in eos_df['rake']]

    eos_df['net_slip_rate'] = [tup_from_scalar(rate, round=True)
                               for rate in eos_df['net_slip_rate']]

    eos_df['lower_seis_depth'] = [tup_from_scalar(lsd)
                                  for lsd in eos_df['lsd']]

    eos_df['upper_seis_depth'] = [tup_from_scalar(usd)
                                  for usd in eos_df['usd']]

    return eos_df



def tup_from_scalar(scalar, round=False):
    if round:
        scalar = '{0:.2f}'.format(scalar)

    return '({},,)'.format(scalar)
