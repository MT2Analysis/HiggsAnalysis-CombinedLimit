#!/bin/bash

homeDir='/scratch/mmasciov/'
inputDir=$homeDir'cards_T2tt_200_0/'
thisDir=$PWD

model='T2tt_200_0'

c=0
for d in $(ls -rt $inputDir/datacard_*HT575to1000*)
do
    echo $d
    if [[ $d != *'combine'* ]] && [[ $d != *'j1'* ]]
#    if [[ $d != *'combine'* ]]
    then
	cards[c]=$d
	c=$(($c+1))
    fi
done

echo ${cards[*]}
cd $inputDir
echo `combineCards.py -S ${cards[*]} > datacard_combine.txt`
echo `text2workspace.py $inputDir$i/datacard_combine.txt -b -o $inputDir$i/datacard_combine.root`
unset cards 
	#cd $homeDir

	#cp $inputDir$i/datacard_combine.txt $thisDir/datacard_${model}_DM.txt
cp $inputDir$i/datacard_combine.root $thisDir/datacard_${model}_mediumHT_redEff.root

