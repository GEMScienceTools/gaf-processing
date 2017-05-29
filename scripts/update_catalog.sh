rm ../outputs/geojson/gem_active_faults.* ../outputs/shapefile/gem_active_faults.*

ipython assemble_catalogs.py

cp ../outputs/geojson/gem_active_faults.geojson ../../gem-global-active-faults/geojson/

cp ../outputs/shapefile/gem_active_faults.* ../../gem-global-active-faults/shapefile/
