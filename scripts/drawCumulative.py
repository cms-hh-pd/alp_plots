from ROOT import *

def drawCumulative(filename):
    hlist = [] 
    tf = TFile(filename)
    if not tf: 
        print "WARNING: files do not exist" 
    
    bkg = tf.Get("bkg_test/classifier-20171219-100739-bm-1_bkg_test")
    tt = tf.Get("sig_test/classifier-20171219-100739-bm-1_sig_test")
    tth = tf.Get("ttHTobb/classifier-20171219-100739-bm-1_ttHTobb")
    sig = tf.Get("HHTo4B_pangea/classifier-20171219-100739-bm-1_HHTo4B_pangea")
    bkg.SetLineColor(kBlue)
    tt.SetLineColor(kRed)
    tth.SetLineColor(kGreen)
    sig.SetLineColor(kBlack)
    print(bkg, tt)
    for hist in [bkg, tt, tth, sig]:
      hist.SetLineWidth(2)
      hist.Scale(1./hist.Integral())
      mysum = 0.
      for b in range(bkg.GetNbinsX()+1):
        mybin = hist.GetBinContent(b)
        mysum += mybin
        hist.SetBinContent(b, mysum)
        print hist, hist.GetBinLowEdge(b), mysum
  
    t = TCanvas("a", "a", 1000,1000)
    bkg.Draw("hist")
    tt.Draw("SAME hist")
    tth.Draw("SAME hist")
    sig.Draw("SAME hist")
    leg = TLegend(0.12,0.66,0.5,0.86)
    leg.SetTextSize(0.033);
    leg.SetFillColor(0);
    leg.SetNColumns(1);
    #pl2.SetHeader(training);
    leg.AddEntry(bkg, "Mixed data",  "L")
    leg.AddEntry(tt, "ttbar",  "L")
    leg.AddEntry(tth, "ttH",  "L")
    leg.AddEntry(sig, "HH",  "L")
    leg.Draw("same")
    t.SaveAs("cumulative.png")

if __name__ == "__main__":
  filename = "/lustre/cmswork/atiko/Hbb/CMSSW_8_0_25/src/Analysis/hh2bbbb_limit/classifier_reports/ttbar_20171219/20171219-withtth-andSM.root"
  drawCumulative(filename)
