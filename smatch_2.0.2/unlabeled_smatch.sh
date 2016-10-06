#!/bin/bash

cat "$1" | grep "#" -v > "$1.filt"
cat "$2" | grep "#" -v > "$2.filt"

./unlabel_data.py "$1.filt" > "$1.unlab"
./unlabel_data.py "$2.filt" > "$2.unlab"

python smatch.py -f "$1.unlab" "$2.unlab"

rm *.filt
