import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.geometry as sg


def get_fault_inds_inside_other_dataset(inside_df, boundary_df,
                                        inside_type='contains'):
    """
    Returns the indices of faults from a dataset (`inside_df`) that fall
    completely inside another fault dataset (`boundary_df`), where the
    boundary of the boundary_df is defined as a convex hull around all
    of the faults.

    Datasets are GeoPandas GeoDataFrames.

    Returns a (Geo)Pandas index of the errant faults.
    """

    boundary_hull = sg.MultiLineString([f.geometry
                                        for i, f in boundary_df.iterrows()]
                                       ).convex_hull

    if inside_type == 'contains':
        faults_inside_idx = [boundary_hull.contains(f.geometry)
                             for i, f in inside_df.iterrows()]

    elif inside_type == 'intersects':
        faults_contains_idx = [boundary_hull.contains(f.geometry)
                               for i, f in inside_df.iterrows()]
        faults_intersect_idx = [boundary_hull.crosses(f.geometry)
                                for i, f in inside_df.iterrows()]

        faults_inside_idx = [any(ins) for ins in zip(faults_contains_idx,
                                                     faults_intersect_idx)]

    return inside_df.loc[faults_inside_idx].index


def filter_faults_inside_other_dataset(master_df, remove_key, keep_key,
                                       inside_type='contains',
                                       verbose=False):

    boundary_df = master_df[master_df.catalog_name == keep_key]
    remove_df = master_df[master_df.catalog_name == remove_key]

    inside_inds = get_fault_inds_inside_other_dataset(remove_df, boundary_df,
                                                      inside_type=inside_type)

    if verbose is True:
        print(inside_inds)

    mdf = master_df.drop(inside_inds)

    return mdf


def fault_intersection_inds(remove_df, keep_df):

    def _crosses(kf, rf):
        try:
            return kf.geometry.crosses(rf.geometry)
        except ValueError:
            print(kf.index, kf.geometry)
            print(rf.index, rf.geometry)
            return False

    cross_list = np.array([np.array([_crosses(keep_f, remove_f)
                                     for i, keep_f in keep_df.iterrows()])
                           for j, remove_f in remove_df.iterrows()])

    cross_df = pd.DataFrame(cross_list, index=remove_df.index,
                            columns=keep_df.index)

    intersect_inds = cross_df.apply(lambda row: any(row), axis=1)

    return cross_df.loc[intersect_inds].index


def filter_faults_crossing_other_faults(master_df, remove_key, keep_key,
                                        verbose=False):

    remove_df = master_df[master_df.catalog_name == remove_key]
    keep_df = master_df[master_df.catalog_name == keep_key]

    crossing_inds = fault_intersection_inds(remove_df, keep_df)

    if verbose is True:
        print(crossing_inds)

    mdf = master_df.drop(crossing_inds)

    return mdf


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
