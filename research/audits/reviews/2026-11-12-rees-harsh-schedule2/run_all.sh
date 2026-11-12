#!/bin/zsh
# Sequential E_2 runs (one heavy process at a time), harsh referee 2026-11-12.
cd ${0:A:h}
D=./e2dfs
for k in 2 3 4 5 6; do nice -n 19 $D $k 3 3000 > ex_k${k}_3_3000.out; done
nice -n 19 $D 7 3 6000 > ex_k7_3_6000.out
nice -n 19 $D 9 3 6000 > ex_k9_3_6000.out
nice -n 19 $D 8 3 4400 > ex_k8_3_4400.out
nice -n 19 $D 5 3000 13000 20000 > hunt_k5_3000_13000.out
nice -n 19 $D 6 3000 234000 20000 > hunt_k6_3000_234000.out
nice -n 19 $D 8 4400 100000 100000 > hunt_k8_4400_100000.out
nice -n 19 $D 9 6000 100000 100000 > hunt_k9_6000_100000.out
nice -n 19 $D 7 6000 1000000 20000 > hunt_k7_6000_1000000.out
echo done > run_all.done
