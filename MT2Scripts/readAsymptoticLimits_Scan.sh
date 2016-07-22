#!bin/bash

### EXAMPLE (HOW TO RUN):
### sh readAsymptoticLimits_Scan.sh T1tttt 2p3ifb_13Apr_sigContOK

Model=$1
Label=$2
#Model='T1tttt'

for i in $(ls /scratch/casal/limits_${Model}_${Label}/*txt)
do
    if [[ $i ]]
    then
	#echo $i
	mass=${i##*log_${Model}_}
	mass=${mass%_combined.txt*}
	echo $mass
	limit=$(grep "50.0%" $i | awk '{print $5}')
	limit_ps=$(grep "84.0%" $i | awk '{print $5}')
	limit_ms=$(grep "16.0%" $i | awk '{print $5}')
	limit_p2s=$(grep "97.5%" $i | awk '{print $5}')
	limit_m2s=$(grep "2.5%" $i | awk '{print $5}')
	limit_obs=$(grep "Observed" $i | awk '{print $5}')
	if [[ $limit ]]
	then
	echo $mass $limit $limit_obs $limit_ps $limit_ms $limit_p2s $limit_m2s  >> limits_${Model}_full_${Label}.txt
	search="_"
	replace=" "
	sed -i "s/$search/$replace/g" limits_${Model}_full_${Label}.txt
	fi
    fi
done

#for i in $(ls /scratch/mmasciov/limits_T1tttt_2p3ifb_13Apr_sigContOK/*txt)
#do
#    if [[ $i ]]
#    then
#	#echo $i
#	mass=${i##*log_${Model}_}
#	mass=${mass%_2p3ifb.txt*}
#	echo $mass
#	limit=$(grep "50.0%" $i | awk '{print $5}')
#	limit_ps=$(grep "84.0%" $i | awk '{print $5}')
#	limit_ms=$(grep "16.0%" $i | awk '{print $5}')
#	limit_p2s=$(grep "97.5%" $i | awk '{print $5}')
#	limit_m2s=$(grep "2.5%" $i | awk '{print $5}')
#	limit_obs=$(grep "Observed" $i | awk '{print $5}')
#	if [[ $limit ]]
#	then
#	echo $mass $limit $limit_obs $limit_ps $limit_ms $limit_p2s $limit_m2s  >> limits_${Model}_full_13Apr_sigContOK.txt
#	search="_"
#	replace=" "
#	sed -i "s/$search/$replace/g" limits_${Model}_full_13Apr_sigContOK.txt
#	fi
#    fi
#done
