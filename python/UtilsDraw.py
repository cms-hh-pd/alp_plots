import json
import os
import math
from glob import glob

import numpy as np
# ROOT imports
from ROOT import TChain, TPad, TH1D, TH2D, TFile, vector, TCanvas, TLatex, TLine, TLegend, THStack, gStyle, TGaxis
import ROOT
from rootpy.plotting import Hist, Hist2D
from array import array
from Analysis.alp_analysis.alpSamplesOptions  import sam_opt


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

def getHistos_bdt(hist, filename, plotDirs, lumi, normtolumi, weights, sf):
    hlist = [] 
    
    tf = TFile(filename)
    #tf = TFile("../hh2bbbb_limit//20171120-160644-bm0.root")
    if not tf: 
        print "## WARNING: files do not exist"  
    for i, Dir in enumerate(plotDirs):
        hname = hist+"_"+Dir            
        if(tf.Get(Dir+"/"+hname)):
            norm = 1
            w = 1.
            sf_ = 1.
            if len(weights)>0:
	            if weights[i]>0:
        	        w = weights[i]
            if len(sf)>0:
                if sf[i]>=0:
                    sf_ = sf[i]

            if normtolumi: norm = w*lumi*sf_
            else: norm = w*sf_
            print "scale[{}]: {}".format(i, norm)
            h = tf.Get(Dir+"/"+hname)
            h.Scale(norm)
            hlist.append(h)
        else:
            print "## WARNING: hist {} not found in {}".format(Dir+"/"+hname,tf)

    return hlist
#------------

def getHistos_tdr(hist, filelist, plotDir, lumi, normtolumi, weight):
    hlist = []    
    for i, f in enumerate(filelist):
        w = 1.
        tf = TFile(f)
        if not tf: 
            print "## WARNING: files do not exist"  

        if weight[i]>=0:
   	    w = weight[i]

        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            h.Scale(w)
            hlist.append(h)
            print h.Integral()
        else:
            print "## WARNING: hist {} not found in {}".format(hist,tf)

    return hlist
#------------


def getHistos(hist, filelist, plotDir, lumi, normtolumi, weight, sf):
    hlist = []    
    for i, f in enumerate(filelist):  #debug - not efficient to loop on file
        norm = 1
        w = 1.
        sf_ = 1.
        tf = TFile(f)
        if not tf: 
            print "## WARNING: files do not exist"  

        if "Run" in f:   #data
            if not "mixed" in f:
                print "is Data"
        else:
            if len(weight)>0:
                if weight[i]>=0:
                    w = weight[i]
            # h_w_oneInvFb plot is not maintained - commented out for the time being
            #else:
                #if not "mixed" in f: #only for MC
                    #if(tf.Get("h_w_oneInvFb")):
                    #    h = tf.Get("h_w_oneInvFb")
                    #    w = h.GetBinContent(1)
                    #else:
                    #    print "WARNING: 'h_w_oneInvFb' not found in {}".format(tf)
            if len(sf)>0:
                if sf[i]>=0:
                    sf_ = sf[i]
            if normtolumi: norm = w*lumi*sf_
            else: norm = w*sf_
        print "scale[{}]: {}".format(i, norm)
        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            h.Scale(norm)
            hlist.append(h)
        else:
            print "## WARNING: hist {} not found in {}".format(hist,tf)

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

def getScale(hsOpt, hlist1, hlist2, skip1=-1, skip2=-1): #h2/h1

    for h in hlist1:         
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    for h in hlist2:         
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

    hsInt = 0
    hsSkip = 0
    norm = 0
    for i, h in enumerate(hlist1):
        if i==skip1: 
            hsSkip += h.Integral()
            print 'skip', hsSkip
            continue 
        hsInt += h.Integral()
        #print h.Integral()
    for i, h in enumerate(hlist2): 
        if isinstance(h,int):
           norm = h
           break
        elif i==skip2: 
            continue 
        else: norm += h.Integral()
    if  hsInt: scale = norm/(hsInt+hsSkip)
    else: scale = 1.
    #print hsInt
    return scale
#------------


def getStackH(histos, hsOpt, rebin, snames, color, scale, fill, postfit_file = None):

    if color: col = color[0]
    else: col = sam_opt[snames[0]]['fillcolor']

    if postfit_file:
        myfile = TFile.Open(postfit_file)
        fit = "postfit"        
        bak = myfile.Get("shapes_fit_s").Get("hh_bbbb").Get("total_background")
        sig = myfile.Get("shapes_fit_s").Get("hh_bbbb").Get("total_signal")
        data = myfile.Get("shapes_fit_s").Get("hh_bbbb").Get("data")
        
        if snames[0] == "data":
            for i in range(0,66):
                x, y = array('d', [0]), array('d', [0])
                data.GetPoint(i, x, y)
            histos[0].SetBinContent(0, 0)
            histos[0].SetBinError(0, 0)
        for ibin in range(1, sig.GetNbinsX()+1):
            #To avoid histos going out of scope later            
            for i in range(len(histos)):
                if snames[i] == "bkg":
                    histos[i].SetBinContent(ibin, bak.GetBinContent(ibin))
                    histos[i].SetBinError(ibin, bak.GetBinError(ibin))
                elif snames[i] == "sig":
                    histos[i].SetBinContent(ibin, sig.GetBinContent(ibin))
                    histos[i].SetBinError(ibin, sig.GetBinError(ibin))
                elif snames[i] == "data":
                    x, y = array('d', [0]), array('d', [0])
                    data.GetPoint(ibin-1, x, y)
                    histos[i].SetBinContent(ibin, y[0])
                    histos[i].SetBinError(ibin, data.GetErrorY(ibin))
        scale = 1
    
    
    
    herr = histos[0].Clone("hs_error")
    herr.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr.Reset()
    herr.Rebin(rebin)
    herr.GetXaxis().SetTitle(hsOpt['xname'])
    herr.SetFillStyle(3005)
    herr.SetFillColor(col)
    herr.SetLineColor(922)
    herr.SetLineWidth(0)         
    herr.SetMarkerSize(0)
    herr.SetMarkerColor(922)
    herr.SetMinimum(0.)

    hs   = THStack("hs","")
    for i, h in enumerate(histos):         
        if color: col = color[i]
        else: col = sam_opt[snames[i]]['fillcolor']
        #print sam_opt[snames[i]]['sam_name']
        
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
        h.Rebin(rebin)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        print "h[{}]: {}".format(i, h.Integral())
        if fill: 
            h.SetFillColorAlpha(col,0.2)
            h.SetFillStyle(1)
        if i==len(histos)-1 :
            h.SetLineStyle(1)
            h.SetLineWidth(2)
            h.SetLineColor(col)
            if not fill: 
                h.SetMarkerSize(0.6)
                h.SetMarkerColor(col)
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(col,0.)
        if i==0: h_  = h.Clone("h_")
        else: h_.Add(h)
        hs.Add(h)
        herr.Add(h)
        
    if "sig" in snames:
        i = snames.index("sig")
        sig100 = histos[i].Clone("sig x5")
        sig100.Scale(5)
        sig100.SetLineStyle(2)
        sig100.SetFillStyle(0)
        histos.append(sig100)
        
        
    return hs, herr, h_

