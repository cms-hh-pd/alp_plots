
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
gROOT.SetBatch(True)

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='-1')
parser.add_argument("-n", "--doNorm"   , help="normalize to data"       , action='store_true')
parser.add_argument("-p", "--plotDir"  , help="root file subfolder in which histos are", default="trg_Iso") #trg_IsoAndJet
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"        , default="output/")
parser.add_argument("-l", "--list", help="hist list" , dest="hlist", type=int, default=1)
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/alp_moriond_base/'
oDir = args.oDir

if args.hlist == 0:
    histList   = ['h_nevts']
elif args.hlist == 1:
    histList   = ['h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
                  'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
                  'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv', 'h_jet3_csv',
                  'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva', 'h_jet3_cmva',
                  'h_all_ht', 'h_met_pt', 'h_mu0_pt', 'h_mu0_iso03', 'h_mu_n', 'h_mu_pt', 'h_mu_iso03','h_nevts']

intLumi_fb = 35.9 # plots normalized to this
weights = [[],[]]
sf = [[],[]]
header = ""
# ---------------

# sig vs bkg
if args.whichPlots == -2:
    optList = ["trgeff_2cmva_2l","trgeff_2cmva_2l"] #2 leptons
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.00208575,0.00202288, 0.023754, 0.013946, 0.009457, 0.000688, 0.000682, 0.000259, 0.000012, 0.010760],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva_2lept"
    header = " 2mu"

if args.whichPlots == -1:
    optList = ["trgeff_2cmva_2l","trgeff_2cmva_2l"] #2 leptons
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.00208575,0.00202288, 0.023754, 0.013946, 0.009457, 0.000688, 0.000682, 0.000259, 0.000012, 0.010760],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva_2lept"
    header = " 2mu"

if args.whichPlots == 0:
    optList = ["trg_2cmva_plots","trg_2cmva_plots"]
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top", "WJetsNuL", "TT"], ["data"]]  
    weights = [[0.005361,0.002020,0.002077, 0.023619,0.013342,0.009363,0.000679,0.000672,0.000253,0.000011, 0.010760],[]]
    sf = [[0.91823,0.91823,0.91823,0.91823,0.91823,0.91823,0.91823,0.91823,0.91823,0.91823,0.91823],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva"

elif args.whichPlots == 1:
    optList = ["trg_2cmva_plots","trg_2cmva_plots"]
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.002020,0.002077, 0.023619,0.013342,0.009363,0.000679,0.000672,0.000253,0.000011, 0.010760],[]]
    sf = [[0.91228,0.91228,0.91228,0.91228,0.91228,0.91228,0.91228,0.91228,0.91228,0.91228,0.91228],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva"

elif args.whichPlots == 2:
    optList = ["trg_4cmva_plots","trg_4cmva_plots"]
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.002020,0.002077, 0.023619,0.013342,0.009363,0.000679,0.000672,0.000253,0.000011, 0.010760],[]]
    sf = [[0.935,0.935,0.935,0.935,0.935,0.935,0.935,0.935,0.935,0.935,0.935],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_4cmva"

elif args.whichPlots == 3:
    optList = ["trg_4cmva_plots","trg_4cmva_plots"]
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.002020,0.002077, 0.023619,0.013342,0.009363,0.000679,0.000672,0.000253,0.000011, 0.010760],[]]
    sf = [[0.878,0.878,0.878,0.878,0.878,0.878,0.878,0.878,0.878,0.878,0.878],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_4cmva"

elif args.whichPlots == 4:
    optList = ["trg_3cmva","trg_3cmva"]
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = [["single top","WJetsNuL","TT"], ["data"]]
    weights = [[0.005361,0.002020,0.002077, 0.023619,0.013342,0.009363,0.000679,0.000672,0.000253,0.000011, 0.010760],[]]
    sf = [[0.898,0.898,0.898,0.898,0.898,0.898,0.898,0.898,0.898,0.898,0.898],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_3cmva"

elif args.whichPlots == 5:
    optList = ["trg_3cmva","trg_3cmva"]
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger'] 
    samlist2 = ['data_singleMu']
    legList = [["single top", "WJetsNuL", "TT"], ["data"]]  
    weights = [[0.005361,0.002020,0.002077,  0.023619,  0.013342,0.009363,0.000679,0.000672,0.000253,0.000011,0.010760],[]]  
    sf = [[0.863,0.863,0.863,0.863,0.863,0.863,0.863,0.863,0.863,0.863,0.863],[]]
    colorList = [430, 1]
    doNormToLumi = [True, False] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_3cmva"

oDir += "/"+oname

if not args.customCol: colors = [0,0]
else: colors = colorList

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

#----------------------------------
for h in histList:    
    hs1 = UtilsDraw.getHistos(h, files1, plotDir, intLumi_fb, doNormToLumi[0], weights[0], sf[0])
    hs2 = UtilsDraw.getHistos(h, files2, plotDir, intLumi_fb, doNormToLumi[1], weights[1], sf[1])
    hOpt = hist_opt[h]
    if hs1 and hs2:
        n1,n1err,n2,n2err = UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], hOpt, doResiduals, doNorm, oDir, colors, dofill, 0, plotDir+header, False)
        if n2: 
           print "### n1/n2 numEvents: {} +- {} ###".format(n1/n2, UtilsDraw.getRelErr(n1,n1err,n2,n2err)*n1/n2) 
           print "### n1: {} +- {} ###".format(n1,n1err) 
           print "### n2: {} +- {} ### \n".format(n2,n2err) 

