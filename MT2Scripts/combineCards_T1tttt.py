import os
import sys

from os import listdir
from os.path import isfile, join

mypath="/pnfs/psi.ch/cms/trivcat/store/user/mmasciov/datacards_T1tttt_28June_2016_corr/"

for d in listdir(mypath):
    m1=d.split("_")[2]
    m2=d.split("_")[3]

    print m1, m2

    command="qsub -q long.q -o /dev/null -e /dev/null -N combiningDatacards_"+str(m1)+"_"+str(m2)+" combineCards_batch_T1tttt.sh "+str(m1)+" "+str(m2)
    print command
    os.system(command)


#m1=600
#m2=100
#print m1, m2
#
#command="qsub -q short.q -o /dev/null -e /dev/null -N combiningDatacards_"+str(m1)+"_"+str(m2)+" combineCards_batch.sh "+str(m1)+" "+str(m2)
#print command
#os.system(command)
