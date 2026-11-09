#!/bin/sh
# low/finish_low.sh : close chunk c00 = (20000, 200000] with what low/*.out contains, then
# become sweep worker 2.  (run_low.sh was stopped by hand during its step (a): P complete
# was run on the witness-less primes up to 99577; the rest of (a) and step (b) are deferred.)
#   low/candidates.txt : primes of (20000, 200000] with no FOUND line in low/*.out
#   dfs2b_queue.txt    : the 20 smallest candidates (run by the workers after the chunks)
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
cd "$D" || exit 1
LOG=low/run_low.log
cat low/*.out | awk '/^FOUND k=9 /{for(i=1;i<=NF;i++) if($i~/^p=/){sub("p=","",$i); print $i}}' | sort -u > low/found_tmp.txt
sort -u low/all_c00.txt | comm -23 - low/found_tmp.txt | sort -n > low/candidates.txt
head -20 low/candidates.txt > dfs2b_queue.txt
echo "$(date) finish_low: candidates (no witness in low/*.out): $(wc -l < low/candidates.txt); dfs2b queue: $(tr '\n' ' ' < dfs2b_queue.txt)" >> $LOG
touch out/done_c00
exec ./run_worker.sh 2
