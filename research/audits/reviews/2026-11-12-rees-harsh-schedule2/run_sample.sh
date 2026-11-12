#!/bin/zsh
cd ${0:A:h}
for spec in "7 1000000 4941830" "8 100000 12000000" "9 100000 5000000"; do
  set -- ${=spec}
  /opt/anaconda3/bin/python sample.py $1 $2 $3 60 20261112 > sample_k$1.txt
  : > sample_k$1.out
  for p in $(cat sample_k$1.txt); do nice -n 19 ./e2dfs $1 $p $p 20000 >> sample_k$1.out; done
done
echo done > run_sample.done
