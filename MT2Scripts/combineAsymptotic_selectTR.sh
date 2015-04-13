#!bin/bash

Model=('T1bbbb_1500_100' 'T1bbbb_1000_900' 'T1tttt_1500_100' 'T1tttt_1200_800' 'T1qqqq_1400_100' 'T1qqqq_1000_800' 'T2bb_900_100' 'T2bb_600_580' 'T2tt_850_100' 'T2tt_650_325' 'T2tt_500_325' 'T2tt_425_325' 'T2qq_1200_100' 'T2qq_600_550')

count=0

homeDir='/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/'

cardDir='/scratch/mmasciov/CMSSW_7_2_3_GammaFunctions/src/MT2Analysis2015/analysis/'
cardDir=$cardDir'datacards_newMT2bin_50GeV_vOK/'

thisDir=$PWD'/'

while [ "x${Model[count]}" != "x" ]
do

filename=$homeDir'AsymptoticRanking_'${Model[$count]}'_new_vOK.txt'

listOfTR=(`python <<END
a={}
for line in open('$filename'):
   a[float(line.split()[1])]=line.split()[0]
limits=a.keys()
limits.sort()
for l in limits:
   print a[l]
END`)

listOfLimits=(`python <<END
a={}
for line in open('$filename'):
   a[float(line.split()[1])]=line.split()[0]
limits=a.keys()
limits.sort()
for l in limits:
   print l
END`)

#echo ${listOfTR[*]}
#
#for i in ${listOfTR[*]}
#do
#    echo $i
#done

#cd $cardDir
for i in $(ls $cardDir)
do
    if [[ $i != *'datacards_'${Model[$count]}* ]]
    then
	continue
    else 
	model=${i##*datacards_}
	echo $model
	r=0
	s=0
	for d in $(ls $cardDir$i)
	do
	    if [[ $d != *'combine'* ]]
	    then
		#echo $r
		cd $cardDir$i
		region=${listOfTR[r]}
		#echo $region
		if [[ "$r" = "0" ]]
		then
		    TopoRegions[r]=${region%_m*}
		    #echo ${TopoRegions[$r]}
		    listOfCards[r]=`ls $cardDir$i/datacard_${TopoRegions[$r]}*`
		    #echo ${listOfCards[$r]}
		    echo `rm -f datacard_${model}_partialCombination2_*.txt log_${model}_*_list.txt`
		    echo `combineCards.py ${listOfCards[$r]} > datacard_${model}_partialCombination2_${r}.txt`
		    echo `combine -M Asymptotic datacard_${model}_partialCombination2_${r}.txt --noFitAsimov > log_${model}_${TopoRegions[$r]}_list.txt`
		    echo `rm -f higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    bestLimit=`grep "50.0%" log_${model}_${TopoRegions[$r]}_list.txt | awk '{print $5}'`
		    echo $bestLimit
		    firstLimit=$bestLimit
		    LastLimit=$bestLimit
		    ThisLimit=$bestLimit
		    t=$r
		    r=$(($r+1))	
		    s=$(($s+1))
		elif [[ "$r" != "0" && "${region%_m*}" != "${TopoRegions[r-1]}" ]]
		then
		    TopoRegions[$r]=${region%_m*}
		    #echo ${TopoRegions[$r]}
		    listOfCards[$r]=`ls $cardDir$i/*${TopoRegions[r]}*`
		    echo `combineCards.py ${listOfCards[$r]} datacard_${model}_partialCombination2_${t}.txt > datacard_${model}_partialCombination2_${r}.txt`
		    echo `combine -M Asymptotic datacard_${model}_partialCombination2_${r}.txt --noFitAsimov > log_${model}_${TopoRegions[$r]}_list.txt`
		    echo `rm -f higgsCombineTest.Asymptotic.mH120.root roostats-*`
		    region=${i##*log_T1bbbb_1000_900_}
		    region=${region%_old_vOK.txt*}
		    lastlog='log_'${model}'_'${TopoRegions[$t]}'_list.txt'
		    #echo $lastlog
		    lastLimit=`grep "50.0%" $lastlog | awk '{print $5}'`
		    #echo $lastLimit
		    thislog='log_'${model}'_'${TopoRegions[$r]}'_list.txt'
		    #echo $thislog
		    thisLimit=`grep "50.0%" $thislog | awk '{print $5}'`
		    #echo $thisLimit
		    FirstLimit=$firstLimit
		    LastLimit=(`python<<END
if float(${listOfLimits[$r]})-float($firstLimit) > float($bestLimit):
    print $ThisLimit
else:
    print $LastLimit
END`)
		    ThisLimit=(`python<<END
if float(${listOfLimits[$r]})-float($firstLimit) > float($bestLimit):
    print $thisLimit
else:
    print $ThisLimit
END`)
		    s=(`python <<END
if float(${listOfLimits[$r]})-float($firstLimit) > float($bestLimit):
    print $r
else:
    print $s
END`)
		    firstLimit=(`python <<END
if float(${listOfLimits[$r]})-float($firstLimit) > float($bestLimit):
    print ${listOfLimits[$r]}
else:
    print $firstLimit
END`)
		    #echo $firstLimit
		    #echo ${listOfLimits[$r]}
		    #echo $ThisLimit
		    #echo $LastLimit
		    lastRegion=(`python <<END
isThisRegion="True"
R=float($ThisLimit)/float($LastLimit)
if R > 0.99 and float(${listOfLimits[$r]})-float($FirstLimit) > float($bestLimit):
    isThisRegion="False"
print isThisRegion
END`)
		    if [ $lastRegion != "True" ]
		    then
			#echo 'Last region improving exclusion limit by >1% is' ${TopoRegions[$t]} ', i.e., after' $r 'regions!'
			echo `rm -f datacard_${model}_partialCombination2_*.txt log_${model}_*_list.txt`
			#r=0
			#t=$r
			break
		    fi
		    t=$r
		    r=$(($r+1))
		fi
	    fi
	done
	
	cd $cardDir$i
	echo `rm -f datacard_combine_reduced2.*`
	echo $s $r
	for ((rr=$s;rr<=$r;++rr))
	do
	    unset listOfCards[$rr]
	done
	echo `combineCards.py ${listOfCards[*]} > datacard_combine_reduced2.txt`
        echo `text2workspace.py $cardDir$i/datacard_combine_reduced2.txt -b -o $cardDir$i/datacard_combine_reduced2.root`
		
	unset TopoRegions
	unset listOfCards
	unset listOfTR
	unset listOfLimits
	
	cp $cardDir$i/datacard_combine_reduced2.root $thisDir/datacard_${model}_loJet_hiHT_noMT_newMT2bins_50GeV_vOK_reduced2.root
	cp $cardDir$i/datacard_combine_reduced2.txt $thisDir/datacard_${model}_loJet_hiHT_noMT_newMT2bins_50GeV_vOK_reduced2.txt

    fi
done

count=$(( $count + 1 ))

done
unset Model