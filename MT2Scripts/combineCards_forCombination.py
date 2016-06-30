import os
import sys

from os import listdir
from os.path import isfile, join

mypath2016="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_2016_corr/"
mypath2015="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_2p3ifb_28June_newBins/"

for d in listdir(mypath2016):
    m1=d.split("_")[2]
    m2=d.split("_")[3]

    print d, m1, m2
    
    if isfile(mypath2015+"/"+d):
        command="qsub -q long.q -o /dev/null -e /dev/null -N combiningDatacards_"+str(m1)+"_"+str(m2)+" combineCards_batch_forCombination.sh "+str(m1)+" "+str(m2)
        print command
        os.system(command)


