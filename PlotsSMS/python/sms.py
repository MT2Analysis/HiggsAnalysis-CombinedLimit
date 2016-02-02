from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()
        if modelname.find("T2tt")   != -1: self.T2tt  ()
        if modelname.find("T2bb")   != -1: self.T2bb  ()
        if modelname.find("T2qq")   != -1: self.T2qq  ()


    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 700
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1900
        self.Zmin = 0.001
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mT = 175
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mT, 20000-mT])        
        # turn off diagonal lines
        self.diagOn = False
        self.mTopDiagOn = False
        
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1900
        self.Zmin = 0.001
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])
        # turn off diagonal lines
        self.diagOn = False
        self.mTopDiagOn = False
 
    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1600
        self.Zmin = 0.001
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{#tilde{g}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])
        # turn off diagonal lines
        self.diagOn = False
        self.mTopDiagOn = False

    def T2tt(self):
        # model name
        self.modelname = "T2tt"
        # decay chain
        self.label= "pp #rightarrow #tilde{t} #tilde{t}, #tilde{t} #rightarrow t #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 100
        self.Xmax = 900
        self.Ymin = 0
        self.Ymax = 500
        self.Zmin = 0.001
        self.Zmax = 20
        #self.Zmin = 0.1
        #self.Zmax = 10
        # produce sparticle
        self.sParticle = "m_{#tilde{t}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 75
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        # turn off diagonal lines
        self.diagOn = True
        #self.mT, self.dM = 172.5, 6.25
        self.mT, self.dM = 175, 25
        self.mTopDiagOn = True
        
    def T2bb(self):
        # model name
        self.modelname = "T2bb"
        # decay chain
        self.label= "pp #rightarrow #tilde{b} #tilde{b}, #tilde{b} #rightarrow b #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 300
        self.Xmax = 1000
        self.Ymin = 0
        self.Ymax = 700
        self.Zmin = 0.001
        self.Zmax = 20
        # produce sparticle
        self.sParticle = "m_{#tilde{b}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 75
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        # turn off diagonal lines
        self.diagOn = False
        #self.mT, self.dM = 172.5, 6.25
        self.mT, self.dM = 175, 25
        self.mTopDiagOn = False
        
    def T2qq(self):
        # model name
        self.modelname = "T2qq"
        # decay chain
        self.label= "pp #rightarrow #tilde{q} #tilde{q}, #tilde{q} #rightarrow q #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 400
        self.Xmax = 1500
        self.Ymin = 0
        self.Ymax = 1200
        self.Zmin = 0.001
        self.Zmax = 5
        # produce sparticle
        self.sParticle = "m_{#tilde{q}} [GeV]"
        # LSP
        self.LSP = "m_{#tilde{#chi}_{1}^{0}} [GeV]"
        # diagonal position: mLSP = mgluino - 2mtop 
        mW = 75
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mW, 20000-mW])        
        # turn off diagonal lines
        self.diagOn = False
        #self.mT, self.dM = 172.5, 6.25
        self.mT, self.dM = 175, 25
        self.mTopDiagOn = False
        
