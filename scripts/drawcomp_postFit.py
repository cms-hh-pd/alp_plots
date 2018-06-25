# to compare histograms - max samples with different options
# python scripts/drawcomp_afterBDT.py -w 0 -b 20170116-181049

import json
import os
from glob import glob
import importlib
import math

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector, TCanvas
import ROOT
from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.alpSamples import samples
from Analysis.alp_plots.histOpt import hist_opt
import Analysis.alp_plots.UtilsDraw as UtilsDraw



# parsing parameters
import argparse




def draw_postfit(args, fit_results, postfit_file, bm):
  which = args.whichPlots
  iDir       = '../hh2bbbb_limit/'+args.report_dir+'/'
  filename = iDir+"/"+args.bdt+".root"
  headerOpt = args.bdt
  intLumi_fb = args.lumi
  sig_xs = 33.53*0.5824*0.5824
  trg_eff = 0.96
  getChi = False
  getVar = False
  drawH2 = False
  doNormToLumi = [False, False]
  weights = [[],[]]
  sf = [[],[]]

  if args.hlist == 0:
      histList   = [ 'classifier']
  elif args.hlist == 1: # exact list of BDT input variables
      histList   = [
                    'h_jets_ht', 'h_jets_ht_r',
                    'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt',
                    'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
                    'h_cmva3','h_cmva4',
                    'h_H0_mass','h_H0_pt','h_H0_csthst0_a','h_H0_dr','h_H0_dphi',
                    'h_H1_mass','h_H1_pt', 'h_H1_dr','h_H1_dphi',
                    'h_H0H1_mass', 'h_H0H1_pt', 'h_H0H1_csthst0_a',
                    'h_X_mass',
                    'classifier'
                   ]
  elif args.hlist == 2:
      histList   = [
                    'h_csv3','h_csv4',
                    'h_H1_csthst2_a', 'h_H1_dr','h_H1_dphi','h_H0H1_dr',
                   ]

  bkg_scale_factor = fit_results["bkg"] * 0.25
  sig_scale_factor = fit_results["sig"][0] * args.lumi * trg_eff / (4172119.0 * 0.2)

  #samples = [['bkg', 'sig'],['data']] #data always  second
  samples = [['sig', 'bkg'],['data']] #data always  second
  fractions = ['','']
  regions = ['appl','']
  if bm == 0:
    legList = [["HH to 4b SM", "Mixed data",], ["Data"]]
  elif bm == 13:
    legList = [["HH to 4b Box", "Mixed data"], ["Data"]]
  else:
    legList = [["HH to 4b BM%d" % bm, "Mixed data"], ["Data"]]
  #legList = [["HH4b SM", "mixed data"], ["data"]]
  #colorList = [[430, 632], [1]]
  colorList = [[632, 600], [1]]
  #sf = [[bkg_scale_factor, sig_scale_factor],[1.]]
  sf = [[sig_scale_factor, bkg_scale_factor],[1.]]
  dofill = [True,False]
  isMC = False
  oname = 'comp_bkgdata_postfit'
  headerOpt = ""#"test sample" #btag CR

  if args.defaultCol: colors = [0,0]
  else: colors = colorList


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
            if regions[i]: option += "_"
        if regions[i]: option += regions[i]

        if option: plotDirs[i].append(sam+'_'+option)
        else: plotDirs[i].append(sam)
    print "HISTS FROM FOLDER {}".format(plotDirs[i])

  oDir = UtilsDraw.get_odir(args, oname, option)

  #----------------------------------
  for n, h in enumerate(histList):
      hOpt = hist_opt[h]
      pf_file = None
      if h == 'classifier': 
          h+='-'+args.bdt
          pf_file = postfit_file
      #hs1 = None
      #hs2 = None
      #if args.hlist > 0:
      print filename
  
      hs = []
      for i in range(len(snames)):
        hs.append(UtilsDraw.getHistos_bdt(h, filename, plotDirs[i], intLumi_fb, doNormToLumi[i], weights[i], sf[i]))

      if drawH2:
          UtilsDraw.drawH2(hs[0], hs[1], hist_opt["h2_bdt"], snames[0], args.clrebin, oDir, legList)
      elif getVar: # variance check
          UtilsDraw.drawBinVar(hs[0], snames[0], legList[0], hOpt, oDir, args.clrebin, headerOpt, isMC)
      elif getChi: # chi square
          UtilsDraw.drawChiSquare(hs[0], snames[0], legList[0], hs2, hOpt, oDir, xbmin, headerOpt, isMC, labels)
      else: 
          if len(hs) > 1:
              print "PF", pf_file
              print h
              n,nerr = UtilsDraw.drawH1(hs, snames, legList,
                           hOpt, args.plotResidual, args.doNorm, oDir, colors, dofill, args.clrebin, headerOpt, isMC, fit_results, pf_file)

