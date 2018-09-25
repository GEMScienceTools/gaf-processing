rm ../outputs/geojson/gem_active_faults.* 
rm ../outputs/geopackage/gem_active_faults.* 
rm ../outputs/shapefile/gem_active_faults.*
rm ../outputs/gmt/gem_active_faults.*
rm ../outputs/kml/gem_active_faults.*

ipython assemble_catalogs.py


ogr2ogr -f "GMT" ../outputs/gmt/gem_active_faults.gmt ../outputs/geojson/gem_active_faults.geojson

ogr2ogr -f "KML" ../outputs/kml/gem_active_faults.kml ../outputs/geojson/gem_active_faults.geojson

cp ../outputs/geojson/gem_active_faults.geojson ../../gem-global-active-faults/geojson/
cp ../outputs/geopackage/gem_active_faults.gpkg ../../gem-global-active-faults/geopackage/

cp ../outputs/shapefile/gem_active_faults.* ../../gem-global-active-faults/shapefile/

cp ../outputs/gmt/gem_active_faults.gmt ../../gem-global-active-faults/gmt/
cp ../outputs/kml/gem_active_faults.kml ../../gem-global-active-faults/kml/

