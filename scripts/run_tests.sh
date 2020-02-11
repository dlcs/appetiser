#!/bin/bash

$APPETISER_DIR/scripts/_get_kdu.sh
$APPETISER_DIR/scripts/_get_opj.sh

cd $APPETISER_DIR && pytest
