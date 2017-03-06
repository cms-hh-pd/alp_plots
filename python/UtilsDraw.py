import json
import os
import math
from glob import glob

# ROOT imports
from ROOT import TChain, TH1D, TH2D, TFile, vector, TCanvas, TLatex, TLine, TLegend, THStack, gStyle
from rootpy.plotting import Hist, Hist2D

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

def getHistos_bdt(hist, filename, plotDir):
    hlist = []   
    hname = hist+"_"+plotDir
    tf = TFile(filename)
    if not tf: 
        print "WARNING: files do not exist"  
    
    if(tf.Get(plotDir+"/"+hname)):
        h = tf.Get(plotDir+"/"+hname)
        hlist.append(h)
    else:
        print "WARNING: hist {} not found in {}".format(hist,tf)

    return hlist
#------------

def getHistos(hist, filelist, plotDir, lumi, normtolumi):
    hlist = []    
    for f in filelist:  #debug - not efficient to loop on file
        norm = 1
        tf = TFile(f)
        if not tf: 
            print "WARNING: files do not exist"  
        if normtolumi:
            if "Run" in f: #data
                norm = 1
            else:         
                if(tf.Get("h_w_oneInvFb")):
                    h = tf.Get("h_w_oneInvFb")
                    norm = h.GetBinContent(1)
                    norm *= lumi;
                else:
                    print "WARNING: 'h_w_oneInvFb' not found in {}".format(tf)
    
        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            h.Scale(norm)
            hlist.append(h)
        else:
            print "WARNING: hist {} not found in {}".format(hist,tf)

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

def getScale(hlist1, hlist2): #h2/h1
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

def getStackH(histos, hsOpt, rebin, snames, color, scale, fill):

    herr = histos[0].Clone("hs_error")  
    herr.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr.Reset()
    herr.Rebin(rebin)
    herr.GetXaxis().SetTitle(hsOpt['xname'])
    herr.GetYaxis().SetTitle(hsOpt['yname'])
    herr.SetFillStyle(3003)
#    herr.SetFillColor(col)
 #   herr.SetLineColor(col)
    herr.SetLineWidth(2)         
    herr.SetMarkerSize(0)
  #  herr.SetMarkerColor(col)
    herr.SetMinimum(0.)

    hs   = THStack("hs","")
    for i, h in enumerate(histos):
        if color: col = color
        else: col = sam_opt[snames[i]]['fillcolor']
        #print sam_opt[snames[i]]['sam_name']

        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
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
        if i==0: h_  = h.Clone("h_")
        else: h_.Add(h)
        hs.Add(h)
        herr.Add(h)
    return hs, herr, h_

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

def drawH1(hlist1, snames1, legstack1, hlist2, snames2, legstack2, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt):
    gStyle.SetOptStat(False)
    legend = setLegend(1,1)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    ymax = 0.
    if(norm): scale1 = getScale(hlist1, hlist2)
    else: scale1 = 1.
    #print "scale1", scale1
    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0])
    legend.AddEntry(hlist1[len(hlist1)-1], legstack1)
    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.1
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.1

    if(norm): scale2 = getScale(hlist2, hlist2)
    else: scale2 = 1.
    #print "scale2", scale2
    hs2, herr2, h2 =  getStackH(hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1])
    legend.AddEntry(hlist2[len(hlist2)-1], legstack2)
    if hs2.GetMaximum() > ymax: ymax = hs2.GetMaximum()*1.1
    if herr2.GetMaximum() > ymax: ymax = herr2.GetMaximum()*1.1

    #print "h1Int ",  h1.Integral()
    #print h1.GetBinContent(1), h1.GetBinError(1)
    #print h2.GetBinContent(1), h2.GetBinError(1)
    #print herr1.GetBinContent(1), herr1.GetBinError(1)

   #debug -- needed before drawing hs
    herr1.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr1.SetMinimum(0.)
    herr1.SetMaximum(ymax)
    herr1.Draw("E")
   #--
    legend.Draw("same")
    drawCMS(-1, headerOpt)

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

    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0
    if hsOpt['hname']=='h_nevts': 
        nev1 = herr1.GetBinContent(1)
        nev2 = herr2.GetBinContent(1)
        nev1err = herr1.GetBinError(1)
        nev2err = herr2.GetBinError(1)

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
    #c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    if residuals: # data as h2!!!
        if residuals>1:
            c2 = TCanvas("c2", "r"+hsOpt['hname'], 800, 800)    
            c2.Divide(1,2)
            c2.cd(1)
        else:
            c2 = TCanvas("c2", "r"+hsOpt['hname'], 800, 400)    
        norm_factor = scale1       
        hdiff = h2.Clone("h_diff")
        hdiff.Add(h1,-1.)   
        hdiff_e = h2.Clone("h_diff_err")
        hdiff_e.Add(h1,norm_factor**2)
        for i in range(0, hdiff_e.GetXaxis().GetNbins()): #improve
            hdiff_e.SetBinContent(i, math.sqrt(hdiff_e.GetBinContent(i)))
            hdiff_e.SetBinError(i,1.) #DEBUG!
        hres = Hist(10,0,1, name="")
        hres = hdiff.Clone("h_residual")
        hres.Divide(hdiff_e)
        hres.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        hres.SetMarkerStyle(8)
        hres.SetMarkerSize(0.8)
        hres.SetMarkerColor(1)
        hres.SetLineColor(1)
        hres.GetXaxis().SetTitle(hsOpt['xname'])
        hres.GetYaxis().SetTitle('residuals (sigma units)')
        hres.Draw("E X0")
        line = TLine(hsOpt['xmin'],0.,hsOpt['xmax'],0.);
        line.Draw()
        if residuals>1: #draw also pull with fit
            c2.cd(2)
            gStyle.SetOptFit(1)
            res_a = []
            for i in range(0, hres.GetXaxis().GetNbins()): #improve
                if (not hres.IsBinOverflow(i)) and (math.fabs(hres.GetBinContent(i)) != 0):
                    res_a.append(hres.GetBinContent(i))
            res_pull = Hist(50, -5., 5, name = "h_res_pull")
            res_pull.GetXaxis().SetTitle("residuals (sigma units)")
            for v in res_a: res_pull.fill(v)
            res_pull.Fit("gaus", "ILL")
            res_pull.Draw("E X0")

        c2.Update()    
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.pdf")
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.png")            
        #c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.root")   

    return [nev1,nev1err,nev2,nev2err]
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
def drawCMS(lumi, text, onTop=False ):
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
    if not onTop: 
        latex.DrawLatex(0.15, 0.855, "CMS   "+text)
    else: 
        latex.DrawLatex(0.15, 0.88, "CMS   "+text)
#------------

def setLegend(doRight, doTop):
    leg = TLegend(0.55,0.70,0.90,0.90)
    leg.SetTextSize(0.03335)
    return leg
#------------

