#!/bin/bash
# sequential SA runs (one process at a time)
cd "$(dirname "$0")"
while read -r k p a s it K fam; do
  [ -z "$k" ] && continue
  nice -n 10 /opt/anaconda3/bin/python -B sa2.py $k $p $a $s $it $K $fam out/sa2_k${k}_p${p}_a${a}_s${s}.json > out/sa2_k${k}_p${p}_a${a}_s${s}.out 2>&1
done <<CFG
2 1009 5 1 250 8 chain4
3 1009 5 2 250 8 chainfull
2 1009 6 3 200 8 mix
3 1009 6 4 200 8 mix
2 1009 7 5 150 6 chain4
3 1009 7 6 150 6 chainfull
CFG
echo SA2-ALL-DONE
