#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# != 5 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

MODEL=$1
MYPATH=$2
DCPATH=$3
M1=$4
M2=$5

MYCARD="${DCPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt"


source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW_7_1_5"
cd /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5_MT2Combine/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/significanceCalculation_${JOB_ID}/

mkdir -p ${JOBDIR}

echo $MYCARD

cd ${JOBDIR}

echo "card ${MYCARD}"
command=`dccp dcap://t3se01.psi.ch:22125/${MYCARD} ${JOBDIR}/`
echo ${command}

command=`combine -M ProfileLikelihood --significance datacard_${MODEL}_${M1}_${M2}_combined.txt -n ${MODEL}_${M1}_${M2} --rMin -5 --uncapped 1 >& log_${MODEL}_${M1}_${M2}_combined.txt`
echo $command

xrdcp -v log_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/significance/log_${MODEL}_${M1}_${M2}_combined.txt

rm -rf $JOBDIR
