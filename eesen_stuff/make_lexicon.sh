#!/bin/bash

#This file should be run to create the required files for training AF feats in the voicedir
#First run:
#setup_for_eesen_dump.sh $VOICEDIR
#Assumes af_feats have already been extracted
VOXNAME=$(basename `pwd`)

#Dump all the words and their phones
mkdir -p eesen_utils/lang_phn
mkdir -p eesen_utils/train
mkdir -p eesen_utils/testdir

mkdir feats_for_dict
$ESTDIR/../festival/examples/dumpfeats -relation Segment -feats etc/featnames2 festival/utts/*.utt -output feats_for_dict/%s.word
cat feats_for_dict/*.word > etc/all.word


#Create the AF-to phone map and the corresponding units for each AF
cat etc/featnames_indic|awk '{print $1}'|tail -n +2|cut -d '_' -f2|sed '/^$/d'>etc/aflist
cat festvox/${VOXNAME}_phoneset.scm|grep "-"|awk '{if (NF>12) print $0}'|sed 's+[()]++g'|sed 's/^[ \t]*//g' >etc/phone_feats
count=2
for i in `cat etc/aflist`; 
do
echo $i
cat etc/phone_feats|awk -v c=$count '{print $1, $c}' >etc/${i}.txt
##make_dict.py all.word, units.txt, phone-af-map, outfilename
python bin/make_dict.py  etc/all.word etc/${i}_units.txt etc/${i}.txt eesen_utils/lang_phn/${i}_lexicon_numbers.txt
cat etc/${i}_units.txt|sed '/666/d'|sed '/^\s*$/d' > eesen_utils/lang_phn/${i}_units.txt
count=$(($count+1))
echo $count
done

#Make the other stuff required for eesen- TEXT UTT2SPK, SPK2UTT and
cat etc/txt.done.data|cut -d '(' -f2-|cut -d ')' -f1|sed 's+"++g'|tr -s '[:space:]'|sed 's/^[ \t]*//g' >eesen_utils/train/text

cat etc/txt.done.data|awk '{print $2}' >etc/filelist
cat etc/filelist|sed 's+^+/data/ASR1/tools/sox-14.4.2/src/sox /home/pbaljeka/multilingual_wavs/hindi/+g'|sed 's/$/.wav -t wav - |/g'>etc/wavscp
paste -d ' ' etc/filelist etc/filelist >eesen_utils/train/utt2spk
paste -d ' ' etc/filelist etc/filelist >eesen_utils/train/spk2utt
paste -d ' ' etc/filelist etc/wavscp >eesen_utils/train/wav.scp
