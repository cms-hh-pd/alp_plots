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
parser.add_argument("-w", "--whichPlots", help="which plots to be produced", type=int, default='0')
parser.add_argument("-b", "--bdt", help="bdt version, equal to input file name (classifier report output)", required=True)
parser.add_argument("-o", "--oDir", help="output directory", default="plots")
parser.add_argument("--res", dest="plotResidual", help="to plot residuals (2==pulls)", type=int, default=0)
parser.add_argument("-r", "--clrebin", help="to rebin (classifier output)", type=int, default=-1)
parser.add_argument("-n", "--doNorm", help="do normalize ", action='store_true')
parser.add_argument("-c", "--defaultCol", help="to use default colors", action='store_true')
parser.add_argument("-l", "--list", help="hist list", dest="hlist", type=int, default=0)
parser.add_argument("--lumi", help="int lumi to normalize to", dest="lumi", type=float, default=35.9)
parser.set_defaults(doNorm=False, defaultCol=False)
args = parser.parse_args()

iDir       = '../hh2bbbb_limit/'
filename = iDir+"/"+args.bdt+".root"
headerOpt = args.bdt
intLumi_fb = args.lumi
trg_eff = 0.96
which = args.whichPlots
getChi = False
getVar = False
drawH2 = False
doNormToLumi = [False, False]
weights = [[],[]]
sf = [[],[]]

if args.hlist == -1:
    histList   = [ 'clf-tt', 'classifier']
elif args.hlist == 0:
    histList   = [ 'classifier']
elif args.hlist == 1: # exact list of BDT input variables
    histList   = [
                  'h_jets_ht', 'h_jets_ht_r',
                  'h_jet0_pt', 'h_jet1_pt', 'h_jet2_pt', 'h_jet3_pt',
                  'h_jet0_eta', 'h_jet1_eta', 'h_jet2_eta', 'h_jet3_eta',
                  'h_cmva3','h_cmva4',
                  'h_H0_mass','h_H0_pt','h_H0_csthst0_a','h_H0_dr','h_H0_dphi',
                  'h_H1_mass','h_H1_pt', 'h_H1_dr','h_H1_dphi',
                  'h_H0H1_mass', 'h_H0H1_pt', 'h_H0H1_csthst0_a',
                  'h_X_mass'
                  'classifier'
                 ]
elif args.hlist == 2:
    histList   = [
                  'h_csv3','h_csv4',
                  'h_H1_csthst2_a', 'h_H1_dr','h_H1_dphi','h_H0H1_dr',
                 ]

histList2  = ["DiJets[0].mass()-DiJets[1].mass()", "CSV_Jet2-CSV_Jet3", "CMVA_Jet2-CMVA_Jet3",] # -- not maintained

###############
if which == -2:
    samples = [['HHTo4B_SM'], ['sig']]
    fractions = ['','train']
    regions = ['','']
    legList = [["ggHH4b - SM"], ["ggHH4b - PangeaSM"]]
    colorList = [[630], [633]]
    sf = [[7.335],[1.]] #7.335 2.439
    dofill = [True,True]
    isMC = True
    oname = 'comp_SMpangeaSM_afterBDT'
    headerOpt = ""

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

