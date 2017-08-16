import pandas as pd
import geopandas as gpd
from data_checks import *# check_value

print('loading data')
mdf = gpd.read_file('../../../gem-global-active-faults/geojson/gem_active_faults.geojson')


#print(check_average_dip('(89,89,90)'))
#print(check_average_dip('(88,89,90)'))
#print(check_average_dip('(89,89,90.5)'))
#print(check_average_dip('(89,,)'))


for val_type in check_val_funcs.keys():
    print('checking {}'.format(val_type))
    _ = [check_value(val, idx, val_type, change_val=False)
         for idx, val in mdf[val_type].iteritems()]
