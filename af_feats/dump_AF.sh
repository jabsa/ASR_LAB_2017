#!/bin/bash

DESTDIR=af_feats
mkdir -p $DESTDIR
#This dumps the phonewise AF feats in dir AF_feats_phone
$ESTDIR/../festival/examples/dumpfeats -relation Segment -feats etc/featnames festival/utts/*.utt -output $DESTDIR/%s.daf

cat etc/txt.done.data |awk '{print $2}' >etc/filelist
for file in `cat etc/filelist`;
do
    python ./bin/get_AF_feats.py $file
done
./bin/check_faf.sh
