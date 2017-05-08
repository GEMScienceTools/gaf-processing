import shutil
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


# begin processing regional catalogs

## import dictionary to match catalog columns
cat_header_match_file = 'regional_catalog_header_matching.json'

with open(cat_header_match_file, 'r') as f:
    header_dict = json.load(f)

## North Africa
n_af_header_dict = header_dict['n_africa']
n_af_sql = '../regional_catalogs/ready_sqls/n_africa_active_faults.sqlite'
n_af_eng = sqa.create_engine('sqlite:///{}'.format(n_af_sql))
n_af_df = pd.read_sql_table('n_africa', n_af_eng)

master_df = cc.merge_regional_df_into_master(n_af_df, master_df,
                                             n_af_header_dict,
                                             catalog_name='GEM_n_africa')
