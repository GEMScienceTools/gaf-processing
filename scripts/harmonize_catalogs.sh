ipython harmonize_catalogs.py


ogr2ogr -f "GMT" ../outputs/gmt/gem_active_faults_harmonized.gmt ../outputs/geojson/gem_active_faults_harmonized.geojson

ogr2ogr -f "KML" ../outputs/kml/gem_active_faults_harmonized.kml ../outputs/geojson/gem_active_faults_harmonized.geojson

cp ../outputs/geojson/gem_active_faults_harmonized.geojson ../../gem-global-active-faults/geojson/
cp ../outputs/geopackage/gem_active_faults_harmonized.gpkg ../../gem-global-active-faults/geopackage/

cp ../outputs/shapefile/gem_active_faults_harmonized.* ../../gem-global-active-faults/shapefile/

cp ../outputs/gmt/gem_active_faults_harmonized.gmt ../../gem-global-active-faults/gmt/
cp ../outputs/kml/gem_active_faults_harmonized.kml ../../gem-global-active-faults/kml/

