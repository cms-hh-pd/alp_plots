#!/usr/bin/env python
import ROOT

from Analysis.alp_analysis.alpSamples import samples

import ROOT
from ROOT import TFile, TCanvas, TPad, TLine, TH1D, TLatex, TLegend


def plot_qcd_gen(infile):
  f = TFile.Open(infile)
    
  c = TCanvas("QCD MC distributions", "QCD MC distributions", 600, 600)
  c.SetGrid()

  leg = TLegend(0.62,0.66,0.9,0.86)
  leg.SetTextSize(0.033);
  leg.SetFillColor(0);
  leg.SetNColumns(1);
  #pl2.SetHeader(training);
  
  bkg = f.Get("bkg_appl/classifier-20171120-160644-bm0_bkg_appl")
  bkg.Scale(1/bkg.Integral())
  bkg.Rebin(5)
  bkg.SetMaximum(0.5)
  bkg.SetLineWidth(2)
  #c.SetLogY()
  bkg.Draw("e1")
  bkg.GetXaxis().SetTitle("BDT")
  leg.AddEntry(bkg, "Mixed data",  "p")
  colors = {
    "bbcc": ROOT.kBlue, 
    "bbll": ROOT.kGreen, 
    "bbbb": ROOT.kRed,
    "cccc": ROOT.kOrange}
  for state in ["bbcc", "bbll", "bbbb", "cccc"]:
    hist = f.Get("QCD_HT2000toInf_m_%s/classifier-20171120-160644-bm0_QCD_HT2000toInf_m_%s" % (state, state))
    hist.Reset()
    assert hist.Integral() == 0
    for htrange in ["700to1000", "1000to1500", "1500to2000", "2000toInf", "200to300", "300to500", "500to700"]:
      sampname = "QCD_HT%s" % htrange 
      qcdname = "%s_m" % sampname
      
      #print "QCD_all_%s/classifier-20171120-160644-bm0_QCD_all_%s" % (state, state)
      myhist = f.Get("%s_%s/classifier-20171120-160644-bm0_%s_%s" % (qcdname, state, qcdname, state))
      samples_std = samples[sampname]
      samples_ext = samples["%s_ext" % sampname]
      n_events = samples_std["nevents"] + samples_ext["nevents"]
      xs_br = samples_ext["xsec_br"]
      scalef = xs_br / n_events
      myhist.Scale(scalef)
      hist.Add(myhist)
    hist.Scale(1/hist.Integral())
    hist.Rebin(5)
    hist.SetLineColor(colors[state])
    hist.SetLineWidth(2)
    hist.SetMarkerColor(colors[state])
    hist.Draw("E1 SAME")
    leg.AddEntry(hist, "QCD MC %s" % state,  "p")
  
  leg.Draw("same")

  c.SaveAs("qcd_gen_plot.png")
  c.SaveAs("qcd_gen_plot.pdf")
  f.Close()
 


if __name__ == "__main__":
  ROOT.gStyle.SetOptStat(0)
  ROOT.gROOT.SetBatch(True)
  infile = "../hh2bbbb_limit/classifier_reports/qcd_gen/20171120-160644-bm0.root"
  plot_qcd_gen(infile)
