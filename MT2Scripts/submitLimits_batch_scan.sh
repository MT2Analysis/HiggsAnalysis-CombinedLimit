#!/bin/bash

echo $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} PATH MODEL M1 M2";
    exit;
fi

MYPATH=$1
MODEL=$2
M1=$3
M2=$4

MYCARD="${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt"


source $VO_CMS_SW_DIR/cmsset_default.sh
echo "Loading CMSSW 80X"
cd /work/mratti/test_combine_area/CMSSW_8_1_0/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/limitCalculation_${SLURM_JOB_ID}/

mkdir -p ${JOBDIR}

echo $MYCARD

cd ${JOBDIR}

echo "Copying ${MYCARD}"
xrdcp root://t3dcachedb.psi.ch:1094/${MYCARD} ${JOBDIR}/

echo "Going to run limit calculation"
combine -M AsymptoticLimits datacard_${MODEL}_${M1}_${M2}_combined.txt -n ${MODEL}_${M1}_${M2} &> log_${MODEL}_${M1}_${M2}_combined.txt

echo "Output is"
ls -al log_${MODEL}_${M1}_${M2}_combined.txt

echo "Creating limit dir"
xrdfs t3dcachedb03.psi.ch mkdir ${MYPATH}/limits/

echo "Copying result back"
xrdcp -v -f log_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/limits/.

rm -rf $JOBDIR
