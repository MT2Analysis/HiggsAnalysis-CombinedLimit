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
  echo "usage: combine_crab_sig.sh <job index> <Model>"
  exit 0;
fi
if [ "$i" = "" ]; then
  echo "Error: missing job index"
  exit 1;
fi

#number of toys
n="250"

#Model
Model="${2##*=}"

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
./combine datacard_${Model}_hiJet_mergeHT.root  -M GenerateOnly -t -1 --expectSignal 0 --saveToys -n ${Model}_${i}

echo "job number: seed #$i with $n toys"
#./combine datacard_${Model}_hiJet_mergeHT.root --toysFile higgsCombine${Model}_${i}.GenerateOnly.mH120.123456.root -t-1 -M HybridNew -T $n -i 10 -s $i --significance --testStat LHC --clsAcc 0 --frequentist --saveHybridResult --saveToys --fullBToys -v -1 -n ${Model}_${i} >& log.txt
./combine datacard_${Model}_hiJet_mergeHT.root --toysFile higgsCombine${Model}_${i}.GenerateOnly.mH120.123456.root -t-1 -M HybridNew -T $n -i 10 -s $i --significance --frequentist --saveHybridResult --saveToys --fullBToys -v -1 -n ${Model}_${i} >& log.txt

mv higgs*.root outputToy_${i}/
mv log.txt outputToy_${i}/
echo "pack the results"
tar cvfz outputToy.tgz outputToy_${i}/
