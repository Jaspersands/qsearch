#!/bin/zsh
# usage: run_cells.sh TIMEOUT_S "p kappa l OMEGA" ...   (one instance per argument)
# Generates the cellsat CNF in the scratch dir, runs kissat, verifies SAT models with check_table.py.
set -u
D=${0:A:h}
S=${SCR:-/private/tmp/claude-501/-Users-jaspersands-Developer-qsearch/265ea4e4-9d06-4353-9b18-ca6cd6e80035/scratchpad/b20}
PY=/opt/anaconda3/bin/python
TO=$1; shift
for inst in "$@"; do
  set -- ${=inst}
  p=$1 k=$2 l=$3 om=$4 xi=${5:-}
  tag="${p}_${k}_${l}_${om//,/-}${xi:+_xi$xi}"
  cnf=$S/cell_$tag.cnf
  gen=$(nice -n 19 $PY $D/cellsat.py $p $k $l $om $cnf $xi)
  sha=$(shasum -a 256 $cnf | cut -c1-16)
  t0=$(date +%s)
  /usr/bin/time -l nice -n 19 kissat -q --time=$TO $cnf > $S/model_$tag.txt 2> $S/time_$tag.txt
  rc=$?
  t1=$(date +%s)
  rss=$(grep 'maximum resident' $S/time_$tag.txt | awk '{print int($1/1048576)}')
  res=$(grep '^s ' $S/model_$tag.txt | head -1)
  chk='-'
  if [[ $rc -eq 10 ]]; then
    chk=$(nice -n 19 $PY $D/check_table.py $cnf.map.json $S/model_$tag.txt | sed 's/.*-> //')
    gzip -c $S/model_$tag.txt > $D/model_cell_$tag.txt.gz
  fi
  print "($p,$k,l=$l,Omega={$om}) | ${gen#*xi=} | sha $sha | rc=$rc ${res:-timeout} | $((t1-t0)) s | ${rss} MB | check $chk"
done
