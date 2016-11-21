
import json
import os
from glob import glob
import importlib

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector, TCanvas, gROOT

from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_plots.histOpt import hist_opt
import Analysis.alp_plots.UtilsDraw as UtilsDraw

TH1F.AddDirectory(0)

# exe parameters
histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a','h_H0_dr','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a']
histList2  = ['h_H0_H1_mass'] #2D histos
samData    = []
samMClist  = ['SM'] #'signals','tt' ,'tt','qcd'
intLumi_fb = 12.9 # plots normalized to this

iDir       = '../alp_analysis/output/' #'../alp_analysis/output/' #'/lustre/cmswork/hh/alp_baseSelector/'
vDirMC     = 'MC_noTrg' #'MC_def'
vDirData   = 'data_def'
oDir       = './output/MC_noTrg' #MC_def
# ---------------

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--doNorm"   , help="normalize to data", action='store_true')
parser.add_argument("-d", "--doDisplay", help="display canvas"   , action='store_true')
parser.add_argument("-s", "--doSave"   , help="save canvas"      , action='store_true')
parser.add_argument("-p", "--plotDir"  , help="subfolder in which histos are", default="")
parser.set_defaults(doNorm=False, doDisplay=False, doSave=False)
args = parser.parse_args()

gROOT.SetBatch(True)
if args.doDisplay:
    gROOT.SetBatch(False)

if not args.plotDir: 
    print "ERROR: missing plotDir (-p)"
    exit()
plotDir    = args.plotDir #'trg_Iso'   #args.plotDir #'trg_Iso' #trg_IsoAndJet trg_Iso
print "HISTS FROM FOLDER {}".format(plotDir) 

doNorm     = args.doNorm
doDisplay  = args.doDisplay
doSave     = args.doSave
doStack = True
doRatio = True

if doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

#debug -- move to functions..
snames = []
for s in samData:
    snames.extend(samlists[s])
snameData = snames
print snames
filesData = []
for sname in snames:
    filesData.append(iDir+vDirData+"/"+sname+".root")

snames = []
for s in samMClist:
    snames.extend(samlists[s])
snameMc = snames
filesMc = []
for sname in snames:
    filesMc.append(iDir+vDirMC+"/"+sname+".root")
print snames

#----------------------------------
# for MC only
for h2 in histList2:
#    hdata = UtilsDraw.getWeightedHistos(h, filesData, plotDir, intLumi_fb)
    hs = UtilsDraw.getWeightedHistos(h2, filesMc, plotDir, intLumi_fb)
    hOpt = hist_opt[h2]
    if hs:  
        UtilsDraw.drawH2(hs, hOpt, snameMc, doDisplay, oDir)

#----------------------------------
for h in histList:

#    hdata = UtilsDraw.getWeightedHistos(h, filesData, plotDir, intLumi_fb)
    hdata = []
    hs = UtilsDraw.getWeightedHistos(h, filesMc, plotDir, intLumi_fb)
    hOpt = hist_opt[h]
    if hs:  # debug - if MC only?
        UtilsDraw.drawH1(hdata, hs, hOpt, snameData, snameMc, doDisplay, doRatio, doNorm, oDir)


