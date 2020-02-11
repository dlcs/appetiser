#!/bin/sh

if [ -z "$OPENJPEG_APPS_LOCATION" ]
then
      echo "\$OPENJPEG_APPS_LOCATION has not been set"
else
    aws s3 cp $OPENJPEG_APPS_LOCATION /opj-apps.tar.gz
    cd / && tar -xzvf /opj-apps.tar.gz
    export OPJ_COMPRESS=/bin/opj_compress
    export OPJ_DECOMPRESS=/bin/opj_decompress
fi
