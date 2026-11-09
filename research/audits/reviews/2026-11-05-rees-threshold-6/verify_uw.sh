#!/bin/sh
# Verify every union-chain witness file written by union_explore2.sh (step 1: rows Z_k -> K;
# step 2: rows K -> {0}).  Output: v_uw.out.
: > v_uw.out
for f in uw_k*_s1.out; do
  k=$(echo $f | sed 's/uw_k\([0-9]*\)_K.*/\1/'); K=$(echo $f | sed 's/.*_K\([0-9-]*\)_s1.out/\1/' | tr '-' ',')
  full=$(python3 -c "print(','.join(map(str,range($k))))")
  echo "== $f" >> v_uw.out; /opt/anaconda3/bin/python verify.py $k $full $K $f --zeros >> v_uw.out
  g=$(echo $f | sed 's/_s1/_s2/')
  echo "== $g" >> v_uw.out; /opt/anaconda3/bin/python verify.py $k $K 0 $g --zeros >> v_uw.out
done
