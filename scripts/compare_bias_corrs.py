import Analysis.alp_plots.UtilsDraw as UtilsDraw
#from UtilsDraw import get_bias_corrected_histo
import json
#import os
#import math
#from glob import glob

import numpy as np
# ROOT imports
from ROOT import TChain, TPad, TH1F, TH1D, TH2D, TFile, vector, TCanvas, TLatex, TLine, TLegend, THStack, gStyle, TGaxis, TPolyLine, TGraph
import ROOT
from rootpy.plotting import Hist

from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.alpSamples import samples



TH1F.AddDirectory(0)
#ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(False)
    

def get_bias_corr(region):
    if region == "ms":
        bkg_bias_fname = "/lustre/cmswork/dcastrom/projects/hh/april_2017/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/notebooks/bias_22032018_with_weights_also_mass_cut/BM0/bias_correction_mass_cut_bigset_unscaled.json"
        bkg_bias_fname = "/lustre/cmswork/dcastrom/projects/hh/april_2017/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/bias_01062018BM0/bias_correction_mass_cut_bigset_unscaled.json"
    elif region == "btag":
        bkg_bias_fname = "/lustre/cmswork/dcastrom/projects/hh/april_2017/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/notebooks/bms_btagside_err_fixed/BM0/bias_correction_bigset_unscaled.json"
    elif region == "sig_unfixed":
        bkg_bias_fname = "/lustre/cmswork/dcastrom/projects/hh/april_2017/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/notebooks/bias_22032018_with_weights_also_mass_cut/BM0/bias_correction_bigset_unscaled.json"
    else:
        bkg_bias_fname = "/lustre/cmswork/dcastrom/projects/hh/april_2017/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/bias_01062018BM0/bias_correction_bigset_unscaled.json"
        
    with open(bkg_bias_fname,"r") as bkg_bias_file:
        json_dict = json.load(bkg_bias_file)
        print ("using bias file: ", bkg_bias_file)

    histo = Hist(json_dict['bin_edges'])
    print histo
    
    #hcorr = histo.Clone("h_bias_corrected")
    #hcorr.Scale(4)
    #hbias = histo.Clone("h_bias")
    for n in range(len(json_dict['bias_corr'])):
        bias = json_dict['bias_corr'][n]
        var = json_dict['var'][n]
        bias_unc = json_dict['bias_corr_unc_bs'][n]
        bias_unc_stat = json_dict['bias_corr_unc_stat'][n]
        
        #bkg_pred_initial = hcorr.GetBinContent(n+1)
        #if var > np.sqrt(bkg_pred_initial):
        new_bkg_pred_stat = var
        #else:
        #  new_bkg_pred_stat = np.sqrt(bkg_pred_initial)

                        
        #new_bkg_pred_tot_unc = np.sqrt(new_bkg_pred_stat**2 + bias_unc**2 + bias_unc_stat**2)
        new_bkg_pred_tot_unc = np.sqrt(bias_unc**2 + bias_unc_stat**2)
        
        histo.SetBinContent(n+1, bias)
        histo.SetBinError(n+1, new_bkg_pred_tot_unc)
        
    histo.Scale(0.25)
    #hcorr.Add(hbias, -1)
    return histo


def plot_comparison():
    reg_fixed = ""
    reg_old = "sig_unfixed"    
    bias_fixed = get_bias_corr(reg_fixed)
    bias_old = get_bias_corr(reg_old)
    c = TCanvas("c", "c", 800,800)
    bias_fixed.Divide(bias_old)
    bias_fixed.SetMinimum(-2)
    bias_fixed.SetMaximum(2)
    bias_fixed.Draw()
    c.SaveAs("plots/bias_comparison.png")


def plot_backgrounds():
    bdt = "20171120-160644-bm0"
    iDir1       = '../hh2bbbb_limit/classifier_reports/reports_SM_nocut_mixing_nofix/BM0'
    iDir2       = "../hh2bbbb_limit/classifier_reports/reports_SM_no_bias_corr_mixing_fix/BM0"
    filename1 = iDir1+"/"+bdt+".root"
    filename2 = iDir2+"/"+bdt+".root"
    intLumi_fb = 35.9
    doNormToLumi = False
    weights = []
    sf = []
    fractions = ['appl']
    regions = ['','']
    #legList = [["Mixed data"], ["Data"]]
    #colorList = [[430], [1]]
    sf = [0.25]
    
    #bm = int(args.bdt.split("-")[2][2:]) 
    
    samples = [["bkg"]]
    snames = []
    for i in range(len(samples)):
        snames.append([])
        for s in samples[i]:
            if not s in samlists: 
                if not s in samples: 
                    snames[i].append(s)
                else:
                    snames[i].append(samples[s]['sam_name'])    
            else: 
                snames[i].extend(samlists[s])
    
    plotDirs = []
    for i in range(len(snames)):
        plotDirs.append([])
        for sam in snames[i]:
            option = ''
            if fractions[i]: 
                option += fractions[i]
                #if regions[i]: option += "_"
            #if regions[i]: option += regions[i]

            if option: plotDirs[i].append(sam+'_'+option)
            else: plotDirs[i].append(sam)
    print "HISTS FROM FOLDER {}".format(plotDirs[i]) 

    print 'classifier-'+bdt+"/", plotDirs[0][0]
    h = 'classifier-'+bdt#+"_"+plotDirs[0][0]

    histo1 = UtilsDraw.getHistos_bdt(h, filename1, plotDirs[0], intLumi_fb, doNormToLumi, weights, sf)[0]
    histo2 = UtilsDraw.getHistos_bdt(h, filename2, plotDirs[0], intLumi_fb, doNormToLumi, weights, sf)[0]
    
    #histo_unfixed = histo1
    #histo_fixed = histo2
    histo_unfixed = UtilsDraw.get_bias_corrected_histo(histo1, "sig_unfixed")
    histo_fixed = UtilsDraw.get_bias_corrected_histo(histo2, "")
    
    c = TCanvas("c", "c", 800,800)
    pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
    #pad1.SetTopMargin(0) 
    pad1.SetBottomMargin(0.09)
    #pad1.SetLeftMargin(0.)
    #pad1.SetRightMargin(0.) 
    pad1.Draw()             
    pad1.cd()
    pad1.SetLogy()
    #bias_fixed.Divide(bias_old)
    #bias_fixed.SetMinimum(-2)
    #bias_fixed.SetMaximum(2)
    histo_unfixed.SetLineColor(ROOT.kRed)
    histo_unfixed.Draw("hist")
    histo_fixed.Draw("same e1")
    
    leg = TLegend(0.7,0.7,0.9,0.9)
    leg.AddEntry(histo_unfixed, "Bkg before bugfix", 'l')
    leg.AddEntry(histo_fixed, "Bkg after bugfix")
    leg.Draw("same")
    c.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.0, 1, 0.4)
    #pad1.SetTopMargin(0) 
    #pad2.SetBottomMargin(0.09)
    #pad1.SetLeftMargin(0.)
    #pad1.SetRightMargin(0.) 
    pad2.Draw()             
    pad2.cd()
    
    
    l = TLine(0,1,1,1)
    histo_rel = histo_fixed.Clone("h_rel")
    histo_rel.Divide(histo_unfixed)
    histo_rel.GetYaxis().SetTitle("Relative change with bugfix")
    histo_rel.GetXaxis().SetTitle("BDT")
    histo_rel.Draw()
    l.Draw("same")
    
    c.SaveAs("plots/bkg_comparison.png")
    
if __name__ == "__main__":
    #plot_comparison()
    plot_backgrounds()
