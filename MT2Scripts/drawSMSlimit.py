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

# coloum-limit map for txt files (n -> column n+1) 
fileMap = {"exp":2, "obs":3, "ep1s":4, "em1s":5, "ep2s":6, "em2s":7}


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

h_lims_mu   = {} # limits in signal-strength, interpolated
h_lims_yn   = {} # limits in excluded/non-exluded, interpolated
h_lims_xs   = {} # limits in cross-section, interpolated
g2_lims_mu  = {} # TGraph2D limits in signal-strength, automatic interpolation

h_lims_mu1   = {} # limits in signal-strength, interpolated & smoothed
h_lims_yn1   = {} # limits in excluded/non-exluded, interpolated & smoothed
h_lims_xs1   = {} # limits in cross-section, interpolated & smoothed
g2_lims_mu1  = {} # TGraph2D limits in signal-strength, automatic interpolation & smoothed

m1min, m1max = 0, 2000
m2min, m2max = 0, 2000
binSize = 25

mass1 = "mGlu" if "T1" in model else "mSq" if model=="T2qq" else "mSb" if model=="T2bb" else "mSt" if model=="T2tt" else "m1"
mass2 = "mLSP"

# create histos
for lim in limits:
    # uniform 25 GeV binning
    h_lims_mu0[lim] = ROOT.TH2F(lim+"_mu0", model, (m1max-m1min+binSize)/binSize, m1min-binSize/2., m1max+binSize/2., (m2max-m2min+binSize)/binSize, m2min-binSize/2., m2max+binSize/2.)
    h_lims_mu0[lim].SetXTitle(mass1)    
    h_lims_mu0[lim].SetYTitle(mass2)

    h_lims_yn0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","yn"))
    h_lims_xs0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","xs"))


# read txt file with limits (map defined above)
print "reading file..."
readLimitsFromFile(INPUT, fileMap, h_lims_mu0, h_lims_xs0, h_lims_yn0)


output = INPUT.replace(".txt",".root")
fout = ROOT.TFile(output, "RECREATE")
fout.cd()

print "interpolating..."
for lim in limits:
    # interpolation done automatically by TGraph2D using Delaunay method
    g2_lims_mu[lim] = ROOT.TGraph2D(h_lims_mu0[lim])
    binSize_inter = binSize/2. # bin size of interpolation graph (12.5 GeV as decided in dec7 meeting @ R40) 
    g2_lims_mu[lim].SetNpx( int((g2_lims_mu[lim].GetXmax()-g2_lims_mu[lim].GetXmin())/binSize_inter) )
    g2_lims_mu[lim].SetNpy( int((g2_lims_mu[lim].GetYmax()-g2_lims_mu[lim].GetYmin())/binSize_inter) )
    h_lims_mu[lim] = g2_lims_mu[lim].GetHistogram()
    h_lims_mu[lim].SetName( h_lims_mu0[lim].GetName().replace("mu0","mu") )

print "translating to x-sec and yes/no limits and saving 2d histos..."
for lim in limits:
    h_lims_yn[lim] = getLimitYN ( h_lims_mu[lim] )
    h_lims_xs[lim] = getLimitXS ( h_lims_mu[lim], h_xs )
    
    h_lims_mu0[lim].Write()
    h_lims_xs0[lim].Write()
    h_lims_yn0[lim].Write()
    h_lims_mu [lim].Write()
    h_lims_xs [lim].Write()
    h_lims_yn [lim].Write()


graphs0 = {}
graphs1 = {}  # smoothed

print "extracting contours and saving graphs..."
for lim in limits:
    # get contour. If graph2D is properly filled there should be only one countour in the list

    g_list = g2_lims_mu[lim].GetContourList(1.0)
    max_points = -1
    for il in range(g_list.GetSize()):
        gr = g_list.At(il)
        n_points = gr.GetN()
        if n_points > max_points:
            graphs0[lim] = gr
            max_points = n_points
    graphs0[lim].SetName("gr_"+lim)
    graphs0[lim].Write()
    
#print "smoothing..."
#for lim in limits:
#    h_lims_mu1[lim] = h_lims_mu[lim].Clone(h_lims_mu[lim].GetName()+"_smoothed")
#    #smooth here
#    h_lims_mu1[lim].Smooth(1,"k3a")
#    g2_lims_mu1[lim] = ROOT.TGraph2D(h_lims_mu1[lim])
#    g2_lims_mu1[lim].SetNpx( g2_lims_mu[lim].GetNpx() )
#    g2_lims_mu1[lim].SetNpy( g2_lims_mu[lim].GetNpy() )
#
#    # get countour of smoothed version
#    g_list = g2_lims_mu1[lim].GetContourList(1.0)
#    max_points = -1
#    for il in range(g_list.GetSize()):
#        gr = g_list.At(il)
#        n_points = gr.GetN()
#        if n_points > max_points:
#            graphs1[lim] = gr
#            max_points = n_points
#    graphs1[lim].SetName("gr_"+lim+"_smoothed")
#    graphs1[lim].Write()


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
    graphs0[lim].SetLineWidth(2)
    graphs0[lim].Draw("same")
    graphs1[lim].SetLineWidth(2)
    graphs1[lim].SetLineColor(2)
    graphs1[lim].Draw("same")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".eps")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".png")
    can.SaveAs(plotsDir+"/" + model + "_" + lim + ".pdf")


print "file "+output+" saved"
fout.Close()
