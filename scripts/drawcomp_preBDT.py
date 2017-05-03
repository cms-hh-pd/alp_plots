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
parser.add_argument("-l", "--list", help="hist list" , dest="hlist", type=int, default=1)
parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==fit)" , type=int, default=0)
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/alp_moriond_base/'
oDir = args.oDir +"/"

# exe parameters
if args.hlist == 0:
    histList   = ['h_nevts' ]
#histList   = ['h_njets' ]
elif args.hlist == 1:
    histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a','h_H0_dr','h_H0_deta_a','h_H0_dphi','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a', 'h_H0H1_dphi',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
              'h_X_mass', 'h_jets_ht_r',
             ]
histList2  = ['h_H0_H1_mass'] #2D histos
intLumi_fb = 35.9 # plots normalized to this
weights = [[],[]]
sf = [[],[]]
headerOpt = ""

# ---------------
if args.whichPlots == -2:
    samlist1 = ['data_moriond'] 
    samlist2 = ['SM'] #'SM'
    optList = ["cmva3","def_cmva"]
    legList = [["bkg (mixed data)"], ["ggHH4b SM (1000x)"]]
    colorList = [430, 632]
    weights = [[],[0.03784]]
    doNormToLumi = [False, True] 
    dofill = [True,True]
    isMC = True
    oname = "bkgSig_preBDT"
    headerOpt = "       "

elif args.whichPlots == -1:
    samlist1 = ['SM'] 
    samlist2 = [] #'SM'
    optList = ["def_cmva","def_cmva"]
    legList = [["signal (HH4b SM)"], ["signal (HH4b SM)"]]
    colorList = [632, 430]
    doNormToLumi = [False, False] 
    dofill = [True,True]
    isMC = True
    oname = "sig_preBDT"
    headerOpt = "       sel:trg"

# sig vs bkg
elif args.whichPlots == 0:
    samlist1 = ['SM']
    samlist2 = ['Data']
    optList = ["def_cmva","def_cmva_mixed"] #mass
    legList = ["signal (HH4b SM)", "bkg (mixed data)"]
    colorList = [632, 430]
    doNormToLumi = [True, False] 
    dofill = [True,True]
    isMC = False
    oname = "comp_sigBkg_preBDT"

# bkg vs data - 2% of lumi
elif args.whichPlots == 1:
    samlist1 = ['Data']
    samlist2 = ['Data']
    optList = ["def_cmva_mixed","def_cmva"]
    legList = ["bkg (mixed data)", "data"]
    colorList = [430, 1]
    doNormToLumi = [False, False]
    dofill = [True,True]
    isMC = False
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
    isMC = True
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
    isMC = True
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
    isMC = False
    oname = "comp_bkg_csvcmva_preBDT"

#QCD - def vs mixed
#elif args.whichPlots == 5:
#    optList = ['def_cmva','def_cmva_plots'] #'def_cmva_mixed'
#    samlist1 = ['qcd_m'] #'qcd_m','tt'
#    samlist2 = ['Data']
#    legList = ['QCD HT>200', 'mixed data']
#    colorList = [402, 430]    
#    weights = [[17.635231,3.476259,0.509821,0.089584,0.046491,0.005935,0.002410],[]] #,0
#    doNormToLumi = [True, False]  
#    dofill = [True,True]
#    isMC = False
#    oname = "comp_qcdBkg_preBDT"

elif args.whichPlots == 6:
    optList = ['def_cmva_mixed','def_cmva_mixed']
    samlist1 = ['qcd_m500']
    samlist2 = ['qcd_m500']
    legList = [['QCD HT>500'], ['QCD HT>200 - mixed']] #200
    colorList = [402, 430]    
    weights = [[0.509821,0.089584,0.046491,0.005935,0.002410],[0.509821,0.089584,0.046491,0.005935,0.002410]]  #17.635231,3.476259,
    doNormToLumi = [True, True]  
    dofill = [True,False]
    isMC = True
    oname = "comp_qcdMixqcd_preBDT"

