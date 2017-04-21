#!/bin/bash
PHONELIST=festival/clunits/phonenames
SOURCE_DIR=af_feats/
TARGET_DIR=binary_af_feats/
rm -rf ${TARGET_DIR}
    cat etc/txt.done.data|
    awk '{print $2}'|
    while read file
      do
        echo $file
        python bin/af_binmapper.py $SOURCE_DIR/${file}.af ${TARGET_DIR} ${PHONELIST}
      done
