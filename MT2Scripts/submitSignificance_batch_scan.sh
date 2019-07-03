#
# exapmle:
# qsub -l h_vmem=6g -q all.q -o $PWD/test.out -e $PWD/test.err -N test submitSignificance_batch_scan.sh /pnfs/psi.ch/cms/trivcat/store/user/mratti/datacards/EventYields_dataETH_SnTMC_35p9ifb/datacards_T2qq/ T2qq 400 200

echo $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

MYPATH=$1
MODEL=$2
M1=$3
M2=$4

MYCARD="${MYPATH}/datacard_${MODEL}_${M1}_${M2}_combined.txt"


source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW 80X"
cd /shome/mratti/test_combine_area/CMSSW_8_1_0/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/significanceCalculation_${JOB_ID}/

mkdir -p ${JOBDIR}

echo $MYCARD

cd ${JOBDIR}

echo "Copying ${MYCARD}"
xrdcp root://t3dcachedb.psi.ch:1094/${MYCARD} ${JOBDIR}/

echo "Going to run significance calculation"
combine -M Significance --pvalue datacard_${MODEL}_${M1}_${M2}_combined.txt -n ${MODEL}_${M1}_${M2} --rMin -5 --uncapped 1 &> log_${MODEL}_${M1}_${M2}_combined.txt

echo "Output is"
ls -al log_${MODEL}_${M1}_${M2}_combined.txt

echo "Creating limit dir"
xrdfs t3dcachedb03.psi.ch mkdir ${MYPATH}/significance/

echo "Copying result back"
xrdcp -v -f log_${MODEL}_${M1}_${M2}_combined.txt root://t3dcachedb.psi.ch:1094//${MYPATH}/significance/.



