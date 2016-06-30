#!/bin/bash

echo $#;
if [ $# -ge 2 ]; then
    echo "USAGE: ${0} [QUEUE]";
    exit;
fi

if [ $# -ge 1 ]
then
    QUEUE=$1
else 
    QUEUE="short.q"
fi

echo "QUEUE="$QUEUE

source $VO_CMS_SW_DIR/cmsset_default.sh
#source //mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
#echo `voms-proxy-init -voms cms --valid 168:00`

homeDir=$PWD
inputDir="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2015plus2016_uncorr/"

thisDir=$PWD

for i in $(ls $inputDir)
do
    if [[ $i != *'T1tttt'* ]]
    then
        continue
    else 
        MODEL=${i##*datacard_}
	MODEL=${MODEL%_2p3ifb.txt}

	echo "MODEL="$MODEL

	if [ -e "/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/log_${MODEL}_2p3ifb.txt" ]
	then
	    echo "file exists for ${MODEL}, don't run"
	else
	    command=`qsub -q ${QUEUE} -o /dev/null -e /dev/null -N asymptoticLimit_${MODEL} /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/combine_Asymptotic_ScanT1tttt.sh $MODEL`
	    echo $command
	fi

#	echo `mkdir -p /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/Limits_T1tttt_2p1ifb_sigSyst/`
#	cd /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/Limits_T1tttt_2p1ifb_sigSyst/
#
#	command=`qsub -q ${QUEUE} -o $PWD/asymptoticLimit_${MODEL}.out -e $PWD/asymptoticLimit_${MODEL}.err -N asymptoticLimit_${MODEL} /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/combineAsymptotic_Scan.sh $MODEL`
#	echo "Submitting limits for signal "${MODEL}
#        echo $command
#	
#	cd $thisDir
 
    fi
done