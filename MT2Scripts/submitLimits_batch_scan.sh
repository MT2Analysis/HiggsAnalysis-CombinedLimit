#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

MODEL=$1
MYPATH=$2
M1=$3
M2=$4

MYCARD="${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt"


source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW_7_1_5"
cd /mnt/t3nfs01/data01/shome/casal/CMSSW_7_1_5_combine/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/casal/limitCalculation_${JOB_ID}/

mkdir -p ${JOBDIR}

echo $MYCARD

cd ${JOBDIR}

echo "card ${MYCARD}"
command=`dccp dcap://t3se01.psi.ch:22125/${MYCARD} ${JOBDIR}/`
echo ${command}

command=`combine -M Asymptotic datacard_${MODEL}_${M1}_${M2}_combined.txt -n ${MODEL}_${M1}_${M2} >& log_${MODEL}_${M1}_${M2}_combined.txt`
echo $command

xrdcp -v log_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/limits/log_${MODEL}_${M1}_${M2}_combined.txt

rm -rf $JOBDIR
