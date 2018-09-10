#!bin/bash                                                                                                                                                                                                                                  
### HOW TO USE:
### source copyLimits.sh T2qq V0 /pnfs/psi.ch/cms/trivcat/store/user/mratti/datacards/EventYields_dataETH_SnTMC_35p9ifb/

Model=$1
Label=$2
SEPath=$3

mkdir -p /scratch/`whoami`/limits_${Model}_${Label}/; 
for i in $(ls -rt ${SEPath}/datacards_${Model}_${Label}/limits/); 
  do 
    xrdcp root://t3dcachedb.psi.ch:1094//${SEPath}/datacards_${Model}_${Label}/limits/$i /scratch/`whoami`/limits_${Model}_${Label}/; 
  done;
