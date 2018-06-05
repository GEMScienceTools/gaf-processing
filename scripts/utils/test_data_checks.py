import logging

import pandas as pd
import geopandas as gpd
from data_checks import *# check_value


logfile = './test_data_checks.log'

logging.basicConfig(filename=logfile,
                    level=logging.INFO,
                    )


#mdf_path = '../../../gem-global-active-faults/geojson/gem_active_faults_harmonized.geojson'
mdf_path = '../../outputs/geojson/gem_active_faults_harmonized.geojson'
mdf = gpd.read_file(mdf_path)
    

for column in check_val_funcs.keys():
    print('checking {}'.format(column))
    logging.info('checking {}'.format(column))
    check_results = [check_value(row, idx, column, change_val=True)
                     for idx, row in mdf.iterrows()]
    changes = []
    change_idxs = []
    for cr in check_results:
        if cr is not None:
            if cr[1] is not None:
                change_idxs.append(cr[0])
                changes.append(cr[1])

    mdf.at[change_idxs, column] = changes

mdf.to_file('../../outputs/geojson/gem_active_faults_corrected.geojson',
            driver='GeoJSON')
