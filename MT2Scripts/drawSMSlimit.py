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

xsfile = "SUSYCrossSections13TeVgluglu.root" if "T1" in model else "SUSYCrossSections13TeVstopstop.root" if model=="T2tt" else "theXSfile.root"
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


def extractSmoothedContour(hist, nSmooth=1):
    # if name contains "mu" histogram is signal strenght limit, otherwise it's a Yes/No limit
    isMu = "mu" in hist.GetName()
    #ROOT.gStyle.SetNumberContours(4 if isMu else 2)
    shist = hist.Clone(hist.GetName()+"_smoothed")

    # if smoothing a limit from mu, we need to modify the zeros outside the diagonal, otherwise the smoothing fools us in the diagonal transition
    if isMu:
        for ix in range(1, shist.GetNbinsX()):
            for iy in range(shist.GetNbinsY(),0,-1):
                if shist.GetBinContent(ix,iy)==0:
                    for iyy in range(iy, shist.GetNbinsY()):
                        shist.SetBinContent(ix,iyy, shist.GetBinContent(ix,iy-1))
                else:
                    break

    for s in range(nSmooth):
        #shist.Smooth() # default smoothing algorithm
        shist.Smooth(1,"k3a")  # k3a smoothing algorithm

    # after smoothing a limit from mu, we need to modify the zeros outside the diagonal, otherwise the contours come wrong for the diagonal
    if isMu:
        for ix in range(1,shist.GetNbinsX()):
            for iy in range(1,shist.GetNbinsY()):
                if hist.GetBinContent(ix,iy)==0:
                    shist.SetBinContent(ix,iy, 1.1)
        
    shist.SetMinimum(0)
    shist.SetMaximum(2 if isMu else 1)
    shist.SetContour(4 if isMu else 2)
    canvas = ROOT.TCanvas()
    shist.Draw("contz list")
    ROOT.gPad.Update()
    obj = ROOT.gROOT.GetListOfSpecials().FindObject("contours")
    list = obj.At(1 if isMu else 0)
    ## take largest graph
    #max_points = -1
    #for l in range(list.GetSize()):
    #    gr = list.At(l).Clone()
    #    n_points = gr.GetN()
    #    if n_points > max_points:
    #        graph = gr
    #        max_points = n_points

    graph = []
    for l in range(list.GetSize()):
        gr = list.At(l).Clone()
        n_points = gr.GetN()
        graph.append((n_points,gr))
    graph.sort(reverse=True)

    #graph = list.First().Clone()
    name = "gr_"
    name += shist.GetName()
    #graph.SetName(name)
    for i,g in enumerate(graph):
        g[1].SetName(name+(str(i)if i>0 else ""))
    #graph.Draw("sameC")
    del canvas
    del shist
    del obj
    del list
    if len(graph)==1: graph.append(graph[0])
    return [graph[0][1], graph[1][1]]  # return list of two largest graphs


def extractSmoothedContourRL(hist, nSmooth1):
    hR, hL = hist.Clone("muR"), hist.Clone("muL")
    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            m1, m2 = hist.GetXaxis().GetBinLowEdge(ix), hist.GetYaxis().GetBinLowEdge(iy)
            if m1-m2>=175:
                hL.SetBinContent(ix,iy, 0)
            if m1-m2<=175:
                hR.SetBinContent(ix,iy, 0)

    # check if graph 0 makes sense, otherwise take graph 1
    nL = 0
    g = extractSmoothedContour(hL, nSmooth)
    x,y = ROOT.Double(0), ROOT.Double(0)
    g[0].GetPoint(8,x,y)
    if (x-y)>175: nL=1

    gR,gL = extractSmoothedContour(hR, nSmooth)[0], g[nL]
    gR.SetName("gr_"+hist.GetName()+"_smoothed")
    gL.SetName("gr_"+hist.GetName()+"_smoothed1")
    return [gR,gL]
    

def unexcludeDiagonal(hist): 
    for ix in range(1,hist.GetNbinsX()+1):
        for iy in range(1,hist.GetNbinsY()+1):
            m1, m2 = hist.GetXaxis().GetBinLowEdge(ix), hist.GetYaxis().GetBinLowEdge(iy)
            val = hist.GetBinContent(ix,iy)
            if m1-m2==175:
                hist.SetBinContent(ix,iy, max(1.5,val))

def mergeGraphs(graphs):
    mg = ROOT.TMultiGraph()
    mg.Add(graphs[0])
    mg.Add(graphs[1])
    g = ROOT.TGraph()
    g.Merge(mg.GetListOfGraphs())
    g.SetName(graphs[0].GetName())
    return g


h_lims_mu0 = {} # limits in signal-strength, original binning
h_lims_yn0 = {} # limits in excluded/non-exluded, original binning
h_lims_xs0 = {} # limits in cross-section, original binning

