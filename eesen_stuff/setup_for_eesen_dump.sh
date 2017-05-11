#!/bin/bash

DESTDIR=$1

cp featnames2 ${DESTDIR}/etc/
cp featnames_indic ${DESTDIR}/etc/
cp make_lexicon.sh ${DESTDIR}/bin
cp make_dict.py ${DESTDIR}/bin
cp units/*.txt ${DESTDIR}/etc
