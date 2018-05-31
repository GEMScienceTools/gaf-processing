import logging

import pandas as pd
import geopandas as gpd
from data_checks import *# check_value


logfile = './test_data_checks.log'

logging.basicConfig(filename=logfile,
                    level=logging.DEBUG,
                    )


mdf = gpd.read_file('../../../gem-global-active-faults/geojson/gem_active_faults_harmonized.geojson')


#print(check_average_dip('(89,89,90)'))
#print(check_average_dip('(88,89,90)'))
#print(check_average_dip('(89,89,90.5)'))
#print(check_average_dip('(89,,)'))


for column in check_val_funcs.keys():
    print('checking {}'.format(column))
    logging.info('checking {}'.format(column))
    _ = [check_value(row, idx, column, change_val=False)
         for idx, row in mdf[[column, 'catalog_name']].iterrows()]
