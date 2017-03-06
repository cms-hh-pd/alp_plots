
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
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '/lustre/cmswork/hh/alp_moriond_base/'
oDir = args.oDir

# exe parameters
#histList   = ['h_nevts']

histList   = ['h_nevts', 'h_jets_n','h_jet0pt_pt', 'h_jet1pt_pt', 'h_jet2pt_pt', 'h_jet3pt_pt', 
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet0_csv', 'h_jet1_csv', 'h_jet2_csv', 'h_jet3_csv',
              'h_jet0_cmva', 'h_jet1_cmva', 'h_jet2_cmva', 'h_jet3_cmva',
              'h_all_ht', 'h_met_pt', 'h_mu0_pt', 'h_mu0_iso03', 'h_mu_n', 'h_mu_pt', 'h_mu_iso03']

intLumi_fb = 35.9 # plots normalized to this
# ---------------

# sig vs bkg
if args.whichPlots == 0:
    optList = ["trgeff_2cmva","trgeff_2cmva"]
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = ["mc", "data"]
    colorList = [430, 1]
    doNormToLumi = [True, True] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva"

elif args.whichPlots == 1:
    optList = ["trgeff_2cmva","trgeff_2cmva"]
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = ["mc", "data"]
    colorList = [430, 1]
    doNormToLumi = [True, True] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_2cmva"

elif args.whichPlots == 2:
    optList = ["trgeff_4cmva","trgeff_4cmva"]
    plotDir = 'trg_Iso'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = ["mc", "data"]
    colorList = [430, 1]
    doNormToLumi = [True, True] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_4cmva"

elif args.whichPlots == 3:
    optList = ["trgeff_4cmva","trgeff_4cmva"]
    plotDir = 'trg_IsoAndJet'
    samlist1 = ['trigger']
    samlist2 = ['data_singleMu']
    legList = ["mc", "data"]
    colorList = [430, 1]
    doNormToLumi = [True, True] 
    dofill = [True,False]
    oname = "comp_mcData_trgEff_4cmva"

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
    hs1 = UtilsDraw.getHistos(h, files1, plotDir, intLumi_fb, doNormToLumi[0])
    hs2 = UtilsDraw.getHistos(h, files2, plotDir, intLumi_fb, doNormToLumi[1])
    hOpt = hist_opt[h]
    if hs1 and hs2:
        n1,n1err,n2,n2err = UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], hOpt, doResiduals, doNorm, oDir, colors, dofill, 0, plotDir)
        if n2: 
           print "### n1/n2 numEvents: {} +- {} ###".format(n1/n2, UtilsDraw.getRelErr(n1,n1err,n2,n2err)*n1/n2) 
           print "### n1: {} +- {} ###".format(n1,n1err) 
           print "### n2: {} +- {} ### \n".format(n2,n2err) 

