#!/bin/bash

DESTDIR=af_feats
mkdir -p $DESTDIR
#This dumps the phonewise AF feats in dir AF_feats_phone
$ESTDIR/../festival/examples/dumpfeats -relation Segment -feats etc/featnames festival/utts/*.utt -output $DESTDIR/%s.af

for file in `cat etc/filelist`;
do
    python ./bin/repeat_vector.py $file
done
