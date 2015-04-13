#!bin/bash

Model='T1tttt_1500_100'

homeDir='/scratch/mmasciov/CMSSW_7_2_3_GammaFunctions/src/MT2Analysis2015/analysis/'
inputDir=$homeDir'datacards_oldMT2bin_vOK2/'

thisDir=$PWD

for i in $(ls $inputDir)
do
    if [[ $i != *'datacards_'$Model* ]]
    then
	continue
    else 
	model=${i##*datacards_}
	echo $model
	r=0
	for d in $(ls $inputDir$i)
	do
	    if [[ $d != *'combine'* && $d != *'list'* && $d != *'partialCombination'* ]]
	    then
		region=${d##*datacard_}
		if [[ "$r" = "0" ]]
		then
		    TopoRegions[r]=${region%_m*}
		    listOfCards[r]=`ls $inputDir$i/datacard_${TopoRegions[$r]}*`
		    echo `combineCards.py ${listOfCards[$r]} > datacard_${model}_${TopoRegions[$r]}.txt`
		    echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt --noFitAsimov > log_${model}_${TopoRegions[$r]}_old_vOK2.txt`
		    echo `rm -f datacard_${model}_${TopoRegions[$r]}.txt higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    r=$(($r+1))
		elif [[ "$r" != "0" && "${region%_m*}" != "${TopoRegions[r-1]}" ]]
		then
		    TopoRegions[r]=${region%_m*}
		    listOfCards[r]=`ls $inputDir$i/*${TopoRegions[$r]}*`
		    echo `combineCards.py ${listOfCards[$r]} > datacard_${model}_${TopoRegions[$r]}.txt`
		    echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt --noFitAsimov > log_${model}_${TopoRegions[r]}_old_vOK2.txt`
		    echo `rm -f datacard_${model}_${TopoRegions[$r]}.txt higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    r=$(($r+1))
		fi
	    fi
	done

	unset TopoRegions
	unset listOfCards
    fi
done
