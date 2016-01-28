import sys
import ROOT as rt
rt.gROOT.SetBatch(True)

class inputFile():

    def __init__(self, fileName):
        self.HISTOGRAM = self.findHISTOGRAM(fileName)
        self.EXPECTED = self.findEXPECTED(fileName)
        self.OBSERVED = self.findOBSERVED(fileName)
        self.EXPECTED2 = self.findEXPECTED2(fileName)
        self.OBSERVED2 = self.findOBSERVED2(fileName)
        self.LUMI = self.findATTRIBUTE(fileName, "LUMI")
        self.ENERGY = self.findATTRIBUTE(fileName, "ENERGY")
        print self.ENERGY
        self.PRELIMINARY = self.findATTRIBUTE(fileName, "PRELIMINARY")

    def findATTRIBUTE(self, fileName, attribute):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != attribute: continue
            fileIN.close()
            return tmpLINE[1]

    def findHISTOGRAM(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "HISTOGRAM": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            x = rootFileIn.Get(tmpLINE[2])
            x.SetDirectory(0)
            return {'histogram': x}
            
    def findEXPECTED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            if len(tmpLINE)==7:
                return {'nominal': rootFileIn.Get(tmpLINE[2]),
                        'plus': rootFileIn.Get(tmpLINE[3]),
                        'minus': rootFileIn.Get(tmpLINE[4]),
                        'colorLine': tmpLINE[5],
                        'colorArea': tmpLINE[6]}
            elif len(tmpLINE)==9:
                return {'nominal': rootFileIn.Get(tmpLINE[2]),
                        'plus': rootFileIn.Get(tmpLINE[3]),
                        'minus': rootFileIn.Get(tmpLINE[4]),
                        'plus2': rootFileIn.Get(tmpLINE[5]),
                        'minus2': rootFileIn.Get(tmpLINE[6]),
                        'colorLine': tmpLINE[7],
                        'colorArea': tmpLINE[8]}

    def findOBSERVED(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'minus': rootFileIn.Get(tmpLINE[4]),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

    def findEXPECTED2(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "EXPECTED2": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            if len(tmpLINE)==7:
                return {'nominal': rootFileIn.Get(tmpLINE[2]),
                        'plus': rootFileIn.Get(tmpLINE[3]),
                        'minus': rootFileIn.Get(tmpLINE[4]),
                        'colorLine': tmpLINE[5],
                        'colorArea': tmpLINE[6]}
            elif len(tmpLINE)==9:
                return {'nominal': rootFileIn.Get(tmpLINE[2]),
                        'plus': rootFileIn.Get(tmpLINE[3]),
                        'minus': rootFileIn.Get(tmpLINE[4]),
                        'plus2': rootFileIn.Get(tmpLINE[5]),
                        'minus2': rootFileIn.Get(tmpLINE[6]),
                        'colorLine': tmpLINE[7],
                        'colorArea': tmpLINE[8]}

    def findOBSERVED2(self, fileName):
        fileIN = open(fileName)        
        for line in fileIN:
            tmpLINE =  line[:-1].split(" ")
            if tmpLINE[0] != "OBSERVED2": continue
            fileIN.close()
            rootFileIn = rt.TFile.Open(tmpLINE[1])
            return {'nominal': rootFileIn.Get(tmpLINE[2]),
                    'plus': rootFileIn.Get(tmpLINE[3]),
                    'minus': rootFileIn.Get(tmpLINE[4]),
                    'colorLine': tmpLINE[5],
                    'colorArea': tmpLINE[6]}

