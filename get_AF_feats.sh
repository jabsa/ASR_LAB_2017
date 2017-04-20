#!/bin/bash

VOXDIR=$1
DESTDIR=$VOXDIR/af_feats
mkdir -p $DESTDIR
#This dumps the phonewise AF feats in dir AF_feats_phone
$ESTDIR/../festival/examples/dumpfeats -relation Segment -feats featnames $VOXDIR/festival/utts/*.utt -output $DESTDIR/%s.af
