#!bin/bash

### EXAMPLE (HOW TO RUN):
### sh readPLSignificance_Scan.sh T1tttt 2p3ifb_13Apr_sigContOK

Model=$1
Label=$2

for i in $(ls /scratch/`whoami`/significance_${Model}_${Label}/*txt)
do
    if [[ $i ]]
    then
	#echo $i
	mass=${i##*log_${Model}_}
	mass=${mass%_combined.txt*}
	echo $mass
	significance=$(grep "Significance:" $i | awk '{print $2}')
	pvalue=$(grep "p-value of background:" $i | awk '{print $4}')
	if [[ $pvalue ]] && [[ $pvalue != "-nan" ]]
	then
	#echo $significance
        echo $pvalue
        echo $mass $significance $pvalue  >> significance_${Model}_full_${Label}.txt
	search="_"
	replace=" "
	sed -i "s/$search/$replace/g" significance_${Model}_full_${Label}.txt
	search=")"
	replace=""
	sed -i "s/$search/$replace/g" significance_${Model}_full_${Label}.txt
	fi
    fi
done

