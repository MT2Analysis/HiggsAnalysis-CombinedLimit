import ROOT
from sys import argv

#line format
# Interactions - gluinos  Nominal (pb) +/- Uncertainty
# 200 GeV 3574.52 +/- 14.0616%

txtfile = argv[1] if len(argv)>0 else "SUSYCrossSections13TeVgluglu.txt"

xsFile = open(txtfile)
lines = [x.strip('\n') for x in xsFile if "GeV" in x]

bin_size = 5.0
mmin = 100.
mmax = 3000.

h_xs = ROOT.TH1F("xs","", int((mmax-mmin)/bin_size)+1, mmin-bin_size/2., mmax+bin_size/2.)

for line in lines:
    mass = float(line.split()[0])
    xsec = float(line.split()[2])
    err  = float(line.split()[4].strip("%"))/100*xsec
    ibin = h_xs.FindBin(mass)
    h_xs.SetBinContent( ibin, xsec ) 
    h_xs.SetBinError  ( ibin, err  ) 

rootFile = ROOT.TFile(xsFile.name.replace(".txt",".root"),"RECREATE")
h_xs.Write()
rootFile.Close()




