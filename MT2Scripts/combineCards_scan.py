import os
import sys
import commands

from os import listdir
from os.path import isfile, join


if len(sys.argv)>1:
    mypath = sys.argv[1]
else:
    mypath = "/pnfs/psi.ch/cms/trivcat/store/user/casal/EventYields_data_Run2016_7p7ifb/datacards_T2bb_final/"

models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]
for m in models:
    if m in mypath:
        model = m

for d in listdir(mypath):

    if ".txt" in d or "datacard" not in d:
        continue

    print d
    m1=d.split("_")[1]
    m2=d.split("_")[2]

    print model, m1, m2

    # check if file exists and is non-empty
    combfile = mypath+"/datacard_"+model+"_"+str(m1)+"_"+str(m2)+"_combined.txt"
    if ( os.path.isfile(combfile) ):
        stat,out = commands.getstatusoutput("ls -l "+combfile+" | awk '{print $5}'")
        if (int(out)==0): # if empty -> remove
            print "file exists and is empty... removing:", combfile
            command = "gfal-rm srm://t3se01.psi.ch/"+combfile
            os.system(command)
        else:
          print "file exists... skiping:",combfile
          continue

    command="qsub -q short.q -o /dev/null -e /dev/null -N combineCards_"+model+"_"+str(m1)+"_"+str(m2)+" combineCards_batch_scan.sh "+model+" "+mypath+" "+str(m1)+" "+str(m2)
    print command
    os.system(command)

