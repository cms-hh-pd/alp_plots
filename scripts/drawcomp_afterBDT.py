# to compare histograms - max samples with different options
# python scripts/drawcomp_afterBDT.py -n -c -w 0 -b 20170116-181049

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
parser.add_argument("-b", "--bdt"       , help="bdt version, equal to input file name", default="")
parser.add_argument("-o", "--oDir"     , help="output directory"        , default="plots_moriond")
parser.add_argument("-r", "--clrebin", help="to rebin (classifier output)"    , type=int, default=-1)
parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==fit)" , type=int, default=0)
parser.add_argument("-n", "--doNorm"    , help="do not normalize"       , action='store_false')
parser.add_argument("-c", "--customCol" , help="do not use custom colors"       , action='store_false')
parser.set_defaults(doNorm=True, customCol=True, plotResidual=False)
args = parser.parse_args()

iDir       = '../hh2bbbb_limit/' #'/lustre/cmswork/hh/alp_afterMVA/'
filename = iDir+"/"+args.bdt+".root"

# exe parameters
histList   = [ "classifier",
              'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 'h_jets_ht', 
              'h_jet2_csv','h_jet3_csv',
              'h_jet2_cmva','h_jet3_cmva',
              'h_H0_mass','h_H0_csthst0_a','h_H0_dr', #'h_H0_pt','h_H0_eta','h_H0_csthst1_a','h_H0_deta_a','h_H0_dphi_a',
              'h_H1_mass','h_H1_csthst2_a','h_H1_dr', #'h_H1_pt','h_H1_eta','h_H1_csthst2_a','h_H1_csthst3_a','h_H1_dr','h_H1_deta_a','h_H1_dphi_a',
              'h_H0H1_mass', 'h_H0H1_csthst0_a', 'h_H0H1_dr', #'h_H0H1_pt','h_H0H1_eta','h_H0H1_csthst1_a',,'h_H0H1_deta_a','h_H0H1_dphi_a',
              'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
              'h_X_mass', 'h_jets_ht_r',               
             ]
histList2  = ["DiJets[0].mass()-DiJets[1].mass()", "CSV_Jet2-CSV_Jet3", "CMVA_Jet2-CMVA_Jet3",] #2D histos,
intLumi_fb = 1. # plots normalized to this

which = args.whichPlots

if which == -1:
    samples = ['sig', 'sample']
    fractions = ['test','']
    regions = ['sr','sr']
    legList = ["signal (HH4b SM - pangea) - SR - test fract", "signal (HH4b SM) - SR"]
    colorList = [632, 630]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 0:
    samples = ['sig', 'bkg']
    fractions = ['test','test']
    regions = ['','']
    legList = ["signal (HH4b SM) - test fract", "bkg (mixed data) - test fract"]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 1:
    samples = ['sig', 'bkg']
    fractions = ['train','train']
    regions = ['','']
    legList = ["signal (HH4b SM) - train fract", "bkg (mixed data) - train fract"]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 2:
    samples = ['sig', 'bkg']
    fractions = ['test','test']
    regions = ['sr', 'sr']
    legList = ["signal (HH4b SM) - SR", "bkg (mixed data) - SR"]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 3:
    samples = ['sig', 'bkg']
    fractions = ['test','test']
    regions = ['cr', 'cr']
    legList = ["signal (HH4b SM) - CR", "bkg (mixed data) - CR"]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 4:
    samples = ['sig', 'bkg']
    fractions = ['train','train']
    regions = ['sr', 'sr']
    legList = ["signal (HH4b SM) - SR, train fract", "bkg (mixed data) - SR, train fract"]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 5:
    samples = ['bkg','data'] #data always  second
    fractions = ['test','']
    regions = ['cr','cr']
    legList = ["bkg (mixed data) - CR", "data - CR"]
    colorList = [430, 1]
    dofill = [True,False]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 6:
    samples = ['bkg','bkg']
    fractions = ['test','test']
    regions = ['','sr']
    legList = ["bkg (mixed data)", "data - SR"]
    colorList = [430, 416]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 7:
    samples = ['sig', 'sig']
    fractions = ['train','test']
    regions = ['', '']
    legList = ["signal (HH4b SM) - train", "signal (HH4b SM) - test"]
    colorList = [632, 600]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 8:
    samples = ['bkg', 'bkg']
    fractions = ['train','test']
    regions = ['', '']
    legList = ["bkg (mixed data) - train", "bkg (mixed data) - test"]
    colorList = [430, 400]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'
    
else: 
    print "ERROR: wrong '-w' argument"
    exit()
#----------------

if not args.customCol: colors = []
else: colors = colorList

plotDir = []
for n, sam in enumerate(samples):
    option = ''
    if fractions[n]: 
        option += fractions[n]
        if regions[n]: option += "_"
    if regions[n]: option += regions[n]

    if option: plotDir.append(sam+'_'+option)
    else: plotDir.append(sam)
    print "HISTS FROM FOLDER {}".format(plotDir[n]) 

    oDir = args.oDir
    oDir += "/"+args.bdt
    if not os.path.exists(oDir): os.mkdir(oDir)
    oDir += "/"+oname
    if args.doNorm: oDir = oDir+"_norm/"
    else: oDir = oDir+"/"
    if not os.path.exists(oDir): os.mkdir(oDir)
    oDir += option #keep the second sample options
    if not os.path.exists(oDir): os.mkdir(oDir)

#----------------------------------
for h in histList:
    hOpt = hist_opt[h]
    if h == 'classifier': 
        h+='-'+args.bdt    
    hs1 = UtilsDraw.getHistos_bdt(h, filename, plotDir[0])
    hs2 = UtilsDraw.getHistos_bdt(h, filename, plotDir[1])

    if hs1 and hs2:
        UtilsDraw.drawH1(hs1, legList[0], hs2, legList[1], hOpt, args.plotResidual, args.doNorm, oDir, colors, dofill, args.clrebin)

