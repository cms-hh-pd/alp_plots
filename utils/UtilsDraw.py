
import json
import os
import math
from glob import glob

# ROOT imports
from ROOT import TChain, TH1D, TFile, vector, TCanvas, TLatex, TLegend, THStack, gStyle

from Analysis.alp_analysis.alpSamplesOptions  import sam_opt

##
# UTILS
#################
def getNames(samlist):
    snames = []
    for s in samlist:
        snames.extend(samlists[s]) 
    return snames
#------------

def getFiles(samlist):
    files = []
    samNames = getNames(samlist)
    return files
#------------

def getRelErr(a,erra,b,errb):
    return math.sqrt(math.pow(erra/a,2)+math.pow(errb/b,2))
#------------

def getWeightedHistos(hist, filelist, plotDir, lumi):
    hs = []    
    for f in filelist:  #debug - not efficient to loop on file
        w = 1
        tf = TFile(f)
        if not tf: 
            print "WARNING: files do not exist"

        if "Run" in f: #data
            w = 1
        else:         
            if(tf.Get("h_w_oneInvFb")):
                h = tf.Get("h_w_oneInvFb")
                w = h.GetBinContent(1)
                print f
                w *= lumi;
            else:
                print "WARNING: weight not found in {}".format(f)
        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            h.Scale(w)
            hs.append(h)
        else:
            print "WARNING: hist not found in {}".format(f)
    return hs
#------------

def setYmaxStack(h1, h2, herr, c, hname):
    if (h1.GetMaximum() > h2.GetMaximum()): ymax = (h1.GetMaximum()*c) 
    else: ymax = h2.GetMaximum()*c 
    h1.SetMaximum(ymax)
    h2.SetMaximum(ymax)
    herr.SetMaximum(ymax)
    if(hname == 'h_nevts'):
        h1.SetMinimum(0.)
        h2.SetMinimum(0.)
        herr.SetMinimum(0.)
#------------

def getScale(hlist, norm):
    hsInt = 0
    for h in hlist: 
        hsInt += h.Integral()
    scale = norm/hsInt
    return scale
#------------

##
# DRAWING FUNCTIONS
#################
def drawH1Stack(hdata, hmc, hsOpt, samData, samMc, display, ratio, norm, oDir):

    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800 if ratio else 600)       

   #add data histos 
    hD = hdata[0].Clone("h_data")
    hD.Reset()
    for i, h in enumerate(hdata): 
        hD.Add(h)
    samOpt = sam_opt[samData[0]] #once per data
    hD.Rebin(hsOpt['rebin'])
    hD.SetMarkerStyle(8)
    hD.SetMarkerSize(0.9)
    hD.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    hD.GetXaxis().SetTitle(hsOpt['xname'])
    hD.GetYaxis().SetTitle(hsOpt['yname'])
    hD.SetLineColor(samOpt['linecolor'])
    hD.SetLineStyle(samOpt['linestyle'])
    hD.SetLineWidth(samOpt['linewidth'])  
    legend.AddEntry(hD, samOpt['label'])
   #end Data

    for i, h in enumerate(hmc): #fix range befor compute integral
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

   #mc histos (stack and stat error)
    if(norm): scale = getScale(hmc, hD.Integral())
    else: scale = 1.

    herr = hmc[0].Clone("h_bkgSum")
    herr.Reset()
    herr.Rebin(hsOpt['rebin'])
    herr.SetFillStyle(3003)
    herr.SetFillColor(1)
    herr.SetLineColor(1)
    herr.SetMarkerSize(0)

    hs   = THStack("hs_mc","")
    for i, h in enumerate(hmc):
        if(norm): h.Scale(scale)
        samOpt = sam_opt[samMc[i]]       
        h.Rebin(hsOpt['rebin'])
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.9)
        h.SetFillColorAlpha(samOpt['fillcolor'],0.2)
        h.SetFillStyle(samOpt['fillstyle'])        
        h.SetLineColor(samOpt['linecolor'])
        h.SetLineStyle(samOpt['linestyle'])
        h.SetLineWidth(samOpt['linewidth'])         
        legend.AddEntry(h, samOpt['label'])
        hs.Add(h)
        herr.Add(h)
    legend.AddEntry(herr, "MC Stat");
    #end mc

    setYmaxStack(hD, hs, herr, 1.1, hsOpt['hname'])

    hD.Draw("HIST") # double drawing needed to avoid issues with png
    herr.Draw("E2same")
    hs.Draw("HISTsame")
    hD.Draw("HISTEsame")
    
    legend.Draw("same")
    drawCMS(12.9, "")
    c1.Update()
    
    nevData = 0
    nevMc = 0
    nevDataErr = 0
    nevMcErr = 0
    if hsOpt['hname']=='h_nevts': 
        nevData = hD.GetBinContent(1)
        nevMc = herr.GetBinContent(1)
        nevDataErr = hD.GetBinError(1)
        nevMcErr = herr.GetBinError(1)

    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root")  

    return [nevData,nevDataErr,nevMc,nevMcErr]
#------------

def drawH1(h, hOpt):
   #to be implemented
    return
#------------


##
# DRAWING TOOLS
#################
def drawCMS(lumi, text, onTop=False):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)
    if (type(lumi) is float or type(lumi) is int) and float(lumi) > 0: latex.DrawLatex(0.90, 0.94, "%.1f fb^{-1}  (13 TeV)" % (float(lumi)))
    elif type(lumi) is str: latex.DrawLatex(0.90, 0.94, "%s fb^{-1}  (13 TeV)" % lumi)
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    latex.SetTextSize(0.03 if len(text)>0 else 0.035)
    if not onTop: latex.DrawLatex(0.15, 0.87 if len(text)>0 else 0.855, "CMS")
    else: latex.DrawLatex(0.20, 0.99, "CMS")
#------------

def setLegend(doRight, doTop):
    leg = TLegend(0.55,0.70,0.70,0.90)
    leg.SetTextSize(0.025)
    return leg
#------------

