import geopandas as gpd

from utils.filtering import *

master_df = gpd.read_file('../outputs/geojson/gem_active_faults.geojson')

mdf = master_df.copy(deep=True)

def filter_share_emme_overlap(master_df):
    """
    Filters out faults from the SHARE catalog where they fall within
    the polygon defined by the newer EMME catalog.
    """
    emme_faults = master_df[master_df.catalog_name == 'EMME']
    share_faults = master_df[master_df.catalog_name == 'SHARE']
    
    share_in_emme_idx = get_fault_inds_inside_other_dataset(share_faults,
                                                            emme_faults)
    mdf = master_df.drop(share_in_emme_idx)

    return mdf

mdf = filter_share_emme_overlap(mdf)

mdf.to_file('../outputs/geojson/gem_active_faults_harmonized.geojson',
            driver='GeoJSON')
