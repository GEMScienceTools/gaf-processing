#import shutil
import configparser
#import json
#import numpy as np
import pandas as pd
import geopandas as gpd
import logging


from utils import catalog_conversions as cc
from utils.data_checks import check_data


logfile = './data_check.log'
logging.basicConfig(filename=logfile,
                   level=logging.INFO,
                   filemode='w',
                   )

# import empty DF for the master database
master_df = pd.read_csv('../master_df_schema.csv', index_col=1)

## import ini file to match catalog columns
cat_header_match_file = 'regional_catalog_header_matching.ini'
header_cfg = configparser.ConfigParser()
header_cfg.read(cat_header_match_file)

# load catalog processing configuration
cfg_file = './catalog_process_config.ini'
cfg = configparser.ConfigParser()
cfg.read(cfg_file)

# begin processing regional catalogs
catalog_list = cc.get_catalogs_from_config(cfg)

for catalog in catalog_list:
    if catalog in cfg.sections():
        print('processing {}'.format(catalog))
        master_df = cc.process_catalog(catalog, cfg, header_cfg, master_df) 

master_df = gpd.GeoDataFrame(master_df) # convert to GeoPandas GeoDataFrame

print('checking data')

master_df = check_data(master_df)

print('writing output files')

logging.info('writing geojson')
master_df.to_file('../outputs/geojson/gem_active_faults.geojson',
                  driver="GeoJSON")

logging.info('writing geopackage')
master_df.to_file('../outputs/geopackage/gem_active_faults.gpkg',
                  driver="GPKG")

logging.info('writing shapefile')
master_df.to_file('../outputs/shapefile/gem_active_faults.shp',
                  driver="ESRI Shapefile")


