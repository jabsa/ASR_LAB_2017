#!/bin/bash

VOXDIR=
DESTDIR=$VOICEDIR/AF_feats_seq
mkdir -p $DESTDIR
cat $VOICEDIR/etc/txt.done.data |awk '{print $2}' >$VOICEDIR/etc/filelist
#This is used to extract feats for seq-2-seq models where inputs are 5 ms world feats and outputs are labels at the phone level
#Each row is one frame

for file in `cat ${VOICEDIR}/etc/filelist`;
do
#extract af feats
#extract world feats
done
