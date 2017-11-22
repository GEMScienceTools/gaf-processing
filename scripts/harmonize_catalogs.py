import os
import geopandas as gpd


from utils.filtering import *

master_df = gpd.read_file('../outputs/geojson/gem_active_faults.geojson')
mdf_write_path = '../outputs/geojson/gem_active_faults_harmonized.geojson'


mdf = master_df.copy(deep=True)

def drop_bad_geometries(master_df, verbose=False):
    n_faults = master_df.shape[0]

    bad_geoms = [f.geometry is None for i, f in master_df.iterrows()]
    bad_geom_inds = master_df.loc[bad_geoms].index

    mdf = master_df.drop(bad_geom_inds)
    new_n_faults = mdf.shape[0]

    if verbose is True:
        print('Removed {} faults with bad geometries'.format(
                                                        n_faults-new_n_faults))
    return mdf


def filter_share_emme_overlap(master_df, verbose=False):
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


def filter_thailand_crossing_myanmar(master_df, verbose=False):

    thai_faults = master_df[master_df.catalog_name == 'thailand']
    myan_faults = master_df[master_df.catalog_name == 'myanmar']

    thai_myan_crossings = fault_intersection_inds(thai_faults, myan_faults)

    if verbose is True:
        print(thai_myan_crossings)

    mdf = master_df.drop(thai_myan_crossings)

    return mdf


def filter_himatibetmap_crossing_myanmar(master_df, verbose=False):

    hima_faults = master_df[master_df.catalog_name == 'HimaTibetMap']
    myan_faults = master_df[master_df.catalog_name == 'myanmar']

    hima_myan_crossings = fault_intersection_inds(hima_faults, myan_faults)

    if verbose is True:
        print(hima_myan_crossings)

    mdf = master_df.drop(hima_myan_crossings)

    return mdf


def filter_thailand_crossing_himatibetmap(master_df, verbose=False):

    thai_faults = master_df[master_df.catalog_name == 'thailand']
    hima_faults = master_df[master_df.catalog_name == 'HimaTibetMap']

    thai_hima_crossings = fault_intersection_inds(thai_faults, hima_faults)

    if verbose is True:
        print(thai_hima_crossings)

    mdf = master_df.drop(thai_hima_crossings)

    return mdf


print('Dropping faults with bad geometries')
mdf = drop_bad_geometries(mdf, verbose=True)

print('Filtering SHARE faults with EMME overlap...')
mdf = filter_share_emme_overlap(mdf)

print('Filtering Thailand faults that cross Myanmar faults...')
mdf = filter_thailand_crossing_myanmar(mdf)

print('Filtering HimatTibetMap faults that cross Myanmar faults...')
mdf = filter_himatibetmap_crossing_myanmar(mdf)

print('Filtering Thailand faults that cross HimatTibetMap faults...')
mdf = filter_thailand_crossing_himatibetmap(mdf)


try:
    os.remove(mdf_write_path)
except:
    pass

mdf.to_file(mdf_write_path, driver='GeoJSON')
