from array import *

class sms():

    def __init__(self, modelname):
        if modelname.find("T1tttt") != -1: self.T1tttt()
        if modelname.find("T1bbbb") != -1: self.T1bbbb()
        if modelname.find("T1qqqq") != -1: self.T1qqqq()
        if modelname.find("T2qq") != -1: self.T2qq()

    def T1tttt(self):
        # model name
        self.modelname = "T1tttt"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow t #bar{t} #tilde{#chi}^{0}_{1}";
        # scan range to plot
        self.Xmin = 700
        self.Xmax = 1950
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmin = 0.005
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"        
        # diagonal position: mLSP = mgluino - 2mtop 
        mT = 175
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[-mT, 20000-mT])        
        
    def T1bbbb(self):
        # model name
        self.modelname = "T1bbbb"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow b #bar{b} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 1800
        self.Zmin = 0.001
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])

    def T1qqqq(self):
        # model name
        self.modelname = "T1qqqq"
        # decay chain
        self.label= "pp #rightarrow #tilde{g} #tilde{g}, #tilde{g} #rightarrow q #bar{q} #tilde{#chi}^{0}_{1}";
        # plot boundary. The top 1/4 of the y axis is taken by the legend
        self.Xmin = 600
        self.Xmax = 2000
        self.Ymin = 0
        self.Ymax = 1600
        self.Zmin = 0.002
        self.Zmax = 2
        # produce sparticle
        self.sParticle = "m_{gluino} (GeV)"
        # LSP
        self.LSP = "m_{LSP} (GeV)"
        # diagonal position: mLSP = mgluino - 2mtop
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])

    def T2qq(self):
        # model name
        self.modelname = "T2qq"
        # decay chain
        self.label= "pp #rightarrow #tilde{q} #tilde{q}, #tilde{q} #rightarrow q #tilde{#chi}^{0}_{1}";#, m(#tilde{g})#gg m(#tilde{b})";
        # plot boundary.
        self.Xmin = 300
        self.Xmax = 1100
        self.Ymin = 0
        self.Ymax = 800
        self.Zmin = 0.001
        self.Zmax = 100
        # produce sparticle
        self.sParticle = "m_{q} [GeV]"
        # LSP
        self.LSP = "m_{LSP} [GeV]"
        # diagonal position: mLSP = msbottom - mbottom
        self.diagX = array('d',[0,20000])
        self.diagY = array('d',[0, 20000])
