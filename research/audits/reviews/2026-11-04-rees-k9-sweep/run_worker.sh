#!/bin/sh
# run_worker.sh W : worker W claims chunks of chunks.txt in file order (mkdir lock
# out/claim_cNN), so the finished range grows from the bottom.  Per chunk:
#   tab  : famsym9 9 lo+1 hi 20000 20 (1000+i) tab              (T1, strict; full index table)
#   ints : famsym9 9 lo+1 hi 200000 50 (1000+i) ints=800000    (T1, strict; needs lo > 3.2e6)
#   calib: skipped (run by hand, see the report)
# then collects the chunk's NOTFOUND primes into out/nf_cNN.txt and runs retry.sh on them
# (out/r_cNN.out).  Outputs: out/cNN.out (flushed per prime), out/worker_W.log.
# When no chunk is left, the worker takes dfs2b jobs from dfs2b_queue.txt (mkdir lock
# out/claim_dfs_P), writing out/dfs2b_P.out, and then logs WORKER_DONE.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
SP=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-02-rees-schedules/small-prime
cd "$D" || exit 1
W=$1
mkdir -p out
LOG=out/worker_$W.log
grep -v '^#' chunks.txt | while read n lo hi np mode; do
  [ -z "$n" ] && continue
  [ "$mode" = calib ] && continue
  mkdir out/claim_$n 2>/dev/null || continue
  i=$(echo $n | sed 's/^c0*//'); [ -z "$i" ] && i=0
  echo "$(date) start $n ($lo,$hi] $mode" >> $LOG
  if [ "$mode" = tab ]; then ./famsym9 9 $((lo+1)) $hi 20000 20 $((1000+i)) tab > out/$n.out 2> out/$n.err < /dev/null
  else ./famsym9 9 $((lo+1)) $hi 200000 50 $((1000+i)) ints=800000 > out/$n.out 2> out/$n.err < /dev/null; fi
  rc=$?
  echo "$(date) end $n rc=$rc $(tail -1 out/$n.out)" >> $LOG
  if [ $rc -ne 0 ] || ! tail -1 out/$n.out | grep -q '^DONE'; then echo "$(date) ABORT: $n did not finish" >> $LOG; exit 1; fi
  awk '/^NOTFOUND/{for(i=1;i<=NF;i++) if($i~/^p=/){sub("p=","",$i); print $i}}' out/$n.out > out/nf_$n.txt
  echo "$(date) $n notfound=$(wc -l < out/nf_$n.txt)" >> $LOG
  ./retry.sh out/nf_$n.txt out/r_$n.out >> $LOG 2>&1
  echo "$(date) $n retry done, unresolved=$(grep -c UNRESOLVED out/r_$n.out)" >> $LOG
  touch out/done_$n
done
[ -f dfs2b_queue.txt ] && while read p; do
  [ -z "$p" ] && continue
  mkdir out/claim_dfs_$p 2>/dev/null || continue
  echo "$(date) dfs2b start $p" >> $LOG
  (cd $SP && ./dfs2b 9 $p $p 4000000000 print < /dev/null) > out/dfs2b_$p.out 2>&1
  echo "$(date) dfs2b end $p: $(grep -h 'k=9' out/dfs2b_$p.out | cut -c1-60)" >> $LOG
done < dfs2b_queue.txt
echo "$(date) WORKER_DONE" >> $LOG
