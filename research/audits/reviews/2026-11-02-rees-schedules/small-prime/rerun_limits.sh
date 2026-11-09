#!/bin/sh
printf '8 4073\n8 4129\n8 4153\n8 4201\n8 6073\n8 6089\n8 8009\n' | xargs -P3 -L1 sh -c 'nice -n 10 timeout 5400 ./dfs2 $0 $1 $1 50000000 > dfs2_k$0_rerun_$1.out 2>&1'
echo done > rerun_limits.done
