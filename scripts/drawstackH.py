
import json
import os
from glob import glob
import importlib

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector, TCanvas, gROOT

from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_plots.histOpt import hist_opt
import Analysis.alp_plots.UtilsDraw

TH1F.AddDirectory(0)

# exe parameters
histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 'h_all_ht', 'h_met_pt', 'h_mu0_pt', 'h_mu0_iso03', 'h_mu_n', 'h_mu_pt', 'h_mu_iso03', 'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv', 'h_jet3_csv']
samData    = ['data_singleMu']
samMClist  = ['tt','st']
intLumi_fb = 12.9 # plots normalized to this

iDir       = '$CMSSW_BASE/src/Analysis/alp_analysis/output/'
vDirMC     = 'trg_mc_def2' #good SF
vDirData   = 'trg_data_def'
oDir       = './output/trg_def2'
# ---------------

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--doNorm"   , help="normalize to data", action='store_true')
parser.add_argument("-d", "--doDisplay", help="display canvas"   , action='store_true')
parser.add_argument("-s", "--doSave"   , help="save canvas"      , action='store_true')
parser.add_argument("-o", "--plotDir"  , help="subfolder in which histos are", default="")
parser.set_defaults(doNorm=False, doDisplay=False, doSave=False)
args = parser.parse_args()

gROOT.SetBatch(True)
if args.doDisplay:
    gROOT.SetBatch(False)

plotDir    = args.plotDir #'trg_Iso'   #args.plotDir #'trg_Iso' #trg_IsoAndJet trg_Iso
doNorm     = args.doNorm
doDisplay  = args.doDisplay
doSave     = args.doSave
doStack = True
doRatio = True

print "HISTS FROM FOLDER {}".format(plotDir) 
if not plotDir: exit()

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
for h in histList:

    hdata = UtilsDraw.getWeightedHistos(h, filesData, plotDir, intLumi_fb)
    hs = UtilsDraw.getWeightedHistos(h, filesMc, plotDir, intLumi_fb)
    hOpt = hist_opt[h]
    if hs and hdata:  
        if doStack:
            nData,nDataErr,nMc,nMcErr = UtilsDraw.drawH1Stack(hdata, hs, hOpt, snameData, snameMc, doDisplay, doRatio, doNorm, oDir)
            if nData: 
                print "### MC/Data numEvents: {} +- {} ###".format(nMc/nData, UtilsDraw.getRelErr(nMc,nMcErr,nData,nDataErr)*nMc/nData) 
                print "### MC numEvents: {} +- {} ###".format(nMc,nMcErr) 
                print "### Data numEvents: {} +- {} ### \n".format(nData,nDataErr) 
        else:
            UtilsDraw.drawH1(hs, hsOpt)

        if doDisplay:
            raw_input() #debug - to be improved

