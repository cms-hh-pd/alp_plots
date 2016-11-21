
# to compare from same sample with different options

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
intLumi_fb = 12.9 # plots normalized to this
# ---------------
#SM
optList = ["pt30btag0_Trg","pt30btag1_Trg","pt30btag2_Trg","pt30btag3_Trg","pt30btag4_Trg"]
legList = [">=0 CSVmed", ">=1 CSVmed", ">=2 CSVmed", ">=3 CSVmed", ">=4 CSVmed"]
colorList = [1, 416, 880+2, 430, 632-4, 632+8]
#optList = ["pt30btag0_noTrg","pt30btag1_noTrg","pt30btag2_noTrg","pt30btag3_noTrg","pt30btag4_noTrg"]
#legList = [">=0 CSVmed, noTrg", ">=1 CSVmed, noTrg", ">=2 CSVmed, noTrg", ">=3 CSVmed, noTrg", ">=4 CSVmed, noTrg"]
#colorList = [1, 416, 880+2, 430, 632-4, 632+8]
#optList = ["pt30btag0_Trg","pt30btag0_Trg_Truth","pt30btag3_Trg","pt30btag3_Trg_Truth","pt30btag4_Trg","pt30btag4_Trg_Truth"]
#legList = [">=0 CSVmed", ">=0 CSVmed, matched", ">=3 CSVmed", ">=3 CSVmed, matched", ">=4 CSVmed", ">=4 CSVmed, matched"]
#colorList = [1, 880+2, 416, 430, 632-4, 800-3]

#tt
#optList = ["pt30btag1_Trg","pt30btag2_Trg","pt30btag3_Trg","pt30btag4_Trg"]
#legList = [">=1 CSVmed", ">=2 CSVmed", ">=3 CSVmed", ">=4 CSVmed"]
#colorList = [1, 880+2, 416, 430]
#qcd
#optList = ["pt30btag2_noTrg", "pt30btag3_noTrg", "pt30btag4_noTrg"]
#legList = [">=2 CSVmed, noTrg", ">=3 CSVmed, noTrg", ">=4 CSVmed, noTrg"]
#colorList = [1, 880+2, 416, 430]

#---------------

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--doNorm"   , help="normalize to data", action='store_true')
parser.add_argument("-p", "--plotDir"  , help="subfolder in which histos are", default="pair")
parser.add_argument("-s", "--samList"  , help="sample list"                  , default="")
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"             , default="")
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()


if not args.samList: samMClist = ['SM']
else: samMClist = [args.samList]
iDir       = '../alp_analysis/output/' #'../alp_analysis/output/' #'/lustre/cmswork/hh/alp_baseSelector/'
if not args.oDir: oDir = "./output/test"
else: oDir = args.oDir
if not args.customCol: colors = []
else: colors = colorList

gROOT.SetBatch(True)

if not args.plotDir:     
    exit()
plotDir    = args.plotDir
print "HISTS FROM FOLDER {}".format(plotDir) 

doNorm     = args.doNorm
doRatio = False

if doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += samMClist[0]+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

snames = []
snameMc = []
for s in samMClist:
    snames.extend(samlists[s])
filesMc = []
for sname in snames:
    for opt in optList:
        filesMc.append(iDir+opt+"/"+sname+".root")
        snameMc.append(sname)
print snames

#----------------------------------
for h in histList:
    hs = UtilsDraw.getWeightedHistos(h, filesMc, plotDir, intLumi_fb)
    hOpt = hist_opt[h]
    if hs:
        nev1, nev2 = UtilsDraw.drawH1comp(hs, hOpt, snameMc, legList, doRatio, doNorm, oDir, colors)
        if nev1:
            print "### nev1/nev2 : {} / {} = {} ###".format(nev1, nev2, nev1/nev2)

