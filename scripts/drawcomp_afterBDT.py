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

# exe parameters
histList   = [ "classifier",
               "DiJets[0].mass()", "DiJets[1].mass()", "DiHiggs[0].mass()", "DiHiggs[0].MX()", "DiHiggs[0].mass()",
               "CSV3", "CSV4", 
               "CMVA3", "CMVA4", 
             ]
histList2  = ["DiJets[0].mass()-DiJets[1].mass()", "CSV3-CSV4", "CMVA3-CMVA4",] #2D histos
intLumi_fb = 1. # plots normalized to this

# parsing parameters
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='-1')
parser.add_argument("-n", "--doNorm"   , help="normalize to data"       , action='store_true')
parser.add_argument("-b", "--bdt"      , help="bdt version, equal to input file name", default="")
parser.add_argument("-c", "--customCol", help="use custom colors"       , action='store_true')
parser.add_argument("-o", "--oDir"     , help="output directory"        , default="output")
parser.set_defaults(doNorm=False, customCol=False)
args = parser.parse_args()

iDir       = '../hh2bbbb_limit/' #'/lustre/cmswork/hh/alp_afterMVA/'
filename = iDir+"/"+args.bdt+".root"

steps = 7
for k in range(0,steps):
    if args.whichPlots == -1:
        which = k
    else: 
        steps = 1
        which = args.whichPlots

    if which == 0:
        samples = ['sig', 'bkg']
        fractions = ['test','test']
        regions = ['','']
        legList = ["signal (HH4b SM)", "bkg (mixed data)"]
        colorList = [632, 430]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 1:
        samples = ['sig', 'bkg']
        fractions = ['train','train']
        regions = ['','']
        legList = ["signal (HH4b SM) - train fract", "bkg (mixed data) - train fract"]
        colorList = [632, 430]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 2:
        samples = ['sig', 'bkg']
        fractions = ['test','test']
        regions = ['sr', 'sr']
        legList = ["signal (HH4b SM) - SR", "bkg (mixed data) - SR"]
        colorList = [632, 430]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 3:
        samples = ['sig', 'bkg']
        fractions = ['test','test']
        regions = ['cr', 'cr']
        legList = ["signal (HH4b SM) - CR", "bkg (mixed data) - CR"]
        colorList = [632, 430]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 4:
        samples = ['sig', 'bkg']
        fractions = ['train','train']
        regions = ['sr', 'sr']
        legList = ["signal (HH4b SM) - SR, train fract", "bkg (mixed data) - SR, train fract"]
        colorList = [632, 430]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 5:
        samples = ['bkg','data']
        fractions = ['test','']
        regions = ['cr','cr']
        legList = ["bkg (mixed data) - CR", "data - CR"]
        colorList = [430, 1]
        dofill = [1,0]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

    elif which == 6:
        samples = ['bkg','bkg']
        fractions = ['test','test']
        regions = ['','sr']
        legList = ["bkg (mixed data)", "data - SR"]
        colorList = [430, 416]
        dofill = [1,1]
        oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'
    
    else: 
        print "ERROR: wrong '-w' argument"
        exit()
    #----------------

    if not args.customCol: colors = []
    else: colors = colorList

    doNorm     = args.doNorm
    doRatio = False
	
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
	if doNorm: oDir = oDir+"_norm/"
	else: oDir = oDir+"/"
	if not os.path.exists(oDir): os.mkdir(oDir)
	oDir += option #keep the second sample options
	if not os.path.exists(oDir): os.mkdir(oDir)

    #----------------------------------
    for h in histList:
        hOpt = hist_opt[h]
        if h == 'classifier': h+='-'+args.bdt    
        hs1 = UtilsDraw.getHistos_bdt(h, filename, plotDir[0])
        hs2 = UtilsDraw.getHistos_bdt(h, filename, plotDir[1])

        if hs1 and hs2:
            UtilsDraw.drawH1(hs1, legList[0], hs2, legList[1], hOpt, doRatio, doNorm, oDir, colors, dofill)

