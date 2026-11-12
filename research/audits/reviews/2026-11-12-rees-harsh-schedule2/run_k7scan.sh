#!/bin/zsh
cd ${0:A:h}
until [ -e run_followup.done ]; do sleep 5; done
nice -n 19 ./e2scan 7 1000000 4941831 400 20261112 > scan_k7_1e6_TA7.out
echo done > run_k7scan.done
