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
       'xname' : "met pt [GeV]",
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
       'xname' : "muons pt [GeV]",
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
       'xmax'  : 0.3,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },     

   "h_mu_iso04" : {
       'hname' : "h_mu_iso04",
       'rebin' : 1,
       'xname' : "muons pfIso04",
       'xmin'  : 0.,
       'xmax'  : 0.3,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_mu0_pt" : {
       'hname' : "h_mu0_pt",
       'rebin' : 5,
       'xname' : "muon0 pt [GeV]",
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
       'xmax'  : 0.20,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },     

   "h_mu0_iso04" : {
       'hname' : "h_mu0_iso04",
       'rebin' : 1,
       'xname' : "muon0 pfIso04",
       'xmin'  : 0.,
       'xmax'  : 0.20,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_all_ht" : {
       'hname' : "h_all_ht",
       'rebin' : 20,
       'xname' : "ht (mu.pt+jets.pt+met.pt) [GeV]",
       'xmin'  : 30.,
       'xmax'  : 1500.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },


#jets
   "h_njets" : {
       'hname' : "h_njets",
       'rebin' : 1,
       'xname' : "# jets",
       'xmin'  : 0.,
       'xmax'  : 15.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

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
       'xname' : "jets ht [GeV]",
       'xmin'  : 0.,
       'xmax'  : 1500.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jets_ht_r" : {
       'hname' : "h_jets_ht_r",
       'rebin' : 5,
       'xname' : "additional jets ht [GeV]",
       'xmin'  : 0.,
       'xmax'  : 800.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jets_csv" : {
       'hname' : "h_jets_csv",
       'rebin' : 2,
       'xname' : "jets CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_csv" : {
       'hname' : "h_jet0_csv",
       'rebin' : 2,
       'xname' : "jet0 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_csv" : {
       'hname' : "h_jet1_csv",
       'rebin' : 2,
       'xname' : "jet1 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_csv" : {
       'hname' : "h_jet2_csv",
       'rebin' : 2,
       'xname' : "jet2 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_csv" : {
       'hname' : "h_jet3_csv",
       'rebin' : 2,
       'xname' : "jet3 CSV",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jets_cmva" : {
       'hname' : "h_jets_cmva",
       'rebin' : 4, 
       'xname' : "jets CMVA",
       'xmin'  : -1.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_cmva" : {
       'hname' : "h_jet0_cmva",
       'rebin' : 4, 
       'xname' : "jet0 CMVA",
       'xmin'  : -1.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_cmva" : {
       'hname' : "h_jet1_cmva",
       'rebin' : 4, 
       'xname' : "jet1 CMVA",
       'xmin'  : -1.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_cmva" : {
       'hname' : "h_jet2_cmva",
       'rebin' : 4, 
       'xname' : "jet2 CMVA",
       'xmin'  : -1.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_cmva" : {
       'hname' : "h_jet3_cmva",
       'rebin' : 4, 
       'xname' : "jet3 CMVA",
       'xmin'  : -1., #0.1,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jets_pt" : {
       'hname' : "h_jets_pt",
       'rebin' : 4,
       'xname' : "jets pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_pt" : {
       'hname' : "h_jet0_pt",
       'rebin' : 4,
       'xname' : "jet 0 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 400.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_pt" : {
       'hname' : "h_jet1_pt",
       'rebin' : 4,
       'xname' : "jet 1 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 400.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_pt" : {
       'hname' : "h_jet2_pt",
       'rebin' : 4,
       'xname' : "jet 2 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 400.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_pt" : {
       'hname' : "h_jet3_pt",
       'rebin' : 4,
       'xname' : "jet 3 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 400,
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
       'xname' : "jet 1 pT (pt sorted) [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2pt_pt" : {
       'hname' : "h_jet2pt_pt",
       'rebin' : 4,
       'xname' : "jet 2 pT (pt sorted) [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3pt_pt" : {
       'hname' : "h_jet3pt_pt",
       'rebin' : 4,
       'xname' : "jet 3 pT (pt sorted) [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jets_eta" : {
       'hname' : "h_jets_eta",
       'rebin' : 2,
       'xname' : "jets |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0_eta" : {
       'hname' : "h_jet0_eta",
       'rebin' : 2,
       'xname' : "jet 0 #eta",
       'xmin'  : -3.5,
       'xmax'  : 3.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet1_eta" : {
       'hname' : "h_jet1_eta",
       'rebin' : 2,
       'xname' : "jet 1 #eta",
       'xmin'  : -3.5,
       'xmax'  : 3.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet2_eta" : {
       'hname' : "h_jet2_eta",
       'rebin' : 2,
       'xname' : "jet 2 #eta",
       'xmin'  : -3.5,
       'xmax'  : 3.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet3_eta" : {
       'hname' : "h_jet3_eta",
       'rebin' : 2,
       'xname' : "jet 3 #eta",
       'xmin'  : -3.5,
       'xmax'  : 3.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_jet0pt_pt" : {
       'hname' : "h_jet0pt_pt",
       'rebin' : 4,
       'xname' : "jet 0 pT (pt sorted) [GeV]",
       'xmin'  : 0.,
       'xmax'  : 900.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

#di-jets
   "h_H0_mass" : {
       'hname' : "h_H0_mass",
       'rebin' : 4,
       'xname' : "leading di-jet mass [GeV]",
       'xmin'  : 0.,
       'xmax'  : 600.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_mass" : {
       'hname' : "h_H1_mass",
       'rebin' : 4,
       'xname' : "trailing di-jet mass [GeV]",
       'xmin'  : 0.,
       'xmax'  : 600.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

     "h_H0_pt" : {
       'hname' : "h_H0_pt",
       'rebin' : 6,
       'xname' : "leading di-jet pt [GeV]",
       'xmin'  : 0.,
       'xmax'  : 700.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_pt" : {
       'hname' : "h_H1_pt",
       'rebin' : 6,
       'xname' : "trailing di-jet pt [GeV]",
       'xmin'  : 0.,
       'xmax'  : 700.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_eta" : {
       'hname' : "h_H0_eta",
       'rebin' : 4,
       'xname' : "leading di-jet #eta",
       'xmin'  : -4.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_eta" : {
       'hname' : "h_H1_eta",
       'rebin' : 4,
       'xname' : "trailing di-jet #eta",
       'xmin'  : -4.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_csthst0_a" : {
       'hname' : "h_H0_csthst0_a",
       'rebin' : 4,
       'xname' : "jet0 vs leading di-jet |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_csthst1_a" : {
       'hname' : "h_H0_csthst1_a",
       'rebin' : 4,
       'xname' : "jet1 vs leading di-jet |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_csthst2_a" : {
       'hname' : "h_H1_csthst2_a",
       'rebin' : 4,
       'xname' : "jet2 vs trailing di-jet |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_csthst3_a" : {
       'hname' : "h_H1_csthst3_a",
       'rebin' : 4,
       'xname' : "jet3 vs trailing di-jet |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_dr" : {
       'hname' : "h_H0_dr",
       'rebin' : 2,
       'xname' : "leading di-jet #Delta R",
       'xmin'  : 0.,
       'xmax'  : 5.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_dr" : {
       'hname' : "h_H1_dr",
       'rebin' : 2,
       'xname' : "trailing di-jet #Delta R",
       'xmin'  : 0.,
       'xmax'  : 5.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_deta_a" : {
       'hname' : "h_H0_deta_a",
       'rebin' : 4,
       'xname' : "leading di-jet |#Delta#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_deta_a" : {
       'hname' : "h_H1_deta_a",
       'rebin' : 4,
       'xname' : "trailing di-jet |#Delta#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_dphi_a" : {
       'hname' : "h_H0_dphi_a",
       'rebin' : 4,
       'xname' : "leading di-jet |#Delta#phi|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_dphi_a" : {
       'hname' : "h_H1_dphi_a",
       'rebin' : 4,
       'xname' : "trailing di-jet |#Delta#phi|",
       'xmin'  : 0,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0_dphi" : {
       'hname' : "h_H0_dphi",
       'rebin' : 2,
       'xname' : "leading di-jet #Delta#phi",
       'xmin'  : -4,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H1_dphi" : {
       'hname' : "h_H1_dphi",
       'rebin' : 2,
       'xname' : "trailing di-jet #Delta#phi",
       'xmin'  : -4,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_X_mass" : {
       'hname' : "h_X_mass",
       'rebin' : 10,
       'xname' : "X mass [GeV]",
       'xmin'  : 0.,
       'xmax'  : 1200.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_mass" : {
       'hname' : "h_H0H1_mass",
       'rebin' : 10,
       'xname' : "di-higgs candidate mass [GeV]",
       'xmin'  : 0.,
       'xmax'  : 1500.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_pt" : {
       'hname' : "h_H0H1_pt",
       'rebin' : 6,
       'xname' : "di-higgs candidate pt [GeV]",
       'xmin'  : 0.,
       'xmax'  : 700.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_eta" : {
       'hname' : "h_H0H1_eta",
       'rebin' : 4,
       'xname' : "di-higgs candidate #eta",
       'xmin'  : -6.,
       'xmax'  : 6.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_csthst0_a" : {
       'hname' : "h_H0H1_csthst0_a",
       'rebin' : 4,
       'xname' : "leading di-jet vs di-higgs |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_csthst1_a" : {
       'hname' : "h_H0H1_csthst1_a",
       'rebin' : 4,
       'xname' : "trailing di-jet vs di-higgs |cos#theta*|",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_dr" : {
       'hname' : "h_H0H1_dr",
       'rebin' : 2,
       'xname' : "di-higgs candidate #Delta R",
       'xmin'  : 0.,
       'xmax'  : 6.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_deta_a" : {
       'hname' : "h_H0H1_deta_a",
       'rebin' : 4,
       'xname' : "di-higgs candidate |#Delta#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_dphi_a" : {
       'hname' : "h_H0H1_dphi_a",
       'rebin' : 2,
       'xname' : "di-higgs candidate |#Delta#phi|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_H0H1_dphi" : {
       'hname' : "h_H0H1_dphi",
       'rebin' : 2,
       'xname' : "di-higgs candidate #Delta#phi",
       'xmin'  : -4.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

#2-D histos
   "h_H0_H1_mass" : {
       'hname' : "h_H0_H1_mass",
       'rebin' : 10,
       'xname' : "leading di-jet mass [GeV]",
       'xmin'  : 0.,
       'xmax'  : 600.,
       'yname' : "trailing di-jet mass [GeV]",
       'ymin'  : 0.,
       'ymax'  : 600. },

   "h2_bdt" : {
       'hname' : "h2_bdt",
       'rebin' : 1,
       'xname' : "bdt output",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'yname' : "bdt output",
       'ymin'  : 0.,
       'ymax'  : 1. },

#bdt
   "h_bdt_allVar" : {
       'hname' : "h_bdt_allVar",
       'rebin' : 4,
       'xname' : "bdt output allVar",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_bdt_massVar" : {
       'hname' : "h_bdt_massVar",
       'rebin' : 4,
       'xname' : "bdt output massVar",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_bdt_HHVar" : {
       'hname' : "h_bdt_HHVar",
       'rebin' : 4,
       'xname' : "bdt output HHVar",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

################################
#after BDT (new plots)

   "classifier" : {
       'hname' : "classifier",
       'rebin' : 1,
       'xname' : "BDT output",
       'xmin'  : 0.2,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "classifier_log" : {
       'hname' : "classifier_log",
       'rebin' : 1,
       'xname' : "BDT output",
       'xmin'  : 0.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_cmva3" : {
       'hname' : "h_cmva3",
       'rebin' : 4, 
       'xname' : "3rd CMVA (cmva sorted)",
       'xmin'  : -1.,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_cmva4" : {
       'hname' : "h_cmva4",
       'rebin' : 4, 
       'xname' : "4th CMVA (cmva sorted)",
       'xmin'  : -1., #0.1,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_csv3" : {
       'hname' : "h_csv3",
       'rebin' : 4, 
       'xname' : "3rd CSV (csv sorted)",
       'xmin'  : 0.1,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_csv4" : {
       'hname' : "h_csv4",
       'rebin' : 4, 
       'xname' : "4th CSV (csv sorted)",
       'xmin'  : 0.1,
       'xmax'  : 1.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjets_n" : {
       'hname' : "h_gjets_n",
       'rebin' : 1,
       'xname' : "# gen jets",
       'xmin'  : 0.,
       'xmax'  : 15.,
       'xlog'  :  0,
       'yname' : "",
       'ylog'  : "" },

   "h_gjets_pt" : {
       'hname' : "h_gjets_pt",
       'rebin' : 4,
       'xname' : "gen jets pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 400.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet0_pt" : {
       'hname' : "h_gjet0_pt",
       'rebin' : 4,
       'xname' : "jet 0 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet1_pt" : {
       'hname' : "h_gjet1_pt",
       'rebin' : 4,
       'xname' : "jet 1 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet2_pt" : {
       'hname' : "h_gjet2_pt",
       'rebin' : 4,
       'xname' : "jet 2 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet3_pt" : {
       'hname' : "h_gjet3_pt",
       'rebin' : 4,
       'xname' : "jet 3 pT [GeV]",
       'xmin'  : 0.,
       'xmax'  : 300,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjets_eta" : {
       'hname' : "h_gjets_eta",
       'rebin' : 2,
       'xname' : "gen jets |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.5,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet0_eta" : {
       'hname' : "h_gjet0_eta",
       'rebin' : 1,
       'xname' : "jet 0 |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet1_eta" : {
       'hname' : "h_gjet1_eta",
       'rebin' : 1,
       'xname' : "jet 1 |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet2_eta" : {
       'hname' : "h_gjet2_eta",
       'rebin' : 1,
       'xname' : "jet 2 |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },

   "h_gjet3_eta" : {
       'hname' : "h_gjet3_eta",
       'rebin' : 1,
       'xname' : "jet 3 |#eta|",
       'xmin'  : 0.,
       'xmax'  : 4.,
       'xlog'  : "",
       'yname' : "",
       'ylog'  : "" },


  
}
