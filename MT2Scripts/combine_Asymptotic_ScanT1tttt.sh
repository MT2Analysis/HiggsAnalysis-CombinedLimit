#!/bin/bash                                                                                                                                                                          
echo $#;
if [ $# != 1 ]; then
    echo "USAGE: ${0} MODEL";
    exit;
fi

MODEL=$1

source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc481
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH
echo "Loading CMSSW_7_1_5/"
cd /mnt/t3nfs01/data01/shome/mmasciov/CMSSW_7_1_5/src/
eval `scramv1 runtime -sh`
###eval `cmsenv`

JOBDIR=/scratch/mmasciov/limitCalculation_${JOB_ID}/

mkdir -p ${JOBDIR}
mkdir -p ${JOBDIR}/limits_T1tttt_2p3ifb/

SEPath="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2015plus2016_uncorr/"

cd ${JOBDIR}/limits_T1tttt_2p3ifb/

if [ -e "/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/log_${MODEL}_2p3ifb.txt" ]
then
    echo "file exists for ${MODEL}, don't run"
else

    for i in $(ls ${SEPath}/datacard_${MODEL}_2p3ifb.txt)
    do
	
	echo "Copying ${i}"
	command=`dccp dcap://t3se01.psi.ch:22125/${i} ${JOBDIR}/limits_T1tttt_2p3ifb/`
	echo ${command}
	
    done

    command=`combine -M Asymptotic datacard_${MODEL}_2p3ifb.txt -n ${MODEL} >& log_${MODEL}_2p3ifb.txt`
    echo $command

    env --unset=LD_LIBRARY_PATH gfal-mkdir -p srm://t3se01.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/
    xrdcp -v ${JOBDIR}/limits_T1tttt_2p3ifb/log_${MODEL}_2p3ifb.txt root://t3dcachedb.psi.ch:1094////pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/log_${MODEL}_2p3ifb.txt
    command_rm=`rm -rf higgsCombine${MODEL}.Asymptotic.mH120.root`
    command_rmdir=`rm -rf ${JOBDIR}`
fi

#for i in $(ls ${SEPath}/datacard_${MODEL}_2p3ifb.txt)
#do
#
#    echo "Copying ${i}"
#    command=`dccp dcap://t3se01.psi.ch:22125/${i} ${JOBDIR}/limits_T1tttt_2p3ifb/`
#    echo ${command}
#
#done
#
#command=`combine -M Asymptotic datacard_${MODEL}_2p3ifb.txt -n ${MODEL} >& log_${MODEL}_2p3ifb.txt`
#echo $command
#
#env --unset=LD_LIBRARY_PATH gfal-mkdir -p srm://t3se01.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/
#xrdcp -v ${JOBDIR}/limits_T1tttt_2p3ifb/log_${MODEL}_2p3ifb.txt root://t3dcachedb.psi.ch:1094////pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/log_${MODEL}_2p3ifb.txt
##env --unset=LD_LIBRARY_PATH gfal-copy file:///${JOBDIR}/limits_T1tttt_2p3ifb/log_${MODEL}_2p3ifb.txt srm://t3se01.psi.ch//pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_T1tttt_2p3ifb_28June_2015plus2016_uncorr/log_${MODEL}_2p3ifb.txt
#
#command_rm=`rm -rf higgsCombine${MODEL}.Asymptotic.mH120.root`
#command_rmdir=`rm -rf ${JOBDIR}`