elif args.whichPlots == 7:
    optList = ['def_cmva','def_cmva_mixed']
    samlist1 = ['tt']
    samlist2 = ['tt']
    legList = [['TT'], ['TT mixed']]
    colorList = [602, 430]
    weights = [[0.010760],[0.010760]]
    doNormToLumi = [False, False]
    dofill = [True,True]
    isMC = True
    oname = "comp_ttMixtt_preBDT"   

elif args.whichPlots == 8: #okay - 20170502
    optList = ['def_cmva','def_cmva_mixed']
    samlist1 = ['tt','qcd_m']  #m b
    samlist2 = ['Data']
    legList = [['tt','QCD HT>200'], ['mixed data']]  #QCD bEnr.   HT>200
    colorList = [402, 430]
    weights = [[0.010760,29.599755,6.338876,0.511526,0.149046,0.078782,0.009964,0.004075],[]]
    sf = [[1,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282],[]]
#   22.325121,4.826995,0.843187,0.110750,0.059825,0.007443,0.003055],[]]
#    weights = [[0.010760,17.635231,3.476259,0.509821,0.089584,0.046491,0.005935,0.002410],[]]
    doNormToLumi = [True, False]
    dofill = [True,True]
    isMC = False
    #oname = "comp_qcdbttBkg_preBDT"
    oname = "comp_qcdttBkg_preBDT"

elif args.whichPlots == 81:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['tt','qcd_m']
    samlist2 = ['SM']
    legList = [['tt','QCD HT>200'], ['ggHH4b SM (1000x)']]
    colorList = [402, 632]
    weights = [[0.010760,29.599755,6.338876,0.511526,0.149046,0.078782,0.009964,0.004075],[0.03784]]
    sf = [[1,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282],[]]
    doNormToLumi = [True, True]
    dofill = [True,False]
    isMC = True
    oname = "comp_qcdttSig_preBDT"

elif args.whichPlots == 9:
    optList = ['def_cmva_mixed','antitag3_cmva']
    samlist1 = ['Data']
    samlist2 = ['Data']
    legList = [['4cmva mixed data'], ['antitag3 data']]
    colorList = [430, 1]
    weights = [[],[]]
    doNormToLumi = [False, False]
    dofill = [True,False]
    isMC = False
    oname = "comp_antagVsTag_preBDT"

elif args.whichPlots == 10:
    optList = ['test','antitag3_cmva']
    samlist1 = ['Data']
    samlist2 = ['Data']
    legList = [['mixed data'], 'data']
    colorList = [430, 1]
    weights = [[],[]]
    doNormToLumi = [False, False]
    dofill = [True,False]
    isMC = False
    oname = "comp_antag_mixData_preBDT"
    headerOpt = "4th Jet antitag"

elif args.whichPlots == 11:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['qcd_m']
    samlist2 = ['qcd_b']
    legList = [['QCD'], ['QCD bEnr.']]
    colorList = [402, 430]
    weights = [[29.599755,6.338876,0.511526,0.149046,0.078782,0.009964,0.004075],
               [0.023755, 0.085170, 0.032952, 18.475847, 6.122864, 0.623063, 0.364026, 0.030071, 0.013571, 0.004531, 2.798854, 0.929341, 0.079645, 0.050250]]
    sf = [[1.0282,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282],
          [1.4819,1.4819,1.4819,1.4819,1.4819,1.4819,1.4819, 1.4819,1.4819,1.4819,1.4819,1.4819,1.4819,1.4819]]
    doNormToLumi = [True, True]
    dofill = [True,False]
    isMC = True
    oname = "comp_qcdqcdb_preBDT"

else: 
    print "ERROR: wrong '-w' argument"
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
    hs1 = UtilsDraw.getHistos(h, files1, plotDir, intLumi_fb, doNormToLumi[0], weights[0], sf[0])
    hs2 = UtilsDraw.getHistos(h, files2, plotDir, intLumi_fb, doNormToLumi[1], weights[1], sf[1])
    hOpt = hist_opt[h]

    if hs1 and hs2:
        UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], 
                         hOpt, args.plotResidual, doNorm, oDir, colors, dofill, 0, headerOpt, isMC)
    elif hs1: UtilsDraw.drawH1only(hs1, snames1, legList[0], hOpt, oDir, colors, dofill, 0, headerOpt, isMC)