def parse_args(parser):
  parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='0')
  parser.add_argument("-b", "--bdt", help="bdt version, equal to input file name (classifier report output)", required=True)
  parser.add_argument("--bm", help="Benchmark number", type = int, required=True)
  parser.add_argument("-o", "--oDir", help="output directory", default="plots")
  parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==pulls)", type=int, default=-4)
  parser.add_argument("-r", "--clrebin", help="to rebin (classifier output)", type=int, default=-1)
  parser.add_argument("-n", "--doNorm", help="do normalize ", action='store_true')
  parser.add_argument("-c", "--defaultCol", help="to use default colors", action='store_true')
  parser.add_argument("-l", "--list", help="hist list", dest="hlist", type=int, default=0)
  parser.add_argument("--lumi", help="int lumi to normalize to", dest="lumi", type=float, default=35.9)
  #parser.add_argument("-p", "--postfit", help="postfit histograms file", required=True)
  parser.add_argument("-d", "--report_dir", help="which report dir to use", dest="report_dir", required=True, default="reports")
  parser.set_defaults(doNorm=False, defaultCol=False)
  return parser.parse_args()

def read_fit_results(infile):
  results = {}
  
  f = TFile(infile)
  tree = f.Get("tree_fit_sb")
  tree.GetEntry(0)
  fit_status = tree.fit_status
  
  if fit_status != 0:
    raise AssertionError("Input fit %d did not converge! Fit status %d." % (bin, fit_status))
  
  mu = tree.mu
  muErr = tree.muErr
  muLoErr = tree.muLoErr
  muHiErr = tree.muHiErr
  
  bkg_yield = tree.n_exp_binhh_bbbb_proc_bkg_hem_mix
  bkg_norm = math.exp(tree.CMS_hh_bbbb_bkg_hem_mix_norm)
  
  prefit_bkg = f.Get("shapes_prefit").Get("hh_bbbb").Get("total_background").Integral()
  
  results["sig"] = (mu, mu - muLoErr, mu + muHiErr)
  #results["bkg"] = bkg_norm
  results["bkg"] = bkg_yield / prefit_bkg
  print results
  return results
  
if __name__ == "__main__":
  ROOT.gROOT.SetBatch(True)
  TH1F.AddDirectory(0)
  parser = argparse.ArgumentParser()
  args = parse_args(parser)
  
  bdt = args.bdt
  
  #bm = int(args.bdt.split("-")[2][2:])
  bm = int(args.bm)
  fit_file = "/lustre/cmswork/atiko/Hbb/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/unblind_08_03_SM_bdt_0_2/BM%d/mlfit.root" % bm
  fit_file = "/lustre/cmswork/atiko/Hbb/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/unblind_11_06_bdt_0_2_bugfix/BM%d/mlfit.root" % bm
  
  fit_results = read_fit_results(fit_file)

  #postfit_file = "/lustre/cmswork/atiko/Hbb/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/unblind_25_01_bdt_0_2/fit/output_postfit.root"
  #args.bdt = bdt.replace("bm0", "bm"+str(bm))
  draw_postfit(args, fit_results, fit_file, bm)
  


