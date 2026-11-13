#!/bin/zsh
# three-level JOINT contraction (K = {0}) at (73, 9): sat3_stream.py CNF + kissat, timeout 1500 s, RSS cap 1.5 GB.
set -u
S=/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/265ea4e4-9d06-4353-9b18-ca6cd6e80035/scratchpad/k9bn
KS=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-13-rees-k9-sat
OUT=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-13-rees-k9-bottleneck
P=$1; K=$2; TO=${3:-1500}
C=$S/l3_${P}_9_${K//,/}.cnf
gen=$(nice -n 19 /opt/anaconda3/bin/python $KS/sat3_stream.py $P 9 $K $C)
sha=$(shasum -a 256 $C | cut -c1-16)
t0=$(date +%s)
nice -n 19 timeout $TO kissat -q $C > ${C%.cnf}.model 2> ${C%.cnf}.err &
pid=$!; maxrss=0
while kill -0 $pid 2>/dev/null; do
  for q in $pid $(pgrep -P $pid 2>/dev/null); do
    r=$(ps -o rss= -p $q 2>/dev/null | tr -d ' '); [[ -n $r && $r -gt $maxrss ]] && maxrss=$r
  done
  if [[ $maxrss -gt 1572864 ]]; then pkill -P $pid; kill $pid; echo KILLED_RSS >> ${C%.cnf}.err; fi
  sleep 5
done
wait $pid; rc=$?; t1=$(date +%s)
res=$(grep '^s ' ${C%.cnf}.model | head -1)
chk=-
if [[ $rc -eq 10 ]]; then chk=$(nice -n 19 /opt/anaconda3/bin/python -I $KS/verify_model.py $P 9 $K ${C%.cnf}.model | sed -n 2p); gzip -c ${C%.cnf}.model > $OUT/model_${P}_9_${K//,/}.txt.gz; fi
echo "p=$P K=$K $gen sha=$sha rc=$rc res='$res' time=$((t1-t0))s maxrss_kb=$maxrss check='$chk'" >> $OUT/sat_runs.log
