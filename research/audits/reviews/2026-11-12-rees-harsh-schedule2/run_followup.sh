#!/bin/zsh
cd ${0:A:h}
until [ -e run_all.done ]; do sleep 5; done
: > resolve_k7.out
for p in $(grep UNDECIDED hunt_k7_6000_1000000.out | cut -d' ' -f1); do nice -n 19 ./e2dfs 7 $p $p 0 >> resolve_k7.out; done
./run_sample.sh
echo done > run_followup.done
