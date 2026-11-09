#!/bin/sh
# validation of e2dfs_c against the paper's exact lists (kappa = 4..9), one process at a time
cd "$(dirname "$0")"
nice -n 10 ./e2dfs_c 4 3 1000  > e2dfs_c_k4.out
nice -n 10 ./e2dfs_c 6 3 2000  > e2dfs_c_k6.out
nice -n 10 ./e2dfs_c 7 3 3400  > e2dfs_c_k7.out
nice -n 10 ./e2dfs_c 8 3 2442  > e2dfs_c_k8.out
nice -n 10 ./e2dfs_c 9 3 3584  > e2dfs_c_k9.out
nice -n 10 ./e2dfs_c 5 3 12721 > e2dfs_c_k5.out
