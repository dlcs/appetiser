#!/bin/sh

. $APPETISER_DIR/scripts/_get_kdu.sh
. $APPETISER_DIR/scripts/_get_opj.sh

cd $APPETISER_DIR
uwsgi --http 0.0.0.0:80 --master --need-app --module appetiser:appetiser --processes 5
