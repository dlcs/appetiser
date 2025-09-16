#!/bin/bash

export KDU_SRC_DIR=/kdu_src
export KDU_SRC=$KDU_SRC_DIR/kdu.tar

# Test if KDU tar is already present
if [ ! -f $KDU_SRC ]; then
  if [ ! -z $KDU_BINARIES ]; then
    uv run aws s3 cp $KDU_BINARIES $KDU_SRC
  else
    echo "ERROR: KDU_BINARIES env variable not set."
    exit 1
  fi
else
  echo "Using existing kdu binaries tar file."
fi

tar -xf $KDU_SRC -C $KDU_SRC_DIR

export KDU_LIB=/usr/local/lib/kdu
export KDU_COMPRESS=/usr/local/bin/kdu_compress
export KDU_EXPAND=/usr/local/bin/kdu_expand

mkdir -p $KDU_LIB

cp $KDU_SRC_DIR/kakadu-[0-9].[0-9].[0-9]/bin/Linux-x86-64-gcc/kdu_compress $KDU_COMPRESS
cp $KDU_SRC_DIR/kakadu-[0-9].[0-9].[0-9]/bin/Linux-x86-64-gcc/kdu_expand $KDU_EXPAND
cp $KDU_SRC_DIR/kakadu-[0-9].[0-9].[0-9]/lib/Linux-x86-64-gcc/* $KDU_LIB

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$KDU_LIB

cd $APPETISER_DIR
uv run uwsgi --http 0.0.0.0:8000 --master --need-app --module appetiser:app --processes 5 --http-timeout $HTTP_TIMEOUT
