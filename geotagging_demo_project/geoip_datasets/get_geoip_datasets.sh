 #!/bin/sh

wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCity.dat.gz
wget http://geolite.maxmind.com/download/geoip/database/GeoLiteCountry/GeoIP.dat.gz

gunzip -d GeoIP.dat.gz
gunzip -d GeoLiteCity.dat.gz
