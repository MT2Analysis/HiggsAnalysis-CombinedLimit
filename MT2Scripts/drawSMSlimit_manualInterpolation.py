#!/usr/bin/env python
from math import *
import os, commands
from sys import argv,exit
from optparse import OptionParser
import ROOT

print "runing:", argv


if len(argv)<2:
    print "Usage: "+argv[0]+" fileWithLimits.txt"
    exit(1)

INPUT = argv[1]

models   = ["T1bbbb", "T1tttt","T1qqqq","T2qq","T2bb","T2tt"]
model = "mymodel"
for m in models:
    if m in INPUT:
        model = m

xsfile = "SUSYCrossSections13TeVgluglu.root" if "T1" in model else "theXSfile.root"
f_xs = ROOT.TFile(xsfile)
h_xs = f_xs.Get("xs")

limits = ["obs", "exp", "ep1s", "em1s", "ep2s", "em2s", "op1s", "om1s"]


def getLimitYN ( h_lim_mu, r_exluded=1):
    name = h_lim_mu.GetName().replace("mu","yn")
    h_lim_yn = h_lim_mu.Clone(name)
    for ix in range(1,h_lim_yn.GetNbinsX()+1):
        for iy in range(1,h_lim_yn.GetNbinsY()+1):
            r = h_lim_yn.GetBinContent(ix,iy)
            h_lim_yn.SetBinContent(ix, iy, 1e-3 if r>r_exluded else 1 if r>0 else 0)
    return h_lim_yn
    
def getLimitXS ( h_lim_mu, h_xs):
    name = h_lim_mu.GetName().replace("mu","xs")
    h_lim_xs = h_lim_mu.Clone(name)
    for ix in range(1,h_lim_xs.GetNbinsX()+1):
        m = h_lim_xs.GetXaxis().GetBinCenter(ix)
        for iy in range(1,h_lim_xs.GetNbinsY()+1):
            r = h_lim_xs.GetBinContent(ix,iy)
            xs  = h_xs.GetBinContent(h_xs.FindBin(m))
            h_lim_xs.SetBinContent(ix, iy, r*xs)
    return h_lim_xs
    
def interpolate(hist, step=2, direction="x"):
    # if step>0 (and even), interpolate only middle point if full gap found of size=step
    # if step==0, interpolate all empty points in gap of any size
    # makes sense to run from big to small steps starting with "x" followed by "y" to optimize the usage of information
    # then use step=0 to fill remaining gaps if any
    if step%2 != 0:
        print "interponlation() step must be an even number"
        return
    if direction!="x" and direction!="y":
        print 'interpolation() direction must be "x" or "y"'   
    N, b = {},{}
    N["x"] = hist.GetNbinsX() 
    N["y"] = hist.GetNbinsY()
    d1 = direction
    d2 = "y" if direction=="x" else "x"
    next = {d1:1, d2:0}
    for b[d2] in range(1, N[d2]+1):
        for b[d1] in range(1, N[d1]+1):
            val1 = hist.GetBinContent(b["x"],b["y"])
            # stop when we find a non-empty bin with an empty neighbour
            if val1==0 or hist.GetBinContent(b["x"]+next["x"],b["y"]+next["y"])!=0: 
                continue

            n=step
            # for step==0 find nearest non empty bin
            if step==0:
                n=2
                while hist.GetBinContent(b["x"]+n*next["x"],b["y"]+n*next["y"])==0 and b[d1]+n<N[d1]+1:
                    n+=1
            val2 = hist.GetBinContent(b["x"]+n*next["x"],b["y"]+n*next["y"])
            if val2 == 0:
                continue

            # i want bin+step filled and all in between empty (if step>0)
            if val2 == 0:
                continue
            doIt = True
            if step>0:
                for x in range(2,step):
                    if hist.GetBinContent(b["x"]+x*next["x"],b["y"]+x*next["y"]) != 0:
                        doIt = False
            if not doIt: 
                continue

            if step>0: # fill middle point
                val = (val2+val1)/2.0
                hist.SetBinContent(b["x"]+next["x"]*step/2,b["y"]+next["y"]*step/2, val)
            else: #fill full gap
                for nn in range(1,n):                    
                    hist.SetBinContent(b["x"]+nn*next["x"],b["y"]+nn*next["y"],val1+(val2-val1)*nn/n)

