#!bin/bash

homeDir='/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/'
thisDir=$PWD

if [ $thisDir != $homeDir ]
then
    cd $homeDir
fi

model=('T1bbbb_1500_100' 'T1bbbb_1000_900' 'T1tttt_1500_100' 'T1tttt_1200_800' 'T1qqqq_1400_100' 'T1qqqq_1000_800' 'T2bb_900_100' 'T2bb_600_580' 'T2tt_850_100' 'T2tt_650_325' 'T2tt_500_325' 'T2tt_425_325' 'T2qq_1200_100' 'T2qq_600_550')

model=('T2qq_600_550')

count=0

#setRegions=('' '_hiJet' '_hiJet_hiHT' '_loJet_hiHT' '_hiJet_mergeHT')
#setRegions=('_10fb' '_hiJet_10fb' '_hiJet_hiHT_10fb' '_loJet_hiHT_10fb' '_hiJet_mergeHT_10fb')
#setRegions=('_noMT' '_hiJet_noMT' '_hiJet_hiHT_noMT' '_loJet_hiHT_noMT' '_hiJet_mergeHT_noMT')
setRegions=('_loJet_hiHT_noMT_MT2final' '_loJet_hiHT_noMT_oldMT2bin_vOK2')
r=0

while [ "x${model[count]}" != "x" ]
do

    #echo ${model[count]}
    localDir='limits_'${model[count]}${setRegions[r]}
    #echo $localDir
    mkdir $localDir

    cd $homeDir

    remoteDir='Limits'${setRegions[r]}
    for i in $(ls /pnfs/psi.ch/cms/trivcat/store/user/mmasciov/$remoteDir/None/crab_${model[count]}${setRegions[r]}/*/*/outputToy_*) 
    do 
	remoteFile=${i##*user/}
	echo `srmcp $SRMUSER$remoteFile file:///${localDir}/${i##*0000/}`
	#srmcp $SRMUSER$remoteFile file:///${locaDir}/${i##*0000/}
	cd $localDir 
	tar xvzf ${i##*0000/} 
	rm -f ${i##*0000/} 
	cd - 
    done

    cd $localDir
    for out in $(ls -d outputToy_*) 
    do 
    	cp $out/higgsCombine* ./ 
    	rm -rf $out 
    done
    
    hadd higgsCombine_${model[count]}_hadd.root higgsCombine*HybridNew* 
    
    logfile='log_'${model[count]}'.txt'
    combine -M HybridNew --frequentist $homeDir/datacard_${model[count]}${setRegions[r]}.root --readHybridResult --grid=higgsCombine_${model[count]}_hadd.root --expectedFromGrid=0.5 --interpAcc 0.01 >& $logfile
    
    cd $homeDir
    
    count=$(( $count + 1 ))

done
unset model