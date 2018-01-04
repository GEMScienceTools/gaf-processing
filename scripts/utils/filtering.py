import numpy as np
import pandas as pd
import geopandas as gpd
import shapely.geometry as sg


def get_fault_inds_inside_other_dataset(inside_df, boundary_df):
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

    faults_inside_idx = [boundary_hull.contains(f.geometry)
                         for i, f in inside_df.iterrows()]

    return inside_df.loc[faults_inside_idx].index


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
