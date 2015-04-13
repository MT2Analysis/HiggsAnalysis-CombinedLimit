#!bin/bash

#homeDir='/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/'
#inputDir=$homeDir'datacards_PHYS14_v3_CSA14_finalSynchronization/'

homeDir='/scratch/mmasciov/CMSSW_7_2_3_GammaFunctions/src/MT2Analysis2015/analysis/'
#inputDir=$homeDir'datacards_PHYS14_v3_AN_purity/'
#inputDir=$homeDir'datacards_PHYS14_v3_hiJet_noMT/'
#inputDir=$homeDir'datacards_PHYS14_v3_hiJet_hiHT_noMT/'
#inputDir=$homeDir'datacards_PHYS14_v3_loJet_hiHT_20fb/'
#inputDir=$homeDir'datacards_PHYS14_v3_hiJet_hiHT_10fb/'
#inputDir=$homeDir'datacards_PHYS14_v3_loJet_hiHT_noMT_10fb/'
#inputDir=$homeDir'datacards_PHYS14_v3_hiJet_mergeHT_noMT_10fb/'
#inputDir=$homeDir'datacards_newMT2bin_50GeV_vOK2/'
#inputDir=$homeDir'datacards_oldMT2bin_vOK3/'
inputDir=$homeDir'datacards_MT2final/'

thisDir=$PWD

for i in $(ls $inputDir)
do
    if [[ $i != *'datacards_T'* ]]
    then
	continue
    else 
	model=${i##*datacards_}
	#echo $model
	c=0
	for d in $(ls $inputDir$i)
	do
	    if [[ $d != *'combine'* ]]
	    then
		cards[c]=$d
		c=$(($c+1))
	    fi
	done;
	#echo ${cards[*]}
	cd $inputDir$i
	echo `combineCards.py ${cards[*]} > datacard_combine.txt`
	echo `text2workspace.py $inputDir$i/datacard_combine.txt -b -o $inputDir$i/datacard_combine.root`
	unset cards 
	#cd $homeDir
	cp $inputDir$i/datacard_combine.root $thisDir/datacard_${model}_loJet_hiHT_noMT_MT2final.root
	#cp $inputDir$i/datacard_combine.root $thisDir/datacard_${model}_loJet_hiHT_noMT_oldMT2bins_vOK.root
    fi
done
