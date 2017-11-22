import geopandas as gpd
import pandas as pd
import numpy as np

from utils.filtering import *

my = gpd.read_file('../regional_catalogs/ready_geojsons/myanmar.geojson')
th = gpd.read_file('../regional_catalogs/ready_geojsons/thailand.geojson')

cx = fault_intersection_inds(my, th)