# DRAWING FUNCTIONS
#################
def drawChiSquare(hlist, snames, legstack, h2, hsOpt, oDir, xbmin, headerOpt, isMC, labels):  
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    x_data =[]
    chisq_ =[]
    n_sample = 0
    nbins = hlist[0].GetNbinsX()
    #print nbins

    for k in range(0, nbins-xbmin+1):
        x_data.append(0.)

    for i, h in enumerate(h2):
        for b in range(xbmin, nbins+1):
            x_data[b-xbmin] = h.GetBinContent(b)
            print b, x_data[b-xbmin] 
    
    for i, h in enumerate(hlist):            
        n_sample +=1
        chisq_.append(0)
        for b in range(xbmin, nbins+1):
            x = h.GetBinContent(b)       
            #print b, x
            #print b, x_data[b-xbmin] 
            if (x+x_data[b-xbmin]) > 0: chisq_[i] += pow((x_data[b-xbmin]-x),2)/(x+x_data[b-xbmin])
            else: 
                print 'sample data bin {} : null bin content?'.format(b)       

    print "\n", n_sample  

    hchi = (TH1D)("h_chisq", "chi square", n_sample, 0., n_sample) 
    hchi.SetMarkerStyle(8)
    hchi.SetMarkerSize(1.)
    hchi.SetMarkerColor(1)

    for i, h in enumerate(hlist):         
        hchi.SetBinContent(i+1, chisq_[i])
       #hchi.SetBinError(j+1, dDiff)
        #print hchi.GetBinContent(i+1) #, hvar.GetBinError(j+1)       

    x_axis = hchi.GetXaxis()
    for b_n, label in enumerate(labels): 
        x_axis.SetBinLabel(b_n+1, label)        

    hchi.GetYaxis().SetTitle("chi2 data-mixed")
    hchi.Draw("PE")
    drawCMS(35.9, headerOpt)

    c1.Update()    
    c1.SaveAs(oDir+"/"+"bdtChisq_allnn.pdf")
    c1.SaveAs(oDir+"/"+"bdtChisq_allnn.png")
    c1.SaveAs(oDir+"/"+"bdtChisq_allnn.root")
#------------

def drawBinVar(hlist, snames, legstack, hsOpt, oDir, rebin, headerOpt, isMC):  
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       
    
    x_=[]
    xsq_=[]
    xs_mean = []
    xs_sqmean = []
    sum_err = []
    n_sample = 0
    hvar = hlist[0].Clone("hvar")
    hvar.Reset()

    #once for all
    nbins = hlist[0].GetNbinsX()
    #print nbins
    for k in range(0, nbins):
        x_.append(0.)
        xsq_.append(0.)
        sum_err.append(0.)

    for i, h in enumerate(hlist):         
        n_sample +=1
        for b in range(1, nbins+1):
            x = h.GetBinContent(b)
            #if b==nbins: print b, x
            x_[b-1] += x
            xsq_[b-1] += pow(x,2)
    #print "\n", n_sample

    for k in range(0, nbins):
        xs_mean.append(x_[k]/n_sample)
        xs_sqmean.append(xsq_[k]/n_sample)

    for i, h in enumerate(hlist):         
        for b in range(1, nbins+1):
            x = h.GetBinContent(b)
           #sum_err[b-1] +=  (pow(x,2) + pow(xs_mean[b-1],2) + 2*x*xs_mean[b-1])*x            
            sum_err[b-1] += pow((2*x - 2*xs_mean[b-1] -1),2)*x

    for j, m in enumerate(xs_mean):
        var = (xs_sqmean[j] - pow(m,2))
       #dVar = math.sqrt(4./pow(n_sample,2)*sum_err[j])
       #dVar = 2*pow(var,2)/(n_sample-1)
       #print var #, dVar
       #print m, math.sqrt(m)

       #if x>0. : 
       #r = var / m
       #dRat = math.sqrt(pow(dVar/var,2)+pow(math.sqrt(m)/m,2))*r
        diff = var - m        
        dDiff = math.sqrt(1./pow(n_sample,2)*sum_err[j])
       #else: 
        #    print 'null mean - r set to zero'
         #   diff = 0.
          #  dDiff = 0.

        hvar.SetBinContent(j+1, diff)
        hvar.SetBinError(j+1, dDiff)
        #print hvar.GetBinContent(j+1), hvar.GetBinError(j+1)       

    hvar.GetYaxis().SetTitle("mean-Variance")
    hvar.Draw("PE")
    legend = setLegend(1,1)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)
    legend.AddEntry(hvar,"mixed data")
    drawCMS(35.9, headerOpt)
    legend.Draw("same")
    l = TLine(0.,0.,1.,0.);
    l.SetLineStyle(3)
    l.Draw("same")
    c1.Update()    
    c1.SaveAs(oDir+"/"+"bdtVar_nn.pdf")
    c1.SaveAs(oDir+"/"+"bdtVar_nn.png")
    c1.SaveAs(oDir+"/"+"bdtVar_nn.root")
#------------

