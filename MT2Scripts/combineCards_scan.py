''' 
Script to launch the datacard combination for the signals
python combineCards_scan.py <full-path> <model>
Will do combination of data-cards present in the specified path
'''

import os
import sys
import commands
import re
from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
  mypath = sys.argv[1]
else:
  mypath = "/pnfs/psi.ch/cms/trivcat/store/user/mratti/datacards/EventYields_moriond2019_35p9ifb/"

if len(sys.argv)>2:
  models = [sys.argv[2]]
else:
  models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]


for m in models:
  #if m in mypath:
  model = m

  version = mypath.split('{}_'.format(model))[1]
  logsDir="{}/jobs_comb_{}_{}/".format(os.getcwd(),model,version)

  os.system("mkdir {}".format(logsDir))

  for d in listdir(mypath):
    # format must be tared_1525_350.tar.gz
    #if 'limits' in d: continue
    if 'tared_' not in d: continue
    if 'tar.gz' not in d: continue

    print 'Working on ', d
    els=re.split('_|\.', d)
    m1=els[1]
    m2=els[2]

    print model, m1, m2

    # check if combined file exists and is non-empty
    combfile = mypath+"/datacard_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(combfile) ):
        print 'Combined file already exists'
        stat,out = commands.getstatusoutput("ls -l "+combfile+" | awk '{print $5}'")
        if (int(out)==0): # if empty -> remove
            print "file exists and is empty... removing:", combfile
            command = "gfal-rm srm://t3se01.psi.ch/"+combfile
            os.system(command)
        else:
          print "file exists... skipping:",combfile
          continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".log"
    job_name = "combineCards_"+model+"_"+str(m1)+"_"+str(m2)

    command="sbatch -p wn --account=cn-test -o {} -e {} --job-name={} --time=0-00:20 --ntasks=1 combineCards_batch_scan.sh {} {} {} {}".format(out, out, job_name, mypath, model, str(m1), str(m2)) 

    print command

    os.system(command)
