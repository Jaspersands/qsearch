#!/bin/zsh
# Mechanical item 8 (topic note section 12.14): the 17 drawn kappa = 7, lambda ~ 0.3 primes, seeds 31..63 odd in
# draw order, rules frozen in predictions_k7_tail.txt (revisions 1-2). Two queues (two cores). Outputs outside the
# repo: $1 is the output directory. Logs in tail7/.
cd "${0:A:h}"
OUT=$1
P=(34147 34217 34231 34511 34651 34679 34721 34819 35141 35393 35533 35603 35617 35771 35897 35911 36107)
q() {
  local i=$1
  while (( i <= ${#P} )); do
    local p=${P[$i]} s=$(( 29 + 2 * i ))
    if [[ ! -f $OUT/mc_k7_p${p}_s${s}.npz ]]; then
      nice -n 19 /opt/anaconda3/bin/python -I mc_classes.py 7 $p 6000 --seed $s --out $OUT/mc_k7_p${p}_s${s}.npz > tail7/mc_k7_p${p}_s${s}.log 2>&1
    fi
    i=$(( i + 2 ))
  done
}
q 1 &
q 2 &
wait
echo ALL DONE
