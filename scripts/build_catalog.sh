rm ../outputs/geojson/gem_active_faults.* 
rm ../outputs/geopackage/gem_active_faults.* 
rm ../outputs/shapefile/gem_active_faults.*

ipython assemble_catalogs.py

cp ../outputs/geojson/gem_active_faults.geojson ../../gem-global-active-faults/geojson/
cp ../outputs/geopackage/gem_active_faults.gpkg ../../gem-global-active-faults/geopackage/

cp ../outputs/shapefile/gem_active_faults.* ../../gem-global-active-faults/shapefile/
