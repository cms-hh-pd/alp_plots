
import json
import os
import math
from glob import glob

# ROOT imports
from ROOT import TChain, TH1D, TH2D, TFile, vector, TCanvas, TLatex, TLegend, THStack, gStyle

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

def getWeightedHistos(hist, filelist, plotDir, lumi, useWeight):
    hlist = []    
    for f in filelist:  #debug - not efficient to loop on file
        w = 1
        tf = TFile(f)
        if not tf: 
            print "WARNING: files do not exist"  
    if useWeight:
        if "Run" in f: #data
            w = 1
        else:         
            if(tf.Get("h_w_oneInvFb")):
                h = tf.Get("h_w_oneInvFb")
                w = h.GetBinContent(1)
                w *= lumi;
            else:
                print "WARNING: weight not found in {}".format(f)
    
    if(tf.Get(plotDir+"/"+hist)):
        h = tf.Get(plotDir+"/"+hist)
        h.Scale(w)
        hlist.append(h)
    else:
        print "WARNING: hist {} not found in {}".format(hist,f)

    return hlist
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

def setYmaxStack_D(hD, h1, h2, herr, c, hname):
    if hD.GetMaximum() > h1.GetMaximum() and hD.GetMaximum() > h2.GetMaximum(): ymax = hD.GetMaximum()*c
    elif h1.GetMaximum() > h2.GetMaximum(): ymax = h1.GetMaximum()*c 
    else: ymax = h2.GetMaximum()*c 

    hD.SetMaximum(ymax)
    h1.SetMaximum(ymax)
    h2.SetMaximum(ymax)
    herr.SetMaximum(ymax)
    if(hname == 'h_nevts'):
        hD.SetMinimum(0.)
        h1.SetMinimum(0.)
        h2.SetMinimum(0.)
        herr.SetMinimum(0.)
#------------

def setYmax(hs, c, hname):
    ymax = 0.
    for h in hs:
        if (h.GetMaximum() > ymax): ymax = (h.GetMaximum()*c) 
    for h in hs:
        h.SetMaximum(ymax)
#------------

def getScale(hlist1, hlist2):
    hsInt = 0
    norm = 0
    for h in hlist1: 
        hsInt += h.Integral()
    for h in hlist2: 
        if isinstance(h,int):
           norm = h
           break
        else: norm += h.Integral()
    if  hsInt: scale = norm/hsInt
    else: scale = 1.
    return scale
#------------

def getStackH(histos, hsOpt, samples, rebin,  color, scale, fill): #hsOpt['rebin']
    if color: col = color
    else: col = samOpt['fillcolor']

    herr = histos[0].Clone("hs_error")  
    herr.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr.Reset()
    herr.Rebin(rebin)
    herr.GetXaxis().SetTitle(hsOpt['xname'])
    herr.GetYaxis().SetTitle(hsOpt['yname'])
    herr.SetFillStyle(3003)
    herr.SetFillColor(col)
    herr.SetLineColor(col)
    herr.SetLineWidth(2)         
    herr.SetMarkerSize(0)
    herr.SetMarkerColor(col)
    herr.SetMinimum(0.)

    hs   = THStack("hs","")
    for i, h in enumerate(histos):
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
#        samOpt = sam_opt[samples[i]]       
        #print samOpt['sam_name']
        h.Rebin(rebin)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        if fill: 
            h.SetFillColorAlpha(col,0.2)
            h.SetFillStyle(1) #samOpt['fillstyle']
        if i==len(histos)-1 :
            h.SetLineStyle(1) #samOpt['linestyle']
            h.SetLineWidth(2)  #samOpt['linewidth']
            h.SetLineColor(col)
            if not fill: h.SetMarkerSize(0.8)
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(col,0.)
        hs.Add(h)
        herr.Add(h)
    return hs, herr

##
# DRAWING FUNCTIONS
#################
def drawH1Stack_data(hdata, hmc, hsOpt, samData, samMc, ratio, norm, oDir):

    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

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
    hD.SetMinimum(0.)
    hD.GetXaxis().SetTitle(hsOpt['xname'])
    hD.GetYaxis().SetTitle(hsOpt['yname'])
    hD.SetLineColor(samOpt['linecolor'])
    hD.SetLineStyle(samOpt['linestyle'])
    hD.SetLineWidth(samOpt['linewidth'])  
    legend.AddEntry(hD, samOpt['label'])
   #end Data

    for i, h in enumerate(hmc): #fix range befor compute integral
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)

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
    hs.Draw("same")
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

