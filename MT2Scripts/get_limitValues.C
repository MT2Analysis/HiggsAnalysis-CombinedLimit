#include<iomanip>
#include<iostream>
#include<fstream>

#include "TFile.h"
#include "TString.h"
//#include "RooStats/HypoTestResult.h"
//#include <RooStats/HypoTestPlot.h>

using namespace RooStats;

void get_limitValues(TString fileName = "results_mt2b_4.7fb-1/higgsCombineMT2scan_hybrid_m0-1000_m12-400.HybridNew.mH120.1.root", bool doPlot=true){

  TString mass = fileName(fileName.Index("m0"),fileName.Index("m12")-fileName.Index("m0")+7);
  cout << "mass = " << mass << endl;

  TFile *file = new TFile(fileName);

  // --- to figure out the name of the toyResult key
  string toyResultName;
  gDirectory->cd("toys");
  TIter next(gDirectory->GetListOfKeys());
  TKey *key;
  while ((key=(TKey*)next())) {
    string name=key->GetName();
    if(name.find("HypoTestResult") != std::string::npos){
      cout << "key name: " << name << endl;
      toyResultName=name;
    }
  }
  gDirectory->cd("..");
  // ---------

  RooStats::HypoTestResult *h = (RooStats::HypoTestResult*)file->Get(("toys/"+toyResultName).c_str());
  //RooStats::HypoTestResult *h = (RooStats::HypoTestResult*)file->Get("toys/HypoTestResult_mh120_r0.1_630311758");
  //RooStats::HypoTestResult *h = (RooStats::HypoTestResult*)file->Get("toys/HypoTestResult_mh120_r0.8_630311758");
  //RooStats::HypoTestResult *h = (RooStats::HypoTestResult*)file->Get("toys/HypoTestResult_mh120_r35_630311758");

  //h->Print();
  RooStats::HypoTestPlot *plot = new RooStats::HypoTestPlot(*h,150);
  TH1F* hb = (TH1F*)gDirectory->Get("HybridNew_mc_b");
  
  Double_t obsTestStat = h->GetTestStatisticData();

  Double_t quantile[5] = {0.5, 0.16,0.84,0.022,0.978};
  Double_t testStat[5];
  
  hb->GetQuantiles(5,testStat,quantile);
  
  //hb->Draw();
  for(int index=0; index<5; index++){
    cout << "quantile,testStat: " << quantile[index] << " , " << testStat[index] << endl;
  }


  float obsCLs, expCLs, pSigmaCLs,mSigmaCLs, p2SigmaCLs,m2SigmaCLs;

  obsCLs = h->CLs();
  float obsCLb = h->CLb();
  cout << "probability of a background only fluctuation to the observed test statistic: " << obsCLb
       << " ("<< TMath::NormQuantile(obsCLb) << "sigma)" << endl;


  h->SetTestStatisticData(testStat[0]);
  expCLs = h->CLs();
  h->SetTestStatisticData(testStat[1]);
  pSigmaCLs = h->CLs();
  h->SetTestStatisticData(testStat[2]);
  mSigmaCLs = h->CLs();
  h->SetTestStatisticData(testStat[3]);
  p2SigmaCLs = h->CLs();
  h->SetTestStatisticData(testStat[4]);
  m2SigmaCLs = h->CLs();

  cout << "Observed CLs: "         << obsCLs    << endl
       << "Median Expected CLs: "  << expCLs    << endl
       << "+1sigma Expected CLs: " << pSigmaCLs << endl
       << "-1sigma Expected CLs: " << mSigmaCLs << endl
       << "+2sigma Expected CLs: " << p2SigmaCLs << endl
       << "-2sigma Expected CLs: " << m2SigmaCLs << endl;

  if (doPlot){
    h->SetTestStatisticData(obsTestStat);
    cout << "**************************" << endl
	 << "***     OBSERVED       ***" << endl
	 << "**************************" << endl;
    h->Print();

    plot->Draw();
    gPad->SetLogy();

    TLine *l[5];
    for (int i=0; i<5;i++){
      l[i] = new TLine(testStat[i],0,testStat[i],10);
      if (i<4) l[i]->Draw("same");
      h->SetTestStatisticData(testStat[i]);
      cout << "**************************" << endl
	   << "***  " << quantile[i]*100 << "% EXPECTED  ***" << endl
	   << "**************************" << endl;
      h->Print();
    }
    TPaveText *title = new TPaveText(.1,.9,.35,.95,"NDC");
    title->SetFillColor(0);
    title->AddText(mass.Data());
    title->Draw("same");
    TPaveText *pave  = new TPaveText(.58,.55,.88,.8,"NDC");
    pave->SetFillColor(0);
    pave->AddText("Obs.CLs = "+TString::Format("%f",obsCLs));
    pave->AddText("Median exp. CLs = "+TString::Format("%f",expCLs));
    pave->AddText("+#sigma exp. CLs = "+TString::Format("%f",pSigmaCLs));
    pave->AddText("-#sigma exp. CLs = "+TString::Format("%f",mSigmaCLs));
    pave->Draw("same");
  }
  else file->Close();

}
