import os
from sys import argv
from commands import getstatusoutput

#if len(argv)>1:
#    HTregion = argv[1]
#else:
#    HTregion = "HT575to1000"

HTregions = ["j1","HT200to450","HT450to575","HT575to1000","HT1000to1500","HT1500toInf",]

for HTregion in HTregions:
    pwd = os.getcwd()
    idir = pwd+"/datacard_templates/"

    # order matters... holy shit!
    flist = ""
    if HTregion !="j1":
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j2to3_b0_m???to*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ") ;  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j2to3_b0_m1000*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ") ;  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j2to3_b1*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j2to3_b2*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j4to6_b0_m???to*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j4to6_b0_m1000**.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j4to6_b1*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j4to6_b2*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j7toInf_b0*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j7toInf_b1*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j7toInf_b2*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j2to6_b3*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_"+HTregion+"_j7toInf_b3*.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
    else:
        status,output = getstatusoutput("ls -l "+idir+"/*HT???to*j1*b0* | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/datacard_HT1000toInf_j1_b0_m0toInf.txt | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        status,output = getstatusoutput("ls -l "+idir+"/*j1*b1* | awk '{print $9}' | sort | awk 'BEGIN{ORS=\" \"}{print}' ");  flist += output
        

    #print flist
    
    command = "combineCards.py -S "+flist+" > datacard_"+HTregion+".txt"
    print command
    os.system(command)
    
    
    command = "text2workspace.py datacard_"+HTregion+".txt -b -o datacard_"+HTregion+".root"
    print command
    os.system(command)
