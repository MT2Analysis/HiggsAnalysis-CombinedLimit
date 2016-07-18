import operator
import sys

signal_point = str(sys.argv[1])

filename="limits_"+signal_point+".txt"

a={}
b={}
for line in open(filename):
    a[(line.split()[0])]=float(line.split()[1])
    b[(line.split()[2])]=float(line.split()[1])

output=open('macroRegions_'+signal_point+'_ranked.txt', 'w+')
limits=a.keys()
limits.sort()
limits=sorted(a.items(), key=operator.itemgetter(1))    
obs=sorted(b.items(), key=operator.itemgetter(1))    
#for l in limits:
#    output.write(str(a[l])+' & '+str(l)+'\\\\\n')
for l,y in zip(limits, obs):
    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) +'\\\\\n')

