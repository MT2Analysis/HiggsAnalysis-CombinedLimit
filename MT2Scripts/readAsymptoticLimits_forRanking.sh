#!bin/bash

Model=$1
#Model='T2qq_1200_850'

workDir=/scratch/`whoami`/ranking/
cd $workDir

for i in $(ls ranking_${Model}/log_${Model}*Paper*post*)
do
    if [[ $i ]]
    then
	#echo $i
	region=${i##*log_${Model}_}
	region=${region%_Paper_post.txt*}
	#echo $region
	limit=$(grep "50.0%" $i | awk '{print $5}')
	obslimit=$(grep "Observed" $i | awk '{print $5}')
	if [[ $limit ]]
	then
            yield=$(grep rate /scratch/`whoami`/datacards/datacards_${Model}/datacard_${region}_m*_${Model}.txt | awk '{ sum+=$2} END {print sum}')
            bkg=$(grep rate /scratch/`whoami`/datacards/datacards_${Model}/datacard_${region}_m*_${Model}.txt | awk '{ sum+=$3+$4+$5} END {print sum}')
	    echo $region $limit $obslimit $yield $bkg>> AsymptoticRanking_${Model}_Paper_post.txt
	    
	    echo $region >> AsymptoticRanking_${Model}_Paper_post_plusBG.txt
	    for d in $(ls -rt /scratch/`whoami`/datacards/datacards_${Model}/datacard_${region}_m*)
	    do
		bin=${d##*${region}_}
		bin=${bin%_${Model}.txt}
		thisyield=$(grep rate /scratch/`whoami`/datacards/datacards_${Model}/datacard_${region}_${bin}_${Model}.txt | awk '{ sum=$2} END {print sum}')
		thisbkg=$(grep rate /scratch/`whoami`/datacards/datacards_${Model}/datacard_${region}_${bin}_${Model}.txt | awk '{ sum=$3+$4+$5} END {print sum}')
		echo $bin '&' $thisyield '&' $thisbkg '\\'>>AsymptoticRanking_${Model}_Paper_post_plusBG.txt
	    done

	fi
    fi
done

cd -