elif which == 0:
    samples = [['sig'], ['bkg']]
    fractions = ['appl','appl']
    regions = ['','']
    legList = [["ggHH4b SM"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    dofill = [True,True]
    weights = [[1.],[1.]] #(33.53*0.5824*0.5824/(4172119.0*0.2))
    sf = [[1.],[0.25]]
    isMC = True
    oname = 'comp_sigBkg_afterBDT'
    headerOpt = "    appl samples"

elif which == 1:
    samples = [['sig'], ['bkg']]
    fractions = ['train','train']
    regions = ['','']
    legList = [["ggHH4b BM12"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    dofill = [True,True]
    weights = [[1.],[1.]]
    sf = [[1.],[0.25]]
    isMC = True
    oname = 'comp_sigBkg_afterBDT'
    headerOpt = "    train samples"

elif which == 2:
    samples = [['sig'], ['bkg']]
    fractions = ['test','test']
    regions = ['', '']
    legList = [["ggHH4b SM"], ["bkg (mixed data)"]]
    colorList = [[632], [430]]
    dofill = [True,True]
    weights = [[1.],[1.]]
    sf = [[1.],[0.25]]
    isMC = True
    oname = 'comp_sigBkg_afterBDT'
    headerOpt = "    test sample"

elif which == 5:
    samples = [['bkg'],['data']] #data always  second
    fractions = ['appl','']
    regions = ['ms','ms']
    legList = [["mixed data"], ["data"]]
    colorList = [[430], [1]]
    sf = [[1.],[4.]]
    dofill = [True,False]
    isMC = False
    oname = 'comp_bkgdata_afterBDT'
    headerOpt = "   mass CR, appl sample" #btag CR

elif which == 500: #!!only with btag root file!!
    samples = [['bkg'],['data']] #data always  second
    fractions = ['appl','']
    regions = ['ttbdt','ttbdt']
    legList = [["mixed data"], ["data"]]
    colorList = [[430], [1]]
    sf = [[1.],[4.]]
    dofill = [True,False]
    isMC = False
    oname = 'comp_bkgdata_afterBDT'
    headerOpt = "   ttBDT<0.3, btag CR, appl sample"

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
    fractions = ['appl','test']
    regions = ['', '']
    legList = [["bkg (mixed data) - appl"], ["bkg (mixed data) - test"]]
    colorList = [[430], [400]]
    dofill = [True,True]
    isMC = False
    oname = 'comp_bkgAppl-bkgTest_afterBDT'

elif which == 9:
    samples = [['sig'],['bkg']] #data always  second
    fractions = ['test','test']
    regions = ['ms','ms'] 
    legList = [["ggHH4b SM"], ["mixed data"]]
    colorList = [[632], [430]]
    sf = [[(33.53*0.5824*0.5824/(4172119.0*0.2))],[0.25]]
    dofill = [True,True]
    isMC = True
    oname = 'comp_sigbkgms_afterBDT'
    headerOpt = "  H mass CR - test sam."

## 10nn
elif which == 16: # -l 0 !!
    getVar = True
    samples = [['mixed-0','mixed-11','mixed-22','mixed-33','mixed-44','mixed-55','mixed-66','mixed-77','mixed-88','mixed-99'],[]]
    #samples = [['mixed-0','mixed-1','mixed-2','mixed-3','mixed-4','mixed-5','mixed-6','mixed-7','mixed-8','mixed-9'],[]]
    #samples = [['mixed-89','mixed-98','mixed-76','mixed-67','mixed-54','mixed-45','mixed-32','mixed-23','mixed-10','mixed-1'],[]]
    fractions = ['','']
    regions = ['','']
    legList = [["bkg (mixed data - 10nn)"], []]
    colorList = [430, 1]
    dofill = [False,False]
    isMC = False
    oname = 'comp_mixedData_10nn_var_diag'
    #oname = 'comp_mixedData_10nn_var_rdm'
    headerOpt = "  antitag selection - 10nn diagonal"
    #headerOpt = "  antitag selection - 10nn various comb."

## 20nn - short
elif which == 17: # -l 0 !!
    getVar = True
    samples = [['mixed-0','mixed-1','mixed-2','mixed-3','mixed-4','mixed-5','mixed-6','mixed-7','mixed-8','mixed-9',
                'mixed-10','mixed-11','mixed-12','mixed-13','mixed-14','mixed-15','mixed-16','mixed-17','mixed-18 mixed-38'],[]]
#    samples = [['mixed-19','mixed-20','mixed-21','mixed-22','mixed-23','mixed-24','mixed-25','mixed-26','mixed-27',
#                'mixed-28','mixed-29','mixed-30','mixed-31','mixed-32','mixed-33','mixed-34','mixed-35','mixed-36','mixed-37','mixed-38'],[]]
    fractions = ['','']
    regions = ['','']
    legList = [["bkg (mixed data - 20nn)"], []] #up to 5 nn
    colorList = [430, 1]
    dofill = [False,False]
    isMC = False
    oname = 'comp_mixedData_20nn_var_diag'
#    oname = 'comp_mixedData_20nn_var_20'
    headerOpt = "  def selection - 20nn diagonal"
#    headerOpt = "  def selection - 20nn comb. with 20th"

elif which == 20: 
    samples = [['ggHbb'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["ggHbb"], ["HH4b SM"]]
    colorList = [[602], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[0.002879],[(33.53*0.5824*0.5824/(4172119.0*0.2))]] 
    oname = 'comp_gghsig_afterBDT'
    headerOpt = "    "

elif which == 21:
    samples = [['vbfHbb'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["vbfHbb"], ["HH4b SM"]]
    colorList = [[434], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[0.000720],[(33.53*0.5824*0.5824/(4172119.0*0.2))]]
    oname = 'comp_vbfhsig_afterBDT'
    headerOpt = "    "

elif which == 22:
    samples = [['ttHbb'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["ttHbb"], ["HH4b SM"]]
    colorList = [[419], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[0.00007621],[(33.53*0.5824*0.5824/(4172119.0*0.2))]]

    oname = 'comp_tthsig_afterBDT'
    headerOpt = "    "

elif which == 23:
    samples = [['ZHbbqq'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["ZH to QQBB"], ["HH4b SM"]]
    colorList = [[398], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[0.0007665],[(33.53*0.5824*0.5824/(4172119.0*0.2))]]
    oname = 'comp_zhsig_afterBDT'
    headerOpt = "    "

elif which == 24:
    samples = [['TTTT'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['',''] 
    legList = [["TTTT"], ["HH4b SM"]]
    colorList = [[413], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[1.],[(33.53*0.5824*0.5824/(4172119.0*0.2))]] ## update xs!!
    oname = 'comp_ttttsig_afterBDT'
    headerOpt = "    "

elif which == 25: 
    samples = [['ttbb'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["ttbb"], ["HH4b SM"]]
    colorList = [[420], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[1.],[(33.53*0.5824*0.5824/(4172119.0*0.2))]] ## update xs!!
    oname = 'comp_ttbbsig_afterBDT'
    headerOpt = "    "

elif which == 26: 
    samples = [['TT'],['sig']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["tt"], ["HH4b SM"]]
    colorList = [[430], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077],[(33.53*0.5824*0.5824/(4172119.0*0.2))]] ## update xs!!
    oname = 'comp_ttsig_afterBDT'
    headerOpt = "    "

elif which == 27: 
    samples = [['TT'],['bkg']] #data always  second
    fractions = ['','appl']
    regions = ['',''] #    regions = ['cr','cr']
    legList = [["tt"], ["mixed data"]]
    colorList = [[425], [400]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077*35.9*0.96],[1.]]
    oname = 'comp_ttbkg_afterBDT'
    headerOpt = "    "

elif which == 2007:
    samples = [['ttHbb','TT'],['bkg']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["ttHbb","tt"], ["mixed data"]]
    colorList = [[419,425], [430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.00007621*35.9*0.96, 0.01077*35.9*0.96], [0.25]] ## update xs!!
    oname = 'comp_tthttbkg_afterBDT'
    headerOpt = "    "

elif which == 207: 
    samples = [['TT-fix-00'],['TT']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["mixed data as TT (0-0)"], ["TT"]]
    colorList = [[603], [430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077*35.9*0.96*4],[0.01077*35.9*0.96*4]]
    oname = 'tt-tt-fix-00'
    headerOpt = "   "

elif which == 208:
    samples = [['TT-fix-00-11'],['TT-fix-00']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as TT (1-1,0-0)"], ["mixed data as TT (0-0)"]]
    colorList = [[603], [430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077*35.9*0.96/4],[0.01077*35.9*0.96]]
    oname = 'tt-fix0011-tt-fix00'
    headerOpt = "   "

elif which == 2071: 
    samples = [['TT-fix-appl'],['TT']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["mixed data as TT (appl)"], ["TT"]]
    colorList = [[603], [430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077*35.9*0.96],[0.01077*35.9*0.96*4]]
    oname = 'tt-tt-fix-appl'
    headerOpt = "   "

elif which == 2072: 
    samples = [['TT'],['TT-fix-appl']]
    fractions = ['','']
    regions = ['','']
    legList = [["TT"], ["mixed data as TT (appl)"]]
    colorList = [[603], [430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.01077*35.9*0.96*4],[0.01077*35.9*0.96]]
    oname = 'tt-tt-fix-appl'
    headerOpt = "   "

elif which == 2008:
    samples = [['ttHbb-fix-00','TT-fix-00'],['ttHbb','TT']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["mixed data as ttHbb (0-0)","mixed data as TT (0-0)"], ["ttHbb","TT"]]
    colorList = [[619,603], [419,430]]
    dofill = [True,True]
    isMC = True
    sf = [[0.00007621*35.9*0.96*4,0.01077*35.9*0.96*4],[0.00007621*35.9*0.96*4,0.01077*35.9*0.96*4]]
    oname = 'ttHtt-fix00-ttHtt'
    headerOpt = "   "

elif which == 208: 
    samples = [['ttHbb-fix-00'],['ttHbb']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["mixed data as ttHbb (0-0)"], ["ttHbb"]]
    colorList = [[619], [419]]
    dofill = [True,True]
    isMC = True
    sf = [[0.00007621*35.9*0.96],[0.00007621*35.9*0.96]]
    oname = 'tth-tth-fix-00'
    headerOpt = "   "

elif which == 29: # -l 0 !!
    samples = [['ttHbb-fix-00-11'],['ttHbb-fix-00']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as ttHbb"], ["mixed data as ttHbb"]]
    colorList = [[619], [419]]
    dofill = [True,True]
    isMC = True
    sf = [[0.00007621],[0.00007621]]
    oname = 'comp_ttHbkgttH1100_afterBDT'
    headerOpt = "    "

elif which == 32: 
    samples = [['ggH-fix-00-11'],['ggH-fix-00']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as ggHbb"], ["mixed data as ggHbb"]]
    colorList = [[613], [602]]
    dofill = [True,True]
    isMC = True
    sf = [[0.002879],[0.002879]]
    oname = 'comp_ggHbkgggH1100_afterBDT'
    headerOpt = "    "

elif which == 33: 
    samples = [['vbfH-fix-00-11'],['vbfH-fix-00']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as vbfHbb"], ["mixed data as vbfHbb"]]
    colorList = [[613], [434]]
    dofill = [True,True]
    isMC = True
    sf = [[0.000720],[0.000720]]
    oname = 'comp_vbfHbkgvbfH1100_afterBDT'
    headerOpt = "    "

elif which == 34: 
    samples = [['ZH-fix-00-11'],['ZH-fix-00']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as ZHbbqq"], ["mixed data as ZHbbqq"]]
    colorList = [[613], [398]]
    dofill = [True,True]
    isMC = True
    sf = [[0.0007665],[0.0007665]]
    oname = 'comp_ZHbkgZH1100_afterBDT'
    headerOpt = "    "

elif which == 35: 
    samples = [['QCD-fix-fix'],['QCD-fix']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as QCD"], ["mixed data as QCD"]]
    colorList = [[613,613,613,613,613,613,613], [603,603,603,603,603,603,603]]
    dofill = [True,False]
    isMC = True
    sf = [[17.635231, 3.476259, 0.509821, 0.089584, 0.046491, 0.005935, 0.002410,],[17.635231, 3.476259, 0.509821, 0.089584, 0.046491, 0.005935, 0.002410,]]
    oname = 'comp_qcdBkgqcd1100_afterBDT'
    headerOpt = "    "

elif which == 300:
    samples = [['QCD-fix','TT-fix-00','ttHbb-fix-00','ZH-fix-00','vbfH-fix-00','ggH-fix-00'],['bkg']] #data always  second 
    fractions = ['','appl']
    regions = ['','']
    legList = [["mixed data as QCD","mixed data as QCD","mixed data as QCD","mixed data as QCD","mixed data as QCD","mixed data as QCD","mixed data as QCD","mixed data as tt","mixed data as ttH","mixed data as ZH","mixed data as vbfHbb","mixed data as ggHbb"], ["mixed data"]] #debug!!! 
    colorList = [[425,425,425,425,425,425,425,634,419,398,434,613], [603]]
    dofill = [True,False]
    isMC = True
    sf = [[17.635231*35.9, 3.476259*35.9, 0.509821*35.9, 0.089584*35.9, 0.046491*35.9, 0.005935*35.9, 0.002410*35.9, 0.01077*35.9, 0.00007621*35.9, 0.0007665*35.9, 0.000720*35.9, 0.002879*35.9],[0.25]]
    oname = 'comp_allBkgBkg_afterBDT'
    headerOpt = "    appl"

elif which == 301: 
    samples = [['vbfH-fix-00-11','ggH-fix-00-11','ZH-fix-00-11','ttHbb-fix-00-11','TT-fix-00-11',],['bkg']] #data always  second
    fractions = ['','appl']
    regions = ['','']
    legList = [["re-mixed data as vbfHbb","re-mixed data as ggHbb","re-mixed data as ZH","re-mixed data as ttH","re-mixed data as tt"], ["mixed data"]] #mixed data
    colorList = [[613,434,398,419,634], [603]]
    dofill = [True,False]
    isMC = True
    sf = [[0.002879*35.9*0.96, 0.000720*35.9*0.96, 0.0007665*35.9*0.96, 0.00007621*35.9*0.96, 0.01077*35.9*0.96],[0.25]]
    oname = 'comp_minBkgBkg11_afterBDT'
    headerOpt = "    appl"

elif which == 302: 
    samples = [['vbfH-fix-00-11','ggH-fix-00-11','ZH-fix-00-11','ttHbb-fix-00-11','TT-fix-00-11'],['vbfHbb','ggHbb','ZHbbqq','ttHbb','TT']] #data always  second
    fractions = ['','']
    regions = ['','']
    legList = [["re-mixed data as vbfHbb","re-mixed data as ggHbb","re-mixed data as ZH","re-mixed data as ttH","re-mixed data as tt"], ["MC samples"]] #mixed data
    colorList = [[613,434,398,419,634], [603, 603,603,603,603,603]]
    dofill = [True,False]
    isMC = True
    sf = [[0.002879*35.9*0.96*4, 0.000720*35.9*0.96*4, 0.0007665*35.9*0.96*4, 0.00007621*35.9*0.96*4, 0.01077*35.9*0.96*4],[0.002879*35.9*0.96*4, 0.000720*35.9*0.96*4, 0.0007665*35.9*0.96*4, 0.00007621*35.9*0.96*4, 0.01077*35.9*0.96*4]]
    oname = 'comp_minBkgminBkg11_afterBDT'
    headerOpt = "    "  

elif which == 137:
    samples = [['sig'], ['bkg']]
    fractions = ['train','train']
    regions = ['','']
    weights = [[0.010760],[]]
    legList = [['tt'], ["bkg (mixed data)"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttBkg_afterBDT'
    headerOpt = "train"
elif which == 138:
    samples = [['sig'], ['bkg']]
    fractions = ['test','test']
    regions = ['','']
    weights = [[0.010760],[]]
    legList = [['tt'], ["bkg (mixed data)"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttBkg_afterBDT'
    headerOpt = "test"
elif which == 490:
    samples = [['bkg'], ['bkg']]
    fractions = ['appl','appl_ttbdt']
    regions = ['','']
    weights = [[1],[1]]
    legList = [["bkg (mixed data) appl"], ["bkg (mixed data) appl tt bdt cut"]]
    colorList = [[604], [430]]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttbdt_bkgdiff_afterBDT'
    headerOpt = ""
elif which == 491:
    samples = [['data'], ['data']]
    fractions = ['','ttbdt']
    regions = ['','']
    weights = [[1],[1]]
    legList = [["data"], ["data ttbdt cut"]]
    colorList = [[604], [430]]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttbdt_datadiff_afterBDT'
    headerOpt = ""

elif which == 500: # -l 0 !!
    samples = [['sig'],['sig']] #data always  second
    fractions = ['appl','appl_ttbdt']
    regions = ['',''] #    regions = ['cr','cr']
    legList = [["SM"], ["HH4b SM ttbdt cut"]]
    colorList = [[434], [632]]
    dofill = [True,True]
    isMC = True
    sf = [[(33.53*0.5824*0.5824/(4172119.0*0.2))],[(33.53*0.5824*0.5824/(4172119.0*0.2))]]
    oname = 'comp_sig_ttbdt_afterBDT'
    headerOpt = "    "
elif which == 501:
    samples = [['bkg'], ['data']]
    fractions = ['appl_ttbdt','ttbdt']
    regions = ['','']
    weights = [[1],[4]]
    legList = [["bkg (mixed data) appl"], ["data"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttbdt_bkgappl_data_afterBDT'
    headerOpt = "ttbar veto"
elif which == 502:
    samples = [['bkg'], ['data']]
    fractions = ['appl_ttbdt','ttbdt']
    regions = ['','']
    weights = [[1*739516.0/304186.0],[4*739516.0/304186.0]]
    legList = [["bkg (mixed data) appl"], ["data"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttbdt_bkgappl_data_afterBDT'
    headerOpt = "ttbar veto"
elif which == 511:
    samples = [['bkg'], ['data']]
    fractions = ['appl','']
    regions = ['msttbdt','msttbdt']
    weights = [[1],[4]]
    legList = [["bkg (mixed data) appl"], ["data"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_ttbdt_bkgappl_data_afterBDT'
    headerOpt = "ttbar veto"

elif which == 583:
    samples = [['bkg'], ['data']]
    fractions = ['appl','']
    regions = ['','']
    weights = [[1],[4]]
    legList = [["bkg (mixed data) appl"], ["data"]]
    colorList = [604, 430]
    dofill = [True,True]
    isMC = True
    oname = 'comp_bkgappl_data_afterBDT'
    headerOpt = ""
else: 
    print "ERROR: wrong '-w' argument"
    exit()
###############

if args.defaultCol: colors = [0,0]
else: colors = colorList

for n, w in enumerate(weights):
    if len(w)==0: print "## WARNING: weight[{}] is empty".format(n)

snames1 = []
for s in samples[0]:
    if not s in samlists: 
        if not s in samples: 
            snames1.append(s)
        else:
            snames1.append(samples[s]['sam_name'])    
    else: 
        snames1.extend(samlists[s])
#print snames1

snames2 = []
for s in samples[1]:
    if not s in samlists: 
        if not s in samples: 
            snames2.append(s)
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
if args.doNorm: oDir = oDir+"_norm"
if args.clrebin > 1: 
    oDir += "_rebin_" + str(args.clrebin)
oDir = oDir+"/"
if not os.path.exists(oDir): os.mkdir(oDir)
oDir += option #keep the second sample options
if not os.path.exists(oDir): os.mkdir(oDir)

#----------------------------------
for n, h in enumerate(histList):
    hOpt = hist_opt[h]
    if h == 'classifier': 
        h+='-'+args.bdt
    hs1 = UtilsDraw.getHistos_bdt(h, filename, plotDirs1, intLumi_fb, doNormToLumi[0], weights[0], sf[0])
    hs2 = UtilsDraw.getHistos_bdt(h, filename, plotDirs2, intLumi_fb, doNormToLumi[1], weights[1], sf[1])

    if drawH2:
        UtilsDraw.drawH2(hs1, hs2, hist_opt["h2_bdt"], snames1, args.clrebin, oDir, legList)
    elif getVar: # variance check
        UtilsDraw.drawBinVar(hs1, snames1, legList[0], hOpt, oDir, args.clrebin, headerOpt, isMC)
    elif getChi: # chi square
        UtilsDraw.drawChiSquare(hs1, snames1, legList[0], hs2, hOpt, oDir, xbmin, headerOpt, isMC, labels)
    else: 
        if hs1 and hs2:
            n1,n1err,n2,n2err = UtilsDraw.drawH1(hs1, snames1, legList[0], hs2, snames2, legList[1], 
                         hOpt, args.plotResidual, args.doNorm, oDir, colors, dofill, args.clrebin, headerOpt, isMC)
        #if n2: 
        #   print "### n1/n2 numEvents: {} +- {} ###".format(n1/n2, UtilsDraw.getRelErr(n1,n1err,n2,n2err)*n1/n2) 
        #   print "### n1: {} +- {} ###".format(n1,n1err) 
        #   print "### n2: {} +- {} ### \n".format(n2,n2err) 

