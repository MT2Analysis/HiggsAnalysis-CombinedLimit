# python submitSignificance_scan.py <path> <model>

import os
import sys
import commands

from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
    mypath = sys.argv[1]
else:
    mypath = "/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"

if len(sys.argv)>2:
  model = sys.argv[2]
else:
  raise RuntimeError("Error: model not specified")

command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"/significance/"
os.system(command)

version = mypath.split('{}_'.format(model))[1]

logsDir="{}/sig_{}_{}/".format(os.getcwd(),model,version)
os.system("mkdir {}".format(logsDir))


for f in listdir(mypath):

    if ".txt" not in f:
      continue

    if "datacard" not in f:
      continue

    if "datacard_T1bbb_" in f:
      continue

    #print f
    model=f.split("_")[1]
    m1   =f.split("_")[2]
    m2   =f.split("_")[3]

    #if m1!=1200 and m2!=900: continue

    print model, m1, m2

    # check if file exists and is non-empty
    logfile = mypath+"/significance/log_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skipping:",logfile
        continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".out"
    err = logsDir+"log_"+str(m1)+"_"+str(m2)+".err"

    command="qsub -q all.q -l h_vmem=6G -o "+out+" -e "+err+" -N plSignificance_"+model+"_"+str(m1)+"_"+str(m2)+" submitSignificance_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)

