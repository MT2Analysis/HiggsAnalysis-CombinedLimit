# Script to combine the data cards into a single data card for a given mass mass point of a model
# accesses the tar , untars , produces final data card , copies output to the input directory
# example:
# qsub -l h_vmem=6g -q short.q -o $PWD/test.out -e $PWD/test.err -N test combineCards_batch_scan.sh /pnfs/psi.ch/cms/trivcat/store/user/mratti/datacards/EventYields_dataETH_SnTMC_35p9ifb//datacards_T2qq_ciao/ T2qq 400 200


o $#;
if [ $# != 4 ]; then
    echo "USAGE: ${0} MODEL PATH M1 M2";
    exit;
fi

MYPATH=$1
MODEL=$2
M1=$3
M2=$4

#SEPath="${MYPATH}/datacards_${M1}_${M2}/"
SEPath="${MYPATH}"
TarFile="tared_${M1}_${M2}.tar.gz"


source $VO_CMS_SW_DIR/cmsset_default.sh
#source /mnt/t3nfs01/data01/swshare/glite/external/etc/profile.d/grid-env.sh
export SCRAM_ARCH=slc6_amd64_gcc491
export LD_LIBRARY_PATH=/mnt/t3nfs01/data01/swshare/glite/d-cache/dcap/lib/:$LD_LIBRARY_PATH

echo "Loading CMSSW 80X"
#cd /mnt/t3nfs01/data01/shome/casal/CMSSW_7_1_5_combine/src/
#cd /shome/mratti/combine_workarea/CMSSW_8_1_0/src/
cd /shome/mratti/test_combine_area/CMSSW_8_1_0/src/
echo $PWD
eval `scramv1 runtime -sh`

JOBDIR=/scratch/`whoami`/datacardCombination_${JOB_ID}/

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
# recreates file if already exists

#rm -rf $JOBDIR