def drawH1Stack_sig(hsig, hbkg, hsOpt, samSig, samBkg, ratio, norm, oDir, kfactor):

    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

   #plot signal histos 
    for i, h in enumerate(hsig):
        samOpt = sam_opt[samSig[i]]
        h.Rebin(hsOpt['rebin'])
        if kfactor>1 and not norm: 
            h.Scale(kfactor)
            legend.AddEntry(h, samOpt['label']+" * "+str(kfactor))
        else: legend.AddEntry(h, samOpt['label'])
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.1)
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.GetXaxis().SetTitle(hsOpt['xname'])
        h.GetYaxis().SetTitle(hsOpt['yname'])
        h.SetLineColor(samOpt['linecolor'])
        h.SetLineStyle(samOpt['linestyle'])
        h.SetLineWidth(samOpt['linewidth'])  
        if i==0 : hsigInt = h.Integral()
   #end signal

    for i, h in enumerate(hbkg): #fix range befor compute integral
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

   #mc histos (stack and stat error)
    if(norm): scale = getScale(hbkg, hsigInt) #normalize MC to signal[0]
    else: scale = 1.

    herr = hbkg[0].Clone("h_bkgSum")
    herr.Reset()
    herr.SetMinimum(0.)
    herr.Rebin(hsOpt['rebin'])
    herr.SetFillStyle(3003)
    herr.SetFillColor(1)
    herr.SetLineColor(1)
    herr.SetMarkerSize(0)

    hs   = THStack("hs_mc","")
    for i, h in enumerate(hbkg):
        if(norm): h.Scale(scale)
        samOpt = sam_opt[samBkg[i]]       
        h.Rebin(hsOpt['rebin'])
        h.SetMinimum(0.)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.1)
        h.SetFillColorAlpha(samOpt['fillcolor'],0.2)
        h.SetFillStyle(samOpt['fillstyle'])        
        h.SetLineStyle(samOpt['linestyle'])
        if(i==len(hbkg)-1 or samOpt['order'] != sam_opt[samBkg[i+1]]['order']):
            h.SetLineWidth(samOpt['linewidth'])         
            h.SetLineColor(samOpt['linecolor'])
            legend.AddEntry(h, samOpt['label'])
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(samOpt['fillcolor'],0.)
        hs.Add(h)
        herr.Add(h)
    legend.AddEntry(herr, "MC Stat");
    #end mc

    setYmaxStack(hsig[0], hs, herr, 1.1, hsOpt['hname'])

    hsig[0].Draw("HIST") #needed before hstack

    drawCMS(12.9, "")
    legend.Draw("same")
    hs.Draw("HISTsame") #nostack
    herr.Draw("E2same")
    for i, h in enumerate(hsig):
        h.Draw("HISTEsame")

    c1.Update()
    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root")  

    return True
#------------

def drawEffH(histos, leg, fld, snames1, oDir, colors):
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", "eff", 800, 800)

    for i, h in enumerate(histos):
        if i == 0: continue
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.9)
        #h.GetXaxis().SetRangeUser(0,1)
        h.SetMinimum(0.)
        h.GetXaxis().SetTitle(leg)
        h.GetYaxis().SetTitle("acc x eff")
        h.SetLineColor(colors[i])
        h.SetLineStyle(1)
        h.SetLineWidth(2)
        if i==1 : h.Draw("HIST")
        else: h.Draw("HISTsame")

    c1.Update()
    c1.SaveAs(oDir+"/"+"eff.pdf")
    c1.SaveAs(oDir+"/"+"eff.png")
#    c1.SaveAs(oDir+"/"+leg+".root")

#------------

