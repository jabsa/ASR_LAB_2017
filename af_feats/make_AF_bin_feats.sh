#!/bin/bash
TYPE=$1 #UTT/FRAME
if [ $TYPE == "UTT"]; then
   ext="af"
else
   ext="faf" 
fi

PHONELIST=festival/clunits/phonenames
SOURCE_DIR=af_feats/
TARGET_DIR=binary_af_feats/
rm -rf ${TARGET_DIR}
    cat etc/txt.done.data|
    awk '{print $2}'|
    while read file
      do
        echo $file
        python bin/AF_binmapper.py $SOURCE_DIR/${file}.$ext ${TARGET_DIR} ${PHONELIST}
      done
