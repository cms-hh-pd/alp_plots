# alp_plots
Scripts collection to create plots from alp_analysis output

## TO INSTALL
It has to be cloned inside usual alp working area ('CMSSW_BASE/src/Analysis').
Python based.
Use 'python scriptname' to execute each script.

## CODE STRUCTURE
- utils -> default functions to create plots (stack, 2d, etc.)
- script -> various script to create histos needed for analysis

## SCRIPTS DESCRIPTION

- drawstackH -> to get stacked bkg vs data OR stacked bkg vs signal
                Used for: 
			- trigger efficiency plots
			- selection of mva input variables

- drawcompH -> to get comparison of distros from the same Sample after different selections
                Used for: 
			- compare categories with different number of btags
