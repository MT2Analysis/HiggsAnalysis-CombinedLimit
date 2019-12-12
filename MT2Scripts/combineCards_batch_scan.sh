#!/bin/bash

# Script to combine the data cards into a single data card for a given mass mass point of a model
# accesses the tar with the data-cards, untars, produces combined data card, copies output to the input directory


o $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

# configurations
MYPATH=$1
MODEL=$2
M1=$3
M2=$4

SEPath="${MYPATH}"
TarFile="tared_${M1}_${M2}.tar.gz"

# setting up environment
source $VO_CMS_SW_DIR/cmsset_default.sh
echo "Loading CMSSW 80X"
cd /work/mratti/test_combine_area/CMSSW_8_1_0/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/datacardCombination_${SLURM_JOB_ID}/

# actual job
mkdir -p ${JOBDIR}
mkdir -p ${JOBDIR}/datacards_${MODEL}/

echo "Going to work on $SEPath/${TarFile}"

cd ${JOBDIR}

echo "Copying ${SEPath}/${TarFile}"
xrdcp root://t3dcachedb.psi.ch:1094//${SEPath}/${TarFile} ${JOBDIR}/${TarFile}

echo "Untarring"
tar -xvzf ${TarFile}

echo "Combining"
combineCards.py -S ${JOBDIR}/datacards_${MODEL}/datacard_*txt > ${JOBDIR}/datacards_${MODEL}/datacard_${MODEL}_${M1}_${M2}_combined.txt

echo "Copying result back"
xrdcp -v -f ${JOBDIR}/datacards_${MODEL}/datacard_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt
# recreates file if already exists, will overwrite!

rm -rf $JOBDIR