def drawH1(hlist1, snames1, legstack1, hlist2, snames2, legstack2, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC, fit_results = None, postfit_file = None, bm = 0):
    gStyle.SetOptStat(False)
    gStyle.SetOptTitle(0);
    print "x range: ", hsOpt['xmin'],hsOpt['xmax']
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       
    if residuals == -1 or residuals == -2:
        pad1 = TPad("pad1", "pad1", 0, 0.4, 1, 1.0)
        pad1.SetBottomMargin(0.03) 
        pad1.Draw()             
        pad1.cd()
        #if residuals == -2: pad1.SetLogy()             

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    isNevts=False
    if hsOpt['hname']=="h_nevts": isNevts=True
    ymax = 0.

    if(norm): 
        scale1 = getScale(hsOpt,hlist1, hlist2)
        print "sc_to_norm1: ",scale1
    else: scale1 = 1.
    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0], postfit_file)
    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.15
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.15
    if isNevts:  print "h1Int ",  h1.GetBinContent(1), h1.GetBinError(1)

    if(norm): 
        scale2 = getScale(hsOpt,hlist2, hlist2)
        print "sc_to_norm2: ",scale2
    else: scale2 = 1.
    if scale2 != 1.: print "sc_to_norm2: ",scale2
    hs2, herr2, h2 =  getStackH(hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1], postfit_file)
    print "12", hlist1, hlist2
    #for asd in hlist1:
    #    print asd.Integral()
    #print "int", h1.Integral(), h2.Integral()
    if hs2.GetMaximum() > ymax: ymax = hs2.GetMaximum()*1.15
    if herr2.GetMaximum() > ymax: ymax = herr2.GetMaximum()*1.15
    if "ymax" in hsOpt: ymax = hsOpt["ymax"]
    if isNevts:  print "h2Int ",  h2.GetBinContent(1), h2.GetBinError(1)

    if len(hlist1) == 1 and len(hlist2) == 1:
        ks = hlist1[0].KolmogorovTest(hlist2[0])
        print("KS: ", ks)
        print("Chi2: ", hlist1[0].Chi2Test(hlist2[0], "UU NORM"))
    else:
        kol1 = hlist1[0].Clone()
        kol2 = hlist2[0].Clone()
        maxn = len(hlist1)
        if "sig" in snames1: maxn -= 1
        for ihist in range(1, maxn):
            kol1.Add(hlist1[ihist])
        for ihist in range(1, len(hlist2)):
            kol2.Add(hlist2[ihist])
        ks = kol1.KolmogorovTest(kol2, "NX")
        print("KS: ", ks)        
   #debug -- needed before drawing hs
    herr1.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr1.SetMinimum(0.)
    herr1.SetMaximum(ymax)
    if len(hlist1)>1: 
        herr1.Draw("E2")
        herr1.SetFillColor(922)
    else: herr1.Draw("E")
   #--
    #Legend & headers
    if isMC: drawCMS(-1, headerOpt)
    else: drawCMS(35.9, headerOpt)
    legend = setLegend(1,1)
    legend.AddEntry(hlist2[len(hlist2)-1], legstack2[0]) #debug - one leg for second samplelist
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)   
    latex.DrawLatex(0.5, 0.88, "KS p-val: %.3f" % ks)
    nskip = 0
    match = False 
    for n, sam in enumerate(snames1):
        # to get one legend for all HT bins - to be implemented for other samples         
        if sam.find("QCD")>=0 and match: 
            nskip+=1 
            continue
        if len(legstack1) > n-nskip:
            if sam.find("QCD")>=0: match = True
            legend.AddEntry(hlist1[n], legstack1[n-nskip])            
    if len(hlist1)>1: legend.AddEntry(herr1, 'bkg. unc. (stat.only)')
    legend.Draw("same")
    #-------------

    if(ymax > 1000): TGaxis.SetMaxDigits(3)
    hs1.SetMaximum(ymax)
    herr1.SetMaximum(ymax)
    plotH(hlist1, hs1, herr1, dofill[0])
    hs2.SetMaximum(ymax)
    herr2.SetMaximum(ymax)
    plotH(hlist2, hs2, herr2, dofill[1])
    herr2.Draw("Esameaxis")

    #hlist1[-1].Draw("same hist")

    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0
    if isNevts: 
        nev1 = herr1.GetBinContent(1)
        nev2 = herr2.GetBinContent(1)
        nev1err = herr1.GetBinError(1)
        nev2err = herr2.GetBinError(1)

    if not (residuals == -1 or residuals == -2):
        c1.Update()    
        c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
        c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
        #c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 
    else:
        herr1.GetXaxis().SetLabelSize(0.)

    if residuals==-3: # division --- utility not clear...
        c1.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
        pad2.SetTopMargin(0.)
        pad2.SetBottomMargin(0.2)
        pad2.Draw()
        pad2.cd()
        hrat = h2.Clone("h_div")
        hb = h2.Clone("h_bias")

        for i in range(0, len(bias)):
            hb.SetBinContent(i+1, bias[i])
            #print(hb.GetBinContent(i+1))

        for ibin in range(1, h2.GetNbinsX()+1):
            hrat.SetBinContent(ibin, h1.GetBinContent(ibin)-h2.GetBinContent(ibin) )
            #print(hrat.GetBinContent(ibin))
            if(h2.GetBinContent(ibin)>0): 
                hrat.SetBinError(ibin, h2.GetBinError(ibin)/h2.GetBinContent(ibin) )
            else: 
                hrat.SetBinError(ibin, 0.)

        # MC uncertainy shadow plot
        herr = herr1.Clone("h_err")
        herr.Reset()
        for ibin in range(1, herr1.GetNbinsX()+1):
            if(herr1.GetBinContent(ibin)>0): 
                herr.SetBinContent (ibin, 1.)
                herr.SetBinError   (ibin, herr1.GetBinError(ibin)/herr1.GetBinContent(ibin))
            else: 
                herr.SetBinContent(ibin, 1.)
                herr.SetBinError   (ibin, 0.)

        hrat.SetTitle("")
        hrat.GetXaxis().SetTitleSize(20)
        hrat.GetXaxis().SetTitleFont(43)
        hrat.GetXaxis().SetTitleOffset(4.)
        hrat.GetXaxis().SetLabelFont(43)
        hrat.GetXaxis().SetLabelSize(20)
        hrat.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        minbin = hrat.GetXaxis().GetFirst()
        maxbin = hrat.GetXaxis().GetLast()
        #print minbin, maxbin        
        ymax_ = 1000 #1.5 
        ymax = 800.
        ymin_ = 0.5
        ymin = -200.

       # print 'rb', rb      
        hrat.GetYaxis().SetRangeUser(ymin,ymax)
        hrat.GetYaxis().SetTitleSize(20)
        hrat.GetYaxis().SetTitleFont(43)
        hrat.GetYaxis().SetTitleOffset(1.40)
        hrat.GetYaxis().SetLabelFont(43)
        hrat.GetYaxis().SetLabelSize(18)
        hrat.SetMarkerStyle(8)
        hrat.SetMarkerSize(0.8)
        hrat.SetMarkerColor(1)
        hrat.SetLineColor(1)
        hrat.GetXaxis().SetTitle(hsOpt['xname'])
        hrat.GetYaxis().SetTitle('exp - obs')


        c00 = TCanvas("c0", "", 800, 800)    
        c00.cd()
        hrat.Draw("X0")
        hb.SetMarkerColor(2)
        hb.SetMarkerSize(0.8)
        hb.Draw("same X0")
        c00.SaveAs(oDir+"/"+hsOpt['hname']+"_div2.root")
        c00.SaveAs(oDir+"/"+hsOpt['hname']+"_div2.png")

        l = TLine(hsOpt['xmin'],1.5,hsOpt['xmax'],1.5);
        l0 = TLine(hsOpt['xmin'],1.4,hsOpt['xmax'],1.4);
        l00 = TLine(hsOpt['xmin'],1.3,hsOpt['xmax'],1.3);
        l000 = TLine(hsOpt['xmin'],1.2,hsOpt['xmax'],1.2);
        l1 = TLine(hsOpt['xmin'],1.1,hsOpt['xmax'],1.1);
        l2 = TLine(hsOpt['xmin'],1.,hsOpt['xmax'],1.);
        l3 = TLine(hsOpt['xmin'],0.9,hsOpt['xmax'],0.9);
        l4 = TLine(hsOpt['xmin'],0.8,hsOpt['xmax'],0.8);
        l.SetLineStyle(3)
        l0.SetLineStyle(3)
        l00.SetLineStyle(3)
        l000.SetLineStyle(3)
        l1.SetLineStyle(3)
        l2.SetLineStyle(3)
        l3.SetLineStyle(3)
        l4.SetLineStyle(3)
        l2.Draw("same")

        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_div.pdf")
        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_div.png")            
        #c1.SaveAs(oDir+"/"+hsOpt['hname']+"_div.root") 
        c1.Clear()

    if residuals==-1: # simple ratio -- data as h2!!!
        c1.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0.)
        pad2.SetBottomMargin(0.2)
        pad2.Draw()
        pad2.cd()
        hrat = h2.Clone("h_rat")
        hrat.Divide(h1)
        # consider only data error in the ratio plot
        for ibin in range(1, h2.GetNbinsX()+1):
            #print(h2.GetBinContent(ibin))
            if(h2.GetBinContent(ibin)>0): 
                hrat.SetBinError(ibin, h2.GetBinError(ibin)/h2.GetBinContent(ibin) )
            else: 
                hrat.SetBinError(ibin, 0.)

        # MC uncertainy shadow plot
        herr = herr1.Clone("h_err")
        herr.Reset()
        for ibin in range(1, herr1.GetNbinsX()+1):
            if(herr1.GetBinContent(ibin)>0): 
                herr.SetBinContent (ibin, 1.)
                herr.SetBinError   (ibin, herr1.GetBinError(ibin)/herr1.GetBinContent(ibin))
            else: 
                herr.SetBinContent(ibin, 1.)
                herr.SetBinError   (ibin, 0.)

        hrat.SetTitle("")
        hrat.GetXaxis().SetTitleSize(20)
        hrat.GetXaxis().SetTitleFont(43)
        hrat.GetXaxis().SetTitleOffset(4.)
        hrat.GetXaxis().SetLabelFont(43)
        hrat.GetXaxis().SetLabelSize(20)
        hrat.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        minbin = hrat.GetXaxis().GetFirst()
        maxbin = hrat.GetXaxis().GetLast()
        ymax_ = 1.5
        ymax = 1.
        ymin_ = 0.5
        ymin = 1.
    
        for ibin in range(minbin, maxbin+1):       
            binc = hrat.GetBinContent(ibin) 
            if binc == 0. or (binc is None): 
                continue
            if binc*1.05 > ymax: 
                ymax = binc*1.05
            if binc*0.95 < ymin: 
                ymin = binc*0.95

        hrat.GetYaxis().SetRangeUser(ymin,ymax)
        hrat.GetYaxis().SetTitleSize(20)
        hrat.GetYaxis().SetTitleFont(43)
        hrat.GetYaxis().SetTitleOffset(1.40)
        hrat.GetYaxis().SetLabelFont(43)
        hrat.GetYaxis().SetLabelSize(18)
        hrat.SetMarkerStyle(8)
        hrat.SetMarkerSize(0.8)
        hrat.SetMarkerColor(1)
        hrat.SetLineColor(1)
        hrat.GetXaxis().SetTitle(hsOpt['xname'])
        hrat.GetYaxis().SetTitle('data/bkg')
        hrat.Draw("E X0")
        herr.SetFillColor(430)
        herr.Draw("E2same")

        l = TLine(hsOpt['xmin'],1.5,hsOpt['xmax'],1.5);
        l0 = TLine(hsOpt['xmin'],1.4,hsOpt['xmax'],1.4);
        l00 = TLine(hsOpt['xmin'],1.3,hsOpt['xmax'],1.3);
        l000 = TLine(hsOpt['xmin'],1.2,hsOpt['xmax'],1.2);
        l1 = TLine(hsOpt['xmin'],1.1,hsOpt['xmax'],1.1);
        l2 = TLine(hsOpt['xmin'],1.,hsOpt['xmax'],1.);
        l3 = TLine(hsOpt['xmin'],0.9,hsOpt['xmax'],0.9);
        l4 = TLine(hsOpt['xmin'],0.8,hsOpt['xmax'],0.8);
        l.SetLineStyle(3)
        l0.SetLineStyle(3)
        l00.SetLineStyle(3)
        l000.SetLineStyle(3)
        l1.SetLineStyle(3)
        l2.SetLineStyle(3)
        l3.SetLineStyle(3)
        l4.SetLineStyle(3)
        #l.Draw("same")
        #l0.Draw("same")
        #l00.Draw("same")
        #l000.Draw("same")
        #l1.Draw("same")
        l2.Draw("same")
        #if ymin<0.9: l3.Draw("same")
        #if ymin<0.8: l4.Draw("same")

        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.pdf")
        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.png")            
        c1.Clear()


    elif residuals == -2: # plot data - fitted (sig+bkg) in residual plot
        c1.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.4)
        pad2.SetTopMargin(0.)
        pad2.SetBottomMargin(0.2)
        pad2.Draw()
        pad2.cd()
        
        #hlist1, snames1, legstack1, hlist2, snames2, legstack2, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC
        histos = {}
        histos["data"] = hlist2[0]
        histos["sig"] = hlist1[1]
        histos["bkg"] = hlist1[0]
        #print histos
        (h_data_bkg, h_sig, h_err) = getHistosPostFit(histos, hsOpt, snames1, colors, fit_results, postfit_file)
        #print h_data_bkg.Integral(), h_sig.Integral(), h_err.Integral()
        """hrat = h2.Clone("h_rat")
        hrat.Divide(h1)
        # consider only data error in the ratio plot
        for ibin in range(1, h2.GetNbinsX()+1):
            #print(h2.GetBinContent(ibin))
            if(h2.GetBinContent(ibin)>0): 
                hrat.SetBinError(ibin, h2.GetBinError(ibin)/h2.GetBinContent(ibin) )
            else: 
                hrat.SetBinError(ibin, 0.)
        """
        
        h_data_bkg.SetTitle("")
        h_data_bkg.GetXaxis().SetTitleSize(20)
        h_data_bkg.GetXaxis().SetTitleFont(43)
        h_data_bkg.GetXaxis().SetTitleOffset(4.)
        h_data_bkg.GetXaxis().SetLabelFont(43)
        h_data_bkg.GetXaxis().SetLabelSize(20)
        h_data_bkg.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        #h_data_bkg.GetYaxis().SetRangeUser(-20,20)
        minbin = h_data_bkg.GetXaxis().GetFirst()
        maxbin = h_data_bkg.GetXaxis().GetLast()
        """ymax_ = 1.5
        ymax = 1.
        ymin_ = 0.5
        ymin = 1.
    
        for ibin in range(minbin, maxbin+1):       
            binc = hrat.GetBinContent(ibin) 
            if binc == 0. or (binc is None): 
                continue
            if binc*1.05 > ymax: 
                ymax = binc*1.05
            if binc*0.95 < ymin: 
                ymin = binc*0.95"""
        y_max = max(h_data_bkg.GetMaximum(), hlist1[-1].GetMaximum())*1.15
        y_min = min(h_data_bkg.GetMinimum(), hlist1[-1].GetMinimum())*1.5

        h_data_bkg.GetYaxis().SetRangeUser(y_min,y_max)
        h_data_bkg.GetYaxis().SetTitleSize(20)
        h_data_bkg.GetYaxis().SetTitleFont(43)
        h_data_bkg.GetYaxis().SetTitleOffset(1.40)
        h_data_bkg.GetYaxis().SetLabelFont(43)
        h_data_bkg.GetYaxis().SetLabelSize(18)
        #h_data_bkg.SetMarkerStyle(33)
        h_data_bkg.SetMarkerStyle(20)
        h_data_bkg.SetMarkerSize(0.7)
        h_data_bkg.SetMarkerColor(1)
        h_data_bkg.SetLineColor(1)
        h_data_bkg.GetXaxis().SetTitle(hsOpt['xname'])
        #h_data_bkg.GetYaxis().SetTitle('data/bkg')
        h_data_bkg.Draw("e3 x0")
        hlist1[-1].Draw("hist same")
        
        h_sig.Draw("hist same")
        
        h_err.SetFillColor(632)
        h_err.Draw("E2same")
        h_data_bkg.Draw("same e3 x0")
        
        
        """l = TLine(hsOpt['xmin'],1.5,hsOpt['xmax'],1.5);
        l0 = TLine(hsOpt['xmin'],1.4,hsOpt['xmax'],1.4);
        l00 = TLine(hsOpt['xmin'],1.3,hsOpt['xmax'],1.3);
        l000 = TLine(hsOpt['xmin'],1.2,hsOpt['xmax'],1.2);
        l1 = TLine(hsOpt['xmin'],1.1,hsOpt['xmax'],1.1);
        l2 = TLine(hsOpt['xmin'],1.,hsOpt['xmax'],1.);
        l3 = TLine(hsOpt['xmin'],0.9,hsOpt['xmax'],0.9);
        l4 = TLine(hsOpt['xmin'],0.8,hsOpt['xmax'],0.8);
        l.SetLineStyle(3)
        l0.SetLineStyle(3)
        l00.SetLineStyle(3)
        l000.SetLineStyle(3)
        l1.SetLineStyle(3)
        l2.SetLineStyle(3)
        l3.SetLineStyle(3)
        l4.SetLineStyle(3)
        #l.Draw("same")
        #l0.Draw("same")
        #l00.Draw("same")
        #l000.Draw("same")
        #l1.Draw("same")
        l2.Draw("same")
        #if ymin<0.9: l3.Draw("same")
        #if ymin<0.8: l4.Draw("same")
        """
        
        leg_coords = 0.65,0.2,0.9,0.4
        if "legpos" in hsOpt:
            if hsOpt["legpos"] == "top":
                leg_coords = 0.65,0.78,0.9,1.
            elif hsOpt["legpos"] == "left" or hsOpt["legpos"] == "topleft":
                leg_coords = 0.1,0.78,0.35,1.
            elif hsOpt["legpos"] == "middle":
                leg_coords = 0.47,0.0,0.63,0.25
        leg = TLegend(*leg_coords)
        leg.SetTextSize(0.05)
        leg.AddEntry(h_data_bkg, "Data - fitted background", "p")
        leg.AddEntry(h_sig, "HH4b fitted")
        leg.AddEntry(hlist1[-1], "HH4b fitted x5")
        leg.AddEntry(h_err, "Total uncertainty")
        leg.Draw("same")
        
        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.pdf")
        c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.png")            
        c1.Clear()

    elif residuals == 10:  # to get comparison of hres with default bias
        c3 = TCanvas("c3", "comp_res"+hsOpt['hname'], 1000, 1000)
        pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0.0) 
        pad1.Draw()             
        pad1.cd()
        #c3.Divide(1,2)
        #c3.cd(1)        
        hres = h2.Clone("h_res")        
        checkbin = False
        for i in range(1, hres.GetXaxis().GetNbins()+1):
            n1 = h1.GetBinContent(i)
            n2 = h2.GetBinContent(i)
            e1 = h1.GetBinError(i)
            e2 = h2.GetBinError(i)
            #print  i, n1, n2, e1, e2
            if n1 :#and e1: 
                hres.SetBinContent(i,(n2-n1)) # order is correct!! bkg - truth
                #err = (pow(n1,3) + 15*pow(n1,2)*n2+15*pow(n2,2)*n1 + pow(n2,3))/(4*pow((n1+n2),3))
                hres.SetBinError(i, math.sqrt(pow(e1,2)+pow(e2,2)))
        hres.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        hres.SetMarkerStyle(8)
        hres.SetMarkerSize(0.8)
        hres.SetMarkerColor(1)
        hres.SetLineColor(1)
        hres.GetXaxis().SetTitle(hsOpt['xname'])
        hres.GetYaxis().SetTitle('Events')

        bkg_bias_fname = "/lustre/cmswork/hh/alp_mva/bias/bias_correction_20171018_bigset_unscaled.json"
        with open(bkg_bias_fname,"r") as bkg_bias_file:
            json_dict = json.load(bkg_bias_file)
            print ("using bias file: ", bkg_bias_file)

        #print("bias_corr", json_dict['bias_corr'])
        #for n, s_bin in enumerate(filt_hists['bkg_hem_mix']):
        hbias = hres.Clone("h_bias")
        for n in range(len(json_dict['bias_corr'])):
                #if not s_bin.overflow:
                #value = s_bin.value

                bias = json_dict['bias_corr'][n]
                var = json_dict['var'][n]
                bias_unc = json_dict['bias_corr_unc_bs'][n]
                bias_unc_stat = json_dict['bias_corr_unc_stat'][n]
                
                #bkg_pred_initial = value
                #print n, n-1+skip_bins
                #print bkg_pred_initial
                #new_bkg_pred = bkg_pred_initial - bias #do not rescale (good for 4 times data)
                #print new_bkg_pred
                #if var > np.sqrt(bkg_pred_initial):
                new_bkg_pred_stat = var
                #else:
                #  new_bkg_pred_stat = np.sqrt(bkg_pred_initial)
                #print new_bkg_pred_stat
                                
                new_bkg_pred_tot_unc = np.sqrt(new_bkg_pred_stat**2 + bias_unc**2 + bias_unc_stat**2)

                #value = new_bkg_pred
                    

                #filt_hists['bkg_hem_mix'][n].value = value
                #filt_hists['bkg_hem_mix'][n].error = unc
                hbias.SetBinContent(n+1, bias)
                hbias.SetBinError(n+1, new_bkg_pred_tot_unc)

        """for n, s_bin in enumerate(filt_hists['bkg_hem_mix']):
            if not s_bin.overflow:
                value = s_bin.value
                unc = s_bin.error
                if dm.swapped:
                    s_name = "CMS_hh_bbbb_bkg_hem_mix_bin_swapped{}".format(n)
                else:    
                    s_name = "CMS_hh_bbbb_bkg_hem_mix_bin_{}".format(n)
                name_up = "bkg_hem_mix_" + s_name + "Up" 
                name_dw = "bkg_hem_mix_" + s_name + "Down" 

                filt_hists[name_up] = filt_hists['bkg_hem_mix'].Clone(name_up)
                filt_hists[name_dw] = filt_hists['bkg_hem_mix'].Clone(name_dw)
                filt_hists[name_up][n].value = value + unc
                filt_hists[name_dw][n].value = value - unc
                #scale after setting bin errors
                filt_hists[name_up].Scale(bkg_scale)
                filt_hists[name_dw].Scale(bkg_scale)"""

        ymax = 650.
        ymin = -200.
        if hbias.GetMaximum() > ymax: ymax = hbias.GetMaximum()*1.15
        if hres.GetMaximum() > ymax: ymax = hres.GetMaximum()*1.15
        if hbias.GetMinimum() < ymin: ymin = hbias.GetMinimum()*1.15
        if hres.GetMinimum() < ymin: ymin = hres.GetMinimum()*1.15
        hres.GetYaxis().SetRangeUser(ymin,ymax)
        hbias.GetYaxis().SetRangeUser(ymin,ymax)

        #print "res", hres.Integral(), "bias", hbias.Integral()
        hbias.SetMarkerColor(ROOT.kRed)
        hbias.SetLineColor(2)
        hbias.Draw("E X0")
        hres.Draw("E X0 same")

        legend = setLegend(1,1)
        legend.AddEntry(hres, "tt mixed - tt MC", "p")
        legend.AddEntry(hbias, "Bias", "p")
        legend.Draw("same")

        #Residual panel
        c3.cd()
        pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
        pad2.SetTopMargin(0.)
        pad2.SetBottomMargin(0.2)
        pad2.Draw()
        pad2.cd()

        hresidual = hres.Clone("h_residual")
        hresidual.Add(hbias, -1)
        # consider only data error in the ratio plot
        for ibin in range(1, hresidual.GetNbinsX()+1):
            #print "A", ibin, hresidual.GetBinContent(ibin), hres.GetBinContent(ibin), hbias.GetBinContent(ibin)
            hresidual.SetBinContent(ibin, hresidual.GetBinContent(ibin) / math.sqrt(hres.GetBinError(ibin)**2 + hbias.GetBinError(ibin)**2) )
            hresidual.SetBinError(ibin, 0.01)
            #print ibin, hresidual.GetBinContent(ibin), hres.GetBinError(ibin), hbias.GetBinError(ibin)
            #if(h2.GetBinContent(ibin)>0): 
            #    #hrat.SetBinError(ibin, h2.GetBinError(ibin)/h2.GetBinContent(ibin) )
            #else: 
            #    hrat.SetBinError(ibin, 0.)"""

        # MC uncertainy shadow plot
        herr = herr1.Clone("h_err")
        herr.Reset()
        for ibin in range(1, herr1.GetNbinsX()+1):
                herr.SetBinContent (ibin, 0.)
                herr.SetBinError   (ibin, 1.)

        hresidual.SetTitle("")
        hresidual.GetXaxis().SetTitleSize(20)
        hresidual.GetXaxis().SetTitleFont(43)
        hresidual.GetXaxis().SetTitleOffset(4.)
        hresidual.GetXaxis().SetLabelFont(43)
        hresidual.GetXaxis().SetLabelSize(20)
        hresidual.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

        hresidual.GetYaxis().SetRangeUser(-2.25,2.)
        hresidual.GetYaxis().SetTitleSize(20)
        hresidual.GetYaxis().SetTitleFont(43)
        hresidual.GetYaxis().SetTitleOffset(1.40)
        hresidual.GetYaxis().SetLabelFont(43)
        hresidual.GetYaxis().SetLabelSize(18)
        hresidual.SetMarkerStyle(8)
        hresidual.SetMarkerSize(0.8)
        hresidual.SetMarkerColor(1)
        hresidual.SetLineColor(1)
        hresidual.GetXaxis().SetTitle("BDT output")
        hresidual.GetYaxis().SetTitle('difference in #sigma units')
        hresidual.Draw("E1 X0")
        herr.GetXaxis().SetTitle("")
        herr.SetFillColor(430)
        herr.Draw("E2same")

        
        c3.SaveAs(oDir+"/"+hsOpt['hname']+"_resc.pdf")
        c3.SaveAs(oDir+"/"+hsOpt['hname']+"_resc.png")            
        c3.SaveAs(oDir+"/"+hsOpt['hname']+"_resc.root")            

    elif residuals >=1: # to get residuals and pulls -- data as h2!!!
        if residuals==2:
            c2 = TCanvas("c2", "res"+hsOpt['hname'], 800, 800)    
            c2.Divide(1,2)
            c2.cd(1)
        else:
            c2 = TCanvas("c2", "res"+hsOpt['hname'], 800, 400)
        hres = h2.Clone("h_res")
        checkbin = False
        for i in range(1, hres.GetXaxis().GetNbins()+1):
            n1 = h1.GetBinContent(i)
            n2 = h2.GetBinContent(i)
            e1 = h1.GetBinError(i)
            e2 = h2.GetBinError(i)
            #print  i, n1, n2, e1, e2
            if n1 and e1: 
                hres.SetBinContent(i,(n1-n2)/math.sqrt(e1*e1+e2*e2)) #sign is fine!!!!!!!!
                err = (pow(n1,3) + 15*pow(n1,2)*n2+15*pow(n2,2)*n1 + pow(n2,3))/(4*pow((n1+n2),3))
                hres.SetBinError(i, err)


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
            gStyle.SetOptStat(111)
            gStyle.SetOptFit(1)
            res_a = []
            for i in range(1, hres.GetXaxis().GetNbins()+1):                
                if (hres.IsBinOverflow(i) and hres.GetBinContent(i) == 0): continue
                else:  res_a.append(hres.GetBinContent(i))
            res_pull = Hist(40, -5., 5, name = "h_res_pull")
            res_pull.GetXaxis().SetTitle("residuals (sigma units)")
            for v in res_a: res_pull.fill(v)
            res_pull.Fit("gaus", "LL")
            res_pull.Draw("E X0")
            text = "BM%d" % bm
            text = text.replace("BM0", "SM").replace("BM13", "Box")
            latex.DrawLatex(0.18, 0.88, text)
            latex.SetTextFont(52)
            latex.SetTextSize(0.04)

        c2.Update()    
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.pdf")
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.png")            
        #c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.root")   

    return [nev1,nev1err,nev2,nev2err]
