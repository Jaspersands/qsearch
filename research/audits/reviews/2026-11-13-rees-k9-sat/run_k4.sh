#!/bin/zsh
# Runner for the three-level union-target SAT search (sat3.py) at (p, 9, K = {0, m}).
# usage: run_k4.sh p "m1 m2 ..." workdir logfile timeout_s solver "solver options"  (run_k3.sh plus solver options, e.g. --sat)
# For each m: generate CNF, record sha256 prefix, run kissat (timeout 1500 s, nice 19), sample RSS every 5 s
# (kill own solver if RSS > 1.5 GB -> NOT computed), on SAT decode+verify with sat3.py --check.
set -u
P=$1; MS=$2; W=$3; LOG=$4; TO=${5:-1500}; SOLV=${6:-kissat}; OPTS=${7:-}
T=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-12-rees-exponent-k8-attack/sat3.py
PY=/opt/anaconda3/bin/python
cd $W
for m in ${=MS}; do
  K="0,$m"; C=l3_${P}_9_0${m}.cnf
  gen=$(nice -n 19 $PY $(dirname $0)/sat3_stream.py $P 9 $K $C)
  sha=$(shasum -a 256 $C | cut -c1-16)
  t0=$(date +%s)
  nice -n 19 timeout $TO $SOLV ${=OPTS} -q $C > ${C%.cnf}.model 2> ${C%.cnf}.err &
  pid=$!
  maxrss=0
  while kill -0 $pid 2>/dev/null; do
    kp=$(pgrep -P $pid $SOLV 2>/dev/null | head -1)
    for q in $pid $kp; do
      r=$(ps -o rss= -p $q 2>/dev/null | tr -d ' ')
      [[ -n $r && $r -gt $maxrss ]] && maxrss=$r
    done
    if [[ $maxrss -gt 1572864 ]]; then pkill -P $pid $SOLV; kill $pid; echo "KILLED rss" >> ${C%.cnf}.err; fi
    sleep 5
  done
  wait $pid; rc=$?
  t1=$(date +%s)
  res=$(grep '^s ' ${C%.cnf}.model | head -1)
  chk=-
  if [[ $rc -eq 10 ]]; then chk=$(nice -n 19 $PY -I $(dirname $0)/verify_model.py $P 9 $K ${C%.cnf}.model | sed -n 2p); fi
  echo "solver=$SOLV opts=$OPTS timeout=$TO p=$P K=$K $gen sha=$sha rc=$rc res='$res' time=$((t1-t0))s maxrss_kb=$maxrss check='$chk'" >> $LOG
  [[ $rc -ne 10 ]] && rm -f ${C%.cnf}.model
done
echo DONE >> $LOG
