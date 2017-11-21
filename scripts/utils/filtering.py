import geopandas as gpd
import shapely.geometry as sg


def get_fault_inds_inside_other_dataset(inside_df, boundary_df):

    boundary_hull = sg.MultiLineString([f.geometry 
                                        for i, f in boundary_df.iterrows()]
                                       ).convex_hull

    faults_inside_idx = [boundary_hull.contains(f.geometry)
                          for i, f in inside_df.iterrows()]

    return inside_df.loc[faults_inside_idx].index
