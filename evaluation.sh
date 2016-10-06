#!/bin/bash

# Evaluation script. Run as: ./evaluation.sh <gold_data> <parsed_data>

echo -e "Smatch -> \c"
python smatch_2.0.2/smatch.py -f "$1" "$2"

echo -e "Unlabeled -> \c"
sed 's/:[a-zA-Z0-9-]*/:label/g' "$1" > 1.tmp
sed 's/:[a-zA-Z0-9-]*/:label/g' "$2" > 2.tmp
python smatch_2.0.2/smatch.py -f 1.tmp 2.tmp

echo -e "No WSD -> \c"
cat "$1" | perl -ne 's/(\/ [a-zA-Z0-9\-][a-zA-Z0-9\-]*)-[0-9][0-9]*/\1-01/g; print;' > 1.tmp
cat "$2" | perl -ne 's/(\/ [a-zA-Z0-9\-][a-zA-Z0-9\-]*)-[0-9][0-9]*/\1-01/g; print;' > 2.tmp
python smatch_2.0.2/smatch.py -f 1.tmp 2.tmp


cat "$1" | perl -ne 's/([a-z])[a-z]*([0-9]+)/\1\2/g; print;' | perl -ne 's/^#.*\n//g; print;' | perl -ne 's/_//g; print;' | perl -ne 's/[0-9]+([a-zA-Z]+)/\1/g; print;' > 1.tmp
cat "$2" | perl -ne 's/([a-z])[a-z]*([0-9]+)/\1\2/g; print;' | perl -ne 's/^#.*\n//g; print;' | perl -ne 's/_//g; print;' | perl -ne 's/[0-9]+([a-zA-Z]+)/\1/g; print;' > 2.tmp

python scores.py "1.tmp" "2.tmp"

rm 1.tmp
rm 2.tmp
