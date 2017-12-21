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
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='3')
parser.add_argument("-n", "--doNorm", help="normalize to data", action='store_true')
parser.add_argument("-p", "--plotDir", help="subfolder of the root file that contains histos", default="pair")
parser.add_argument("-c", "--defaultCol", help="to use default colors", action='store_true')
parser.add_argument("-o", "--oDir", help="output directory", default="output/")
parser.add_argument("-l", "--list", help="hist list", dest="hlist", type=int, default=1)
parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==pulls)" , type=int, default=0)
parser.add_argument("--lumi", help="int lumi to normalize to", dest="lumi", type=float, default=35.9)
parser.set_defaults(doNorm=False, defaultCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/alp_moriond_base/'
oDir = args.oDir +"/"
intLumi_fb = args.lumi
trg_eff = 0.96
doNorm     = args.doNorm
weights = [[],[]]
sf = [[],[]]
headerOpt = ""

if args.hlist == 0:
    histList   = ['h_nevts']
elif args.hlist == 1:
    histList   = [ # default plots list
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 'h_jets_ht_r',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_dr','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a',
              'h_X_mass', 
             ]
elif args.hlist == 2:
    histList   = [
              'h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt',
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht',
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv','h_jet3_csv',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_pt','h_H0_eta','h_H0_csthst0_a','h_H0_csthst1_a',
              'h_H0_dr','h_H0_deta_a','h_H0_dphi','h_H0_dphi_a',
              'h_H1_mass','h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a',
              'h_H1_dr','h_H1_deta_a','h_H1_dphi','h_H1_dphi_a',
              'h_H0H1_mass','h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst0_a','h_H0H1_csthst1_a',
              'h_H0H1_dr','h_H0H1_deta_a','h_H0H1_dphi_a', 'h_H0H1_dphi',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
              'h_X_mass', 'h_jets_ht_r',
             ]
histList2  = ['h_H0_H1_mass'] #2D histos

# ---------------
if args.whichPlots == -2:
    samlist1 = ['BM7']
    samlist2 = []
    optList = ["def_cmva",]
    legList = [["HH4b BM7"],]
    colorList = [[635],]
    doNormToLumi = [True,]
    dofill = [True,]
    isMC = False
    oname = "BM7_preBDT"

elif args.whichPlots == -1:
    samlist1 = ['BM2']
    samlist2 = ['SM']
    optList = ["def_cmva","def_cmva"]
    legList = [["HH4b BM2"], ["HH4b SM"]]
    colorList = [[635], [632]]
    doNormToLumi = [True, True]
    dofill = [True,True]
    isMC = True
    oname = "comp_smBm2_preBDT"

elif args.whichPlots == 0:
    samlist1 = ['SM'] ## only SM (Pangea not reweighted after alp_analysis)
    samlist2 = ['Data_train']
    optList = ["def_cmva","def_cmva_mixed"]
    legList = [["signal (HH4b SM)"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    doNormToLumi = [True, False] ###
    dofill = [True,True]
    isMC = False
    oname = "comp_sigBkgTrain_preBDT"

elif args.whichPlots == 1:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['qcd_m']
    samlist2 = []
    legList = [['QCD HT>200'],]
    colorList = []    
    weights = [[29.599755,6.338876,0.509821,0.089584,0.046491,0.005935,0.002410],]
    doNormToLumi = [True, True]  
    dofill = [True,]
    isMC = True
    oname = "QCD_preBDT"

elif args.whichPlots == 2:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['qcd_m500']
    samlist2 = ['TT']
    legList = [['QCD HT>500'], ['TT']]
    colorList = []    
    weights = [[0.509821,0.089584,0.046491,0.005935,0.002410],[0.010760]]
    doNormToLumi = [True, True]  
    dofill = [True,True]
    isMC = True
    oname = "comp_qcdtt_preBDT"

elif args.whichPlots == 3:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['TT','qcd_m']
    samlist2 = ['SM']
    legList = [['TT','QCD'], ['ggHH4b SM (1000x)']]
    colorList = []
    weights = [[0.010760,29.599755,6.338876,0.511526,0.149046,0.078782,0.009964,0.004075],[0.03771]]
    doNormToLumi = [True, True]
    dofill = [True,False]
    isMC = True
    oname = "comp_qcdttSig_preBDT"

elif args.whichPlots == 4:
    optList = ['def_cmva','def_cmva']
    samlist1 = ['qcd_m']
    samlist2 = ['qcd_b']
    legList = [['QCD'], ['QCD bEnr.']]
    colorList = []
    weights = [[29.599755,6.338876,0.511526,0.149046,0.078782,0.009964,0.004075],
               [0.023755, 0.085170, 0.032952, 18.475847, 6.122864, 0.623063, 0.364026, 0.030071, 0.013571, 0.004531, 2.798854, 0.929341, 0.079645, 0.050250]]
    sf = [[1.0282,1.0282,1.0282,1.0282,1.0282,1.0282,1.0282],
          [1.4819,1.4819,1.4819,1.4819,1.4819,1.4819,1.4819, 1.4819,1.4819,1.4819,1.4819,1.4819,1.4819,1.4819]]
    doNormToLumi = [True, True]
    dofill = [True,True]
    isMC = True
    oname = "comp_qcdqcdb_preBDT"

elif args.whichPlots == 5:
    samlist1 = ['ttH'] ## only SM (Pangea not reweighted after alp_analysis)
    samlist2 = ['Data']
    optList = ["def_cmva","def_cmva_mixed"]
    legList = [["ttH"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    doNormToLumi = [True, False] ###
    dofill = [True,False]
    isMC = False
    oname = "comp_ttHBkg_preBDT"

elif args.whichPlots == 6:
    samlist1 = ['ttH'] ## only SM (Pangea not reweighted after alp_analysis)
    samlist2 = ['SM']
    optList = ["def_cmva","def_cmva"]
    legList = [["ttH"], ["SM signal"]]
    colorList = [[632], [430]]
    doNormToLumi = [True, False] ###
    dofill = [True,False]
    isMC = False
    oname = "comp_ttH_signal_preBDT"

elif args.whichPlots == 7:
    samlist1 = ['TT'] ## only SM (Pangea not reweighted after alp_analysis)
    samlist2 = ['Data']
    optList = ["def_cmva","def_cmva_mixed"]
    legList = [["ttbar"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    doNormToLumi = [True, False] ###
    dofill = [True,False]
    isMC = False
    oname = "comp_ttbar_bkg_preBDT"

elif args.whichPlots == 8:
    samlist1 = ['TT'] ## only SM (Pangea not reweighted after alp_analysis)
    samlist2 = ['ttH']
    optList = ["def_cmva","def_cmva"]
    legList = [["ttbar"], ["ttH"]]
    colorList = [[632], [430]]
    doNormToLumi = [True, False] ###
    dofill = [True,False]
    isMC = False
    oname = "comp_ttbar_ttH_preBDT"

else: 
    print "## ERROR: wrong '-w' argument"
    exit()

oDir += oname

if args.defaultCol: colors = [[],[]]
else: colors = colorList

for n, w in enumerate(weights):
    if len(w)==0: print "## WARNING: weight[{}] is empty".format(n)

if not args.plotDir:     
    exit()
plotDir    = args.plotDir
print "HISTS FROM FOLDER {}".format(plotDir) 

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
            snames1.append(s)
        else:
            snames1.append(samples[s]['sam_name'])    
    else: 
        snames1.extend(samlists[s])
print snames1
snames2 = []
for s in samlist2:
    if not s in samlists: 
        if not s in samples: 
            snames2.append(s)
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

#----------------------------------
for h in histList:    
    hs1 = []
    hs2 = []
    if files1: hs1 = UtilsDraw.getHistos(h, files1, plotDir, intLumi_fb, doNormToLumi[0], weights[0], sf[0])
    if files2: hs2 = UtilsDraw.getHistos(h, files2, plotDir, intLumi_fb, doNormToLumi[1], weights[1], sf[1])
    hOpt = hist_opt[h]

    if hs1 and hs2:
        UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], 
                         hOpt, args.plotResidual, doNorm, oDir, colors, dofill, 0, headerOpt, isMC)
    elif hs1: UtilsDraw.drawH1only(hs1, snames1, legList[0], hOpt, oDir, colors, dofill, 0, headerOpt, isMC)

