#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# -le 2 ]; then
    echo "USAGE: ${0} MODEL job Njobs singlePoint";
    exit;
fi

MODEL=$1
JOB=$2
NJobs=$3
SinglePoint=$4

source $VO_CMS_SW_DIR/cmsset_default.sh
source /swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc481
export LD_LIBRARY_PATH=/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH
echo "Loading CMSSW_7_1_5/"
cd /shome/mmasciov/CMSSW_7_1_5/src/
eval `scramv1 runtime -sh`
eval `cmsenv`

cd /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/Limits_Expected_loJet_hiHT_10fb/

##T1-like
#echo "combine -M HybridNew --testStat LHC --clsAcc 0 --frequentist -T 1000 -i 20 --saveHybridResult --saveToys --fullBToys -v -1 -n ${MODEL}_${JOB} -s ${JOB}  /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/datacards_PHYS14_v3_CSA14_finalSynchronization/datacards_$MODEL/datacard_combine.root"

#command=`combine -M HybridNew --testStat LHC --clsAcc 0 --frequentist -T 1000 -i 20 --saveHybridResult --saveToys --fullBToys -v -1 -n ${MODEL}_${JOB} -s ${JOB}  /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/datacards_PHYS14_v3_CSA14_finalSynchronization/datacards_${MODEL}/datacard_combine.root`

command_1=`combine /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/datacard_${MODEL}_loJet_hiHT_10fb.root  -M GenerateOnly -t -1 --expectSignal 0 --saveToys -n ${MODEL}_${JOB}`
command=`combine /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/datacard_${MODEL}_loJet_hiHT_10fb.root --toysFile higgsCombine${MODEL}_${JOB}.GenerateOnly.mH120.123456.root -t -1 -M HybridNew --testStat LHC --clsAcc 0 --frequentist -T 250 -i 5 -s ${JOB} --saveHybridResult --saveToys --fullBToys -v -1 -n ${MODEL}_${JOB} --singlePoint ${SinglePoint} >& log_${MODEL}_${JOB}.txt`

echo $command_1
echo $command

#copy="cp output /shome/"