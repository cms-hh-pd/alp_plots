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

def getHistos_bdt(hist, filename, plotDirs, weights, sf):
    hlist = [] 
    tf = TFile(filename)
    if not tf: 
        print "WARNING: files do not exist"  
    print 'aa'
    for i, Dir in enumerate(plotDirs):
        hname = hist+"_"+Dir            
        print hname
        if(tf.Get(Dir+"/"+hname)):
            print hname
            w = 1.
            sf_ = 1.
            if len(weights)>0:
	            if weights[i]>0:
        	        w = weights[i]
            if len(sf)>0:
                if sf[i]>=0:
                    sf_ = sf[i]
            print w*sf_
            h = tf.Get(Dir+"/"+hname)
            print h.GetName()
            print h.Integral()
            h.Scale(w*sf_)
            print h.Integral()
            hlist.append(h)
        else:
            print "WARNING: hist {} not found in {}".format(hist,tf)

    return hlist
#------------

def getHistos_tdr(hist, filelist, plotDir, lumi, normtolumi, weight):
    hlist = []    
    for i, f in enumerate(filelist):  #debug - not efficient to loop on file
        w = 1.
        tf = TFile(f)
        #print tf
        if not tf: 
            print "WARNING: files do not exist"  

      #  if weight[i]>=0:
#   	        w = weight[i]

       # print w
        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            #print "h1Int ",  h.GetBinContent(1), h.GetBinError(1)
 #           h.Scale(w)
            hlist.append(h)
        else:
            print "WARNING: hist {} not found in {}".format(hist,tf)

    return hlist
#------------


def getHistos(hist, filelist, plotDir, lumi, normtolumi, weight, sf):
    hlist = []    
    for i, f in enumerate(filelist):  #debug - not efficient to loop on file
        w = 1.
        sf_ = 1.
        tf = TFile(f)
        #print tf
        if not tf: 
            print "WARNING: files do not exist"  

        if "Run" in f: #data
            norm = 1
        else:
            if len(weight)>0:
	        if weight[i]>=0:
                    w = weight[i]
            else:
                if(tf.Get("h_w_oneInvFb")):
                    h = tf.Get("h_w_oneInvFb")
                    w = h.GetBinContent(1)
                else:
                    print "WARNING: 'h_w_oneInvFb' not found in {}".format(tf)
            if len(sf)>0:
                if sf[i]>=0:
                    sf_ = sf[i]

            if normtolumi: norm = w*lumi*sf_
            else: norm = w*sf_

        print norm    
        if(tf.Get(plotDir+"/"+hist)):
            h = tf.Get(plotDir+"/"+hist)
            #print "h1Int ",  h.GetBinContent(1), h.GetBinError(1)
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
        print h.Integral()
    for i, h in enumerate(hlist2): 
        if isinstance(h,int):
           norm = h
           break
        elif i==skip2: 
            continue 
        else: norm += h.Integral()
    if  hsInt: scale = norm/(hsInt+hsSkip)
    else: scale = 1.
    print hsInt
    return scale
#------------

def getStackH(histos, hsOpt, rebin, snames, color, scale, fill, hl2):

    if color: col = color
    else: col = sam_opt[snames[0]]['fillcolor']

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
        if color: col = color
        else: col = sam_opt[snames[i]]['fillcolor']
        #print sam_opt[snames[i]]['sam_name']

        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
        h.Rebin(rebin)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        print h.Integral()
        if fill: 
            h.SetFillColorAlpha(col,0.2)
            h.SetFillStyle(1) #samOpt['fillstyle']
        if i==len(histos)-1 :
            h.SetLineStyle(1) #samOpt['linestyle']
            h.SetLineWidth(2)  #samOpt['linewidth']
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
    return hs, herr, h_

##
# DRAWING FUNCTIONS
#################
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
    c1.SaveAs(oDir+"/"+leg+".root")
#------------

