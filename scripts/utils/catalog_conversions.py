from ast import literal_eval as leval
import json
import sqlalchemy as sqa
import numpy as np
import pandas as pd

# import catalog processing functions for each regional catalog
from .ata import process_ata
from .e_africa import process_e_africa
from .emme import process_emme

def merge_regional_df_into_master(regional_df, master_df, merge_dict,
                                  catalog_name=None):
    """
    Merge a DataFrame of regional faults into the master catalog, using
    the `merge_dict` dictionary to describe the column conversions.

    Returns a new DataFrame.

    :param regional_df:
        Regional fault DataFrame.

    """
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

    cat_engine = sqa.create_engine('sqlite:///{}'.format(cfg_d['sql_file']))
    cat_df = pd.read_sql_table(cfg_d['table_name'], cat_engine)

    if 'extra_processing' in cfg_d:
        cat_df = eval('{}(cat_df)'.format(cfg_d['extra_processing']))

    master_df = merge_regional_df_into_master(cat_df, master_df,
                                        header_dict[cfg_d['header_match_key']],
                                        catalog_name=cfg_d['catalog_name'])
    cat_engine.dispose()

    return master_df