def drawH1Stack(hdata, hsig, hbkg, hsOpt, samData, samSig, samBkg, ratio, norm, oDir, kfactor):

    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

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
    hD.SetMinimum(0.)
    hD.GetXaxis().SetTitle(hsOpt['xname'])
    hD.GetYaxis().SetTitle(hsOpt['yname'])
    hD.SetLineColor(samOpt['linecolor'])
    hD.SetLineStyle(samOpt['linestyle'])
    hD.SetLineWidth(samOpt['linewidth'])  
    legend.AddEntry(hD, samOpt['label'])
   #end Data

    for i, h in enumerate(hbkg): #fix range befor compute integral
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

   #mc histos (stack and stat error)
    if(norm): scale = getScale(hbkg, hD.Integral()) #normalize MC to data
    else: scale = 1.

    herr = hbkg[0].Clone("h_bkgSum")
    herr.Reset()
    herr.SetMinimum(0.)
    herr.Rebin(hsOpt['rebin'])
    herr.SetFillStyle(3003)
    herr.SetFillColor(1)
    herr.SetLineColor(1)
    herr.SetMarkerSize(0)

    hs   = THStack("hs_mc","")
    for i, h in enumerate(hbkg):
        if(norm): h.Scale(scale)
        samOpt = sam_opt[samBkg[i]]       
        h.Rebin(hsOpt['rebin'])
        h.SetMinimum(0.)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.1)
        h.SetFillColorAlpha(samOpt['fillcolor'],0.2)
        h.SetFillStyle(samOpt['fillstyle'])        
        h.SetLineStyle(samOpt['linestyle'])
        if(i==len(hbkg)-1 or samOpt['order'] != sam_opt[samBkg[i+1]]['order']):
            h.SetLineWidth(samOpt['linewidth'])         
            h.SetLineColor(samOpt['linecolor'])
            legend.AddEntry(h, samOpt['label'])
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(samOpt['fillcolor'],0.)
        hs.Add(h)
        herr.Add(h)
    legend.AddEntry(herr, "MC Stat");
    #end mc
      
    #plot signal histos 
    for i, h in enumerate(hsig):
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        if(norm): h.Scale(hD.Integral()/h.Integral())
        samOpt = sam_opt[samSig[i]]
        h.Rebin(hsOpt['rebin'])
        if kfactor>1 and not norm:
            h.Scale(kfactor)
            legend.AddEntry(h, samOpt['label']+" * "+str(kfactor))
        else: legend.AddEntry(h, samOpt['label'])
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.1)
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.GetXaxis().SetTitle(hsOpt['xname'])
        h.GetYaxis().SetTitle(hsOpt['yname'])
        h.SetLineColor(samOpt['linecolor'])
        h.SetLineStyle(samOpt['linestyle'])
        h.SetLineWidth(samOpt['linewidth'])
        h.SetMinimum(0.)
    #end signal   

    setYmaxStack_D(hD, hsig[0], hs, herr, 1.1, hsOpt['hname']) #debug

    hD.Draw("HIST") #needed befor hstack
    drawCMS(12.9, "")
    legend.Draw("same")
    hs.Draw("HISTsame") #nostack
    herr.Draw("E2same")
    for i, h in enumerate(hsig):
        h.Draw("HISTEsame")

    hD.Draw("HISTEsame") #last data
    c1.Update()
    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root")  

    return True
#------------

def drawH1(hlist1, legstack1, hlist2, legstack2, hsOpt, sam1, sam2, ratio, norm, oDir, colors, dofill):
    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    ymax = 0.
    if(norm): scale = getScale(hlist1, hlist2)
    else: scale = 1.
    hs1, herr1 =  getStackH(hlist1, hsOpt, sam1, hsOpt['rebin'], colors[0], scale, dofill[0])
    legend.AddEntry(hlist1[len(hlist1)-1], legstack1)
    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.1
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.1

    if(norm): scale = getScale(hlist2, hlist2)
    hs2, herr2 =  getStackH(hlist2, hsOpt, sam2, hsOpt['rebin'], colors[1], scale, dofill[1])
    legend.AddEntry(hlist2[len(hlist2)-1], legstack2)
    if hs2.GetMaximum() > ymax: ymax = hs2.GetMaximum()*1.1
    if herr2.GetMaximum() > ymax: ymax = herr2.GetMaximum()*1.1

   #debug -- needed before drawing hs
    herr1.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr1.SetMinimum(0.)
    herr1.SetMaximum(ymax)
    herr1.Draw("E")
   #--
    legend.Draw("same")
    drawCMS(-1, "")

    hs1.SetMaximum(ymax)
    herr1.SetMaximum(ymax)
    hs1.Draw("HISTsame")
    herr1.Draw("Esame")
    hs2.SetMaximum(ymax)
    herr2.SetMaximum(ymax)
    if dofill[1]:
        hs2.Draw("HISTsame")
        herr2.Draw("Esame")
    else:
        hs2.Draw("Esame")
        herr2.Draw("E2same")

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root")  

    return True
