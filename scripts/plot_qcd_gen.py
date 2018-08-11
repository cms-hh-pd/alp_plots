#!/usr/bin/env python
import ROOT

from Analysis.alp_analysis.alpSamples import samples
from Analysis.alp_plots.UtilsDraw import setTDRStyle, CMS_lumi, setLegend, get_bias_corrected_histo

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
 
def plot_qcd(infile, rebin = 1, bkg_file = "../hh2bbbb_limit/classifier_reports/reports_no_bias_corr_SM_mixing_fix/BM0/20171120-160644-bm0.root"):
    f = TFile.Open(infile)
    f2 = TFile.Open(bkg_file)
    H_ref = 800     
    W_ref = 800
    W = W_ref
    H = H_ref
    
    iPos = 11
    iPeriod = 4
    
    c1 = TCanvas("c1", "QCD MC distributions", H_ref, W_ref)
    setTDRStyle()
    
    T = 0.08*H_ref
    B = 0.12*H_ref 
    L = 0.12*W_ref
    R = 0.04*W_ref
    
    c1.SetFillColor(0)
    c1.SetBorderMode(0)
    c1.SetFrameFillStyle(0)
    c1.SetFrameBorderMode(0)
    c1.SetLeftMargin( L/W )
    c1.SetRightMargin( R/W )
    c1.SetTopMargin( T/H )
    c1.SetBottomMargin( B/H )
    #c1.SetBottomMargin( 0 )

    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    pad1.SetTopMargin(0.1) 
    pad1.SetBottomMargin(0.03) 
    pad1.Draw()             
    pad1.cd()
    #pad1.SetLogy()
    
    bkg = f2.Get("bkg_appl/classifier-20171120-160644-bm0_bkg_appl")
    bkg_corr = get_bias_corrected_histo(bkg)

    for b in range(1, bkg.GetNbinsX()+1):
        print bkg.GetBinContent(b), bkg_corr.GetBinContent(b)

    bkg.Scale(1/bkg.Integral())
    bkg.Rebin(rebin)
    bkg.SetMaximum(0.12)
    #bkg.SetLineWidth(2)
    #c.SetLogY()
    bkg_corr.Scale(1/bkg_corr.Integral())
    bkg_corr.Rebin(rebin)
        

    bkg.GetYaxis().SetTitleSize(20)
    bkg.GetYaxis().SetTitleFont(43)
    bkg.GetYaxis().SetTitleOffset(1.40)
    bkg.GetYaxis().SetLabelFont(43)
    bkg.GetYaxis().SetLabelSize(18)
    #bkg.GetYaxis().SetTitle("Events")
    pad1.SetTickx(1)
    CMS_lumi(pad1, iPeriod, iPos)
    
    legend = setLegend(0.7,0.60,0.90,0.85)    
    

    #leg.SetTextSize(0.033);
    #leg.SetFillColor(0);
    #leg.SetNColumns(1);
    #pl2.SetHeader(training);
  
    bkg.Draw("e1")
    bkg.GetXaxis().SetTitle("BDT")
    legend.AddEntry(bkg, "Mixed data",  "p")
    
    total_mc = f.Get("QCD_HT2000toInf_m_%s/classifier-20171120-160644-bm0_QCD_HT2000toInf_m_%s" % ("bbbb", "bbbb"))
    total_mc.Reset()
    assert total_mc.Integral() == 0
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
        total_mc.Add(hist)
  
    total_mc.Rebin(rebin)
    total_mc.SetLineColor(ROOT.kBlue)
    total_mc.SetLineWidth(1)
    total_mc.SetMarkerStyle(8)
    total_mc.SetMarkerColor(ROOT.kBlue)
    total_mc.Scale(1/total_mc.Integral())
    total_mc.Draw("E1 SAME")
    legend.AddEntry(total_mc, "QCD MC",  "p")
  
    for bin in range(1, bkg.GetNbinsX() + 1):
        print bin, bkg.GetBinContent(bin), bkg_corr.GetBinContent(bin)

    bkg_corr.SetLineColor(ROOT.kRed)
    bkg_corr.SetMarkerColor(ROOT.kRed)
    bkg_corr.Draw("E1 same")
    legend.AddEntry(bkg_corr, "Mixed data bias corrected",  "p")
    
    #ks = hlist[0][0].KolmogorovTest(hlist[1][0])
    #        print("KS: ", ks)
    #        print("Chi2: ", hlist[0][0].Chi2Test(hlist[1][0], "UU NORM"))
    
    
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)   
        
    legend.Draw("same")

    #if(ymax > 1000): TGaxis.SetMaxDigits(3)
    """for i in range(len(hs)):
        hs[i].SetMaximum(ymax)
        herr[i].SetMaximum(ymax)
        plotH(hlist[i], hs[i], herr[i], dofill[i], residuals)
        if i == len(hs) - 1:
            herr[i].Draw("Esameaxis")
    """
    
    bkg.GetXaxis().SetLabelSize(0.)
    legend.Draw("same")


    c1.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
    pad2.SetTopMargin(0.)
    pad2.SetBottomMargin(0.2)
    pad2.Draw()
    pad2.cd()
    
    ratio = bkg.Clone("ratio")
    ratio.Divide(total_mc)

    ratio.SetMinimum(0.)
    ratio.SetMaximum(2.)

    ratio_corr = bkg_corr.Clone("ratio_corr")
    ratio_corr.Divide(total_mc)
    """h_err = total_mc.Clone("error_bar")    
    
    h_err.GetXaxis().SetRangeUser(0, 1)
    #h_err.Reset()
    #herr.Rebin(rebin)
    h_err.GetXaxis().SetTitle("BDT classifier")
    h_err.SetFillStyle(3005)
    h_err.SetFillColor(ROOT.kBlue)
    h_err.SetLineColor(922)
    h_err.SetLineWidth(0)         
    h_err.SetMarkerSize(0)
    h_err.SetMarkerColor(922)
    #h_err.SetMinimum(0.)
    
    
    #h_sig.SetLineStyle(1)
    #h_sig.SetLineWidth(2)
    #h_sig.SetLineColor(sam_opt["sig"]['linecolor'])
    
    #Set error centered at zero as requested by ARC
    for ibin in range(1, h_err.GetNbinsX()+1):
        h_err.SetBinContent(ibin, 0. )

    #If not loading already morphed fit results
    if postfit_file == None:
        for ibin in range(1, h_err.GetNbinsX()+1):
            h_err.SetBinError(ibin, math.sqrt((err * h_err.GetBinContent(ibin))**2 + h_data_bkg.GetBinError(ibin)**2) )
    else:
        for ibin in range(1, h_err.GetNbinsX()+1):
            if not only_bias_unc:
                h_err.SetBinError(ibin, math.sqrt(h_sig.GetBinError(ibin)**2 + h_data_bkg.GetBinError(ibin)**2) )
            else:
                h_err.SetBinError(ibin, math.sqrt(h_data_bkg.GetBinError(ibin)**2) )
    return h_data_bkg, h_sig, h_err
    """

    ratio.Draw("e1")
    ratio_corr.Draw("e1 same")
    
    l = TLine(0.,1.,1.,1.)
    l.SetLineStyle(3)
    l.Draw("same")
   
    
    """leg_coords = 0.65,0.2,0.9,0.4
    if "legpos" in hsOpt:
        if hsOpt["legpos"] == "top":
            leg_coords = 0.65,0.78,0.9,1.
        elif hsOpt["legpos"] == "left" or hsOpt["legpos"] == "topleft":
            leg_coords = 0.1,0.78,0.35,1.
        elif hsOpt["legpos"] == "middle":
            leg_coords = 0.47,0.0,0.63,0.25
    leg = TLegend(*leg_coords)
    leg.SetTextSize(0.05)
    leg.AddEntry(h_data_bkg, "Data - fitted background", "p")
    leg.AddEntry(h_sig, "HH4b fitted")
    leg.AddEntry(hlist[0][-1], "HH4b fitted x5")
    leg.AddEntry(h_error, "Total uncertainty")
    leg.Draw("same")"""
    

    c1.SaveAs("qcd_plot.png")
    c1.SaveAs("qcd_plot.pdf")
    c1.Clear()
    f.Close()

if __name__ == "__main__":
  ROOT.gStyle.SetOptStat(0)
  ROOT.gROOT.SetBatch(True)
  infile = "../hh2bbbb_limit/classifier_reports/qcd_gen/20171120-160644-bm0.root"
  #plot_qcd_gen(infile)
  plot_qcd(infile, rebin = 1)
