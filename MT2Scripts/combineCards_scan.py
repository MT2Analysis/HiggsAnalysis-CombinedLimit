# Script to launch the datacard combination for the signals
# python combineCards_scan.py <path> <model>

import os
import sys
import commands
import re
from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
  mypath = sys.argv[1]
else:
  mypath = "/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"

if len(sys.argv)>2:
  models = [sys.argv[2]]
else:
  models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]


for m in models:
  #if m in mypath:
  model = m

  logsDir="{}/jobs_{}/".format(os.getcwd(),model)
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
          print "file exists... skiping:",combfile
          continue

    out = logsDir+"log_"+str(m1)+"_"+str(m2)+".out"
    err = logsDir+"log_"+str(m1)+"_"+str(m2)+".err"
    command="qsub -q short.q -o "+out+" -e "+err+" -N combineCards_"+model+"_"+str(m1)+"_"+str(m2)+" combineCards_batch_scan.sh "+mypath+" "+model+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)
