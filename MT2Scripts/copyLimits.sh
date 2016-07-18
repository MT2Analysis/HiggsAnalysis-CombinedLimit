#!bin/bash                                                                                                                                                                                                                                  
 
Model=$1

mkdir -p /scratch/mmasciov/limits_$Model/; for i in $(ls -rt /pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_$Model/); do dccp dcap://t3se01.psi.ch:22125/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/limits_${Model}/$i /scratch/mmasciov/limits_${Model}/; done;
