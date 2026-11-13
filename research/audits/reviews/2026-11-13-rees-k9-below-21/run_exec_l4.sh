#!/bin/zsh
# 4-level executor runs at a = 1, forced mode (lucky objects discarded), plus negative control.
cd ${0:A:h}
PY=/opt/anaconda3/bin/python
nice -n 19 $PY tensor_exec.py 37 9 0 B4_37.json 1 4 uniform,lowrank forced
nice -n 19 $PY tensor_exec.py 19 9 0 B4_19.json 1 4 uniform,lowrank forced
nice -n 19 $PY tensor_exec.py 127 9 0 B4_127_chain.json 1 2 uniform,lowrank forced
nice -n 19 $PY tensor_exec.py 37 9 0 B4_37_perturbed.json 1 2 uniform,lowrank forced
