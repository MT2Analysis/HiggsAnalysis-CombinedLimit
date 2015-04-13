#!/bin/sh
#########################
#
# Driver script for Toy Monte Carlo submission with CRAB 
#
# author: Luca Lista, INFN
#                      
#########################

#echo "================= Dumping Input files ===================="
#python -c "import PSet; print '\n'.join(list(PSet.process.source.fileNames))"

i="$1"
if [ "$i" == "help" ]; then
  echo "usage: combine_crab_exp.sh <job index> <Model>"
  exit 0;
fi
if [ "$i" = "" ]; then
  echo "Error: missing job index"
  exit 1;
fi

I=$(($i-1))

#number of toys
n="250"

#Model
Model="${2##*=}"
count="${3##*=}"

singlePoint=(`python <<END
rAsymptotic=[0.43, 0.77, 0.85, 2.30, 0.77, 1.04, 1.53, 6.95, 1.56, 1.46, 4.55, 3.55, 1.19, 0.71]
rMax=[1.5*r for r in rAsymptotic]
rMin=[0.5*r for r in rAsymptotic]
div=(rMax[$count]-rMin[$count])/20
singlePoint=[rMax[$count], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, rMin[$count]]
for j in range(1, 19):
    singlePoint[j]=singlePoint[j-1]-div
for j in range(0, 20):
    print singlePoint[j]
END`)

#echo ${singlePoint[*]}

# first, link locally the executable:
# ln -s ../../../../bin/slc5_amd64_gcc434/combine .

if [ -e outputToy_${i} ]; then
  rm -rf outputToy_${i}
fi
mkdir outputToy_${i}

echo "Copying library libHiggsAnalysisCombinedLimit.so to $CMSSW_BASE ..."
cp libHiggsAnalysisCombinedLimit.so $CMSSW_BASE/lib/slc*/
echo "Library copied correctly"

echo "Creating input for expected (pre-fit) limits:"
./combine datacard_${Model}_loJet_hiHT_noMT_MT2final.root  -M GenerateOnly -t -1 --expectSignal 0 --saveToys -n ${Model}_${i}
#./combine datacard_${Model}_hiJet_hiHT.root  -M GenerateOnly -t -1 --expectSignal 0 --saveToys -n ${Model}_${i}

echo "job number: seed #$i with $n toys"
./combine datacard_${Model}_loJet_hiHT_noMT_MT2final.root --toysFile higgsCombine${Model}_${i}.GenerateOnly.mH120.123456.root -t-1 -M HybridNew -T $n -i 5 -s $i --testStat LHC --frequentist --saveHybridResult --saveToys --fullBToys -v -1 -n ${Model}_${i} --singlePoint ${singlePoint[$I]} >& log.txt
#./combine datacard_${Model}_hiJet_hiHT.root --toysFile higgsCombine${Model}_${i}.GenerateOnly.mH120.123456.root -t-1 -M HybridNew -T $n -i 10 -s $i --testStat LHC --clsAcc 0 --frequentist --saveHybridResult --saveToys --fullBToys -v -1 -n ${Model}_${i} --singlePoint ${singlePoint[$I]} >& log.txt

mv higgs*.root outputToy_${i}/
mv log.txt outputToy_${i}/
echo "pack the results"
tar cvfz outputToy.tgz outputToy_${i}/
