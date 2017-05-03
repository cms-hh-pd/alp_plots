# to compare histograms - max samples with different options
# python scripts/drawcomp_afterBDT.py -w 0 -b 20170116-181049

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
parser.add_argument("-c", "--noCustomCol" , help="do not use custom colors"       , action='store_true')
parser.add_argument("-l", "--list", help="hist list" , dest="hlist", type=int, default=1)
parser.set_defaults(doNorm=True, noCustomCol=False, plotResidual=False)
args = parser.parse_args()

iDir       = '../hh2bbbb_limit/' #'/lustre/cmswork/hh/alp_afterMVA/'
filename = iDir+"/"+args.bdt+".root"
headerOpt = args.bdt

# exe parameters
if args.hlist == 0:
    histList   = [ 'classifier'] #'h_H0_mass', 'h_H1_mass', 'h_H0H1_mass',
elif args.hlist == 1:
    histList   = [
                  'h_jets_ht', 'h_jets_ht_r',                
                  'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt', 
                  'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
                  'h_csv3','h_csv4',
                  'h_cmva3','h_cmva4',
                  'h_H0_mass','h_H0_pt','h_H0_csthst0_a','h_H0_dr','h_H0_dphi',
                  'h_H1_mass','h_H1_pt','h_H1_csthst2_a', 'h_H1_dr','h_H1_dphi',
                  'h_H0H1_mass', 'h_H0H1_pt', 'h_H0H1_csthst0_a', 'h_H0H1_dr',
                  'h_X_mass', 
                  'classifier'
                 ]
# exact list of BDT input variables:
elif args.hlist == 2:
    histList   = [
                  'h_jets_ht', 'h_jets_ht_r',
                  'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt',
                  'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
                  'h_cmva3','h_cmva4',
                  'h_H0_mass','h_H0_pt','h_H0_csthst0_a','h_H0_dr','h_H0_dphi',
                  'h_H1_mass','h_H1_pt', 'h_H1_dr','h_H1_dphi',
                  'h_H0H1_mass', 'h_H0H1_pt', 'h_H0H1_csthst0_a', #'h_H0H1_dr',
                  'h_X_mass'
                 ]
# exact list of BDT input variables:
elif args.hlist == 3:
    histList   = [
                  'h_jets_ht', 'h_jets_ht_r',
                  'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt',
                  'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
                  'h_cmva3','h_cmva4',
                  'h_H0_mass','h_H0_pt','h_H0_csthst0_a','h_H0_dr','h_H0_dphi',
                  'h_H1_mass','h_H1_pt', 'h_H1_dr','h_H1_dphi',
                  'h_H0H1_mass', 'h_H0H1_pt', 'h_H0H1_csthst0_a', #'h_H0H1_dr', 'h_H0H1_dphi_a',
                  'h_X_mass'
                 ]




histList2  = ["DiJets[0].mass()-DiJets[1].mass()", "CSV_Jet2-CSV_Jet3", "CMVA_Jet2-CMVA_Jet3",] #2D histos,
intLumi_fb = 1. # plots normalized to this
weights = [[],[]]
sf = [[],[]]

which = args.whichPlots