#-----------

def drawH1tdrAcc(hs, snames, leg,
                   oDir, colors, headerOpt, isMC):
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", 'acc', 800, 800)
    markers = [23,24,25]

    legend = TLegend(0.50,0.7,0.85,0.85)
    legend.SetBorderSize(0)
    legend.SetFillColor(0)
    legend.SetFillStyle(0)

    for h_ in hs[0]:
        hd =  h_.Clone('hd')    
    for i, h_ in enumerate(hs):
        if i==0: 
            continue
        for h__ in h_:
            h =  h__.Clone('h')
        h.SetTitle("")
        h.Divide(hd) 
        h.GetXaxis().SetTitle('generator p_{T} (GeV)')
        h.GetYaxis().SetTitle('acceptance')
        h.GetYaxis().SetLabelOffset(0.010)
        h.GetYaxis().SetTitleOffset(1.45)
        h.GetXaxis().SetLabelOffset(0.010)
        h.GetXaxis().SetTitleOffset(1.45)
        h.SetMaximum(1.15)
        h.GetXaxis().SetRangeUser(0.,100.)
        h.SetMarkerStyle(markers[i-1])
        h.SetMarkerSize(1.)
        h.SetMarkerColor(colors[i-1])
        legend.AddEntry(h, leg[i-1], "P")
        if i==1: 
            h.Draw("PE")
            #Legend & headers
            drawCMStdr(headerOpt)

        h.Draw("PE same") #draw first twice
    legend.Draw("same")
    c1.Update()
    c1.SaveAs(oDir+"/acc.pdf")
    c1.SaveAs(oDir+"/acc.png")


