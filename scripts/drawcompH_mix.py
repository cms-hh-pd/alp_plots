
# to compare from same sample with different options

import json
import os
from glob import glob
import importlib

# ROOT imports
from ROOT import TChain, TH1F, TFile, vector, TCanvas, gROOT

from Analysis.alp_analysis.samplelists import samlists
from Analysis.alp_analysis.alpSamples import samples
from Analysis.alp_plots.histOpt import hist_opt
import Analysis.alp_plots.UtilsDraw as UtilsDraw

TH1F.AddDirectory(0)

# exe parameters
histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a','h_H0_dr','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a',
              #'h_X_mass', 'h_jets_ht_r', 'h_bdt_allVar', 'h_bdt_massVar', 'h_bdt_HHVar',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
             ]
histList2  = ['h_H0_H1_mass'] #2D histos
intLumi_fb = 1. # plots normalized to this
# ---------------
#SM
bdtver = ''
samlist1 = ['SM']
samlist2 = ['SM']
optList = ["def","cmva4M"]
legList = ["HH4b SM, 4 CSV", "HH4b SM, 4 CMVA"]
colorList = [632+4, 632-4] 
useWeight = [1, 1] 
dofill = [1,1]

#SM
#samlist1 = ['SM']
#samlist2 = ['SM']
#optList = ["def_noW","def_mixed"]
#optList = ["csv4L_noTrg_noW","csv4L_noTrg_mixed"]
#legList = ["HH4b SM", "HH4b SM mixed"]
#colorList = [1, 632-4]

#optList = ["def_noTrg_mixed","def_noTrg_noW"]
#samlist1 = ["QCD_HT500toInf"]
#samlist2 = ["qcd_500toInf_m"]
#legList = ["QCD HT>500 mixed", "QCD HT>500"]
#colorList = [430, 1] 
#useWeight = [0, 1] 
#samlist1 = ['QCD_HT200to500']
#samlist2 = ['qcd_200to500_m']
#legList = ["QCD 200<HT<500 mixed", "QCD 200<HT<500"]
#colorList = [416, 1]
#useWeight = [0, 1]  
#dofill = [1,0]

#optList = ["csv4L_noTrg_noW","csv4L_noTrg_mixed"]
#samlist1 = ['qcd']
#samlist2 = ['QCD_HT200toInf']
#legList = ["QCD HT>200 - 4CSVLoose", "QCD HT>200 mixed - 4CSVLoose"]
#colorList = [1, 420] 
#useWeight = [0, 1]

#optList = ["def_noTrg_mixed", "def_noTrg"]
#samlist1 = ['QCD500_tt_SM300']
#samlist2 = ['SM']
#legList = ["QCD HT>500 + tt + 300SM", "SM"]
#colorList = [1, 420] 
#useWeight = [0, 1] 
#dofill = [1,0]

#optList = ["def_mixed_frac20", "def_frac20"]
#samlist1 = ['data_ichep']
#samlist2 = ['data_ichep']
#legList = ["data (1/20) mixed", "data (1/20)"]
#colorList = [395, 1] 
#useWeight = [0, 0] 
#dofill = [1,0]

#bdtver = 'Data_BDT_08_12'
#optList = ["bdt_", "bdt_"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_sig']
#legList = ["bkg (mixed data)", "signal (SM)"] #
#colorList = [430, 632-4] 
#useWeight = [0, 0] 
#dofill = [1,1]

#bdtver = 'Data_BDT_08_12'
#optList = ["bdt_HHp2p1", "bdt_HHp2p1"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_sig']
#legList = ["bkg (mixed data) BDTHHvar>0.2", "signal (SM) BDTHHvar>0.2"] #
#colorList = [430, 632-4] 
#useWeight = [0, 0] 
#dofill = [1,1]

#bdtver = 'Data_BDT_08_12'
#optList = ["bdt_", "bdt_HHp2p1"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_bkg']
#legList = ["bkg (mixed data)", "bkg (mixed data) BDTHHvar>0.2"] #
#colorList = [430, 416] 
#useWeight = [0, 0] 
#dofill = [1,1]

#bdtver = 'Data_BDT_07_12'
#optList = ["bdt_HHp0p2", "bdt_HHp0p2"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_data']
#legList = ["bkg (mixed data) BDTHHvar<0.2", "data BDTHHvar<0.2"] #
#colorList = [436, 1] 
#useWeight = [0, 0] 
#dofill = [1,1]

#bdtver = 'QCD_BDT_07_12'
#optList = ["bdt_HHp0p2", "bdt_HHp0p2"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_data']
#legList = ["mixed QCD BDTHHvar<0.2", "plain QCD BDTHHvar<0.5"] #
#colorList = [416, 1] 
#useWeight = [0, 0] 
#dofill = [1,0]

#bdtver = 'QCD_BDT_03_12'
#optList = ["bdt_HHp5p1", "bdt_HHp5p1"]
#samlist1 = [bdtver+'_bkg']
#samlist2 = [bdtver+'_data']
#legList = ["mixed QCD BDTHHvar>0.5", "plain QCD BDTHHvar>0.5"] #
#colorList = [416, 1] 
#useWeight = [0, 0] 
#dofill = [1,0]


#---------------

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-n", "--doNorm"   , help="normalize to data", action='store_true')
parser.add_argument("-p", "--plotDir"  , help="subfolder in which histos are", default="pair")
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"             , default="")
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

#iDir       = '../alp_analysis/output/'
iDir       = '/lustre/cmswork/hh/alp_baseSelector/' 
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
oDir += bdtver+"/"  #debug samlist1[0]
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

snames1 = []
for s in samlist1:  #debug!!!
    if not s in samlists: 
        if not s in samples: 
            snames1.append(s)    #debug
        else:
            snames1.append(samples[s]['sam_name'])    
    else: 
        snames1.extend(samlists[s])
print snames1
snames2 = []
for s in samlist2:
    if not s in samlists: 
        if not s in samples: 
            snames2.append(s)    #debug
        else:
            snames2.append(samples[s]['sam_name'])
    else: 
        snames2.extend(samlists[s])
print snames2
files1 = []
for sname in snames1:
    files1.append(iDir+optList[0]+"/"+sname+".root")
files2 = []
for sname in snames2:
    files2.append(iDir+optList[1]+"/"+sname+".root")
#print files2

#----------------------------------
for h in histList:    
    hs1 = UtilsDraw.getWeightedHistos(h, files1, plotDir, intLumi_fb, useWeight[0])
    hs2 = UtilsDraw.getWeightedHistos(h, files2, plotDir, intLumi_fb, useWeight[1])
    hOpt = hist_opt[h]

    if hs1 and hs2:
        UtilsDraw.drawH1(hs1, legList[0], hs2, legList[1], hOpt, snames1, snames2, doRatio, doNorm, oDir, colors, dofill)

