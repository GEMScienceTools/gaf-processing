import os
import json
import sqlalchemy as sqa
import numpy as np
import pandas as pd


# Connect to master 
master_sql = '../gem_active_fault_db/sql/GEM_global_active_faults.sqlite'
master_eng = sqa.create_engine('sqlite:///{}'.format(master_sql))

master_df = pd.read_sql_table('base_schema', master_eng)




n_africa_merge_dict = {'WKT_GEOMETRY': 'WKT_GEOMETRY',
                       'accuracy': 'accuracy',
                       'average_dip': 'ns_average_dip',
                       'activity_confidence': 'ns_is_active',
                       'name': 'ns_name',
                       'dip_dir': 'ns_dip_dir',
                       'downthrown_side_dir': 'ns_downthrown_side_id',
                       'last_movement': 'ns_last_movement',
                       'net_slip_rate': 'ns_net_slip_rate',
                       'strike_slip_rate': 'ns_strike_slip_rate',
                       'vert_slip_rate': 'ns_vert_slip_rate',
                       'fz_name': 'fs_name',
                       'slip_type': 'slip_type',
                       'average_rake': 'ns_average_rake',
                       'reference': 'reference',
                       'exposure_quality': 'ns_exposure_quality',
                       'epistemic_quality': 'ns_epistemic_quality',
                       'shortening_rate': 'ns_shortening_rate',
                       'notes': 'notes',
                       }


c_am_merge_dict = n_africa_merge_dict






n_af_sql = '../gis/regional_catalogs/n_africa.sqlite'
n_af_eng = sqa.create_engine('sqlite:///{}'.format(n_af_sql))
n_af_df = pd.read_sql_table('n_africa', n_af_eng)