def drawH1tdr(hlist1, snames1, leg1, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    ymax = 0.
    nh1 = hlist1[0].Integral()  

    herr = hlist1[0].Clone("hs_error")  
    herr.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])

    herr.Rebin(rb)
    herr.GetXaxis().SetTitle(hsOpt['xname'])
    herr.GetYaxis().SetTitle(hsOpt['yname'])
    herr.SetMinimum(0.)
    herr.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr.SetMinimum(0.)
    herr.Draw()

    #Legend & headers
    if isMC: drawCMS(-1, headerOpt)
    else: drawCMS(35.9, headerOpt)
    legend = setLegend(1,1)
    if len(leg1) > 1:
        for n, leg in enumerate(leg1):
            legend.AddEntry(hlist1[n], leg)
    else:
        legend.AddEntry(hlist1[len(hlist1)-1], leg1[0])
    legend.Draw("same")
    #-------------

    scale = 1.
    for i, h in enumerate(hlist1):         
        if(norm): scale = nh1/h.Integral()
        col = colors[i]
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
        h.Rebin(rb)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        if dofill[i]: 
            h.SetFillColorAlpha(col,0.1)
            h.SetFillStyle(1)
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(col,0.)
        if i == 0: ymax = h.GetMaximum()*1.15
        h.SetMaximum(ymax)
        if i ==0: h.Draw("HISTEsame") 
        else: h.Draw("HISTEsame")

    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
   #c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    return [nev1,nev1err,nev2,nev2err]
