# alp_plots
Scripts collection to create plots from alp_analysis and hh2bbbb_limit output

## TO INSTALL
It has to be cloned inside usual alp working area ('CMSSW_BASE/src/Analysis').
Python based.
Use 'python scriptname' to execute each script.

## CODE STRUCTURE
- utils -> default functions to create plots (stack, 2d, etc.)
- script -> various script to create histos needed for analysis

## DESCRIPTION

General idea: 
  compare two binned histograms with defined normalization. Input are always histograms. 
     - the two histograms can be made by stack of multiple histograms.
     - colors, legends, binning can be costumized
     - default weights (PU, BTag, ...) must have been applied already to input histograms.
                 
Scripts:
 - drawcomp_afterBDT -> to plot ditributions from classifier report output, e.g.
    - get sig vs MC bkg (pangea not reweighted after alp_analysis!
    - trigger efficiency plots
    - selection of mva input variables
 - drawcomp_preBDT -> to plot ditributions from alp_analysis
    - get sig vs MC bkg (only single signal sample)
    - compare MC bkgs
    - compare signals
    - plot single sample distributions
    - N.B. if weights vector is null, weights are taken from h_w_oneInvFb histogram (to normalized to 1Fb-1)
    CMD: python scripts/drawcomp_preBDT.py -w 2 -o test (-c --res -1)

 - drawcomp_trgEff -> to plot ditributions for trigger efficiency study (not maintained)

 - drawcomp_tktdr -> to plot ditributions for phase2 tracker TDR (not maintained)
