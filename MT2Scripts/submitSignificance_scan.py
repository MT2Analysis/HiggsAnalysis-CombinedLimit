''' 
Script to launch the asymptotic limit calculation
python submitSignificance_scan.py <full-path> <model>
'''

import os
import sys
import commands

from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
    mypath = sys.argv[1]
else:
    mypath = "/pnfs/psi.ch/cms/trivcat/store/user/mratti/datacards/EventYields_moriond2019_35p9ifb/datacards_T1qqqq_12_19_V0"

if len(sys.argv)>2:
  model = sys.argv[2]
else:
  raise RuntimeError("Error: model not specified")

command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"/significance/"
os.system(command)

version = mypath.split('{}_'.format(model))[1]

logsDir="{}/jobs_sig_{}_{}/".format(os.getcwd(),model,version)
#logsDir="{}/exp_sig_{}_{}/".format(os.getcwd(),model,version)
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
    #logfile = mypath+"/exp_significance/log_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skipping:",logfile
        continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".log"
    job_name = "significance_" + model + "_" +str(m1)+"_"+str(m2)

    command="sbatch -p wn --mem=6000 --account=cn-test -o {} -e {} --job-name={}  --ntasks=1 submitSignificance_batch_scan.sh {} {} {} {}".format(out, out, job_name, mypath, model, str(m1), str(m2)) 
    # time limit might have to be optimized, default is 1 day...
    print command
    os.system(command)