#------------


def drawH1only(hlist1, snames1, legstack1, hsOpt, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
    gStyle.SetOptTitle(0);
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    ymax = 0.
    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], 1., dofill[0])
    ymax = hs1.GetMaximum()*1.15

   #debug -- needed before drawing hs
    herr1.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr1.SetMinimum(0.)
    herr1.SetMaximum(ymax)
    if len(hlist1)>1: 
        herr1.Draw("E2")
        herr1.SetFillColor(922)
    else: herr1.Draw("E")
   #--

    hs1.SetMaximum(ymax)
    herr1.SetMaximum(ymax)

    #Legend & headers
    if isMC: drawCMS(-1, headerOpt)
    else: drawCMS(35.9, headerOpt)
    legend = setLegend(1,1)
    nskip = 0
    match = False
    for n, sam in enumerate(snames1):
        # to get one legend for all HT bins - to be implemented for other samples         
        if sam.find("QCD")>=0 and match: 
            nskip+=1 
            continue
        if len(legstack1) > n-nskip:
            if sam.find("QCD")>=0: match = True
            legend.AddEntry(hlist1[n], legstack1[n-nskip])            
    if len(hlist1)>1: legend.AddEntry(herr1, 'bkg. unc. (stat.only)')
    legend.Draw("same")
    #-------------

    plotH(hlist1, hs1, herr1, dofill[0])
    nev1 = 0
    nev1err = 0
    if hsOpt['hname']=='h_nevts': 
        nev1 = herr1.GetBinContent(1)
        nev1err = herr1.GetBinError(1)

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
   #c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    return [nev1,nev1err]
