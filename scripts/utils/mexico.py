from ast import literal_eval
import numpy as np


def process_mexico(mx_df):
    """
    Master processing function for the Mexican database. This simply
    runs all of the functions below and returns the updated database, ready to
    merge.  
    """

    mx_df['average_dip'] = mx_df.apply(make_dip_tup, axis=1)
    mx_df['net_slip_rate'] = mx_df.apply(process_slip_rate, axis=1)
    mx_df['slip_type'] = mx_df.apply(process_fault_type, axis=1)

    return mx_df


def process_fault_type(row):

    tipo = row['Tipo_Falla']
    
    if tipo == 'Normal':
        slip_type = 'Normal'

    elif tipo is 'Transcurrente Lateral Direcha' or \
                 'Transcurrente Lateral Direcho':
        slip_type = 'Dextral'

    elif tipo is 'Transcurrente Lateral Izquierda':
        slip_type = 'Sinistral'

    else:
        firstword = tipo.split(' ')[0]
        
        if firstword == 'Normal':
            if 'Izquierda' in tipo:
                slip_type = 'Normal-Sinistral'
            elif 'Derecha' in tipo:
                slip_type = 'Normal-Dextral'

        elif firstword == 'Transcurrente':
            if 'Izquierda' in tipo:
                slip_type = 'Sinistral-Normal'
            elif 'Derecha' in tipo:
                slip_type = 'Normal-Sinistral'

    return slip_type


def make_dip_tup(row):

    return '({},,)'.format(row['Inclin'])


def process_slip_rate(row):
    if (row['Taza_des'] is not None) and ~np.isnan(row['Taza_des']):
        sr = '({},,)'.format(row['Taza_des'])
    elif (row['Tasa_Des'] is not None) and ~np.isnan(row['Taza_des']):
        sr = '({},,)'.format(row['Tasa_Des'])
    else:
        sr = None

    return sr


