
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
# for trigger study:
#histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
#              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
#              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv', 'h_jet3_csv',
#              'h_all_ht', 'h_met_pt', 'h_mu0_pt', 'h_mu0_iso03', 'h_mu_n', 'h_mu_pt', 'h_mu_iso03']

histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a','h_H0_dr','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a']
histList2  = ['h_H0_H1_mass'] #2D histos

samData    = ['data_unblind'] #'data_ichep'  'data_singleMu'
vDir_data  = 'pt30btag4_Trg_noBW'  #DEBUG
samSigList  = ['SM'] #,'BM2','BM13'
samBkgList  = ['qcd','tt'] #'st' 'qcd_b',
optOutFolder = 'data_qcd_tt_SM/'
intLumi_fb = 12.9 # plots normalized to this
kfactorSig = 1 #100000
iDir       = '$CMSSW_BASE/src/Analysis/alp_analysis/output/' #/lustre/cmswork/hh/alp_baseSelector/

#optList = ["pt30btag0_noTrg","pt30btag1_noTrg","pt30btag2_noTrg","pt30btag3_noTrg","pt30btag4_noTrg"]
#legList = [">=0 CSVmed, noTrg", ">=1 CSVmed, noTrg", ">=2 CSVmed, noTrg", ">=3 CSVmed, noTrg", ">=4 CSVmed, noTrg"]
colorList = [1, 416, 880+2, 430, 632-4, 632+8]

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--doNorm"   , help="normalize to data", action='store_true')
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-p", "--plotDir"  , help="subfolder in which histos are", default="pair")

parser.add_argument("-o", "--oDir"     , help="output directory"             , default="")
parser.add_argument("-v", "--vDir"     , help="ntuple version directory"     , default="")
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

if not args.customCol: colors = []
else: colors = colorList
if not args.oDir: oDir = "./output/test"
else: oDir = args.oDir
if not args.vDir: vDir = "MC_def"
else: vDir = args.vDir
# ---------------

gROOT.SetBatch(True)

plotDir    = args.plotDir
doNorm     = args.doNorm
doRatio = True

print "HISTS FROM FOLDER {}".format(plotDir) 
if not plotDir: exit()

if doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
if optOutFolder: 
    oDir += optOutFolder
    if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

snames = []
for s in samData:
    snames.extend(samlists[s])
snameData = snames
print snames
filesData = []
for sname in snames:
    filesData.append(iDir+vDir_data+"/"+sname+".root")

snames = []
for s in samBkgList:
    snames.extend(samlists[s])
snameBkg = snames
filesBkg = []
for sname in snames:
    filesBkg.append(iDir+vDir+"/"+sname+".root")
print snames

snames = []
for s in samSigList:
    snames.extend(samlists[s])
snameSig = snames
filesSig = []
for sname in snames:
    filesSig.append(iDir+vDir+"/"+sname+".root")
print snames

#----------------------------------
hdata = []
hsig  = []
hbkg  = []
for h in histList:
    
    if(snameData): hdata = UtilsDraw.getWeightedHistos(h, filesData, plotDir, intLumi_fb)
    if(snameSig) : hsig  = UtilsDraw.getWeightedHistos(h, filesSig , plotDir, intLumi_fb)
    if(snameBkg) : hbkg  = UtilsDraw.getWeightedHistos(h, filesBkg , plotDir, intLumi_fb)
    hOpt = hist_opt[h]
    if hsig: 
        if not hdata: 
            UtilsDraw.drawH1Stack_sig(hsig, hbkg, hOpt, snameSig, snameBkg, doRatio, doNorm, oDir, kfactorSig)
        else: 
            UtilsDraw.drawH1Stack(hdata, hsig, hbkg, hOpt, snameData, snameSig, snameBkg, doRatio, doNorm, oDir, kfactorSig)
    else:
        if hdata: 
            nData,nDataErr,nMc,nMcErr = UtilsDraw.drawH1Stack_data(hdata, hbkg, hOpt, snameData, snameBkg, doRatio, doNorm, oDir)
            if nData: 
                print "### MC/Data numEvents: {} +- {} ###".format(nMc/nData, UtilsDraw.getRelErr(nMc,nMcErr,nData,nDataErr)*nMc/nData) 
                print "### MC numEvents: {} +- {} ###".format(nMc,nMcErr) 
                print "### Data numEvents: {} +- {} ### \n".format(nData,nDataErr) 