#-------------------------


def fillH2(h,h1):
    h2 = (TH2D)("h2_bdt","h2_bdt",h.GetNbinsX(),0.,1.,h.GetNbinsX(),0.,1.) 
    for i in range(1,h.GetNbinsX()):
        for j in range(1,h1.GetNbinsX()):
         h2.SetBinContent(i, j, h.GetBinContent(i)+h1.GetBinContent(j))
    return h2

def drawH2(hs, hs1, hsOpt, sname, rebin, oDir, legs):
    gStyle.SetOptStat(False)
    legend = setLegend(1,1)

    if len(hs1):
        hs2 = []
        for h in hs:
            for h1 in hs1:
                hs2.append(fillH2(h1,h))
    else:
        hs2 = hs

    for i, h2 in enumerate(hs2):
        name = hsOpt['hname']
        print name
        c2 = TCanvas(name, name, 800, 800)
        print h2.GetBinContent(10)
        h2.Rebin2D(rebin, rebin)
        h2.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h2.GetYaxis().SetRangeUser(hsOpt['ymin'],hsOpt['ymax'])
        h2.GetXaxis().SetTitle(hsOpt['xname']+" "+str(legs[1]))
        h2.GetYaxis().SetTitle(hsOpt['yname']+" "+str(legs[0]))

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
        c2.Update() 

        c2.SaveAs(oDir+"/"+name+".pdf")
        c2.SaveAs(oDir+"/"+name+".png")            
        c2.SaveAs(oDir+"/"+name+".root")  

    return True
#------------

# DRAWING TOOLS
#################
def plotH(hlist, h, herr, fill):
    if fill:         
        if len(hlist)>1: 
            h.Draw("HISTsame")
            herr.Draw("E2same")
        else: h.Draw("HISTEsame")
    else:
        if len(hlist)>1: 
            h.Draw("HISTsame")   
            herr.Draw("E2same") 
        else: h.Draw("Esame")    

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
        latex.SetTextFont(52)
        latex.SetTextSize(0.02)
        latex.DrawLatex(0.15, 0.830, "preliminary")
    else: 
        latex.DrawLatex(0.15, 0.88, "CMS   "+text)
        latex.SetTextFont(52)
        latex.SetTextSize(0.02)
        latex.DrawLatex(0.15, 0.850, "preliminary")
#------------

def drawCMStdr(text, onTop=False):
    latex = TLatex()
    latex.SetNDC()
    latex.SetTextSize(0.035)
    latex.SetTextColor(1)
    latex.SetTextFont(42)
    latex.SetTextAlign(33)
    latex.DrawLatex(0.90, 0.94, "14 TeV")
    if not onTop: latex.SetTextAlign(11)
    latex.SetTextFont(62)
    latex.SetTextSize(0.03 if len(text)>0 else 0.035)
    if not onTop:
        latex.DrawLatex(0.15, 0.85, "CMS Phase-2   "+text)
        latex.SetTextFont(52)
        latex.SetTextSize(0.030)
        latex.DrawLatex(0.15, 0.820, "Simulation. Preliminary")
        latex.SetTextFont(52);
        latex.SetTextSize(0.030);
        latex.DrawLatex(0.15, 0.780, "pp #rightarrow HH #rightarrow b#bar{b}b#bar{b}");

def setLegend(doRight, doTop):
    leg = TLegend(0.55,0.70,0.90,0.90)
    leg.SetTextSize(0.032)
    return leg
#------------

def drawPostFitH1(hlist1, snames1, legstack1, hlist2, snames2, legstack2, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
    gStyle.SetOptTitle(0);

    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       
    if residuals==-1:
        pad1 = TPad("pad1", "pad1", 0, 0.3, 1, 1.0)
        pad1.SetBottomMargin(0.03) 
        pad1.Draw()             
        pad1.cd()               
    
    isNevts=False
    if hsOpt['hname']=="h_nevts": isNevts=True
    ymax = 0.

    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0])

    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.15
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.15
    if isNevts:  print "h1Int ",  h1.GetBinContent(1), h1.GetBinError(1)

    if(norm): scale2 = getScale(hsOpt,hlist2, hlist2)
    else: scale2 = 1.
    if scale2 != 1.: print "sc_to_norm2: ",scale2
    hs2, herr2, h2 =  getStackH(hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1])
    if hs2.GetMaximum() > ymax: ymax = hs2.GetMaximum()*1.15
    if herr2.GetMaximum() > ymax: ymax = herr2.GetMaximum()*1.15
    if isNevts:  print "h2Int ",  h2.GetBinContent(1), h2.GetBinError(1)

    if len(hlist1) == 1 and len(hlist2) == 1:
        print("KS: ", hlist1[0].KolmogorovTest(hlist2[0]))
        print("Chi2: ", hlist1[0].Chi2Test(hlist2[0], "UU NORM"))
    else:
        print("Not doing KS test, stacks as input")
   #debug -- needed before drawing hs
    herr1.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    herr1.SetMinimum(0.)
    herr1.SetMaximum(ymax)
    if len(hlist1)>1: 
        herr1.Draw("E2")
        herr1.SetFillColor(922)
    else: herr1.Draw("E")
   #--

    #Legend & headers
    if isMC: drawCMS(-1, headerOpt)
    else: drawCMS(35.9, headerOpt)
    legend = setLegend(1,1)
    legend.AddEntry(hlist2[len(hlist2)-1], legstack2[0]) #debug - one leg for second samplelist
    nskip = 0
    match = False 
    for n, sam in enumerate(snames1):
        # to get one legend for all HT bins - to be implemented for other samples         
        if sam.find("QCD")>=0 and match: 
            nskip+=1 
            continue
        if len(legstack1) > n-nskip:
            if sam.find("QCD")>=0: match = True
            legend.AddEntry(hlist1[n], legstack1[n-nskip])            
    if len(hlist1)>1: legend.AddEntry(herr1, 'bkg. unc. (stat.only)')
    legend.Draw("same")
    #-------------

    if(ymax > 1000): TGaxis.SetMaxDigits(3)
    hs1.SetMaximum(ymax)
    herr1.SetMaximum(ymax)
    plotH(hlist1, hs1, herr1, dofill[0])
    hs2.SetMaximum(ymax)
    herr2.SetMaximum(ymax)
    plotH(hlist2, hs2, herr2, dofill[1])
    herr2.Draw("Esameaxis")

    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0
    if isNevts: 
        nev1 = herr1.GetBinContent(1)
        nev2 = herr2.GetBinContent(1)
        nev1err = herr1.GetBinError(1)
        nev2err = herr2.GetBinError(1)

    herr1.GetXaxis().SetLabelSize(0.)

    c1.cd()
    pad2 = TPad("pad2", "pad2", 0, 0.05, 1, 0.3)
    pad2.SetTopMargin(0.)
    pad2.SetBottomMargin(0.2)
    pad2.Draw()
    pad2.cd()
    hrat = h2.Clone("h_rat")
    hrat.Divide(h1)
    # consider only data error in the ratio plot
    for ibin in range(1, h2.GetNbinsX()+1):
	    #print(h2.GetBinContent(ibin))
	    if(h2.GetBinContent(ibin)>0): 
		hrat.SetBinError(ibin, h2.GetBinError(ibin)/h2.GetBinContent(ibin) )
	    else: 
		hrat.SetBinError(ibin, 0.)

    # MC uncertainy shadow plot
    herr = herr1.Clone("h_err")
    herr.Reset()
    for ibin in range(1, herr1.GetNbinsX()+1):
	    if(herr1.GetBinContent(ibin)>0): 
		herr.SetBinContent (ibin, 1.)
		herr.SetBinError   (ibin, herr1.GetBinError(ibin)/herr1.GetBinContent(ibin))
	    else: 
		herr.SetBinContent(ibin, 1.)
		herr.SetBinError   (ibin, 0.)
    
    hrat.SetTitle("")
    hrat.GetXaxis().SetTitleSize(20)
    hrat.GetXaxis().SetTitleFont(43)
    hrat.GetXaxis().SetTitleOffset(4.)
    hrat.GetXaxis().SetLabelFont(43)
    hrat.GetXaxis().SetLabelSize(20)
    hrat.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    minbin = hrat.GetXaxis().GetFirst()
    maxbin = hrat.GetXaxis().GetLast()
    ymax_ = 1.5
    ymax = 1.
    ymin_ = 0.5
    ymin = 1.

    for ibin in range(minbin, maxbin+1):       
	    binc = hrat.GetBinContent(ibin) 
	    if binc == 0. or (binc is None): 
		continue
	    if binc*1.05 > ymax: 
		ymax = binc*1.05
	    if binc*0.95 < ymin: 
		ymin = binc*0.95

    hrat.GetYaxis().SetRangeUser(ymin,ymax)
    hrat.GetYaxis().SetTitleSize(20)
    hrat.GetYaxis().SetTitleFont(43)
    hrat.GetYaxis().SetTitleOffset(1.40)
    hrat.GetYaxis().SetLabelFont(43)
    hrat.GetYaxis().SetLabelSize(18)
    hrat.SetMarkerStyle(8)
    hrat.SetMarkerSize(0.8)
    hrat.SetMarkerColor(1)
    hrat.SetLineColor(1)
    hrat.GetXaxis().SetTitle(hsOpt['xname'])
    hrat.GetYaxis().SetTitle('data/bkg')
    hrat.Draw("E X0")
    herr.SetFillColor(430)
    herr.Draw("E2same")

    l = TLine(hsOpt['xmin'],1.5,hsOpt['xmax'],1.5)
    l0 = TLine(hsOpt['xmin'],1.4,hsOpt['xmax'],1.4)
    l00 = TLine(hsOpt['xmin'],1.3,hsOpt['xmax'],1.3)
    l000 = TLine(hsOpt['xmin'],1.2,hsOpt['xmax'],1.2)
    l1 = TLine(hsOpt['xmin'],1.1,hsOpt['xmax'],1.1)
    l2 = TLine(hsOpt['xmin'],1.,hsOpt['xmax'],1.)
    l3 = TLine(hsOpt['xmin'],0.9,hsOpt['xmax'],0.9)
    l4 = TLine(hsOpt['xmin'],0.8,hsOpt['xmax'],0.8)
    l.SetLineStyle(3)
    l0.SetLineStyle(3)
    l00.SetLineStyle(3)
    l000.SetLineStyle(3)
    l1.SetLineStyle(3)
    l2.SetLineStyle(3)
    l3.SetLineStyle(3)
    l4.SetLineStyle(3)
    #l.Draw("same")
    #l0.Draw("same")
    #l00.Draw("same")
    #l000.Draw("same")
    #l1.Draw("same")
    l2.Draw("same")
    #if ymin<0.9: l3.Draw("same")
    #if ymin<0.8: l4.Draw("same")
    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+"_rat.png")
    c1.Clear()

    return [nev1,nev1err,nev2,nev2err]


