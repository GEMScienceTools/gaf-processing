rm ../outputs/geojson/gem_active_faults.* 
rm ../outputs/geopackage/gem_active_faults.* 
rm ../outputs/shapefile/gem_active_faults.*
rm ../outputs/gmt/gem_active_faults.*
rm ../outputs/kml/gem_active_faults.*

ipython assemble_catalogs.py


org2ogr -f "GMT" ../outputs/gmt/gem_active_faults.gmt ../outputs/gem_active_faults.geojson

org2ogr -f "KML" ../outputs/gmt/gem_active_faults.kml ../outputs/gem_active_faults.geojson

cp ../outputs/geojson/gem_active_faults.geojson ../../gem-global-active-faults/geojson/
cp ../outputs/geopackage/gem_active_faults.gpkg ../../gem-global-active-faults/geopackage/

cp ../outputs/shapefile/gem_active_faults.* ../../gem-global-active-faults/shapefile/
