bms=("20171120-160644-bm0" "20171120-161211-bm1" "20171120-161730-bm2" "20171120-162255-bm3" "20171120-162812-bm4" "20171120-163332-bm5" "20171120-163852-bm6" "20171120-164402-bm7" "20171120-164916-bm8" "20171120-165436-bm9" "20171120-165954-bm10" "20171120-170526-bm11" "20171120-171044-bm12" "20171120-171608-bm13")
i=0
for bm in ${bms[@]}
do
    #python scripts/drawcomp_afterBDT.py -b $bm -l 0 -w 6 --res 2 -n
	#python scripts/drawcomp_afterBDT.py -b $bm -l 0 -w 5 -c --res -1
    #python scripts/drawcomp_postFit.py -b $bm -l 1
	python scripts/drawcomp_afterBDT.py -b $bm -l 0 -w 2072 --res 10 -d ttbar_bias_check/BM$i
	((i++))
done
