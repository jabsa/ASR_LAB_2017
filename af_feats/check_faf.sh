#!/bin/bash

for i in `cat etc/filelist`; 
do
echo $i
cat af_feats/${i}.faf|awk '{print $1}' >a
tac festival/coeffs/${i}.feats|awk '{print $1}'|cut -d '_' -f1 >b
diff a b
done
