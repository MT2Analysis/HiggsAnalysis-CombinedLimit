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

SEPath="${MYPATH}/datacards_${M1}_${M2}/"


source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW_7_1_5"
cd /mnt/t3nfs01/data01/shome/casal/CMSSW_7_1_5_combine/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/casal/datacardCombination_${JOB_ID}/

mkdir -p ${JOBDIR}
mkdir -p ${JOBDIR}/datacards_${MODEL}/

echo $SEPath

cd ${JOBDIR}

for i in $(ls ${SEPath}/*txt)
do

    echo "Copying ${i}"
    command=`dccp dcap://t3se01.psi.ch:22125/${i} ${JOBDIR}/`
    echo ${command}

done

combineCards.py -S ${JOBDIR}/datacard_*txt > ${JOBDIR}/datacards_${MODEL}/datacard_${MODEL}_${M1}_${M2}_combined.txt
xrdcp -v ${JOBDIR}/datacards_${MODEL}/datacard_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt

rm -rf $JOBDIR
