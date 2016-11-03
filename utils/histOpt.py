# database for histograms options
# histName rebin xname xmin xmax xlog yname ymin ymax ylog

hist_opt = {

   "h_nevts" : {
       'hname' : "h_nevts",
       'rebin' : 1,
       'xname' : "",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  :  0,
       'yname' : "num events",
       'ylog'  : "" },

#miscellanea
   "h_met_pt" : {
       'hname' : "h_met_pt",
       'rebin' : 5,
       'xname' : "met pt",
       'xmin'  : 20.,
       'xmax'  : 300.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_mu_n" : {
       'hname' : "h_mu_n",
       'rebin' : 1,
       'xname' : "# muons",
       'xmin'  : 0.,
       'xmax'  : 5.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_mu_pt" : {
       'hname' : "h_mu_pt",
       'rebin' : 5,
       'xname' : "muons pt",
       'xmin'  : 20.,
       'xmax'  : 200.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_mu_iso03" : {
       'hname' : "h_mu_iso03",
       'rebin' : 1,
       'xname' : "muons pfIso03",
       'xmin'  : 0.,
       'xmax'  : 0.1,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },     

   "h_mu0_pt" : {
       'hname' : "h_mu0_pt",
       'rebin' : 5,
       'xname' : "muon0 pt",
       'xmin'  : 20.,
       'xmax'  : 200.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_mu0_iso03" : {
       'hname' : "h_mu0_iso03",
       'rebin' : 1,
       'xname' : "muon0 pfIso03",
       'xmin'  : 0.,
       'xmax'  : 0.1,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },     

   "h_all_ht" : {
       'hname' : "h_all_ht",
       'rebin' : 20,
       'xname' : "ht (mu.pt+jets.pt+met.pt)",
       'xmin'  : 30.,
       'xmax'  : 1500.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },


#jets
   "h_jets_n" : {
       'hname' : "h_jets_n",
       'rebin' : 1,
       'xname' : "# jets",
       'xmin'  : 0.,
       'xmax'  : 15.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_jets_ht" : {
       'hname' : "h_jets_ht",
       'rebin' : 10,
       'xname' : "jets ht",
       'xmin'  : 30.,
       'xmax'  : 1500.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_csv" : {
       'hname' : "h_jet0_csv",
       'rebin' : 5,
       'xname' : "jet0 CSV",
       'xmin'  : 0.5,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_csv" : {
       'hname' : "h_jet1_csv",
       'rebin' : 5,
       'xname' : "jet1 CSV",
       'xmin'  : 0.5,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_csv" : {
       'hname' : "h_jet2_csv",
       'rebin' : 6,
       'xname' : "jet2 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_csv" : {
       'hname' : "h_jet3_csv",
       'rebin' : 6,
       'xname' : "jet3 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_pt" : {
       'hname' : "h_jet0_pt",
       'rebin' : 4,
       'xname' : "jet 0 pT",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_pt" : {
       'hname' : "h_jet1_pt",
       'rebin' : 4,
       'xname' : "jet 1 pT",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_pt" : {
       'hname' : "h_jet2_pt",
       'rebin' : 4,
       'xname' : "jet 2 pT",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_pt" : {
       'hname' : "h_jet3_pt",
       'rebin' : 4,
       'xname' : "jet 3 pT",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0pt_pt" : {
       'hname' : "h_jet0pt_pt",
       'rebin' : 4,
       'xname' : "jet 0 pT (pt sorted)",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1pt_pt" : {
       'hname' : "h_jet1pt_pt",
       'rebin' : 4,
       'xname' : "jet 1 pT (pt sorted)",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2pt_pt" : {
       'hname' : "h_jet2pt_pt",
       'rebin' : 4,
       'xname' : "jet 2 pT (pt sorted)",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3pt_pt" : {
       'hname' : "h_jet3pt_pt",
       'rebin' : 4,
       'xname' : "jet 3 pT (pt sorted)",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

#di-jets


#2-D histos

}
