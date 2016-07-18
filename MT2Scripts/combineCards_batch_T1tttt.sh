#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# != 2 ]; then
    echo "USAGE: ${0} M1 M2";
    exit;
fi

M1=$1
M2=$2

SEPath="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_28June_2016_corr/datacards_T1tttt_${M1}_${M2}/"

source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW_7_1_5"
cd /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/mmasciov/datacardCombination_${JOB_ID}/
#JOBDIR=/scratch/mmasciov/datacardCombination_test/

mkdir -p ${JOBDIR}
mkdir -p ${JOBDIR}/datacards_T1tttt_2p3ifb/

cd ${JOBDIR}

for i in $(ls ${SEPath}/*txt)
do

    echo "Copying ${i}"
    command=`dccp dcap://t3se01.psi.ch:22125/${i} ${JOBDIR}/`
    echo ${command}

done

combineCards.py -S ${JOBDIR}/datacard_*txt > ${JOBDIR}/datacards_T1tttt_2p3ifb/datacard_T1tttt_${M1}_${M2}_2p3ifb.txt
env --unset=LD_LIBRARY_PATH gfal-mkdir -p srm://t3se01.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2016_corr
xrdcp -v ${JOBDIR}/datacards_T1tttt_2p3ifb/datacard_T1tttt_${M1}_${M2}_2p3ifb.txt root://t3dcachedb.psi.ch:1094///pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2016_corr/datacard_T1tttt_${M1}_${M2}_2p3ifb.txt
#env --unset=LD_LIBRARY_PATH gfal-copy file:///${JOBDIR}/datacards_T1tttt_2p3ifb/datacard_T1tttt_${M1}_${M2}_2p3ifb.txt srm://t3se01.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2016_corr/datacard_T1tttt_${M1}_${M2}_2p3ifb.txt

rm -rf $JOBDIR
