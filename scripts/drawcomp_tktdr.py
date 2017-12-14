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
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='0')
parser.add_argument("-n", "--doNorm"   , help="normalize to data"       , action='store_true')
parser.add_argument("-p", "--plotDir"  , help="root file subfolder in which histos are", default="acc")
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"        , default="output/")
parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==pulls)" , type=int, default=0)
parser.add_argument("-l", "--list", help="hist list" , dest="hlist", type=int, default=1)
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/tkTDR/HHTo4B_SM_'
oDir = args.oDir +"/"
intLumi_fb = 1.
weights = [[],[]]
headerOpt = ""
isAcc = False

if args.hlist == 0:
    histList   = ['h_gjets_n',
                  'h_gjets_pt', 'h_gjet0_pt', 'h_gjet1_pt', 'h_gjet2_pt', 'h_gjet3_pt',
                  'h_gjets_eta', 'h_gjet0_eta', 'h_gjet1_eta', 'h_gjet2_eta', 'h_gjet3_eta',
                 ]
elif args.hlist == 1:
    histList = ['h_nevts', 'h_jets_n','h_jets_pt', 'h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
                'h_jets_csv', 'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
                'h_jets_cmva',   'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
                'h_jets_eta', 'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta'
               ]
histList2  = ['h_H0_H1_mass'] #2D histos

# ---------------
if args.whichPlots == -2:
    samlist1 = ['SM']
    optList1 = ["Run2_30.0_2.4_cmva","g_PU0_30.0_2.4_cmva"]
    legList = [["ggHH4b SM, Run2","ggHH4b SM, PU0"]]
    colorList = [797,632]
    doNormToLumi = [[False, False],[]]
    weights = [[3.33568E-06,3.42578E-06],[]]
    dofill = [True,True]
    isMC = True
    oname = "comp_sig_tkTDRRun2PU0_gen"

elif args.whichPlots == -1:
    samlist1 = ['SM']
    optList1 = ["g_PU0_20.0_4.0_cmva","g_PU140_20.0_4.0_cmva","g_PU200_20.0_4.0_cmva"]
    legList = [["ggHH4b SM, PU0", "ggHH4b SM, PU140", "ggHH4b SM, PU200"]]
    colorList = [632, 430, 418]
    doNormToLumi = [[False, False, False],[]]
    dofill = [True,True, True]
    isMC = True
    oname = "comp_sig_tkTDR_gen"

elif args.whichPlots == 0:
    samlist1 = ['SM']
    optList1 = ["g_PU0_20.0_4.0_cmva","g_PU140_20.0_4.0_cmva","g_PU200_20.0_4.0_cmva"]
    legList = [["ggHH4b SM, PU0", "ggHH4b SM, PU140", "ggHH4b SM, PU200"]]
    colorList = [632, 430, 418]
    doNormToLumi = [[False, False, False],[]] 
    weights = [[0.000003977139402713204, 0.0000038012840737601161, 0.0000040088515442096],[]]
    dofill = [True,True, True]
    isMC = True
    oname = "comp_sig_tkTDR"

elif args.whichPlots == 1:
    samlist1 = ['SM']
    optList1 = ["Run2_30.0_2.4_cmva","g_PU0_30.0_2.4_cmva","g_PU140_30.0_2.4_cmva","g_PU200_30.0_2.4_cmva"]
    legList = [["ggHH4b SM, Run2","ggHH4b SM, PU0", "ggHH4b SM, PU140", "ggHH4b SM, PU200"]]
    colorList = [797, 632, 430, 418]
    doNormToLumi = [[False, False, False, False],[]] 
    weights = [[7.22966E-06, 5.24604E-06, 4.80783E-06, 5.13468E-06],[]] 
    dofill = [True,True, True, True]
    isMC = True
    oname = "comp_sig_tkTDRRun2"


elif args.whichPlots == 2:
    samlist1 = ['SM']
    optList1 = ["Run2_30.0_2.4_cmva","g_PU0_30.0_2.4_cmva"]
    legList = [["ggHH4b SM, Run2","ggHH4b SM, PU0"]]
    colorList = [797,632]
    doNormToLumi = [[False, False],[]]
    weights = [[7.22966E-06, 5.24604E-06],[]]
    dofill = [True,True]
    isMC = True
    oname = "comp_sig_tkTDRRun2PU0"

elif args.whichPlots == 3:
    samlist1 = ['SM']
    optList1 = ["g_PU0_20.0_4.0_cmva"]
    legList = [["generator |#eta| < 2.5","generator |#eta| < 3.0","generator |#eta| < 4.0"]]
    colorList = [2,4,1]
    doNormToLumi = [[False, False,False],[]]
    histList   = ["h_gjetspt", "h_gjetspt_eta0", "h_gjetspt_eta1", "h_gjetspt_eta2"]
    weights = [[1.,1.,1.,1.],[]]
    dofill = [False,False,False]
    isMC = True
    isAcc = True
    oname = "comp_sig_tkTDR_acc"

else: 
    print "ERROR: wrong '-w' argument"
    exit()

#--------------

oDir += oname

snames1 = ["HHTo4BSM","HHTo4BSM","HHTo4BSM","HHTo4BSM"]

if not args.customCol: colors = [0,0]
else: colors = colorList

if not args.plotDir:     
    exit()
plotDir    = args.plotDir
print "HISTS FROM FOLDER {}".format(plotDir) 

doNorm     = args.doNorm

if doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += "/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += plotDir
if not os.path.exists(oDir): os.mkdir(oDir)

files1 = []
for opt in optList1:
    files1.append(iDir+opt+".root")

#----------------------------------
if isAcc:
    hs1 = []
    for h in histList:
        hs1.append(UtilsDraw.getHistos_tdr(h, files1, plotDir, intLumi_fb, doNormToLumi[0], weights[0]))
    UtilsDraw.drawH1tdrAcc(hs1, snames1, legList[0],
                   oDir, colors, headerOpt, isMC)
else:
    for h in histList:        
        hs1 = UtilsDraw.getHistos_tdr(h, files1, plotDir, intLumi_fb, doNormToLumi[0], weights[0])
        hOpt = hist_opt[h]
        if hs1:         
            UtilsDraw.drawH1tdr(hs1, snames1, legList[0],  
                   hOpt, args.plotResidual, doNorm, oDir, colors, dofill, 0, headerOpt, isMC)

