#!bin/bash

#Model=('T1bbbb_fullScan_900_850' 'T1bbbb_fullScan_1600_0' 'T1bbbb_fullScan_1400_900')

Model=($1)

homeDir='/scratch/mmasciov/'
inputDir=$homeDir'datacards_'${Model[0]}'/'

thisDir=$PWD
copyDir=$thisDir'/ranking_'${Model[0]}'/'

workDir='/scratch/mmasciov/ranking_'${Model[0]}'/'

mkdir -p $workDir
cd $workDir

c=0
while [ "x${Model[c]}" != "x" ]
#for i in $(ls $inputDir)
do
#    if [[ $i != *'datacard_'*$Model* ]]
#    then
#	continue
#    else 
	model=${Model[$c]}
#	model=${i##*datacards_}
#	echo $model
	r=0
	for d in $(ls $inputDir*'datacard_'*${Model[$c]}*)
	do
	    if [[ $d != *'combine'* && $d != *'list'* && $d != *'partialCombination'* ]]
	    then
		region=${d##*datacard_}
		if [[ "$r" = "0" ]]
		then
		    TopoRegions[r]=${region%_m*}
		    listOfCards[r]=`ls $inputDir/datacard_${TopoRegions[$r]}*${model}*`
		    echo `combineCards.py ${listOfCards[$r]} > datacard_${model}_${TopoRegions[$r]}.txt`
		    #echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt --noFitAsimov > log_${model}_${TopoRegions[$r]}_Paper.txt`
		    echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt > log_${model}_${TopoRegions[$r]}_Paper_post.txt`
		    echo `rm -f datacard_${model}_${TopoRegions[$r]}.txt higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    r=$(($r+1))
		elif [[ "$r" != "0" && "${region%_m*}" != "${TopoRegions[r-1]}" ]]
		then
		    TopoRegions[r]=${region%_m*}
		    listOfCards[r]=`ls $inputDir/*${TopoRegions[$r]}*${model}*`
		    echo `combineCards.py ${listOfCards[$r]} > datacard_${model}_${TopoRegions[$r]}.txt`
		    #echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt --noFitAsimov > log_${model}_${TopoRegions[r]}_Paper.txt`
		    echo `combine -M Asymptotic datacard_${model}_${TopoRegions[$r]}.txt > log_${model}_${TopoRegions[r]}_Paper_post.txt`
		    echo `rm -f datacard_${model}_${TopoRegions[$r]}.txt higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    r=$(($r+1))
		fi
	    fi
	done

	unset TopoRegions
	unset listOfCards
#    fi
    
     c=$(( $c + 1 ))
done
unset Model