def interpolateDiagonal(hist):
    # interpolate in diagonal direction to fill remaining missing holes
    # start from 15 bins away and finish in the diagonal
    Nx = hist.GetNbinsX() 
    Ny = hist.GetNbinsY()
    for i in range(14,-1,-1): # 14...0
        j=0
        while i+j<Nx and j<Ny:
           j+=1
           val1=hist.GetBinContent(i+j,j)
           if val1==0 or hist.GetBinContent(i+j+1,j+1)!=0:
               continue

           n=2
           while hist.GetBinContent(i+j+n,j+n)==0 and i+j+n<Nx and j+n<Ny:
               n+=1
           val2 = hist.GetBinContent(i+j+n,j+n)
           if val2==0:
               continue
           for nn in range(1,n):                    
               hist.SetBinContent(i+j+nn,j+nn,val1+(val2-val1)*nn/n) 
       



def extractSmoothedContour(hist, nSmooth=1, optname=""):
    isMu = "mu" in hist.GetName()
    ROOT.gStyle.SetNumberContours(4 if isMu else 2)
    shist = hist.Clone(hist.GetName()+optname+"smoothed")

    # if smoothing a limit from mu, we need to modify the zeros outside the diagonal, otherwise the smoothing fools us in the diagonal transition
    if isMu:
        for ix in range(shist.GetNbinsX(),0,-1):
            for iy in range(shist.GetNbinsY(),0,-1):
                if shist.GetBinContent(ix,iy)==0:
                    shist.SetBinContent(ix,iy, shist.GetBinContent(ix,iy-1))

    for s in range(nSmooth):
        #shist.Smooth()
        shist.Smooth(1,"k3a")

    # after smoothing a limit from mu, we need to modify the zeros outside the diagonal, otherwise the contours come wrong for the diagonal
    if isMu:
        for iy in range(shist.GetNbinsY(),0,-1):
            for ix in range(shist.GetNbinsX(),0,-1):
                if hist.GetBinContent(ix,iy)==0:
                    shist.SetBinContent(ix,iy, 5)
        

    shist.SetMinimum(0)
    shist.SetMaximum(2 if isMu else 1)
    #shist.SetContour(20) # n=2 defined above
    canvas = ROOT.TCanvas()
    shist.Draw("contz list")
    ROOT.gPad.Update()
    obj = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    list = obj.At(1 if isMu else 0)
    graph = list.First().Clone()
    name = "gr_"
    name += hist.GetName() if optname=="" else optname
    graph.SetName(name)
    graph.Draw("sameC")
    del canvas
    del shist
    del obj
    del list
    return graph

def readLimitsFromFile(INPUT, fileMap, h_lims_mu0, h_lims_xs0, h_lims_yn0):
    rlim = {}
    for line in open(INPUT, "r"):
        m1        = float(line.split()[0])
        m2        = float(line.split()[1])
        for lim,index in fileMap.iteritems():
            rlim[lim]  = float(line.split()[index])
    
        # get xs for the given mass
        xs  = h_xs.GetBinContent(h_xs.FindBin(m1))
        exs = h_xs.GetBinError  (h_xs.FindBin(m1))
    
        rlim['op1s'] = rlim['obs'] * xs / (xs+exs)
        rlim['om1s'] = rlim['obs'] * xs / (xs-exs)
    
        #fill the 2d limit histos
        binX=h_lims_mu0[lim].GetXaxis().FindBin(m1)
        binY=h_lims_mu0[lim].GetYaxis().FindBin(m2)
    
        for lim in limits:
            h_lims_mu0[lim].SetBinContent(binX, binY, rlim[lim])
            h_lims_xs0[lim].SetBinContent(binX, binY, rlim[lim]*xs)
            h_lims_yn0[lim].SetBinContent(binX, binY, 1 if rlim[lim]<1 else 1e-3)



