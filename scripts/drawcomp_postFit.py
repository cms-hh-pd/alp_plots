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




def draw_postfit(args, fit_results, postfit_file):
  which = args.whichPlots
  iDir       = '../hh2bbbb_limit/'
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

  samples = [['bkg', 'sig'],['data']] #data always  second
  #samples = [['sig', 'bkg'],['data']] #data always  second
  fractions = ['','']
  regions = ['appl','']
  legList = [["mixed data", "HH4b SM"], ["data"]]
  #legList = [["HH4b SM", "mixed data"], ["data"]]
  colorList = [[430, 632], [1]]
  #colorList = [[632, 430], [1]]
  sf = [[bkg_scale_factor, sig_scale_factor],[1.]]
  #sf = [[sig_scale_factor, bkg_scale_factor],[1.]]
  dofill = [True,False]
  isMC = False
  oname = 'comp_bkgdata_postfit'
  headerOpt = "" #appl sample" #btag CR

  if args.defaultCol: colors = [0,0]
  else: colors = colorList


  snames1 = []
  for s in samples[0]:
      if not s in samlists: 
          if not s in samples: 
              snames1.append(s)
          else:
              snames1.append(samples[s]['sam_name'])    
      else: 
          snames1.extend(samlists[s])
  #print snames1

  snames2 = []
  for s in samples[1]:
      if not s in samlists: 
          if not s in samples: 
              snames2.append(s)
          else:
              snames2.append(samples[s]['sam_name'])    
      else: 
          snames2.extend(samlists[s])
  #print snames2

  plotDirs1 = []
  for sam in snames1:
      option = ''
      if fractions[0]: 
          option += fractions[0]
          if regions[0]: option += "_"
      if regions[0]: option += regions[0]

      if option: plotDirs1.append(sam+'_'+option)
      else: plotDirs1.append(sam)
  print "HISTS FROM FOLDER {}".format(plotDirs1) 

  plotDirs2 = []
  for sam in snames2:
      option = ''
      if fractions[1]: 
          option += fractions[1]
          if regions[1]: option += "_"
      if regions[1]: option += regions[1]

      if option: plotDirs2.append(sam+'_'+option)
      else: plotDirs2.append(sam)
  print "HISTS FROM FOLDER {}".format(plotDirs2) 

  oDir = args.oDir
  oDir += "/"+args.bdt
  if not os.path.exists(oDir): os.mkdir(oDir)
  oDir += "/"+oname
  if args.doNorm: oDir = oDir+"_norm"
  if args.clrebin > 1: 
      oDir += "_rebin_" + str(args.clrebin)
  oDir = oDir+"/"
  if not os.path.exists(oDir): os.mkdir(oDir)
  oDir += option #keep the second sample options
  if not os.path.exists(oDir): os.mkdir(oDir)

  #----------------------------------
  for n, h in enumerate(histList):
      hOpt = hist_opt[h]
      pf_file = None
      if h == 'classifier': 
          h+='-'+args.bdt
          pf_file = postfit_file
      hs1 = UtilsDraw.getHistos_bdt(h, filename, plotDirs1, intLumi_fb, doNormToLumi[0], weights[0], sf[0])
      hs2 = UtilsDraw.getHistos_bdt(h, filename, plotDirs2, intLumi_fb, doNormToLumi[1], weights[1], sf[1])

      if drawH2:
          UtilsDraw.drawH2(hs1, hs2, hist_opt["h2_bdt"], snames1, args.clrebin, oDir, legList)
      elif getVar: # variance check
          UtilsDraw.drawBinVar(hs1, snames1, legList[0], hOpt, oDir, args.clrebin, headerOpt, isMC)
      elif getChi: # chi square
          UtilsDraw.drawChiSquare(hs1, snames1, legList[0], hs2, hOpt, oDir, xbmin, headerOpt, isMC, labels)
      else: 
          if hs1 and hs2:
              print "PF", pf_file
              print h
              n1,n1err,n2,n2err = UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], 
                           hOpt, args.plotResidual, args.doNorm, oDir, colors, dofill, args.clrebin, headerOpt, isMC, fit_results, pf_file)

def parse_args(parser):
  parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='0')
  parser.add_argument("-b", "--bdt", help="bdt version, equal to input file name (classifier report output)", required=True)
  parser.add_argument("-o", "--oDir", help="output directory", default="plots")
  parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==pulls)", type=int, default=-2)
  parser.add_argument("-r", "--clrebin", help="to rebin (classifier output)", type=int, default=-1)
  parser.add_argument("-n", "--doNorm", help="do normalize ", action='store_true')
  parser.add_argument("-c", "--defaultCol", help="to use default colors", action='store_true')
  parser.add_argument("-l", "--list", help="hist list", dest="hlist", type=int, default=0)
  parser.add_argument("--lumi", help="int lumi to normalize to", dest="lumi", type=float, default=35.9)
  #parser.add_argument("-p", "--postfit", help="postfit histograms file", required=True)
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
  
  fit_file = "/lustre/cmswork/atiko/Hbb/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/unblind_25_01_bdt_0_2/fit/mlfit.root"
  fit_results = read_fit_results(fit_file)

  #postfit_file = "/lustre/cmswork/atiko/Hbb/CMSSW_7_4_7/src/HiggsAnalysis/CombinedLimit/unblind_25_01_bdt_0_2/fit/output_postfit.root"

  draw_postfit(args, fit_results, fit_file)
  


