#!bin/bash

for c in {0..13} 
do 
    search="count=$(( $c-1 ))"
    replace="count=$c"
    if [ $c > 0 ]
    then
	sed -i "s/$search/$replace/g" crabConfig_exp.py
    fi
    echo `crab submit -c crabConfig_exp.py`
done