#------------

def drawH1comp(hmc, hsOpt, samMc, legList, ratio, norm, oDir, colors):
    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)

    scale = 1.
    for i, h in enumerate(hmc):
        h.Rebin(hsOpt['rebin'])
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        if(norm): h.Scale(1/h.Integral())
        samOpt = sam_opt[samMc[i]]
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.1)
        #h.SetFillColorAlpha(samOpt['fillcolor'],0.2)
        #h.SetFillStyle(samOpt['fillstyle'])        
        if colors: h.SetLineColor(colors[i])
        else : h.SetLineColor(samOpt['linecolor'])
        h.SetLineStyle(samOpt['linestyle'])
        h.SetLineWidth(samOpt['linewidth'])
        h.GetXaxis().SetTitle(hsOpt['xname'])
        h.GetYaxis().SetTitle(hsOpt['yname'])
        leg = samOpt['label']+", "+legList[i]
        legend.AddEntry(h, leg)
        if i==0: h.Draw("HISTE")
        else: h.Draw("HISTEsame")
    #end mc

    setYmax(hmc, 1.1, hsOpt['hname'])
    legend.Draw("same")
    drawCMS(12.9, "")
    c1.Update()

    #debug
    nevOpt1= 0
    nevOpt2= 0
    if hsOpt['hname']=='h_nevts': 
        nevOpt1 = hmc[0].GetBinContent(1)
        nevOpt2 = hmc[1].GetBinContent(1)

    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root")

    return [nevOpt1,nevOpt2]
#------------


def drawH2(hs, hsOpt, sname, oDir):
    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    for i, h2 in enumerate(hs):
        name = hsOpt['hname'] + "_" + sname[i]
        print name
        c2 = TCanvas(name, name, 800, 800)       #debug
        h2.Rebin2D(hsOpt['rebin'], hsOpt['rebin'])
        h2.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h2.GetYaxis().SetRangeUser(hsOpt['ymin'],hsOpt['ymax'])
        h2.GetXaxis().SetTitle(hsOpt['xname'])
        h2.GetYaxis().SetTitle(hsOpt['yname'])

        h2.GetXaxis().SetLabelFont(43)
        h2.GetXaxis().SetLabelSize(20)
        h2.GetXaxis().SetTitleFont(43)
        h2.GetXaxis().SetTitleOffset(1.)
        h2.GetXaxis().SetTitleSize(23) 
        h2.GetYaxis().SetLabelFont(43)
        h2.GetYaxis().SetLabelSize(20)
        h2.GetYaxis().SetTitleFont(43)
        h2.GetYaxis().SetTitleOffset(1.2)
        h2.GetYaxis().SetTitleSize(23)    
 
        h2.Draw("COLZ")
        c2.Update() 
        palette = h2.FindObject("palette")
        #palette.GetAxis().SetLabelSize(0.005); #debug
        #palette.GetAxis().SetTitleSize(0.005);
        drawCMS(12.9, "")
        c2.Update() 

        c2.SaveAs(oDir+"/"+name+".pdf")
        c2.SaveAs(oDir+"/"+name+".png")            
        c2.SaveAs(oDir+"/"+name+".root")  

    return True
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
    else: latex.DrawLatex(0.90, 0.94, "simulation (13 TeV)")
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    latex.SetTextSize(0.03 if len(text)>0 else 0.035)
    if not onTop: latex.DrawLatex(0.15, 0.87 if len(text)>0 else 0.855, "CMS")
    else: latex.DrawLatex(0.20, 0.99, "CMS")
#------------

def setLegend(doRight, doTop):
    leg = TLegend(0.55,0.70,0.90,0.90)
    leg.SetTextSize(0.03335)
    return leg
#------------