h_lims_mu   = {} # limits in signal-strength, interpolated
h_lims_yn   = {} # limits in excluded/non-exluded, interpolated
h_lims_xs   = {} # limits in cross-section, interpolated
g2_lims_mu  = {} # TGraph2D limits in signal-strength, automatic interpolation

m1min, m1max = 0, 2000
m2min, m2max = 0, 2000
binSize = 25

mass1 = "mGlu" if "T1" in model else "mSq" if model=="T2qq" else "mSb" if model=="T2bb" else "mSt" if model=="T2tt" else "m1"
mass2 = "mLSP"

# create histos
for lim in limits:
    # uniform 25 GeV binning
    #h_lims_mu0[lim] = ROOT.TH2F(lim+"_mu0", model, (m1max-m1min+binSize)/binSize, m1min-binSize/2., m1max+binSize/2., (m2max-m2min+binSize)/binSize, m2min-binSize/2., m2max+binSize/2.)
    h_lims_mu0[lim] = ROOT.TH2F(lim+"_mu0", model, (m1max-m1min+binSize)/binSize, m1min-binSize/2., m1max+binSize/2., (m2max-m2min+2*binSize)/(binSize), m2min-3*binSize/2., m2max+binSize/2.)
    h_lims_mu0[lim].SetXTitle(mass1)    
    h_lims_mu0[lim].SetYTitle(mass2)

    h_lims_yn0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","yn"))
    h_lims_xs0[lim] = h_lims_mu0[lim].Clone(h_lims_mu0[lim].GetName().replace("mu","xs"))


# read txt file with limits (map defined above)
print "reading file..."
readLimitsFromFile(INPUT, fileMap, h_lims_mu0, h_lims_xs0, h_lims_yn0)

# so graph goes below mLSP=0 and there is no cut off above zero
def fillHorizontalBelowZero(hist):
    for ix in range(1,hist.GetNbinsX()+1):
        hist.SetBinContent( ix,1,hist.GetBinContent(ix,2) )

output = INPUT.replace(".txt",".root")
fout = ROOT.TFile(output, "RECREATE")
fout.cd()

print "interpolating..."
for lim in limits:
    fillHorizontalBelowZero(h_lims_mu0[lim])
    # interpolation done automatically by TGraph2D using Delaunay method
    g2_lims_mu[lim] = ROOT.TGraph2D(h_lims_mu0[lim])
    binSize_inter = binSize/2. # bin size of interpolation graph (12.5 GeV as decided in dec7 meeting @ R40) 
    g2_lims_mu[lim].SetNpx( int((g2_lims_mu[lim].GetXmax()-g2_lims_mu[lim].GetXmin())/binSize_inter) )
    g2_lims_mu[lim].SetNpy( int((g2_lims_mu[lim].GetYmax()-g2_lims_mu[lim].GetYmin())/binSize_inter) )
    h_lims_mu[lim] = g2_lims_mu[lim].GetHistogram()
    h_lims_mu[lim].SetName( h_lims_mu0[lim].GetName().replace("mu0","mu") )
             

print "translating to x-sec and yes/no limits and saving 2d histos..."
for lim in limits:
    #if model=="T2tt":
    #    unexcludeDiagonal( h_lims_mu[lim] )

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
    # get contour. choose the one with maximum number of points
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
    

print "smoothing..."
for lim in limits:
    nSmooth = 1 if model=="T2tt" else 2 if model!="T1tttt" else 3  # more aggresive smoothing for t1tttt since it's full of holes
    if model!="T2tt":
        graphs = extractSmoothedContour(h_lims_mu[lim], nSmooth)
        graphs1[lim]=graphs[0]
    else:
        graphs = extractSmoothedContourRL(h_lims_mu[lim], nSmooth)
        graphs1[lim]=mergeGraphs(graphs)
    #if model!="T2tt":
    #    graphs1[lim]=graphs[0]
    #else:
    #    graphs1[lim]=mergeGraphs(graphs)

    graphs1[lim].SetName( graphs1[lim].GetName().replace("_mu","") ) 
    graphs1[lim].Write()


print "saving x-check plots"
plotsDir = "xcheckPlots"
can = ROOT.TCanvas("can","can",600,600)
if( not os.path.isdir(plotsDir) ):
    os.system("mkdir "+plotsDir)
for lim in limits:
    ROOT.gStyle.SetNumberContours( 100 )
    xmin = 600 if "T1" in model else 100 if model=="T2tt" else 0
    xmax = 1000 if model=="T2tt" else 2000
    ymax = 600  if model=="T2tt" else 1500
    h_lims_yn0[lim].GetXaxis().SetRangeUser(xmin, xmax)
    h_lims_yn0[lim].GetYaxis().SetRangeUser(0   , ymax)
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
