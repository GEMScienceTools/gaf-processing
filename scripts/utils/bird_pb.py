from ast import literal_eval as leval
import numpy as np
import pandas as pd


def process_bird_pb(bird_df):
    """
    Master processing function for Peter Bird's plate boundary dataset
    (Bird, 2003 G-cubed). This function runs the functions below and
    returns the aggregated result, ready to be merged into the GEM-GAF.
    """

    bird_df = bird_df.copy(deep=True)

    bird_df = bird_keep_boundary_types(bird_df, 
                                       retain_types=('SUB','OSR','OTF','OCB'))
    bird_df['slip_type'] = bird_df.apply(bird_slip_type_parse, axis=1)
    #bird_df['average_rake'] = bird_df.apply(bird_rake_parse, axis=1)
    bird_df['net_slip_rate'] = bird_df.apply(bird_slip_rate_parse, axis=1)
    bird_df['strike_slip_rate'] = bird_df.apply(bird_strike_slip_rate, axis=1)
    bird_df['shortening_rate'] = bird_df.apply(bird_short_rate, axis=1)
    bird_df['epistemic_quality'] = 1
    bird_df['activity_confidence'] = 1

    return bird_df



def bird_keep_boundary_types(bird_df, retain_types=tuple(['SUB'])):
    keep_idx = [s.STEPCLASS in retain_types for i, s in bird_df.iterrows()]
    bird_df = bird_df.loc[keep_idx, :]
    return bird_df


def bird_slip_rate_parse(row):
    return '({},,)'.format(row.VELOCITYLE)


def bird_slip_type_parse(row):
    
    if row.STEPCLASS == 'SUB':
        return 'Subduction Thrust'

    elif row.STEPCLASS == 'OSR':
        #return 'Normal'
        return 'Spreading Ridge'

    elif row.STEPCLASS == 'CRB':
        return 'Normal'

    elif row.STEPCLASS == 'OTF':
        if row.VELOCITYRI > 0:
            return 'Dextral Transform'
        else:
            return 'Sinistral Transform'

    elif row.STEPCLASS == 'CTF':
        if row.VELOCITYRI > 0:
            return 'Dextral'
        else:
            return 'Sinistral'

    elif row.STEPCLASS == 'OCB':
        return 'Subduction Thrust'

    elif row.STEPCLASS == 'CCB':
        return 'Reverse'


def bird_rake_parse(row):
    # Need dip information to calculate
    pass


def bird_strike_slip_rate(row):
    return '({},,)'.format(np.abs(row.VELOCITYRI))

def bird_short_rate(row):
    return '({},,)'.format(-row.VELOCITYDI)


