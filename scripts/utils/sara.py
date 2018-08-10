from ast import literal_eval as leval
import numpy as np

def process_sara(sara_df):
    """
    Master processing function for the SARA  database. 
    This simply runs all of the functions below and returns
    the updated database, ready to merge.
    """
    
    sara_df['average_dip'] = [_dips_from_row(row) 
                             for i, row in sara_df.iterrows()]
    
    sara_df['sr'] = [_srs_from_row(row) for i, row in sara_df.iterrows()]

    sara_df['slip_type'] = [sar_slip_type[row.rup_type] 
                            for i, row in sara_df.iterrows()]

    sara_df['lower_seis_depth'] = sara_df.apply(lsd, axis=1)
    sara_df['upper_seis_depth'] = sara_df.apply(usd, axis=1)

    return sara_df


def usd(row):
    return '({},,)'.format(row['usd'])


def lsd(row):
    return '({},,)'.format(row['lsd'])



def _dips_parse(dip, dips):
    
    dip_tup = '({},{},{})'
    
    if '<' in dips:
        dip_min = ''
        dip_max = dips.split('<')[1]
    elif '>' in dips:
        dip_min = dips.split('>')[0]
        dip_max = ''
    elif '-' in dips:
        dip_min, dip_max = dips.split('-')
    elif 'a' in dips:
        dip_min, dip_max = dips.split('a')
    else:
        if np.isscalar(leval(dips)):
            dip = dips
            dip_min = ''
            dip_max = ''
        
    return dip_tup.format(dip, dip_min, dip_max)
    
    
def _dips_from_row(row):
    return _dips_parse(row.dip, row.dips)


def _srs_parse(sr, srs):
    
    sr_tup = '({},{},{})'
    
    if '<' in srs:
        sr_min = ''
        sr_max = srs.split('<')[1]
    elif '>' in srs:
        sr_min = srs.split('>')[0]
        sr_max = ''
    elif '-' in srs:
        sr_min, sr_max = srs.split('-')
    elif 'a' in srs:
        sr_min, sr_max = srs.split('a')
    else:
        if np.isscalar(leval(srs)):
            sr = srs
            sr_min = ''
            sr_max = ''
        
    return sr_tup.format(sr, sr_min, sr_max)
    
    
def _srs_from_row(row):
    return _srs_parse(row.slip_rate, row.slip_rates)


sar_slip_type = {'reverse': 'Reverse' ,
 'dextral': 'Dextral',
 'normal': 'Normal',
 'sinistral-reverse': 'Sinistral-Reverse',
 'dextral-normal': 'Dextral-Normal',
 'sinistral-normal': 'Sinistral-Normal' ,
 'None': None,
 'sinistral': 'Sinistral',
 'dextral-reverse': 'Dextral-Reverse',
 'normal-sinistral': 'Normal-Sinistral',
 'normal-dextral': 'Normal-Dextral',
 'reverse-sinistral': 'Reverse-Sinistral',
 'reverse-dextral': 'Reverse-Dextral',
 'strikeslip': 'Strike-Slip',
 'strikeslip-reverse': 'Strike-Slip-Reverse',
 'strikeslip-normal':'Strike-Slip-Normal' }
