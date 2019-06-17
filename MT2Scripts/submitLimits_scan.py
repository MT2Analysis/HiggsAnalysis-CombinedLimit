# python submitLimits_scan.py <path> <model>

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

command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"limits/"
os.system(command)
  
logsDir="{}/lim_{}/".format(os.getcwd(),model)
os.system("mkdir {}".format(logsDir))


for f in listdir(mypath):

    if ".txt" not in f:
        continue

    if "datacard" not in f:
        continue

    #print f
    #if os.stat(f).st_size == 0:
    #    print "Combined data-card ", f, " is empty, skipping limit calculation"
    #    continue

    print f
    #model=f.split("_")[1]
    m1   =f.split("_")[2]
    m2   =f.split("_")[3]

    print model, m1, m2

    # temporary PATCH
    #if int(m1) < 1400: 
    #  print 'Only submitting jobs with mass above 1400, will skip this point', m1, m2
    #  continue

    # check if file exists and is non-empty
    logfile = mypath+"/limits/log_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skipping:",logfile
        continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".out"
    err = logsDir+"log_"+str(m1)+"_"+str(m2)+".err"

    #command="qsub -q long.q -o "+out+" -e "+err+" -N asymptoticLimit_"+model+"_"+str(m1)+"_"+str(m2)+" submitLimits_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    command="qsub -q all.q -l h_vmem=4G -o "+out+" -e "+err+" -N asymptoticLimit_"+model+"_"+str(m1)+"_"+str(m2)+" submitLimits_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    #command="qsub -q all.q -o "+out+" -e "+err+" -N asymptoticLimit_"+model+"_"+str(m1)+"_"+str(m2)+" submitLimits_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    #command="qsub -q short.q -o "+out+" -e "+err+" -N asymptoticLimit_"+model+"_"+str(m1)+"_"+str(m2)+" submitLimits_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)
