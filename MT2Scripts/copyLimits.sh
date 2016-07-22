#!bin/bash                                                                                                                                                                                                                                  
### HOW TO USE:
### sh copyLimits.sh T1qqqq noBtag2 /pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/

Model=$1
Label=$2
SEPath=$3

mkdir -p /scratch/`whoami`/limits_${Model}_${Label}/; 
for i in $(ls -rt ${SEPath}/datacards_${Model}_${Label}/limits/); do dccp dcap://t3se01.psi.ch:22125/${SEPath}/datacards_${Model}_${Label}/limits/$i /scratch/`whoami`/limits_${Model}_${Label}/; done;
