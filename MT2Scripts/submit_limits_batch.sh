#!/bin/bash

echo $#;
if [ $# -le 1 ]; then
    echo "USAGE: ${0} MODEL Njobs";
    exit;
fi

MODEL=$1
NJobs=$2
if [ $# -ge 3 ]
then
    QUEUE=$3
else 
    QUEUE="long.q"
fi

echo "MODEL="$MODEL
echo "NJobs="$NJobs
echo "QUEUE="$QUEUE
count=5

source $VO_CMS_SW_DIR/cmsset_default.sh
source /swshare/glite/external/etc/profile.d/grid-env.sh
#echo `voms-proxy-init -voms cms --valid 168:00`

cd /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/
if [ ! -d Limits_Expected_loJet_hiHT_10fb ]
then
    mkdir Limits_Expected_loJet_hiHT_10fb
else 
    echo "Directory limits already exists, writing there!"
fi
cd Limits_Expected_loJet_hiHT_10fb

singlePoint=(`python <<END 
rAsymptotic=[0.43, 0.77, 0.85, 2.30, 0.77, 1.04, 1.56, 1.46, 4.55, 3.55, 1.53, 6.95, 1.19, 0.71]
#rMax=[0.86, 1.44, 1.70, 4.60, 1.44, 2.08, 3.12, 2.92, 9.10, 7.10, 3.06, 13.90, 2.38, 1.42]
rMax=[1.2*r for r in rAsymptotic]
rMin=[0.2*r for r in rAsymptotic]
div=(rMax[$count]-rMin[$count])/20
singlePoint=[rMax[$count], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, rMin[$count]]
for j in range(1, 19):
    singlePoint[j]=singlePoint[j-1]-div
for j in range(0, 20):
    print singlePoint[j]
END`)


for (( j=0; j<$NJobs; ++j ))
do
    command=`qsub -q ${QUEUE} -o $PWD/${MODEL}_${j}_${NJobs}.out -e $PWD/${MODEL}_${j}_${NJobs}.err -N combineHybrid_${MODEL} /shome/mmasciov/CMSSW_7_1_5/src/HiggsAnalysis/CombinedLimit/combine_Hybrid.sh $MODEL $j $NJobs ${singlePoint[$j]}`
    echo "Submitting job $j"
    echo $command
done