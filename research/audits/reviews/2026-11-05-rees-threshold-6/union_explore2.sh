#!/bin/sh
# Rerun of union_explore.sh with ALLOWDUP=1 (repeated beta allowed; union targets do not force
# distinct beta).  For each kappa and prime: try every K containing 0 with |K| in {2,3}
# (and K = {0,1,2,3} for kappa = 7): step 1 = rows Z_kappa -> K, step 2 = rows K -> {0}
# (complete search, zeros allowed).  Logs every attempt; FEASIBLE witness lines go to
# uw_k<kappa>_K<K>_s1.out / _s2.out for verify.py.  Stops at the first K that covers p.
export ALLOWDUP=1
try() { k=$1; shift; for p in "$@"; do
  full=$(python3 -c "print(','.join(map(str,range($k))))")
  Ks=$(python3 -c "
import itertools
k=$k
for s in (1,2):
  for c in itertools.combinations(range(1,k),s): print(','.join(map(str,(0,)+c)))
if k==7: print('0,1,2,3')")
  cov=no
  for K in $Ks; do
    tag=$(echo $K | tr ',' '-')
    a=$(./rectu $k "$full" "$K" $p $p 1); sa=$(echo "$a" | awk '{print $2}')
    if [ "$sa" != FEASIBLE ]; then echo "kappa=$k p=$p K=$K step1=$sa"; continue; fi
    b=$(./rectu $k "$K" "0" $p $p 1); sb=$(echo "$b" | awk '{print $2}')
    echo "kappa=$k p=$p K=$K step1=FEASIBLE step2=$sb"
    if [ "$sb" = FEASIBLE ]; then echo "$a" >> uw_k${k}_K${tag}_s1.out; echo "$b" >> uw_k${k}_K${tag}_s2.out
      echo "kappa=$k p=$p COVERED by K=$K"; cov=yes; break; fi
  done
  [ $cov = no ] && echo "kappa=$k p=$p NOT COVERED (all K tried)"
done; }
try 5 11
try 4 5 13 29
try 6 7 13 19 31 43 67 79 139
try 7 29 43 71 113 127 197 211 239 337 631
try 8 17 41 73 89 137 233 761
try 9 19 37 73 109 127 163 181 199 271 307 379 433 487 523
