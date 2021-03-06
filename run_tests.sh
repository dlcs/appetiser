#!/bin/bash

aws s3 cp $KAKADU_APPS_LOCATION /kdu-apps.tar.gz


cd / && tar -xzvf /kdu-apps.tar.gz

export KDU_COMPRESS=/usr/local/bin/kdu_compress
export KDU_EXPAND=/usr/local/bin/kdu_expand
export KDU_LIB=/usr/local/bin

cd $APPETISER_DIR && pytest
