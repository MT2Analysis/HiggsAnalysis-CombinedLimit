''' 
Script to launch the asymptotic limit calculation
python submitLimits_scan.py <full-path> <model>
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

command = "gfal-mkdir -p srm://t3se01.psi.ch/"+mypath+"/limits/"
os.system(command)

version = mypath.split('{}_'.format(model))[1]
 
logsDir="{}/jobs_lim_{}_{}/".format(os.getcwd(),model,version)
os.system("mkdir {}".format(logsDir))


for f in listdir(mypath):

    if ".txt" not in f:
      continue

    if "datacard" not in f:
      continue

    if "datacard_T1bbb_" in f:
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

    #if int(m1) >= 850: 
    #  print 'temp patch for T2qq, Only submitting jobs with mass below 850, will skip this point', m1, m2
    #  continue

    #if (int(m1) < 350 or int(m1)>550) and (int(m2)<1 or int(m2)>200):
    #  print 'temp patch for T2bb,  will skip this point', m1, m2  
    #  continue

    #if int(m1) >= 1300: 
    #  print 'temp patch for T1bbbb,  will skip this point', m1, m2 
    #  continue

    # check if file exists and is non-empty
    logfile = mypath+"/limits/log_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(logfile) ):
        print "file exists... skipping:",logfile
        continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".log"
    job_name = "limit_" + model + "_" +str(m1)+"_"+str(m2)

    command="sbatch -p wn --mem=6000 --account=cn-test -o {} -e {} --job-name={}  --ntasks=1 submitLimits_batch_scan.sh {} {} {} {}".format(out, out, job_name, mypath, model, str(m1), str(m2)) 
    # time limit might have to be optimized, default is 1 day...
    print command
    os.system(command)
