data=$3
echo "LANGUAGE $1"
echo "silver ($2)"
./evaluation.sh $data/$2-test.$1-en.parsed ../data/$2-test.txt.graphs

echo "gold"
./evaluation.sh $data/ldc.$1-en.parsed ../data/deft-p2-amr-r1-amrs-test-all.txt.graphs

echo "full-cycle"
./evaluation.sh $data/ldc.en-$1-en.parsed ../data/deft-p2-amr-r1-amrs-test-all.txt.graphs