#def getHistosPostFit(histos, hsOpt, rebin, snames, color, scale, fill):
def getHistosPostFit(histos, hsOpt, snames, color, fit_results, postfit_file = None):
    
    print hsOpt
    h_data_bkg = histos["data"].Clone("data-bkg")
    h_data_bkg.Add(histos["bkg"], -1)

    for ibin in range(1, h_data_bkg.GetNbinsX()+1):
        #print h_data_bkg.GetBinError(ibin), histos["bkg"].GetBinError(ibin), histos["bkg"].GetBinError(ibin)/histos["bkg"].GetBinContent(ibin)
        #print h_data_bkg.GetBinError(ibin), histos["bkg"].GetBinError(ibin), histos["data"].GetBinError(ibin), histos["sig"].GetBinError(ibin), histos["sig"].GetBinContent(ibin)
        pass

    h_sig = histos["sig"].Clone("signal")
    h_err = histos["sig"].Clone("error_bar")    
    
    #if color: col = color[0][0]
    #else: col = sam_opt[snames[0]]['fillcolor']
    #print col, color, sam_opt[snames[0]]
    
    h_err.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
    #h_err.Reset()
    #herr.Rebin(rebin)
    h_err.GetXaxis().SetTitle(hsOpt['xname'])
    h_err.SetFillStyle(3005)
    h_err.SetFillColor(sam_opt["sig"]['fillcolor'])
    h_err.SetLineColor(922)
    h_err.SetLineWidth(0)         
    h_err.SetMarkerSize(0)
    h_err.SetMarkerColor(922)
    #h_err.SetMinimum(0.)
    
    
    h_sig.SetLineStyle(1)
    h_sig.SetLineWidth(2)
    h_sig.SetLineColor(sam_opt["sig"]['linecolor'])
    
    """for i, h in enumerate(histos):         
        if color: col = color[i]
        else: col = sam_opt[snames[i]]['fillcolor']
        #print sam_opt[snames[i]]['sam_name']
        
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
        h.Rebin(rebin)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        print "h[{}]: {}".format(i, h.Integral())
        if fill: 
            h.SetFillColorAlpha(col,0.2)
            h.SetFillStyle(1)
        if i==len(histos)-1 :
            h.SetLineStyle(1)
            h.SetLineWidth(2)
            h.SetLineColor(col)
            if not fill: 
                h.SetMarkerSize(0.6)
                h.SetMarkerColor(col)
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(col,0.)
    """
    
    
    
    err = max((fit_results["sig"][0] - fit_results["sig"][1]) / fit_results["sig"][0], (fit_results["sig"][2] - fit_results["sig"][0]) / fit_results["sig"][0])

    #If not loading already morphed fit results
    if postfit_file == None:
        for ibin in range(1, h_err.GetNbinsX()+1):
            #print ibin, err, h_err.GetBinContent(ibin), err * h_err.GetBinContent(ibin), h_err.GetBinError(ibin)
            h_err.SetBinError(ibin, math.sqrt((err * h_err.GetBinContent(ibin))**2 + h_data_bkg.GetBinError(ibin)**2) )
    else:
        for ibin in range(1, h_err.GetNbinsX()+1):
            #print ibin, err, h_err.GetBinContent(ibin), err * h_err.GetBinContent(ibin), h_err.GetBinError(ibin)
            h_err.SetBinError(ibin, math.sqrt(h_sig.GetBinError(ibin)**2 + h_data_bkg.GetBinError(ibin)**2) )
            #print ibin, h_err.GetBinContent(ibin), h_err.GetBinError(ibin)
            
    return h_data_bkg, h_sig, h_err


"""def make_residual_comparison(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0], hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1])
    
    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0])
    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.15
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.15
    if isNevts:  print "h1Int ",  h1.GetBinContent(1), h1.GetBinError(1)

    if(norm): scale2 = getScale(hsOpt,hlist2, hlist2)
    else: scale2 = 1.
    if scale2 != 1.: print "sc_to_norm2: ",scale2
    hs2, herr2, h2 =  getStackH(hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1])"""

