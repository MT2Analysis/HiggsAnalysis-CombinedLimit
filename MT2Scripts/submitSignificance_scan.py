import os
import sys
import commands

from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
    mypath = sys.argv[1]
    dcpath = sys.argv[2]
else:
    mypath = "/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"
    dcpath = "/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"

#models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]
#for m in models:
#    if m in mypath:
#        model = m

command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"significance/"
os.system(command)


for f in listdir(dcpath):

    if ".txt" not in f:
        continue

    print f
    model=f.split("_")[1]
    m1   =f.split("_")[2]
    m2   =f.split("_")[3]

    print model, m1, m2

    # check if file exists and is non-empty
    logfile = mypath+"/significance/log_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skiping:",logfile
        continue

    command="qsub -q short.q -o /dev/null -e /dev/null -N plSignificance_"+model+"_"+str(m1)+"_"+str(m2)+" submitSignificance_batch_scan.sh "+model+" "+mypath+" "+dcpath+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)

