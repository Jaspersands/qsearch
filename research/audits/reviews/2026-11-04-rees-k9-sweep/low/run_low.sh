#!/bin/sh
# low/run_low.sh : finish chunk c00 = (20000, 200000], then become sweep worker 2.
# Inputs already produced by hand (see the report):
#   low/t1_20001_60000.out      old famsym T1 random (200000 x 50, seed 1)  [also crosscheck]
#   low/t1c_20001_76231.out     old famsym T1 complete (1e8, all b) on every prime of
#                               (20000, 76231] (stopped there by hand)      [strict]
#   low/P_rand_20001_200000.out famsym9 fam=P tab random (20000 x 20)       [non-strict]
# Steps here, for the primes of (20000, 200000] with no FOUND line yet:
#   (a) famsym9 fam=P tab complete (1e8 nodes, all b = 1..8) -> low/Pc.out   (decides P)
#   (b) p > 76231: old famsym T1 complete                     -> low/t1c_hi.out (decides T1)
#   (c) the rest -> low/candidates.txt (no T1, no P witness); dfs2b_queue.txt = its
#       20 smallest primes (they are decided by the workers after the chunks).
# Then: exec run_worker.sh 2.
D=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-k9-sweep
OLDD=/Users/jaspersands/Developer/qsearch/research/audits/reviews/2026-11-04-rees-threshold-5
cd "$D" || exit 1
LOG=low/run_low.log
until grep -q '^DONE' low/P_rand_20001_200000.out; do sleep 30; done
echo "$(date) inputs done" >> $LOG
# found_set: sorted list of primes that have a FOUND line in low/*.out
found_set() { cat low/*.out | awk '/^FOUND k=9 /{for(i=1;i<=NF;i++) if($i~/^p=/){sub("p=","",$i); print $i}}' | sort -u > low/found_tmp.txt; }
# without IN OUT: primes of IN (sorted as text) with no FOUND line
without() { found_set; sort -u "$1" | comm -23 - low/found_tmp.txt | sort -n > "$2"; }
awk '/FOUND/{for(i=1;i<=NF;i++) if($i~/^p=/){sub("p=","",$i); print $i}}' low/P_rand_20001_200000.out | sort -n -u > low/all_c00.txt
without low/all_c00.txt low/nowit_a.txt
echo "$(date) primes=$(wc -l < low/all_c00.txt) without witness before (a): $(wc -l < low/nowit_a.txt)" >> $LOG
while read p; do ./famsym9 9 $p $p 100000000 8 1 complete tab fam=P < /dev/null | grep -v '^DONE' >> low/Pc.out; done < low/nowit_a.txt
without low/nowit_a.txt low/nowit_b.txt
echo "$(date) without witness after (a): $(wc -l < low/nowit_b.txt)" >> $LOG
while read p; do [ "$p" -gt 76231 ] && $OLDD/famsym 9 $p $p 100000000 9 1 complete < /dev/null | grep -v '^DONE' >> low/t1c_hi.out; done < low/nowit_b.txt
: >> low/t1c_hi.out
without low/nowit_b.txt low/candidates.txt
head -20 low/candidates.txt > dfs2b_queue.txt
echo "$(date) candidates (no T1, no P witness): $(wc -l < low/candidates.txt); dfs2b queue: $(tr '\n' ' ' < dfs2b_queue.txt)" >> $LOG
touch out/done_c00
exec ./run_worker.sh 2