if which == -3:
    samples = [['tt','qcd_m'], ['bkg']]
    fractions = ['','test']
    regions = ['','']
    weights = [[0.010760,17.635231,3.476259,0.509821,0.089584,0.046491,0.005935,0.002410],[]]
    legList = [['tt','qcd HT>200'], ["bkg (mixed data)"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_qcdttBkg_afterBDT'
    headerOpt = ""

elif which == -2:
    samples = [['sm'], ['sig']]
    fractions = ['','']
    regions = ['','']
    legList = [["ggHH4b - SM"], ["ggHH4b - PangeaSM"]]
    colorList = [630, 633]
    dofill = [True,True]
    isMC = True
    oname = 'comp_SMpangeaSM_afterBDT'
    headerOpt = ""

#elif which == 4:
 #   samples = [['sm'], ['bkg']]
  #  fractions = ['test','test']
   # regions = ['','']
    #legList = [["ggHH4b SM"], ["bkg (mixed data)"]]  # - test fract
    #colorList = [632, 430]
    #dofill = [True,True]
    #isMC = True
    #oname = 'comp_sigBkg_afterBDT'
    #headerOpt = "    test fr." #{}".format()

elif which == -1:
    samples = [['pan'], ['sig']]
    fractions = ['','']
    regions = ['','']
    legList = [["ggHH4b - Pangea"], ["ggHH4b - PangeaSM"]]
    colorList = [630, 633]
    dofill = [True,True]
    isMC = True
    oname = 'comp_SMpangea_afterBDT'
    headerOpt = ""

#elif which == -1:
 #   samples = [['sig'], ['sample']]
  ##  fractions = ['test','']
   # regions = ['sr','sr']
  #  legList = [["ggHH4b - pangeaSM"],["ggHH4b - SM"]]
  #  colorList = [633, 630]
  #  dofill = [True,True]
  #  isMC = True
  #  oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'
  #  headerOpt = "SR"

elif which == 0:
    samples = [['sig'], ['bkg']]
    fractions = ['test','test']
    regions = ['','']
    legList = [["ggHH4b SM"], ["bkg (mixed data)"]]  # - test fract
    colorList = [632, 430]
    dofill = [True,True]
    sf = [[9901117.35673],[1.]]
    isMC = True
    oname = 'comp_sigBkg_afterBDT'
    headerOpt = "    test fr." #{}".format()

elif which == 1:
    samples = [['sig'], ['bkg']]
    fractions = ['train','train']
    regions = ['','']
    legList = [["ggHH4b SM"], ["bkg (mixed data)"]]
    colorList = [632, 430]
    dofill = [True,True]
    sf = [[9901117.35673],[1.]]
    isMC = True
    oname = 'comp_sigBkg_afterBDT'
    headerOpt = "    train fr."#H1-H2 mass blinded 

elif which == 2:
    samples = [['sig'], ['bkg']]
    fractions = ['test','test']
    regions = ['sr', 'sr']
    legList = [["signal (HH4b SM) - SR"], ["bkg (mixed data) - SR"]]
    colorList = [632, 430]
    dofill = [True,True]
    isMC = False
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 3:
    samples = [['sig'], ['bkg']]
    fractions = ['test','test']
    regions = ['cr', 'cr']
    legList = [["signal (HH4b SM) - CR"], ["bkg (mixed data) - CR"]]
    colorList = [632, 430]
    dofill = [True,True]
    isMC = False
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 4:
    samples = [['sig'], ['bkg']]
    fractions = ['train','train']
    regions = ['sr', 'sr']
    legList = [["signal (HH4b SM) - SR, train fract"], ["bkg (mixed data) - SR, train fract"]]
    colorList = [632, 430]
    dofill = [True,True]
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 5:
    samples = [['bkg'],['data']] #data always  second
    fractions = ['test','']
    regions = ['cr','cr'] #    regions = ['cr','cr']
    legList = [["bkg (mixed data)"], ["data"]]
    colorList = [430, 1]
    dofill = [True,False]
    isMC = False
    oname = 'comp_bkgdata_afterBDT'
    headerOpt = "   0<bdtout<0.8" #h1-h2 mass cut

elif which == 6:
    samples = [['bkg'],['bkg']]
    fractions = ['test','test']
    regions = ['','sr']
    legList = [["bkg (mixed data)"], ["data - SR"]]
    colorList = [430, 416]
    dofill = [True,True]
    isMC = False
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 7:
    samples = [['sig'], ['sig']]
    fractions = ['train','test']
    regions = ['', '']
    legList = [["signal (HH4b SM) - train"], ["signal (HH4b SM) - test"]]
    colorList = [632, 600]
    dofill = [True,True]
    isMC = True
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 8:
    samples = [['bkg'], ['bkg']]
    fractions = ['train','test']
    regions = ['', '']
    legList = [["bkg (mixed data) - train"], ["bkg (mixed data) - test"]]
    colorList = [430, 400]
    dofill = [True,True]
    isMC = False
    oname = 'comp_'+samples[0]+samples[1]+'_afterBDT'

elif which == 9:
    samples = [['bkg'],['data']] #data always  second
    fractions = ['test','']
    regions = ['msbdt','msbdt'] 
    legList = [["bkg (mixed data)"], ["data"]]
    colorList = [430, 1]
    sf = [[1.],[1.]]
    dofill = [True,False]
    isMC = False
    oname = 'comp_bkgdata_afterBDT'
    headerOpt = " BDT[0.8-1] & H1-H2 mass blinded" #h1-h2 mass cut

elif which == 10:
    samples = [['bkg'],['data']] #data always  second
    fractions = ['test','']
    regions = ['ms','ms'] 
    legList = [["bkg (mixed data)"], ["data"]]
    colorList = [430, 1]
    sf = [[1.],[1.]]
    dofill = [True,False]
    isMC = False
    oname = 'comp_bkgdata_afterBDT'
    headerOpt = "    H1-H2 mass blinded" #

#elif which == 10:
#    samples = [['bkg'],['bkg']] #data always  second
 #   fractions = ['test','test']
#    regions = ['ms',''] 
 #   legList = [["bkg (mixed data), mCut"], ["bkg (mixed data)"]]
 #   colorList = [404, 430]
 #   dofill = [True,True]
 #   isMC = False
 #   oname = 'comp_bkgbkg__mCR_afterBDT'
 #   headerOpt = "   H1-H2 mass blinded" #h1-h2 mass cut

#antitag ---
elif which == 11:
    samples = [['antiMixed'],['data']] #data always  second
    fractions = ['','']
    regions = ['',''] #    regions = ['cr','cr']
    legList = [["bkg (mixed data)"], ["data"]]
    colorList = [430, 1]
    dofill = [True,False]
    isMC = False
    sf = [[1.],[1.]]
    oname = 'comp_antiTagdata_afterBDT'
    headerOpt = "   4thjetCMVA<=medWP" #h1-h2 mass cut

elif which == 12:
    samples = [['antiMixed'],['bkg']] #data always  second
    fractions = ['','test']
    regions = ['cr','cr'] #    regions = ['cr','cr']
    legList = [["mixed data - antiTag"], ["mixed data - 4CMVA"]]
    colorList = [416, 430]
    sf = [[1.],[1.]]
    dofill = [True,True]
    isMC = False
    oname = 'comp_antiTagMixed_afterBDT'
    headerOpt = "    " #h1-h2 mass cut

elif which == 13:
    samples = [['antiMixed'],['data']] #data always  second
    fractions = ['','']
    regions = ['sr','sr'] # check on 0.8-1 region
    legList = [["bkg (mixed data)"], ["data"]]
    colorList = [430, 1]
    dofill = [True,False]
    sf = [[1.],[1.]]
    isMC = False
    oname = 'comp_antiTagdata_afterBDT'
    headerOpt = "  BDT[0.8-1] & 4thjetCMVA<=medWP" #h1-h2 mass cut
    
else: 
    print "ERROR: wrong '-w' argument"
    exit()
#----------------

if args.noCustomCol: colors = [0,0]
else: colors = colorList

snames1 = []
for s in samples[0]:
    if not s in samlists: 
        if not s in samples: 
            snames1.append(s)    #debug
        else:
            snames1.append(samples[s]['sam_name'])    
    else: 
        snames1.extend(samlists[s])
#print snames1

snames2 = []
for s in samples[1]:
    if not s in samlists: 
        if not s in samples: 
            snames2.append(s)    #debug
        else:
            snames2.append(samples[s]['sam_name'])    
    else: 
        snames2.extend(samlists[s])
#print snames2


plotDirs1 = []
for sam in snames1:
    option = ''
    if fractions[0]: 
        option += fractions[0]
        if regions[0]: option += "_"
    if regions[0]: option += regions[0]

    if option: plotDirs1.append(sam+'_'+option)
    else: plotDirs1.append(sam)
print "HISTS FROM FOLDER {}".format(plotDirs1) 

plotDirs2 = []
for sam in snames2:
    option = ''
    if fractions[1]: 
        option += fractions[1]
        if regions[1]: option += "_"
    if regions[1]: option += regions[1]

    if option: plotDirs2.append(sam+'_'+option)
    else: plotDirs2.append(sam)
print "HISTS FROM FOLDER {}".format(plotDirs2) 


oDir = args.oDir
oDir += "/"+args.bdt
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += "/"+oname
if args.doNorm: oDir = oDir+"_norm/"
else: oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += option #keep the second sample options
if not os.path.exists(oDir): os.mkdir(oDir)

sname = [] #to avoid crash
#----------------------------------
for h in histList:
    hOpt = hist_opt[h]
    if h == 'classifier': 
        h+='-20170502-234140' #+args.bdt   #20170502-234140
    hs1 = UtilsDraw.getHistos_bdt(h, filename, plotDirs1, weights[0], sf[0])
    hs2 = UtilsDraw.getHistos_bdt(h, filename, plotDirs2, weights[1], sf[1])

    if hs1 and hs2:
        n1,n1err,n2,n2err = UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], 
                         hOpt, args.plotResidual, args.doNorm, oDir, colors, dofill, args.clrebin, headerOpt, isMC)
        #if n2: 
        #   print "### n1/n2 numEvents: {} +- {} ###".format(n1/n2, UtilsDraw.getRelErr(n1,n1err,n2,n2err)*n1/n2) 
        #   print "### n1: {} +- {} ###".format(n1,n1err) 
        #   print "### n2: {} +- {} ### \n".format(n2,n2err) 

