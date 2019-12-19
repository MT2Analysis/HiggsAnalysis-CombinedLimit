import operator
import sys

signal_point = str(sys.argv[1])
m1 = signal_point.split("_")[1]
#print m1

path="/scratch/mratti/ranking/"
filename=path+"AsymptoticRanking_"+signal_point+"_Paper_post.txt"

xsecFileName="/work/mratti/SUSxsecs/NNLO_approx_NNLL_80X_compatible/"
if "T1" in signal_point:
    xsecFileName=xsecFileName+"gluglu.txt"
elif "T2qq" in signal_point:
    xsecFileName=xsecFileName+"sqsq.txt"
else:
    xsecFileName=xsecFileName+"thirdGen.txt"

xsecFile = open(xsecFileName, "r")

xsec=1.0;
xsecs = xsecFile.readlines()
for l in xsecs:
    if l.split()[1].replace(".", "")==m1:
        xsec = float(l.split()[3])
        if "T2qq" in signal_point:
            xsec=float(xsec)*1./10.
        break

if xsec==1: print 'WARNING: xsec was read as 1'
print xsec

a={}
b={}
c={}

for line in open(filename):
#    a[float(line.split()[1])]=line.split()[0]
    a[(line.split()[0])]=float(line.split()[1])
    b[(line.split()[0])]=float(line.split()[3])
    c[(line.split()[0])]=float(line.split()[2])

output=open(path+'AsymptoticRanking_'+signal_point+'_Paper_post_ranked.txt', 'w+')
#limits=a.keys()
#limits.sort()
limits=sorted(a.items(), key=operator.itemgetter(1))    
###yields=sorted(b.items(), key=operator.itemgetter(1))    
###obs_limits=sorted(c.items(), key=operator.itemgetter(1))    
##for l in limits:
##    output.write(str(a[l])+' & '+str(l)+'\\\\\n')
for l in limits:
    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(xsec*1000)*100.)) +'\\\\\n') # acceptance assumes 1/fb, will be corrected in makeRankingTables



###    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(0.00470323*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(0.0431418*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(0.51848*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(121.416*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(64.5085*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(13.3231*2263.55)*100.)) +'\\\\\n')
#    output.write(str(l[0])+' & '+str(l[1])+' & '+str(c[l[0]]) + ' & ' + str(b[l[0]]) + ' & ' + ('%.3f' % (float(b[l[0]])/(0.0283338*2263.55)*100.)) +'\\\\\n')
##    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) + ' & ' + ('%.3f' % (float(y[0])/(0.174599*2263.55)*100.)) +'\\\\\n')
##    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) + ' & ' + ('%.3f' % (float(y[0])/(3.78661*2263.55)*100.)) +'\\\\\n')
##    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) + ' & ' + ('%.3f' % (float(y[0])/(8.51615*2263.55)*100.)) +'\\\\\n')
##    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) + ' & ' + ('%.3f' % (float(y[0])/(0.0431418*2263.55)*100.)) +'\\\\\n')
##    output.write(str(l[0])+' & '+str(l[1])+ ' & ' + str(y[0]) +'\\\\\n')