def drawH1(hlist1, snames1, legstack1, hlist2, snames2, legstack2, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    isNevts=False
    if hsOpt['hname']=="h_nevts": isNevts=True
    ymax = 0.

    if(norm): scale1 = getScale(hsOpt,hlist1, hlist2) #debug -v1 1.25
    else: scale1 = 1.
    print "scale1", scale1
    hs1, herr1, h1 =  getStackH(hlist1, hsOpt, rb, snames1, colors[0], scale1, dofill[0], hlist2)
    if hs1.GetMaximum() > ymax: ymax = hs1.GetMaximum()*1.15
    if herr1.GetMaximum() > ymax: ymax = herr1.GetMaximum()*1.15
    if isNevts:  print "h1Int ",  h1.GetBinContent(1), h1.GetBinError(1)
#    if hsOpt['hname']=="h_jets_n":  print "h1Int ",  h1.Integral(), h1.GetBinError(1)

    if(norm): scale2 = getScale(hsOpt,hlist2, hlist2) #debug -v1 1.
    else: scale2 = 1.
    print "scale2", scale2
    hs2, herr2, h2 =  getStackH(hlist2, hsOpt, rb, snames2, colors[1], scale2, dofill[1], hlist2)
    if hs2.GetMaximum() > ymax: ymax = hs2.GetMaximum()*1.15
    if herr2.GetMaximum() > ymax: ymax = herr2.GetMaximum()*1.15
    if isNevts:  print "h2Int ",  h2.GetBinContent(1), h2.GetBinError(1)
#    if hsOpt['hname']=="h_jets_n":  print "h2Int ",  h2.Integral(), h2.GetBinError(1)

    #print herr1.GetBinContent(1), herr1.GetBinError(1)

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
    if len(legstack1) > 1:
        #for n, leg in enumerate(legstack1):
        #    legend.AddEntry(hlist1[n], leg)
        legend.AddEntry(hlist1[0], legstack1[0])
        #legend.AddEntry(hlist1[len(hlist1)-2], legstack1[1]) #debug
        #legend.AddEntry(hlist1[len(hlist1)-1], legstack1[2]) #debug
        legend.AddEntry(hlist1[len(hlist1)-1], legstack1[1]) #debug
    else:
        legend.AddEntry(hlist1[len(hlist1)-1], legstack1[0])
    legend.AddEntry(hlist2[len(hlist2)-1], legstack2[0]) #debug - one leg for second samplelist
    legend.Draw("same")
    #-------------

    hs1.SetMaximum(ymax)
    herr1.SetMaximum(ymax)
    hs1.Draw("HISTsame")
    if len(hlist1)>1: herr1.Draw("E2same")
    else: herr1.Draw("Esame")
    hs2.SetMaximum(ymax)
    herr2.SetMaximum(ymax)
    if dofill[1]: hs2.Draw("HISTsame")
    else: hs2.Draw("Esame")
    #if len(hlist2)>1: herr2.Draw("E2same")
    herr2.Draw("Esame")

    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0
    if isNevts: 
#    if hsOpt['hname']=='h_jets_n': 
        nev1 = herr1.GetBinContent(1)
        nev2 = herr2.GetBinContent(1)
        nev1err = herr1.GetBinError(1)
        nev2err = herr2.GetBinError(1)
    #nev1 = herr1.Integral()
    #nev2 = herr2.Integral()
    #nev1err = herr1.Integral()
    #nev2err = herr2.Integral()

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
#    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    if residuals: # data as h2!!!
        if residuals>1:
            c2 = TCanvas("c2", "r"+hsOpt['hname'], 800, 800)    
            c2.Divide(1,2)
            c2.cd(1)
        else:
            c2 = TCanvas("c2", "r"+hsOpt['hname'], 800, 400)
        hres = h2.Clone("h_res")
      #  hres = h2.Reset()
        checkbin = False
        for i in range(1, hres.GetXaxis().GetNbins()+1):
            n1 = h1.GetBinContent(i)
            n2 = h2.GetBinContent(i)
            e1 = h1.GetBinError(i)
            e2 = h2.GetBinError(i)
            if n1 and n2 and e1 and e2 : 
                hres.SetBinContent(i,(n2-n1)/math.sqrt(e1*e1+e2*e2)) #debug v1
            #elif not checkbin: hres.SetBinContent(i,0) #to avoid error
               # hres.SetBinError(i,1)
                err = (pow(n1,3) + 15*pow(n1,2)*n2+15*pow(n2,2)*n1 + pow(n2,3))/(4*pow((n1+n2),3))
                hres.SetBinError(i, err)
     # to chek just histos ratio:
     #  hres = Hist(10,0,1, name="")
     #  hres = hdiff.Clone("h_residual")
     #  hres.Divide(h1)

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
            for i in range(0, hres.GetXaxis().GetNbins()): #improve
                if (not hres.IsBinOverflow(i)) and (math.fabs(hres.GetBinContent(i)) != 0):
                    res_a.append(hres.GetBinContent(i))
            res_pull = Hist(60, -6., 6, name = "h_res_pull")
            res_pull.GetXaxis().SetTitle("residuals (sigma units)")
            for v in res_a: res_pull.fill(v)
            res_pull.Fit("gaus", "ILL")
            res_pull.Draw("E X0")

        c2.Update()    
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.pdf")
        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.png")            
#        c2.SaveAs(oDir+"/"+hsOpt['hname']+"_res.root")   

    return [nev1,nev1err,nev2,nev2err]
#------------

def drawH1tdr(hlist1, snames1, leg1, hsOpt, residuals, norm, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
    c1 = TCanvas("c1", hsOpt['hname'], 800, 800)       

    if rebin > 0: rb = rebin
    else: rb =  hsOpt['rebin']

    ymax = 0.
    nh1 = hlist1[0].Integral()
#    for i, h in enumerate(hlist1):         

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
        print scale
        col = colors[i]
        print hsOpt['xmin'], hsOpt['xmax']
        h.GetXaxis().SetRangeUser(hsOpt['xmin'],hsOpt['xmax'])
        h.SetMinimum(0.)
        h.Scale(scale)
        h.Rebin(rb)
        h.SetMarkerStyle(8)
        h.SetMarkerSize(0.)
        if dofill[i]: 
            h.SetFillColorAlpha(col,0.2)
            h.SetFillStyle(1) #samOpt['fillstyle']
        else:     
            h.SetLineWidth(1)         
            h.SetLineColorAlpha(col,0.)
        if i == 0: ymax = h.GetMaximum()*1.15
        h.SetMaximum(ymax)
        if i ==0: h.Draw("HISTsame")
        else: h.Draw("HISTsame")



    nev1 = 0
    nev2 = 0
    nev1err = 0
    nev2err = 0

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
#    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    return [nev1,nev1err,nev2,nev2err]
#------------



def drawH1only(hlist1, snames1, legstack1, hsOpt, oDir, colors, dofill, rebin, headerOpt, isMC):
    gStyle.SetOptStat(False)
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
    if len(legstack1) > 1:
        #for n, leg in enumerate(legstack1):
        #    legend.AddEntry(hlist1[n], leg)
        legend.AddEntry(hlist1[0], legstack1[0])
        legend.AddEntry(hlist1[len(hlist1)-1], legstack1[1])
    else:
        legend.AddEntry(hlist1[len(hlist1)-1], legstack1[0])
    legend.Draw("same")
    #-------------

    hs1.Draw("HISTsame")
    if len(hlist1)>1: herr1.Draw("E2same")
    else: herr1.Draw("Esame")

    nev1 = 0
    nev1err = 0
    if hsOpt['hname']=='h_nevts': 
        nev1 = herr1.GetBinContent(1)
        nev1err = herr1.GetBinError(1)

    c1.Update()    
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".pdf")
    c1.SaveAs(oDir+"/"+hsOpt['hname']+".png")            
#    c1.SaveAs(oDir+"/"+hsOpt['hname']+".root") 

    return [nev1,nev1err]
#-------------------------


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
#        c2.SaveAs(oDir+"/"+name+".root")  

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
    else: latex.DrawLatex(0.90, 0.94, "simulation ") #(13 TeV)
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

def setLegend(doRight, doTop):
    leg = TLegend(0.55,0.70,0.90,0.90)
    leg.SetTextSize(0.032)
    return leg
#------------

