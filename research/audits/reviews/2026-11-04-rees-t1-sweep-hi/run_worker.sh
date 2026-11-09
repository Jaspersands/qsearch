#!/bin/sh
# run_worker.sh W : worker W (0..3) runs chunks W, W+4, W+8, W+12 of chunks.txt with
# famsym_direct (T1, window 3072), then retries its NOTFOUND primes (retry.sh).
# Outputs: out/cNN.out (one FOUND/NOTFOUND line per prime, flushed per line),
#          out/worker_W.log, out/notfound_wW.txt, out/retry_wW.out.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-t1-sweep-hi
cd "$D" || exit 1
W=$1
mkdir -p out
for i in $W $((W+4)) $((W+8)) $((W+12)); do
  n=$(printf "c%02d" $i)
  line=$(grep "^$n " chunks.txt)
  lo=$(echo $line | awk '{print $2}'); hi=$(echo $line | awk '{print $3}')
  if grep -q '^DONE' out/$n.out 2>/dev/null; then echo "$(date) $n already done" >> out/worker_$W.log; continue; fi
  echo "$(date) start $n ($lo,$hi]" >> out/worker_$W.log
  ./famsym_direct 8 $((lo+1)) $hi 200000 50 $((1000+i)) win=3072 > out/$n.out 2> out/$n.err
  echo "$(date) end $n rc=$? $(tail -1 out/$n.out)" >> out/worker_$W.log
done
cat $(for i in $W $((W+4)) $((W+8)) $((W+12)); do printf "out/c%02d.out " $i; done) | awk '/^NOTFOUND/{for(i=1;i<=NF;i++) if($i~/^p=/){sub("p=","",$i); print $i}}' > out/notfound_w$W.txt
echo "$(date) notfound=$(wc -l < out/notfound_w$W.txt)" >> out/worker_$W.log
./retry.sh out/notfound_w$W.txt out/retry_w$W.out >> out/worker_$W.log 2>&1
echo "$(date) WORKER_DONE" >> out/worker_$W.log
