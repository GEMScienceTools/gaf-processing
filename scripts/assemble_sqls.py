import shutil
import configparser
import json
import sqlalchemy as sqa
import numpy as np
import pandas as pd

from utils import catalog_conversions as cc

# Copy empty SQLite file to new master file and connect
base_schema_file = '../base_schema.sqlite'
master_sql = '../GEM_global_active_faults.sqlite'

shutil.copyfile(base_schema_file, master_sql)

master_eng = sqa.create_engine('sqlite:///{}'.format(master_sql))
master_df = pd.read_sql_table('GEM_Global_Active_Faults', master_eng)


## import dictionary to match catalog columns
cat_header_match_file = 'regional_catalog_header_matching.json'

with open(cat_header_match_file, 'r') as f:
    header_dict = json.load(f)

# load catalog processing configuration
cfg_file = './catalog_process_config.ini'
cfg = configparser.ConfigParser()
cfg.read(cfg_file)

# begin processing regional catalogs
catalog_list = cc.get_catalogs_from_config(cfg)

for catalog in catalog_list:
    if catalog in cfg.sections():
        print('processing {}'.format(catalog))
        master_df = cc.process_catalog(catalog, cfg, header_dict, master_df) 
