#!/bin/bash

# Evaluation script. Run as: ./evaluation.sh <parsed_data> <gold_data>

out=`python smatch/smatch.py --pr -f "$1" "$2"`
pr=`echo $out | cut -d' ' -f2`
rc=`echo $out | cut -d' ' -f4`
fs=`echo $out | cut -d' ' -f6`
echo 'Smatch -> P: '$pr', R: '$rc', F: '$fs

sed 's/:[a-zA-Z0-9-]*/:label/g' "$1" > 1.tmp
sed 's/:[a-zA-Z0-9-]*/:label/g' "$2" > 2.tmp
out=`python smatch/smatch.py --pr -f 1.tmp 2.tmp`
pr=`echo $out | cut -d' ' -f2`
rc=`echo $out | cut -d' ' -f4`
fs=`echo $out | cut -d' ' -f6`
echo 'Unlabeled -> P: '$pr', R: '$rc', F: '$fs 

cat "$1" | perl -ne 's/(\/ [a-zA-Z0-9\-][a-zA-Z0-9\-]*)-[0-9][0-9]*/\1-01/g; print;' > 1.tmp
cat "$2" | perl -ne 's/(\/ [a-zA-Z0-9\-][a-zA-Z0-9\-]*)-[0-9][0-9]*/\1-01/g; print;' > 2.tmp
out=`python smatch/smatch.py --pr -f 1.tmp 2.tmp`
pr=`echo $out | cut -d' ' -f2`
rc=`echo $out | cut -d' ' -f4`
fs=`echo $out | cut -d' ' -f6`
echo 'No WSD -> -> P: '$pr', R: '$rc', F: '$fs

cat "$1" | perl -ne 's/^#.*\n//g; print;' | tr '\t' ' ' | tr -s ' ' > 1.tmp
cat "$2" | perl -ne 's/^#.*\n//g; print;' | tr '\t' ' ' | tr -s ' ' > 2.tmp
python scores.py "1.tmp" "2.tmp"

rm 1.tmp
rm 2.tmp
