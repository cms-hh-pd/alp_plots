# to compare histograms - max samples with different options
# python scripts/drawcomp_preBDT.py -w 0 -n -c -o plots_moriond/

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
gROOT.SetBatch(True)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='-1')
parser.add_argument("-n", "--doNorm"   , help="normalize to data"       , action='store_true')
parser.add_argument("-p", "--plotDir"  , help="root file subfolder in which histos are", default="pair")
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"        , default="output/")
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/alp_moriond_base/'
oDir = args.oDir

# exe parameters
histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a','h_H0_dr','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
              'h_X_mass', 'h_jets_ht_r',
             ]
histList2  = ['h_H0_H1_mass'] #2D histos
intLumi_fb = 1. # plots normalized to this

# ---------------
# sig vs bkg
if args.whichPlots == 0:
    samlist1 = ['SM']
    samlist2 = ['data']
    optList = ["def_cmva","def_cmva_mixed"]
    legList = ["signal (HH4b SM)", "bkg (mixed data)"]
    colorList = [632, 430]
    doNormToLumi = [True, False] 
    dofill = [True,True]
    oname = "comp_sigBkg_preBDT"

# bkg vs data - 2% of lumi
elif args.whichPlots == 1:
    samlist1 = ['test']
    samlist2 = ['data']
    optList = ["def_cmva_mixed","def_cmva"]
    legList = ["bkg (mixed data)", "data"]
    colorList = [430, 1]
    doNormToLumi = [False, False]
    dofill = [True,True]
    oname = "comp_dataBkg_preBDT"

# bkg vs data - 2% of lumi
#elif args.whichPlots == 1:
#    samlist1 = ['data_moriond']
#    samlist2 = ['data_moriond']
#    optList = ["def_cmva_mixed_f20","def_cmva_f20"]
#    legList = ["bkg (1/20)", "data (1/20)"]
#    colorList = [430, 1]
#    doNormToLumi = [False, False]
#    dofill = [1,1]
#    oname = "comp_dataBkg_f20_preBDT"

# SM - def vs mixed
elif args.whichPlots == 2:
    samlist1 = ['SM']
    samlist2 = ['SM']
    optList = ["def_cmva_mixed","def_cmva"]
    legList = ["HH4b SM mixed", "HH4b SM"]
    colorList = [632-4, 632]
    doNormToLumi = [False, True]
    dofill = [True,True]
    oname = "comp_sig_defMixed_preBDT"

# sig - CSV vs CMVA
elif args.whichPlots == 3:
    samlist1 = ['SM']
    samlist2 = ['SM']
    optList = ["def_csv","def_cmva"]
    legList = ["HH4b SM, 4 med CSV", "HH4b SM, 4 med CMVA"]
    colorList = [632-4, 632] 
    doNormToLumi = [True, True] 
    dofill = [True,True]
    oname = "comp_sig_csvcmva_preBDT"

# bkg - CSV vs CMVA
elif args.whichPlots == 4:
    samlist1 = ['data_moriond']
    samlist2 = ['data_moriond']
    optList = ["def_csv_mixed","def_cmva_mixed"]
    legList = ["bkg, 4 med CSV", "bkg, 4 med CMVA"]
    colorList = [430-4, 430]
    doNormToLumi = [False, False]
    dofill = [True,True]
    oname = "comp_bkg_csvcmva_preBDT"

#QCD - def vs mixed
elif args.whichPlots == 5:
    optList = ["def_noTrg_csv","def_noTrg_mixed"]
    samlist1 = ["QCD_HT500toInf"]
    samlist2 = ["qcd_500toInf_m"]
    legList = ["QCD HT>500", "QCD HT>500 mixed"]
    colorList = [430, 1]    
    #samlist1 = ['QCD_HT200to500']
    #samlist2 = ['qcd_200to500_m']
    #legList = ["QCD 200<HT<500", "QCD 200<HT<500 mixed"]
    #colorList = [416, 1]
    doNormToLumi = [False, True]  
    dofill = [True,False]
    oname = "comp_qcd_defMixed_preBDT"

else: 
    print "ERROR: wrong '-i' argument"
    exit()

#additional possibilities:
#------------------
#optList = ["def_noTrg_mixed", "def_noTrg"]
#samlist1 = ['QCD500_tt_SM300']
#samlist2 = ['SM']
#legList = ["QCD HT>500 + tt + 300SM", "SM"]
#colorList = [1, 420] 
#doNormToLumi = [0, 1] 
#dofill = [1,0]

#SM
#optList = ["pt30btag0_Trg","pt30btag1_Trg","pt30btag2_Trg","pt30btag3_Trg","pt30btag4_Trg"]
#legList = [">=0 CSVmed", ">=1 CSVmed", ">=2 CSVmed", ">=3 CSVmed", ">=4 CSVmed"]
#colorList = [1, 416, 880+2, 430, 632-4, 632+8]
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

#--------------

oDir += oname

if not args.customCol: colors = []
else: colors = colorList

if not args.plotDir:     
    exit()
plotDir    = args.plotDir
print "HISTS FROM FOLDER {}".format(plotDir) 

doNorm     = args.doNorm
doResiduals = False

if doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += "/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

snames1 = []
for s in samlist1:
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
    hs1 = UtilsDraw.getHistos(h, files1, plotDir, intLumi_fb, doNormToLumi[0])
    hs2 = UtilsDraw.getHistos(h, files2, plotDir, intLumi_fb, doNormToLumi[1])
    hOpt = hist_opt[h]

    if hs1 and hs2:
        UtilsDraw.drawH1(hs1, legList[0], hs2, legList[1], hOpt, doResiduals, doNorm, oDir, colors, dofill, 0)

