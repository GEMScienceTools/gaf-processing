from ast import literal_eval as leval
import json
import requests
import tempfile
import os
import numpy as np
import pandas as pd
import geopandas as gpd

# import catalog processing functions for each regional catalog
from .ata import process_ata
from .e_africa import process_e_africa
from .emme import process_emme
from .eur_share import process_eur_share
from .himatibetmap import process_htm
from .myanmar import process_myanmar
from .sara import process_sara
from .usgs_hazfaults import process_usgs_hazfaults
from .shyu_taiwan import process_taiwan
from .mexico import process_mexico
from .bird_pb import process_bird_pb
from .nz_litchfield import process_nz_litchfield
from .eos_se_asia import process_eos_se_asia
from .gaf import process_gaf

# This makes a dictionary of the imported processing master functions above
# to be called by the string version of the function
fn_dict = {}
fn_dict['process_ata'] = process_ata
fn_dict['process_e_africa'] = process_e_africa
fn_dict['process_emme'] = process_emme
fn_dict['process_eur_share'] = process_eur_share
fn_dict['process_htm'] = process_htm
fn_dict['process_myanmar'] = process_myanmar
fn_dict['process_sara'] = process_sara
fn_dict['process_usgs_hazfaults'] = process_usgs_hazfaults
fn_dict['process_taiwan'] = process_taiwan
fn_dict['process_mexico'] = process_mexico
fn_dict['process_bird_pb'] = process_bird_pb
fn_dict['process_nz_litchfield'] = process_nz_litchfield
fn_dict['process_eos_se_asia'] = process_eos_se_asia
fn_dict['process_gfe'] = process_gfe


def merge_regional_df_into_master(regional_df, master_df, merge_dict,
                                  catalog_name=None):
    """
    Merge a DataFrame of regional faults into the master catalog, using
    the `merge_dict` dictionary to describe the column conversions.

    Returns a new DataFrame.

    :param regional_df:
        Regional fault DataFrame.

    """

    merge_dict['catalog_id'] = 'catalog_id'

    merge_gen = (pd.Series({k:row[v] for k, v in merge_dict.items()})
                 for i, row in regional_df.iterrows())
    new_df = pd.concat(merge_gen, axis=1).T
    new_df['catalog_name'] = catalog_name
    
    return pd.concat((master_df, new_df), axis=0, ignore_index=True)


def get_catalogs_from_config(cfg_obj):
    """
    Returns a list of catalog names (strings) from the config object
    (`cfg_obj`) created from parsing the configuration file.
    
    The catalog names are listed in the `[config][catalogs]` variable.
    """

    cat_string = cfg_obj.get('config', 'catalogs')
    return list(filter(None, [x.strip(',') for x in cat_string.splitlines()]))


def process_catalog(catalog_name, cfg_obj, header_dict, master_df):
    """
    Master catalog processing and merging function.

    :param catalog_name:
        Name (string) of catalog in the catalog processing configuration file.

    :param cfg_obj:
        `configparser.ConfigParser()` object created from reading the config
        file.

    :param header_dict:
        Dictionary with column headers for the regional and master dataframes.
        Keys are master_df headers, values are regional catalog headers.

    :param master_df:
        Pandas DataFrame of master catalog.

    :returns master_df:
        Returns updated master catalog.
    """

    cfg_d = dict(cfg_obj[catalog_name])

    abbrev = cfg_d['abbrev']

    if 'gis_file' in cfg_d.keys():
        cat_df = gpd.read_file(cfg_d['gis_file'])

    elif 'gis_file_url' in cfg_d.keys():
        print('    downloading', cfg_d['header_match_key'], 'data')
        #tf = tempfile.NamedTemporaryFile()
        _make_dir('./tmp')
        with open('./tmp/temp.geojson', 'w') as tf:
            tf.write(requests.get(cfg_d['gis_file_url']).content.decode())
            cat_df = gpd.read_file(tf.name)

        os.remove('./tmp/temp.geojson')
        os.rmdir('./tmp')


    if 'extra_processing' in cfg_d:
        cat_df = fn_dict[cfg_d['extra_processing']](cat_df)

    cat_df = make_catalog_id(cat_df, abbrev, 
                             header_dict[cfg_d['header_match_key']])

    master_df = merge_regional_df_into_master(cat_df, master_df,
                                        header_dict[cfg_d['header_match_key']],
                                        catalog_name=cfg_d['catalog_name'])

    return master_df


def make_catalog_id(cat_df, abbrev, header_dict):

    if 'catalog_id' in header_dict.keys():
        _id = cat_df[header_dict['catalog_id']]

    else:
        _id = cat_df.index.tolist()

    id_list = ['{}_{}'.format(abbrev, i) for i in _id]

    cat_df['catalog_id'] = id_list
    
    return cat_df


def _make_dir(dirpath):
    try:
        os.makedirs(dirpath)
    except OSError:
        if not os.path.isdir(dirpath):
            raise