h_lims_mu0 = {} # limits in signal-strength, original binning
h_lims_yn0 = {} # limits in excluded/non-exluded, original binning
h_lims_xs0 = {} # limits in cross-section, original binning
h_lims_mu  = {} # limits in signal-strength, interpolated
h_lims_yn  = {} # limits in excluded/non-exluded, interpolated
h_lims_xs  = {} # limits in cross-section, interpolated

m1min, m1max = 0, 2000
m2min, m2max = 0, 2000

mass1 = "mGlu" if "T1" in model else "mSq" if model=="T2qq" else "mSb" if model=="T2bb" else "mSt" if model=="T2tt" else "m1"
mass2 = "mLSP"

# create histos
for lim in limits:
    # uniform 25 GeV binning
    h_lims_mu0[lim] = ROOT.TH2F(lim+"_mu0", model, (m1max-m1min+25)/25, m1min-12.5, m1max+12.5, (m2max-m2min+25)/25, m2min-12.5, m2max+12.5)
    h_lims_mu0[lim].SetXTitle(mass1)    
    h_lims_mu0[lim].SetYTitle(mass2)

    h_lims_yn0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","yn"))
    h_lims_xs0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","xs"))


# read txt file with limits
print "reading file..."
fileMap = {"exp":2, "obs":3, "ep1s":4, "em1s":5, "ep2s":6, "em2s":7}
readLimitsFromFile(INPUT, fileMap, h_lims_mu0, h_lims_xs0, h_lims_yn0)


output = INPUT.replace(".txt",".root")
fout = ROOT.TFile(output, "RECREATE")
fout.cd()

print "interpolating..."
for lim in limits:
    # runnin interpolation from big steps to small to optimize information
    h_lims_mu[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu0","mu"))
    interpolate(h_lims_mu[lim], 8,"x")
    interpolate(h_lims_mu[lim], 8,"y")
    interpolate(h_lims_mu[lim], 4,"x")
    interpolate(h_lims_mu[lim], 4,"y")
    interpolate(h_lims_mu[lim], 2,"x")
    interpolate(h_lims_mu[lim], 2,"y")
    interpolate(h_lims_mu[lim], 0,"x")
    interpolate(h_lims_mu[lim], 0,"y")
    interpolateDiagonal(h_lims_mu[lim])

print "translating to x-sec and yes/no limits and saving 2d histos..."
for lim in limits:
    h_lims_yn[lim] = getLimitYN ( h_lims_mu[lim] )
    h_lims_xs[lim] = getLimitXS ( h_lims_mu[lim], h_xs )
    
    h_lims_mu0[lim].Write()
    h_lims_xs0[lim].Write()
    h_lims_yn0[lim].Write()
    h_lims_mu[lim].Write()
    h_lims_xs[lim].Write()
    h_lims_yn[lim].Write()


graphsMU = {}
graphsYN = {}

print "extracting contours and saving graphs..."
for lim in limits:
    # countour from smoothed Y/N limit
    #graphsYN[lim] = extractSmoothedContour(h_lims_yn[lim], 1)
    #graphsYN[lim].Write()
    # countour from smoothed signal strenght limit
    graphsMU[lim] = extractSmoothedContour(h_lims_mu[lim], 1)
    graphsMU[lim].Write()
    
print "file "+output+" saved"


print "saving x-check plots"
plotsDir = "xcheckPlots"
can = ROOT.TCanvas("can","can",600,600)
if( not os.path.isdir(plotsDir) ):
    os.system("mkdir "+plotsDir)
for lim in limits:
    ROOT.gStyle.SetNumberContours( 100 )
    h_lims_yn0[lim].GetXaxis().SetRangeUser(600,2000)
    h_lims_yn0[lim].GetYaxis().SetRangeUser(0  ,1500)
    h_lims_yn0[lim].Draw("colz")
    graphsMU[lim].SetLineWidth(2)
    graphsMU[lim].Draw("same")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".eps")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".png")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".pdf")


fout.Close()
